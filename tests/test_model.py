"""Unit tests for model configurations."""

import pytest
from pytest import MonkeyPatch
from my_python_ai_kata.agents.model import ModelConfig, ModelType, get_or_create_ai_model
from strands.models.openai import OpenAIModel
from strands.models.litellm import LiteLLMModel


def test_model_config_from_environment_openai(monkeypatch: MonkeyPatch):
    """Test ModelConfig.from_environment for OpenAI config."""
    monkeypatch.setenv("MODEL_TYPE", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")
    monkeypatch.setenv("MODEL_MAX_TOKEN", "123")
    monkeypatch.setenv("MODEL_TEMPERATURE", "0.5")
    config = ModelConfig.from_environment()
    assert config.model_type == ModelType.OPENAI
    assert config.api_key == "test-key"
    assert config.model_id == "gpt-test"
    assert config.max_tokens == 123
    assert config.temperature == 0.5


def test_model_config_from_environment_litellm(monkeypatch: MonkeyPatch):
    """Test ModelConfig.from_environment for LiteLLM config."""
    monkeypatch.setenv("MODEL_TYPE", "litellm")
    monkeypatch.setenv("LITELLM_API_KEY", "test-key")
    monkeypatch.setenv("LITELLM_MODEL", "gpt-test")
    monkeypatch.setenv("MODEL_MAX_TOKEN", "456")
    monkeypatch.setenv("MODEL_TEMPERATURE", "0.2")
    config = ModelConfig.from_environment()
    assert config.model_type == ModelType.LITELLM
    assert config.api_key == "test-key"
    assert config.model_id == "gpt-test"
    assert config.max_tokens == 456
    assert config.temperature == 0.2


def test_model_config_validation_errors():
    """Test ModelConfig validation raises errors for invalid input."""
    with pytest.raises(ValueError):
        ModelConfig(model_type=None, api_key="x", base_url=None, model_id="id", max_tokens=1, temperature=0.5)
    with pytest.raises(ValueError):
        ModelConfig(model_type=ModelType.OPENAI, api_key="", base_url=None, model_id="id", max_tokens=1, temperature=0.5)
    with pytest.raises(ValueError):
        ModelConfig(model_type=ModelType.OPENAI, api_key="x", base_url=None, model_id="", max_tokens=1, temperature=0.5)
    with pytest.raises(ValueError):
        ModelConfig(model_type=ModelType.OPENAI, api_key="x", base_url=None, model_id="id", max_tokens=0, temperature=0.5)
    with pytest.raises(ValueError):
        ModelConfig(model_type=ModelType.OPENAI, api_key="x", base_url=None, model_id="id", max_tokens=1, temperature=1.5)


def test_get_or_create_ai_model_openai(monkeypatch: MonkeyPatch):
    """Test get_or_create_ai_model returns OpenAIModel instance."""
    monkeypatch.setenv("MODEL_TYPE", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")
    monkeypatch.setenv("MODEL_MAX_TOKEN", "123")
    monkeypatch.setenv("MODEL_TEMPERATURE", "0.5")

    model = get_or_create_ai_model(None)

    assert isinstance(model, OpenAIModel)

    model_config = model.get_config()
    assert model_config["model_id"] == "gpt-test"
    
    params = model_config["params"]
    assert params["max_tokens"] == 123
    assert params["temperature"] == 0.5

def test_get_or_create_ai_model_litellm(monkeypatch: MonkeyPatch):
    """Test get_or_create_ai_model returns LiteLLMModel instance."""
    monkeypatch.setenv("MODEL_TYPE", "litellm")
    monkeypatch.setenv("LITELLM_API_KEY", "test-key")
    monkeypatch.setenv("LITELLM_MODEL", "gpt-test")
    monkeypatch.setenv("MODEL_MAX_TOKEN", "456")
    monkeypatch.setenv("MODEL_TEMPERATURE", "0.2")
    
    model = get_or_create_ai_model(None)
    
    assert isinstance(model, LiteLLMModel)
    
    model_config = model.get_config()
    assert model_config["model_id"] == "gpt-test"

    params = model_config["params"]
    assert params["max_tokens"] == 456
    assert params["temperature"] == 0.2
    


def test_model_config_from_environment_invalid_type(monkeypatch: MonkeyPatch):
    """Test ModelConfig.from_environment raises for invalid model type."""
    monkeypatch.setenv("MODEL_TYPE", "invalid")
    with pytest.raises(ValueError):
        ModelConfig.from_environment()


def test_model_config_model_type_none():
    """Test that passing None for model_type raises a TypeError or ValueError."""
    with pytest.raises((TypeError, ValueError)):
        ModelConfig(model_type=None, api_key="x", base_url=None, model_id="id", max_tokens=1, temperature=0.5)
