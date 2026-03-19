import os
from typing import Dict, Any

def _parse_properties(content: str) -> Dict[str, str]:
    messages: Dict[str, str] = {}
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            messages[key.strip()] = value.strip()
    return messages


class MessageSource:
    def __init__(self, path: str) -> None:
        self.path = path
        self.messages = self._load()

    def _load(self) -> Dict[str, str]:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            content = f.read()
        return _parse_properties(content)

    def reload(self) -> None:
        self.messages = self._load()

    def get_message(self, key: str, params: Dict[str, Any] | None = None, default: str | None = None) -> str:
        template = self.messages.get(key, default or key)
        try:
            return template.format(**(params or {}))
        except Exception:
            return template
