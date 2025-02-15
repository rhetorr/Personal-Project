import math

def round_to(value: float, precision: float):
    return round(value/precision)*precision

def good_atan2(y, x) -> float:
    if x == 0:
        if y < 0:
            return 3*math.pi/2
        else:
            return math.pi/2
    else:
        if y < 0:
            return (3*math.pi/2)-math.atan(y/x)
        elif y == 0:
            if x < 0:
                return math.pi
            else:
                return 0
        else:
            return (math.pi/2)-math.atan(y/x)

def mean(*args):
    ran = 0
    accum = 0
    for i in args:
        ran+=1
        accum+=i
    return accum/ran
        