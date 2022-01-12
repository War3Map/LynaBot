import json
import os.path
from pathlib import Path

CONFIG_PATH = "./config"
CONFIG: dict = {}


def read_config(config_path):
    try:
        with open(config_path, 'r', encoding="utf-8") as file_obj:
            config_dict = json.load(file_obj)
        return config_dict
    except FileNotFoundError:
        # TODO: to log file
        return dict()
    except PermissionError:
        # TODO: to log file
        return dict()
    except Exception as ex:
        # TODO: to log file
        print(f"unknown exception in config load {ex}")
        return dict()


def load_configs():
    """
    Loads configuration from config files (folder config)
    """
    conf_path: Path = Path(CONFIG_PATH)
    for file_path in conf_path.rglob("*.json"):
        conf = read_config(file_path)
        if conf:
            CONFIG.update(conf)


def get_setting(setting_name: str):
    return CONFIG[setting_name] if setting_name in CONFIG else ""


load_configs()
