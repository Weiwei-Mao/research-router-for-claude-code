from .base import BaseProvider


class GeminiProvider(BaseProvider):
    name = "gemini"

    def ask(self, prompt: str) -> str:
        return self._run(self.command, prompt)
