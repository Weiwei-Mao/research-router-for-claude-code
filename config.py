"""Configuration loader for research-router."""

import json
import os
import sys

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
_config = None


def load_config() -> dict:
    """Load config.json once and cache the result."""
    global _config
    if _config is not None:
        return _config

    if not os.path.exists(_CONFIG_PATH):
        print(
            f"Error: config.json not found at {_CONFIG_PATH}\n"
            "Please create it. Example:\n"
            '{\n  "session_dir": "data/sessions",\n  "default_analyzer": "qwen",\n'
            '  "providers": { ... }\n}',
            file=sys.stderr,
        )
        sys.exit(1)

    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        _config = json.load(f)
    return _config


def get(key: str, default=None):
    """Get a top-level config value."""
    cfg = load_config()
    return cfg.get(key, default)


def get_provider_config(provider_name: str) -> dict:
    """Get config dict for a specific provider."""
    cfg = load_config()
    providers = cfg.get("providers", {})
    if provider_name not in providers:
        raise ValueError(
            f"Provider '{provider_name}' not found in config.json. "
            f"Available: {', '.join(providers)}"
        )
    return providers[provider_name]


def get_session_dir() -> str:
    """Get absolute path for session directory."""
    cfg = load_config()
    rel = cfg.get("session_dir", "data/sessions")
    if os.path.isabs(rel):
        return rel
    return os.path.join(os.path.dirname(__file__), rel)
