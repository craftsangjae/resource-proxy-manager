import logging
from typing import Union

import boto3
from botocore.exceptions import ClientError

from resource_proxy_manager.exceptions import StorageAPIException, NotFoundDataException
from resource_proxy_manager.storage.base import ObjectStorageInterface

logger = logging.getLogger(__name__)


class S3ObjectStorage(ObjectStorageInterface):
    """ S3 Object Storage에 대한 구현체
    """

    def __init__(
            self,
            s3_storage_endpoint_url: str,
            s3_storage_access_key: str,
            s3_storage_secret_key: str,
            s3_storage_bucket_name: str
    ):
        """ object storage에 업로드 / 다운로드 하는 클래스

        :param s3_storage_endpoint_url: related to S3StorageSettings.S3_STORAGE_ENDPOINT_URL
        :param s3_storage_access_key: related to S3StorageSettings.S3_STORAGE_ACCESS_KEY
        :param s3_storage_secret_key: related to S3StorageSettings.S3_STORAGE_SECRET_KEY
        :param s3_storage_bucket_name: related to S3StorageSettings.S3_STORAGE_BUCKET_NAME
        """
        self.endpoint_url = s3_storage_endpoint_url
        self.access_key = s3_storage_access_key
        self.secret_key = s3_storage_secret_key
        self.bucket_name = s3_storage_bucket_name
        self.s3 = boto3.resource('s3',
                                 endpoint_url=s3_storage_endpoint_url,
                                 aws_access_key_id=s3_storage_access_key,
                                 aws_secret_access_key=s3_storage_secret_key)
        self.bucket = self.s3.Bucket(self.bucket_name)
        self._create_bucket_if_not_exists()

    def _create_bucket_if_not_exists(self):
        # bucket이 없으면 생성 요청
        try:
            self.s3.meta.client.head_bucket(Bucket=self.bucket_name)
            return
        except ClientError:
            logger.warning(f"Bucket({self.bucket_name})이 존재하지 않습니다. 새로 생성합니다.")

        try:
            self.s3.create_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            logger.warning(f"Bucket({self.bucket_name})을 생성하지 못했습니다. error : {e}")

    def exists(self, key) -> bool:
        """ 주어진 key가 존재하는지 여부 확인
        """
        logger.debug(f"S3ObjectStorage.exists({key}) called")
        try:
            self.bucket.Object(key).load()
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise StorageAPIException("S3ObjectStorage: Object.load()을 수행하는 중 오류가 발생했습니다.")

    def download(self, key: str) -> bytes:
        """ 주어진 key에 해당하는 object를 다운로드
        """
        logger.debug(f"S3ObjectStorage.download({key}) called")
        try:
            obj = self.bucket.Object(key)
            return obj.get()['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                raise StorageAPIException(f"S3ObjectStorage: 버킷({self.bucket_name})이 생성되지 않았습니다.")
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise NotFoundDataException(f"S3ObjectStorage: 버킷({self.bucket_name})이 생성되지 않았습니다.")
            raise StorageAPIException("S3ObjectStorage: object.get()을 수행하는 중 오류가 발생했습니다")

    def upload(self, key: str, body: Union[str, bytes]) -> None:
        """ 주어진 key에 body를 업로드
        """
        logger.debug(f"S3ObjectStorage.upload({key},body) called")
        try:
            self.bucket.Object(key).put(Body=body)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                raise StorageAPIException(f"S3ObjectStorage: 버킷({self.bucket_name})이 생성되지 않았습니다.")
            raise StorageAPIException("S3ObjectStorage: object.put()을 수행하는 중 실패가 발생했습니다.")

    def delete(self, key: str) -> None:
        """ 주어진 key에 대한 object 삭제

        :param key:
        :return:
        """
        logger.debug(f"S3ObjectStorage.delete({key},body) called")
        try:
            self.bucket.Object(key).delete()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                raise StorageAPIException(f"S3ObjectStorage: 버킷({self.bucket_name})이 생성되지 않았습니다.")
            raise StorageAPIException("S3ObjectStorage: object.delete()을 수행하는 중 실패가 발생했습니다.")
