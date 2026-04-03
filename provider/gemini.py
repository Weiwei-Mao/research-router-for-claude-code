import shutil

from .base import BaseProvider


class GeminiProvider(BaseProvider):
    name = "gemini"

    def ask(self, prompt: str) -> str:
        if not shutil.which(self.command[0]):
            raise RuntimeError(
                f"{self.command[0]} CLI not found. Please install it and add to PATH."
            )
        return self._run(self.command, prompt)
