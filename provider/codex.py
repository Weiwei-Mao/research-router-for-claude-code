from .base import BaseProvider


class CodexProvider(BaseProvider):
    name = "codex"

    def ask(self, prompt: str) -> str:
        return self._run(self.command, prompt)
