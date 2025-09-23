import json
import os
from typing import Dict, Optional


class I18nManager:
    def __init__(self, messages: Dict[str, Dict[str, str]], default_lang: str = "en"):
        self.messages = messages
        self.default_lang = default_lang
        self.supported_languages = self._get_supported_languages()

    @classmethod
    def from_json_file(cls, path: str, default_lang: str = "en") -> "I18nManager":
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Message file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            messages = json.load(f)
        return cls(messages=messages, default_lang=default_lang)

    def _get_supported_languages(self):
        langs = set()
        for msg in self.messages.values():
            langs.update(msg.keys())
        return langs

    def get_message(self, key: str, lang: Optional[str] = None) -> str:
        lang = (lang or self.default_lang).lower()
        if lang not in self.supported_languages:
            lang = self.default_lang

        return self.messages.get(key, {}).get(
            lang,
            self.messages.get(key, {}).get(self.default_lang, f"[{key}]")
        )
