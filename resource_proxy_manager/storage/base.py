from abc import ABC, abstractmethod
from typing import Union


class ObjectStorageInterface(ABC):
    """Object Storage에 대한 구현체"""

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
