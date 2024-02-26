from pydantic import Field

from resource_proxy_manager.config import CommonSettings


class K8SSpawnerSettings(CommonSettings):
    ##################
    # spawner 관련된 설정
    ##################
    K8S_SPAWNER_NAMESPACE: str = Field(description="k8s spawner에서 job을 생성할 namespace")
