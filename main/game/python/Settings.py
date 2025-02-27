import os
from util.mathextra.Location import Point
from util.FileWriter import File, Folder, delete_until

_SETTINGS_FILE_NAME = "settings.txt"
_EMPTY_SETTINGS = {
    "main_monitor": 0,
    "fullscreen": False,
    "fuel_usage": 2/60, # per second per frame
    "max_fuel": 125,
    "best_time": 0.0
    }

def save_settings(config: dict):
    settings = File().make(_SETTINGS_FILE_NAME)
    settings.write([str(config)])
    
def get_config_dict() -> dict:
    settings = File().make(_SETTINGS_FILE_NAME)
    if not settings.exists():
        save_settings(_EMPTY_SETTINGS)
        return _EMPTY_SETTINGS

    try:
        content = settings.read()
        config = eval(content)
        if not isinstance(config, dict):
            save_settings(_EMPTY_SETTINGS)
        return _EMPTY_SETTINGS
    except (IndexError, SyntaxError, ValueError, NameError):
        save_settings(_EMPTY_SETTINGS)
        return _EMPTY_SETTINGS