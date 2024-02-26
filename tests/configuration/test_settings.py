import pytest
import os

from resource_proxy_manager.spawner.config import K8SSpawnerSettings
from resource_proxy_manager.storage.config import S3StorageSettings


@pytest.fixture
def start_envs(request):
    env_vars = request.param
    for key, value in env_vars.items():
        print(key, value)
        os.environ[key] = value

    yield

    for key in env_vars.keys():
        del os.environ[key]


@pytest.mark.parametrize("start_envs", [
    {"S3_STORAGE_ENDPOINT_URL": "http://localhost:9000",
     "S3_STORAGE_ACCESS_KEY": "minio",
     "S3_STORAGE_SECRET_KEY": "minio123",
     "S3_STORAGE_BUCKET_NAME": "raw-data"}
], indirect=True)
def test_storageSettings_initialize_success_when_enviornment_variables_are_set(start_envs):
    storage_settings = S3StorageSettings()

    assert storage_settings.S3_STORAGE_ENDPOINT_URL == "http://localhost:9000"
    assert storage_settings.S3_STORAGE_ACCESS_KEY == "minio"
    assert storage_settings.S3_STORAGE_SECRET_KEY == "minio123"
    assert storage_settings.S3_STORAGE_BUCKET_NAME == "raw-data"


@pytest.mark.parametrize("start_envs", [
    {"S3_STORAGE_ENDPOINT_URL": "http://localhost:9000",
     "S3_STORAGE_SECRET_KEY": "minio123",
     "S3_STORAGE_BUCKET_NAME": "raw-data"}
], indirect=True)
def test_initialize_fail_when_environment_variables_are_not_set(start_envs):
    with pytest.raises(Exception):
        storage_settings = S3StorageSettings()


@pytest.mark.parametrize("start_envs", [
    {"S3_STORAGE_ENDPOINT_URL": "http://localhost:9000",
     "S3_STORAGE_ACCESS_KEY": "minio",
     "S3_STORAGE_SECRET_KEY": "minio123",
     "S3_STORAGE_BUCKET_NAME": "raw-data",
     "K8S_SPAWNER_NAMESPACE": "test-namespace"
     }
], indirect=True)
def test_storageSettings_merge(start_envs):
    """ 두개의 환경 변수 세팅이 있을때 합쳐서 관리될 수 있는지 확인"""
    storage_settings = S3StorageSettings()
    spawner_settings = K8SSpawnerSettings()

    merged = storage_settings + spawner_settings

    assert merged.S3_STORAGE_ENDPOINT_URL == "http://localhost:9000"
    assert merged.S3_STORAGE_ACCESS_KEY == "minio"
    assert merged.S3_STORAGE_SECRET_KEY == "minio123"
    assert merged.S3_STORAGE_BUCKET_NAME == "raw-data"
    assert merged.K8S_SPAWNER_NAMESPACE == 'test-namespace'
