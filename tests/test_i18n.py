import os

from buddybet_i18n.i18n_service import I18nService  # <-- Aquí importas la clase principal


def test_token_expired_translations():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    i18n = I18nService(root_dir=root_dir)

    i18n.set_language("en")
    assert i18n.gettext("token_expired") == "Token has expired"

    i18n.set_language("es")
    assert i18n.gettext("token_expired") == "El token ha expirado"

    i18n.set_language("fr")
    assert i18n.gettext("token_expired") == "Le jeton a expiré"

    """
    i18n.set_language("de")  # idioma no existente, fallback a inglés
    assert i18n.gettext("token_expired") == "Token has expired"
    """
