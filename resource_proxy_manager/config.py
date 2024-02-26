from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    # 참고 : extra='ignore' 하지 않으면, 다른 환경변수가 들어올때 에러 발생
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
