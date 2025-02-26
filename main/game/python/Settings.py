from util.mathextra.Location import Point
from util.FileWriter import File
import getpass

_USER = getpass.getuser()

_SETTINGS_FILE_NAME = "settings.txt"
_EMPTY_SETTINGS = {
    "main_monitor": 0,
    "fullscreen": False
    }
_SETTINGS_PATH = 'C:/Users/' + _USER + '/AppData/Local/PersonalProject/' + _SETTINGS_FILE_NAME

def player_speed(res_scalar: Point):
    return res_scalar.times(Point.fill(64).scale_by(2)) # REMEMBER IT IS PX/S

def save_settings(settings: dict):
    file = File()
    file.make(_SETTINGS_FILE_NAME)
    file.__file_path = _SETTINGS_PATH
    file.write([str(settings)])
    
def get_config_dict() -> dict:
    settings = File()
    settings.make(_SETTINGS_FILE_NAME)
    settings.__file_path = _SETTINGS_PATH
    if not settings.read():
        return _EMPTY_SETTINGS
    return eval(settings.read())