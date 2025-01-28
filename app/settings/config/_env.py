from pydantic_settings import BaseSettings, SettingsConfigDict


class ExportEnvSettingsFile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="export.env", case_sensitive=True, extra="ignore"
    )

    EXPORT_HOST: str = ""
    EXPORT_USERNAME: str = ""
    EXPORT_PASSWORD: str = ""
