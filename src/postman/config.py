from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for Postman."""

    def __init__(self):
        self._load_environment()
        self._validated = False

    def _ensure_validated(self):
        """Validate configuration if not already validated."""
        if not self._validated:
            self._validate_configuration()
            self._validated = True

    def _load_environment(self) -> None:
        """Load environment variables from .env file and system environment."""
        env_path = Path(".env")
        if env_path.exists():
            logger.debug("Loading environment from .env file")
            try:
                import dotenv

                dotenv.load_dotenv(env_path)
            except ImportError:
                logger.debug("python-dotenv not installed, skipping .env loading")

    def _validate_configuration(self) -> None:
        """Validate required configuration and provide helpful error messages."""
        required_vars = ["OPENROUTER_API_KEY"]

        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(
                    f"Required environment variable {var!r} is missing. "
                    f"Please set it in .env file or system environment."
                )

    @property
    def api_key(self) -> str:
        """Get OpenRouter API key."""
        self._ensure_validated()
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key is None:
            raise ValueError("OPENROUTER_API_KEY is not set")
        return api_key

    @property
    def model(self) -> str:
        """Get OpenRouter model configuration."""
        return os.getenv("OPENROUTER_MODEL", "gpt-3.5-turbo")

    @property
    def min_width(self) -> int:
        """Get minimum terminal width."""
        return int(os.getenv("POSTMAN_MIN_WIDTH", "80"))

    @property
    def min_height(self) -> int:
        """Get minimum terminal height."""
        return int(os.getenv("POSTMAN_MIN_HEIGHT", "24"))

    @property
    def content_length(self) -> int:
        """Get content length setting."""
        return int(os.getenv("POSTMAN_CONTENT_LENGTH", "3"))

    @property
    def debug(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv("POSTMAN_DEBUG", "0") == "1"

    def redact(self, message: str, *sensitive_fields: str) -> str:
        """Redact sensitive information from log messages."""
        redacted_message = message
        for field in sensitive_fields:
            redacted_message = redacted_message.replace(
                os.getenv(field, ""), "[REDACTED]"
            )
        return redacted_message


# Global configuration instance
config = Config()
