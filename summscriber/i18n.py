"""
GUI translations. Detects system locale and provides strings in English, Spanish, or Portuguese.
Falls back to English for unsupported locales.
"""
import locale
import os

# Keys used in the GUI (and CLI when invoked from GUI)
MESSAGES = {
    "en": {
        "summary": "Summary",
        "original_text": "Original text",
        "reply": "Reply",
        "copy_selection": "Copy selection",
        "copy_all": "Copy all",
        "error": "Error",
        "usage": "Usage: summscriber-gui FILE",
        "running": "Running...",
        "loading": "Loading...",
    },
    "es": {
        "summary": "Resumen",
        "original_text": "Texto original",
        "reply": "Respuesta",
        "copy_selection": "Copiar selección",
        "copy_all": "Copiar todo",
        "error": "Error",
        "usage": "Uso: summscriber-gui ARCHIVO",
        "running": "Ejecutando...",
        "loading": "Cargando...",
    },
    "pt": {
        "summary": "Resumo",
        "original_text": "Texto original",
        "reply": "Resposta",
        "copy_selection": "Copiar seleção",
        "copy_all": "Copiar tudo",
        "error": "Erro",
        "usage": "Uso: summscriber-gui ARQUIVO",
        "running": "Executando...",
        "loading": "Carregando...",
    },
}

_SUPPORTED = frozenset(MESSAGES.keys())
_current_lang: str | None = None


def _detect_language() -> str:
    """Return language code (en, es, pt) from system locale. Defaults to en."""
    try:
        loc, _ = locale.getdefaultlocale()
    except Exception:
        loc = None
    if not loc:
        loc = os.environ.get("LANG", "") or os.environ.get("LC_ALL", "")
    if loc:
        code = (loc.split("_")[0] or "en").lower()[:2]
        if code in _SUPPORTED:
            return code
    return "en"


def get_language() -> str:
    """Return current UI language (en, es, pt)."""
    global _current_lang
    if _current_lang is None:
        _current_lang = _detect_language()
    return _current_lang


def set_language(lang: str) -> None:
    """Set UI language (en, es, pt). Used for tests or overrides."""
    global _current_lang
    _current_lang = lang if lang in _SUPPORTED else "en"


def _(key: str) -> str:
    """Return translated string for key. Falls back to English if key or language missing."""
    lang = get_language()
    table = MESSAGES.get(lang, MESSAGES["en"])
    return table.get(key, MESSAGES["en"].get(key, key))
