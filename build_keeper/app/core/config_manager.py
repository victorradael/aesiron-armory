import json
import os
from typing import Any, Dict

from core.logger import get_logger

logger = get_logger(__name__)

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "app_config.json")

_DEFAULTS: Dict[str, Any] = {
    "app_code": "1MZVW78M",
}


def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_FILE):
        return dict(_DEFAULTS)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {**_DEFAULTS, **data}
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading app config: {e}")
        return dict(_DEFAULTS)


def save_config(config: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    logger.info("App config saved.")


def get_app_code() -> str:
    return load_config().get("app_code", _DEFAULTS["app_code"])


def set_app_code(code: str) -> None:
    config = load_config()
    config["app_code"] = code.strip()
    save_config(config)
