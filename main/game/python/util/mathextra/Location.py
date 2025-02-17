import math
from util.mathextra import MathModule

class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    def fill(both: float):
        return Point(both, both).with_mid(Point(both, both))
    def with_mid(self, window_size):
        self.mid = window_size.minus(self).div_by(2)
        return self
    def _key():
        return Point(1.23234, 242.3322)
        
    def plus(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def minus(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def times(self, other):
        return Point(self.x * other.x, self.y * other.y)
    def div(self, other):
        return Point(self.x / other.x, self.y / other.y)
    def scale_by(self, num: float):
        return self.times(Point(num, num))
    def div_by(self, num: float):
        return self.div(Point(num, num))
    
    def negate(self):
        return self.scale_by(-1)
    
    def tuple(self)->tuple[float, float]:
        return (self.x, self.y)
    def equals(self, other)->bool:
        return (self.x == other.x) and (self.y == other.y)
    def is_key(self)->bool:
        return self.equals(self._key())
    
    def norm(self):
        return math.hypot(self.x, self.y)
    def angle(self):
        return Angle().in_radians(MathModule.good_atan2(self.y, self.x))
        
class Angle:
    def __init__(self):
        self.rad = 0.0
        self.deg = 0.0
        self.rot = 0.0
        
    def in_radians(self, rad: float):
        self.rad = rad
        self.deg = math.degrees(rad)
        self.rot = rad/(math.pi*2.0)
        
    def in_degrees(self, deg: float):
        self.deg = deg
        self.rad = math.radians(deg)
        self.rot = deg/360.0
        
    def in_rotations(self, rot: float):
        self.rot = rot
        self.deg = rot*360.0
        self.rad = rot*(math.pi*2.0)
        
    def plus(self, other):
        return Angle().in_radians(self.rad + other.rad)
    def minus(self, other):
        return Angle().in_radians(self.rad - other.rad)
    def times(self, num):
        return Angle().in_radians(self.rad * num)
    
    def negate(self):
        return self.times(-1)
    
    def cos(self):
        return math.cos(self.rad)
    def sin(self):
        return math.sin(self.rad)
    def tan(self):
        return math.tan(self.rad)
    
    def acos(self):
        return math.acos(self.rad)
    def asin(self):
        return math.asin(self.rad)
    def atan(self):
        return math.atan(self.rad)
    

class Orientation:
    def __init__(self, x: float, y: float, angle: Angle):
        self.__point__ = Point(x, y)
        self.angle = angle
    def __init__(self, point: Point, angle: Angle):
        self.__point__ = point(point.x, point.y)
        self.angle = angle
    
    def get_point(self) -> Point:
        return self.__point__
    def X(self) -> float:
        return self.__point__.x
    def Y(self) -> float:
        return self.__point__.y
    def get_angle(self) -> Angle:
        return self.angle
    
    def plus(self, other):
        return Orientation(self.translate_by(other.get_point()), self.rotate_by(other.get_angle()))
    def minus(self, other):
        return Orientation(self.translate_by(other.get_point().negate()), self.rotate_by(other.get_angle().negate()))
    
    def translate_by(self, new: Point) -> Point:
        return self.__point__.plus(new)
    def rotate_by(self, new: Angle) -> Angle:
        return self.angle.plus(new)