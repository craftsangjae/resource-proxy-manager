class ResourceProxyManagerException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class StorageAPIException(ResourceProxyManagerException):
    """ storage api 호출 중 에러
    """
    pass


class NotFoundDataException(ResourceProxyManagerException):
    """ 데이터가 존재하지 않을 때 에러
    """
    pass


class MissingConfigException(ResourceProxyManagerException):
    """ 환경설정 정보가 잘못되었을 때 에러
    """
    pass


class FailedJobRequestException(ResourceProxyManagerException):
    """ job에 대한 호출이 실패되었을 때 에러
    """
    pass


class NotExistJobException(ResourceProxyManagerException):
    """ 존재하지 않은 job에 접근할 때 에러
    """
    pass


class AlreadyExistedJobException(ResourceProxyManagerException):
    """ 이미 존재하고 있는 job에 대해 생성 시도할 때 에러
    """
    pass
