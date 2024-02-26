from pydantic import Field

from resource_proxy_manager.config import CommonSettings


class S3StorageSettings(CommonSettings):
    ##################
    # S3 storage 관련된 설정
    ##################
    S3_STORAGE_ENDPOINT_URL: str = Field(description="object storage의 endpoint url")
    S3_STORAGE_ACCESS_KEY: str = Field(description="object storage의 access key")
    S3_STORAGE_SECRET_KEY: str = Field(description="object storage의 secret key")
    S3_STORAGE_BUCKET_NAME: str = Field(description="object storage의 bucket name")
