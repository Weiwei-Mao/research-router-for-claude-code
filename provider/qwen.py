from .base import BaseProvider


class QwenProvider(BaseProvider):
    name = "qwen"

    def ask(self, prompt: str) -> str:
        return self._run(self.command, prompt)
