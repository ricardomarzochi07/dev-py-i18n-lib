import os
import pytest
from contextvars import ContextVar

from buddybet_i18n.i18n_manager import I18nManager


# Simula un ContextVar de idioma (como harías en el microservicio)
test_language: ContextVar[str] = ContextVar("test_language", default="en")

def get_test_language():
    return test_language.get()


# Ruta del archivo de mensajes de prueba
MESSAGES_FILE_PATH = os.path.join(os.path.dirname(__file__), "messages.json")

@pytest.fixture
def i18n():
    return I18nManager.from_json_file(
        path=MESSAGES_FILE_PATH,
        default_lang="en",
        language_getter=get_test_language
    )


def test_get_message_with_contextvar_es(i18n):
    test_language.set("es")
    msg = i18n.get_message("token_expired")
    assert msg == "El token ha expirado"


def test_get_message_with_contextvar_en(i18n):
    test_language.set("en")
    msg = i18n.get_message("token_expired")
    assert msg == "Token has expired"


def test_get_message_with_unsupported_lang_fallback(i18n):
    test_language.set("de")  # alemán no está soportado
    msg = i18n.get_message("token_expired")
    assert msg == "Token has expired"  # fallback al default_lang


def test_get_message_with_manual_lang_override(i18n):
    test_language.set("es")  # Esto debería ignorarse
    msg = i18n.get_message("token_expired", lang="fr")
    assert msg == "Le jeton a expiré"


def test_missing_key_returns_placeholder(i18n):
    test_language.set("es")
    msg = i18n.get_message("non_existent_key")
    assert msg == "[non_existent_key]"


def test_get_message_without_contextvar_and_without_lang(i18n):
    # Borra el valor en el contextvar (no se ha seteado explícitamente)
    test_language = ContextVar("test_language", default="en")
    msg = i18n.get_message("user_not_found")
    assert msg == "User not found"
