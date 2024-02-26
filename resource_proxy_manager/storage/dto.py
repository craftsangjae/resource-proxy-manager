from dataclasses import dataclass


@dataclass
class MultipartUploadPart:
    """ ObjectStorage 내 저장된 part 정보
    """
    part_number: int
    etag: str


@dataclass
class MultipartUploadKey:
    """ ObjectStorage 내 multipart upload key 정보
    """
    key: str  # object key
    upload_id: str  # multipart upload key
