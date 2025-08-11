"""Example weather agent using OpenAI and HTTP requests to fetch weather data."""

from dataclasses import dataclass
from enum import Enum
from os import environ
from typing import Any, Optional

from strands.models import Model
from strands.models.openai import OpenAIModel
from strands.models.litellm import LiteLLMModel
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TEMPERATURE: float = 0.7
DEFAULT_MAX_TOKENS: int = 1000
DEFAULT_AI_MODEL: str = "gpt-4.1"


class ModelType(Enum):
    """Supported model types."""
    OPENAI = "openai"
    LITELLM = "litellm"


@dataclass
class ModelConfig:
    """Configuration for the AI model."""
    model_type: ModelType
    api_key: str
    base_url: Optional[str]
    model_id: str
    max_tokens: int
    temperature: float

    def __post_init__(self):
        """Validate the model configuration after initialization."""
        if not self.model_type:
            raise ValueError("Model type is required (openai|litellm).")
        if not self.api_key:
            raise ValueError("API key is required.")
        if not self.model_id:
            raise ValueError("Model ID is required.")
        if self.max_tokens <= 0:
            raise ValueError("Max tokens must be positive.")
        if not (0 <= self.temperature <= 1):
            raise ValueError("Temperature must be between 0 and 1.")

    @classmethod
    def from_environment(cls) -> "ModelConfig":
        """Create ModelConfig from environment variables."""
        def get_env(key: str, default: Optional[Any] = None, required: bool = False, cast: Any = str) -> Any:
            val = environ.get(key, default)
            if required and val is None:
                raise ValueError(f"Missing required environment variable: {key}")
            if val is not None and cast is not None:
                try:
                    return cast(val)
                except Exception as ex:
                    raise ValueError(f"Invalid value for {key}: {val}") from ex
            return val

        model_type_str = get_env("MODEL_TYPE", "openai")
        try:
            model_type = ModelType(model_type_str)
        except ValueError as ex:
            raise ValueError(f"Unsupported model type: {model_type_str}") from ex

        match model_type:
            case ModelType.LITELLM:
                return cls(
                    model_type=model_type,
                    api_key=get_env("LITELLM_API_KEY", required=True),
                    base_url=get_env("LITELLM_BASE_URL"),
                    model_id=get_env("LITELLM_MODEL", DEFAULT_AI_MODEL),
                    max_tokens=get_env("MODEL_MAX_TOKEN", DEFAULT_MAX_TOKENS, cast=int),
                    temperature=get_env("MODEL_TEMPERATURE", DEFAULT_TEMPERATURE, cast=float),
                )
            case ModelType.OPENAI:
                return cls(
                    model_type=model_type,
                    api_key=get_env("OPENAI_API_KEY", required=True),
                    base_url=get_env("OPENAI_BASE_URL"),
                    model_id=get_env("OPENAI_MODEL", DEFAULT_AI_MODEL),
                    max_tokens=get_env("MODEL_MAX_TOKEN", DEFAULT_MAX_TOKENS, cast=int),
                    temperature=get_env("MODEL_TEMPERATURE", DEFAULT_TEMPERATURE, cast=float),
                )
            case _:
                raise ValueError(f"Unsupported model type: {model_type}")


def get_or_create_ai_model(model_config: ModelConfig | None) -> Model:
    """Factory method for creating an AI model that is ready to use according to required configuration.

    Args:
        model_config (ModelConfig | None): The model configuration to use. If None, will create from environment.

    Returns:
        Model: The created AI model.

    Raises:
        ValueError: If the model configuration is invalid.
    """
    if model_config is None:
        model_config = ModelConfig.from_environment()

    client_args: dict[str, Any] = {"api_key": model_config.api_key}
    if model_config.base_url:
        client_args["base_url"] = model_config.base_url

    match model_config.model_type:
        case ModelType.OPENAI:
            return OpenAIModel(
                client_args=client_args,
                model_id=model_config.model_id,
                params={
                    "max_tokens": model_config.max_tokens,
                    "temperature": model_config.temperature,
                },
            )
        case ModelType.LITELLM:
            return LiteLLMModel(
                client_args=client_args,
                model_id=model_config.model_id,
                params={
                    "max_tokens": model_config.max_tokens,
                    "temperature": model_config.temperature,
                },
            )
        case _:
            raise ValueError(f"Unsupported model type: {model_config.model_type}")
