#!/usr/bin/env python3
"""
List models from the configured OpenAI-compatible API (e.g. Open WebUI).
Uses the same config as summscriber. Run from project root with venv active.
"""
import json
import os
import sys
from pathlib import Path

import configparser
CONFIG_FILENAME = "config.ini"
def _global_config_path():
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "summscriber" / CONFIG_FILENAME
def load_config():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    candidates = [Path.cwd() / CONFIG_FILENAME, _global_config_path(), project_root / CONFIG_FILENAME]
    config_path = next((p for p in candidates if p.exists()), None)
    out = {"api_key": "", "base_url": "https://api.openai.com/v1", "model": "gpt-4o-mini"}
    if config_path:
        parser = configparser.ConfigParser()
        parser.read(config_path, encoding="utf-8")
        if parser.has_section("openai"):
            out["api_key"] = parser.get("openai", "api_key", fallback="").strip()
            out["base_url"] = parser.get("openai", "base_url", fallback="").strip() or out["base_url"]
            out["model"] = parser.get("openai", "model", fallback="gpt-4o-mini").strip()
    out["api_key"] = os.environ.get("OPENAI_API_KEY") or out["api_key"]
    out["base_url"] = os.environ.get("OPENAI_BASE_URL") or out["base_url"]
    return out

def main() -> int:
    cfg = load_config()
    if not cfg["api_key"]:
        print("No API key found.", file=sys.stderr)
        return 1
    base = cfg["base_url"].rstrip("/")
    # Open WebUI: GET /api/models. OpenAI-style: often GET /v1/models or /models.
    for path in ["/models", "/api/models", "/v1/models"]:
        url = base + path
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {cfg['api_key']}"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
                break
        except Exception as e:
            continue
    else:
        print("Could not list models (tried /models, /api/models, /v1/models).", file=sys.stderr)
        print("Tip: For Open WebUI use base_url = https://chat.ccad.unc.edu.ar/api", file=sys.stderr)
        return 1
    # Handle both OpenAI format ({data: [{id: "..."}]}) and Open WebUI format
    models = []
    if isinstance(data, dict) and "data" in data:
        models = [m.get("id") or m.get("id") for m in data["data"] if isinstance(m, dict)]
    elif isinstance(data, list):
        models = [m.get("id") or m.get("name", m) if isinstance(m, dict) else str(m) for m in data]
    else:
        models = list(data) if isinstance(data, (list, dict)) else []
    if not models and isinstance(data, dict):
        models = [data.get("id") or data.get("name")] if data.get("id") or data.get("name") else []
    print("Configured model:", cfg["model"])
    print("Available models:", ", ".join(str(m) for m in models[:30]) or "(none parsed)")
    if cfg["model"] and models and cfg["model"] not in models:
        print("Warning: configured model not in list. Check the name in the web UI.", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
