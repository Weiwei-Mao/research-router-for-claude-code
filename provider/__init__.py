from .base import BaseProvider
from .codex import CodexProvider
from .gemini import GeminiProvider
from .qwen import QwenProvider

PROVIDERS = {
    "codex": CodexProvider,
    "gemini": GeminiProvider,
    "qwen": QwenProvider,
}


def get_provider(name: str) -> BaseProvider:
    cls = PROVIDERS.get(name)
    if cls is None:
        raise ValueError(f"Unknown provider: {name}. Available: {', '.join(PROVIDERS)}")
    return cls()
