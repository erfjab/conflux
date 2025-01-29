from urllib.parse import urlparse
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    """
    Loads from .env
    """

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )

    EXPORT_HOST: str = ""
    EXPORT_USERNAME: str = ""
    EXPORT_PASSWORD: str = ""

    IMPORT_HOST: str = ""
    IMPORT_USERNAME: str = ""
    IMPORT_PASSWORD: str = ""

    def validate_host(cls, value: str) -> bool:
        """Validate that HOST is a valid URL."""
        parsed = urlparse(value)

        # Check if scheme is http or https
        if parsed.scheme not in ("http", "https"):
            raise ValueError("URL must start with http:// or https://")

        # Check if hostname exists
        if not parsed.hostname:
            raise ValueError(
                "URL must contain a valid host (e.g., domain.com or IP address)"
            )

        # Check if port is valid (if specified)
        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("Port must be between 1 and 65535")

        # Ensure there is nothing after the port (path, query, or fragment)
        if parsed.path or parsed.query or parsed.fragment:
            raise ValueError(
                "URL must not contain a path, query parameters, or fragments after the port"
            )

        return True

    def export_is_config(self) -> bool:
        """Check if all required fields are configured."""
        return all([self.EXPORT_HOST, self.EXPORT_USERNAME, self.EXPORT_PASSWORD])
