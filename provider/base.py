import shutil
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

    @abstractmethod
    def ask(self, prompt: str) -> str:
        ...

    def _run(self, args: list[str], prompt: str) -> str:
        """Execute a subprocess call with the provider's settings.

        Resolves the command via PATH using shutil.which() to avoid shell=True.
        Prompt is always passed via stdin to prevent command injection.
        """
        # Resolve command executable to full path
        resolved = [shutil.which(args[0]) or args[0]] + args[1:]

        kwargs = dict(
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout,
            input=prompt,
        )

        result = subprocess.run(resolved, **kwargs)
        if result.returncode != 0:
            raise RuntimeError(f"{self.name} error: {result.stderr.strip()}")
        return result.stdout.strip()
