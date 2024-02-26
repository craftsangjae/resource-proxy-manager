import pytest
import subprocess
import logging

logging = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return pytestconfig.rootdir / "tests/storage/s3/docker-compose.yml"


@pytest.fixture(scope="session")
def start_docker_container(docker_compose_file):
    logging.warning('start docker container(minio)....')
    subprocess.run(["docker-compose", "-f", str(docker_compose_file), "up", "-d"], check=True)
    yield
    logging.warning('stop docker container(minio)....')
    subprocess.run(["docker-compose", "-f", str(docker_compose_file), "down"], check=True)
