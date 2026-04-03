import subprocess
from abc import ABC, abstractmethod

import config


class BaseProvider(ABC):
    """Base class for all model providers. Reads settings from config.json."""

    name: str = ""

    def __init__(self):
        self._cfg = config.get_provider_config(self.name)

    @property
    def command(self) -> list[str]:
        return self._cfg.get("command", [])

    @property
    def timeout(self) -> int:
        return self._cfg.get("timeout", 600)

    @property
    def use_stdin(self) -> bool:
        return self._cfg.get("use_stdin", False)

    @abstractmethod
    def ask(self, prompt: str) -> str:
        ...

    def _run(self, args: list[str], prompt: str) -> str:
        """Execute a subprocess call with the provider's settings."""
        kwargs = dict(
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout,
            shell=True,
        )
        if self.use_stdin:
            kwargs["input"] = prompt
        else:
            args = args + [prompt]

        result = subprocess.run(args, **kwargs)
        if result.returncode != 0:
            raise RuntimeError(f"{self.name} error: {result.stderr.strip()}")
        return result.stdout.strip()
