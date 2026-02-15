#!/usr/bin/env python3
"""
Test OpenAI connection using the same config as summscriber (config.ini or env).
Run from project root with the same venv you use for summscriber:
  python scripts/test_openai_connection.py
  # or: .venv/bin/python scripts/test_openai_connection.py
"""
import configparser
import os
import sys
from pathlib import Path

# Same config resolution as summscriber.cli
CONFIG_FILENAME = "config.ini"


def _global_config_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "summscriber" / CONFIG_FILENAME


def load_config() -> dict:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    candidates = [
        Path.cwd() / CONFIG_FILENAME,
        _global_config_path(),
        script_dir / CONFIG_FILENAME,
        project_root / CONFIG_FILENAME,
    ]
    config_path = next((p for p in candidates if p.exists()), None)
    out = {"api_key": "", "base_url": "https://api.openai.com/v1", "model": "gpt-4o-mini"}
    if config_path:
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        if parser.has_section("openai"):
            out["api_key"] = parser.get("openai", "api_key", fallback="").strip()
            out["base_url"] = (
                parser.get("openai", "base_url", fallback="").strip() or out["base_url"]
            )
            out["model"] = parser.get("openai", "model", fallback="gpt-4o-mini").strip()
    out["api_key"] = os.environ.get("OPENAI_API_KEY") or out["api_key"]
    out["base_url"] = os.environ.get("OPENAI_BASE_URL") or out["base_url"]
    return out


def main() -> int:
    cfg = load_config()
    if not cfg["api_key"]:
        print("No API key found (config.ini [openai] api_key or OPENAI_API_KEY)", file=sys.stderr)
        return 1
    print(f"Config: base_url={cfg['base_url']!r}  model={cfg['model']!r}")
    try:
        from openai import OpenAI
    except ImportError:
        print("Install openai: pip install openai", file=sys.stderr)
        return 1
    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
    try:
        r = client.chat.completions.create(
            model=cfg["model"],
            messages=[{"role": "user", "content": "Responde solo con una palabra: ¿qué color tiene el cielo?"}],
            max_tokens=20,
        )
        text = (r.choices[0].message.content or "").strip()
        print("Connection OK. Response:", repr(text) if text else "(empty)")
        return 0
    except Exception as e:
        print("Error:", type(e).__name__, str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
