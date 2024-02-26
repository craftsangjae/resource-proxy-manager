from abc import ABC, abstractmethod
from typing import Union, List

from resource_proxy_manager.storage.dto import MultipartUploadPart, MultipartUploadKey


class ObjectStorageInterface(ABC):
    """Object Storage의 기본 인터페이스"""

    @abstractmethod
    def exists(self, key) -> bool:
        """key에 해당하는 오브젝트 존재 여부 반환

        :param key:
        :return:
        """
        pass

    @abstractmethod
    def download(self, key: str) -> bytes:
        """key에 해당하는 오브젝트 다운로드
        :param key:
        :return:
        """
        pass

    @abstractmethod
    def upload(self, key: str, body: Union[str, bytes]) -> None:
        """key에 해당하는 오브젝트 업로드

        :param key:
        :param body:
        :return:
        """
        pass


class ObjectStorageMultipartUploadInterface(ABC):
    """Object Storage에서 multipart upload에 관련된 인터페이스"""

    def initialize_multipart_upload(self, key: str, checksum: str) -> MultipartUploadKey:
        """ multipart upload를 초기화 합니다.
        :param key: 올리고자 하는 object의 key
        :param checksum: 올리고자 하는 object에 대한 checksum

        :return: upload_id
        """
        pass

    def cancel_multipart_upload(self, upload_key: MultipartUploadKey):
        """ multipart upload를 취소합니다.
        :param upload_key: MultipartUploadKey:
        :return:
        """
        pass

    def generate_presigned_url_for_part(self, upload_key: MultipartUploadKey, part_number: int) -> str:
        """ multipart upload의 part를 업로드하기 위한 presigned url을 생성합니다.
        :param upload_key:
        :param part_number:
        :return: presigned_url
        """
        pass

    def list_uploaded_parts(self, upload_key: MultipartUploadKey) -> List[MultipartUploadPart]:
        """ multipart upload의 part 리스트를 반환합니다.
        :param upload_key
        :return:
        """
        pass

    def complete_multipart_upload(self, upload_key: MultipartUploadKey):
        """ multipart upload를 완료합니다.
        :param upload_key: MultipartUploadKey
        :return:
        """
        pass

    def compare_multipart_checksum(self, upload_key: MultipartUploadKey, checksum: str) -> bool:
        """ multipart upload에 올라가 있는 checksum과 비교합니다.
        :param upload_key: MultipartUploadKey
        :param checksum: checksum

        :return: bool
        """
        pass
