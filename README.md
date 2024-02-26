# Resource Proxy Maanger

## 목적

인프라 리소스(instance / storage)를 제어하는 WAS 서버 & 패키지

### 구성

* [resource_proxy_manager](resource_proxy_manager)
    * 프록시서버와 jobs에서 필요한 제어 로직 구현
    * 주요 로직
        * [storage](resource_proxy_manager/storage) : object storage에 대한 제어(생성/삭제/조회) 로직
        * [spawner](resource_proxy_manager/spawner) : k8s job에 대한 제어(생성/삭제/조회) 로직

* [webapp](webapp/README.md)
    * 유저의 요청에 따라 job을 생성하는 proxy 서버, fastAPI로 구성되어 있음

* [examples](jobs/README.md)
    * 리소스에 대한 주요 예제 정리

#### 개발환경 구성하기

1. poetry 설치

2. python dependency 설치 : `poetry install`

3. pre-commit 설정 : `poetry run pre-commit install`

4. 테스트 환경을 위해, docker & docker compose는 필수로 설치되어 있어야 합니다.
