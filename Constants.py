import screeninfo

_ASPECT_RATIO = (16,9)
_SMALL_RESOLUTION = (_ASPECT_RATIO[0]*80, _ASPECT_RATIO[1]*80)#(1280,720)
_MONITOR_RESOLUTION = (screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height)

_CAPTION = "new game"

_BUTTON_GAP = 2

_TRANSITION_DELAY = 0.2 # secs

_WORLDS_PATH = "C:/Users/User/Desktop/Game/worlds/"