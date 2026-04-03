"""Simple session manager: read/write session.json per task."""

import json
import os
import re
from datetime import datetime

import config

_SAFE_NAME_RE = re.compile(r'^[a-zA-Z0-9_\-.]+$')


def _sessions_dir() -> str:
    path = config.get_session_dir()
    os.makedirs(path, exist_ok=True)
    return path


def _validate_task_name(name: str) -> str:
    """Sanitize task_name: reject path traversal and special characters."""
    if not name or not _SAFE_NAME_RE.match(name):
        raise ValueError(
            f"Invalid task name '{name}'. "
            "Only letters, digits, hyphens, underscores, and dots are allowed."
        )
    return name


class SessionManager:
    def __init__(self, task_name: str = "default"):
        self.task_name = _validate_task_name(task_name)
        self.path = os.path.join(_sessions_dir(), f"{self.task_name}.json")
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"task": self.task_name, "created": _now(), "entries": []}

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_entry(self, provider: str, prompt: str, response: str, kind: str = "ask"):
        entry = {
            "timestamp": _now(),
            "provider": provider,
            "kind": kind,
            "prompt": prompt,
            "response": response,
        }
        self.data["entries"].append(entry)
        self.save()
        return entry

    def show(self) -> str:
        lines = [f"Task: {self.task_name}", f"Created: {self.data['created']}", ""]
        for i, e in enumerate(self.data["entries"], 1):
            lines.append(f"[{i}] ({e['kind']}) {e['provider']} @ {e['timestamp']}")
            lines.append(f"    Q: {e['prompt'][:80]}{'...' if len(e['prompt']) > 80 else ''}")
            lines.append("")
        return "\n".join(lines)

    def get_history_text(self) -> str:
        """Format all entries as a text block for synthesis."""
        blocks = []
        for e in self.data["entries"]:
            blocks.append(f"--- {e['provider']} ({e['kind']}) @ {e['timestamp']} ---\nPrompt: {e['prompt']}\nResponse: {e['response']}\n")
        return "\n".join(blocks)

    def export_markdown(self) -> str:
        """Export the full session as a markdown document."""
        lines = [
            f"# Task: {self.task_name}",
            f"Created: {self.data['created']}",
            f"Entries: {len(self.data['entries'])}",
            "",
        ]
        for i, e in enumerate(self.data["entries"], 1):
            kind = e["kind"]
            provider = e["provider"]
            timestamp = e["timestamp"]
            prompt = e["prompt"]
            response = e["response"]

            # Section header
            kind_label = {
                "ask": "Ask",
                "compare": "Compare",
                "compare-analysis": "Compare Analysis",
                "execute": "Executor Output",
                "review": "Review",
                "synthesize": "Synthesize",
            }.get(kind, kind.title())

            lines.append(f"## {i}. {kind_label} — {provider}")
            lines.append(f"**Time:** {timestamp}  ")
            lines.append(f"**Model:** {provider}  ")
            lines.append(f"**Kind:** {kind}  ")
            lines.append("")
            lines.append("### Prompt")
            lines.append("")
            lines.append(f"> {prompt}")
            lines.append("")
            lines.append("### Response")
            lines.append("")
            lines.append(response)
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def list_sessions() -> list[str]:
        """List all available task names."""
        dir_path = _sessions_dir()
        files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
        return [f[:-5] for f in files]

    @staticmethod
    def get_current_task() -> str:
        """Get the current task name from current.txt."""
        path = os.path.join(_sessions_dir(), "current.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        return "default"

    @staticmethod
    def set_current_task(name: str):
        """Set the current task name to current.txt."""
        path = os.path.join(_sessions_dir(), "current.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(name)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
