import pytest
import os
from buddybet_i18n.i18n_manager import I18nManager  # Ajusta si usas otro path

# Ruta real del archivo messages.json
MESSAGES_FILE_PATH = os.path.join(os.path.dirname(__file__), "messages.json")


@pytest.fixture(scope="module")
def i18n():
    return I18nManager.from_json_file(MESSAGES_FILE_PATH, default_lang="en")


def test_get_message_in_supported_languages(i18n):
    # Asegúrate que estos valores existan en tu messages.json
    assert i18n.get_message("token_expired", lang="es") == "El token ha expirado"
    assert i18n.get_message("token_expired", lang="en") == "Token has expired"
    assert i18n.get_message("welcome", lang="fr") == "Bienvenue"


def test_fallback_to_default_language(i18n):
    assert i18n.get_message("token_expired", lang="de") == "Token has expired"


def test_missing_key_returns_key_in_brackets(i18n):
    assert i18n.get_message("nonexistent_key", lang="es") == "[nonexistent_key]"


def test_supported_languages(i18n):
    assert "en" in i18n.supported_languages
    assert "es" in i18n.supported_languages
    assert "fr" in i18n.supported_languages
    assert "de" not in i18n.supported_languages


def test_existing_language_missing_key_falls_back_to_default(i18n):
    # Simula una clave con solo traducción en inglés
    i18n.messages["partial_key"] = {"en": "Only English"}
    assert i18n.get_message("partial_key", lang="es") == "Only English"
