import pytest

from resource_proxy_manager.exceptions import NotFoundDataException
from resource_proxy_manager.storage.s3 import S3ObjectStorage


@pytest.fixture
def storage():
    return S3ObjectStorage(
        endpoint_url="http://localhost:9000",
        access_key="minio-access-key",
        secret_key="minio-secret-key",
        bucket_name="test-bucket",
    )


def test_exists_return_false_when_object_not_exist(start_docker_container, storage):
    # given
    given_key = "hello"

    # when
    result = storage.exists(given_key)

    # then
    assert result is False


def test_exists_return_true_when_object_exist(start_docker_container, storage):
    # given
    given_key = "hello"
    given_object = "world"
    storage.upload(given_key, body=given_object)  # create

    # when
    result = storage.exists(given_key)

    # then
    assert result is True


def test_exists_return_false_when_object_is_deleted(start_docker_container, storage):
    # given
    given_key = "hello"
    given_object = "world"
    storage.upload(given_key, body=given_object)  # create
    storage.delete(given_key)

    # when
    result = storage.exists(given_key)

    # then
    assert result is False


def test_delete_when_object_not_exist(start_docker_container, storage):
    # given
    given_key = "hello"

    # when
    storage.delete(given_key)
    result = storage.exists(given_key)

    assert result is False


def test_download_raise_exception_when_object_not_exists(start_docker_container, storage):
    # given
    given_key = "hello"

    # when
    with pytest.raises(NotFoundDataException):
        storage.download(given_key)


def test_download_return_object_when_object_exists(start_docker_container, storage):
    # given
    given_key = "hello"
    given_object = "world"
    storage.upload(given_key, body=given_object)  # create

    # when
    result = storage.download(given_key)

    # then
    assert result == given_object.encode()
