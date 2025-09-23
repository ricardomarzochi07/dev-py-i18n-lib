import json
import os
from typing import Dict, Optional, Callable


class I18nManager:
    def __init__(
        self,
        messages: Dict[str, Dict[str, str]],
        default_lang: str = "en",
        language_getter: Optional[Callable[[], str]] = None,
    ):
        self.messages = messages
        self.default_lang = default_lang
        self.language_getter = language_getter
        self.supported_languages = self._get_supported_languages()

    @classmethod
    def from_json_file(
        cls,
        path: str,
        default_lang: str = "en",
        language_getter: Optional[Callable[[], str]] = None
    ) -> "I18nManager":
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Message file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            messages = json.load(f)
        return cls(messages=messages, default_lang=default_lang, language_getter=language_getter)

    def _get_supported_languages(self):
        langs = set()
        for msg in self.messages.values():
            langs.update(msg.keys())
        return langs

    def _resolve_lang(self, lang: Optional[str]) -> str:
        if lang:
            resolved = lang.lower()
        elif self.language_getter:
            try:
                resolved = self.language_getter().lower()
            except Exception:
                resolved = self.default_lang
        else:
            resolved = self.default_lang

        return resolved if resolved in self.supported_languages else self.default_lang

    def get_message(self, key: str, lang: Optional[str] = None) -> str:
        resolved_lang = self._resolve_lang(lang)

        return self.messages.get(key, {}).get(
            resolved_lang,
            self.messages.get(key, {}).get(self.default_lang, f"[{key}]")
        )
