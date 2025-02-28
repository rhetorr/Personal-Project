import math
from util.mathextra import MathModule

class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y
    def fill(both: float)->"Point":
        return Point(both, both).with_mid(Point(both, both))
    def from_tuple(tup: tuple[float, float]) -> 'Point':
        return Point(tup[0], tup[1])
    def with_mid(self, window_size):
        self.mid = Point(window_size.x/2-self.x/2, window_size.y/2-self.y/2)
        return self
    def _key():
        return Point(1.23234, 242.3322)
        
    def plus(self, other: "Point"):
        return Point(self.x + other.x, self.y + other.y)
    def minus(self, other: "Point"):
        return Point(self.x - other.x, self.y - other.y)
    def times(self, other: "Point"):
        return Point(self.x * other.x, self.y * other.y)
    def div(self, other: "Point"):
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
        return Angle.in_radians(MathModule.good_atan2(self.y, self.x))
    
    def vector(self)->"Vector":
        return Vector(self.norm(), self.angle())
        
class Angle:
    def __init__(self, rad, deg, rot):
        self.rad = rad
        self.deg = deg
        self.rot = rot
        
    def in_radians(rad: float)->"Angle":
        return Angle(rad, math.degrees(rad), rad/(math.pi*2.0))
        
    def in_degrees(deg: float)->"Angle":
        return Angle(math.radians(deg), deg, deg/360.0)
        
    def in_rotations(rot: float)->"Angle":
        return (rot*(math.pi*2.0), rot*360.0, rot)
        
    def plus(self, other: "Angle")->"Angle":
        return Angle.in_radians(self.rad + other.rad)
    def minus(self, other: "Angle")->"Angle":
        return Angle.in_radians(self.rad - other.rad)
    def times(self, num):
        return Angle.in_radians(self.rad * num)
    
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
    
    def toVector(self, length: float)->Point:
        return Point(length*self.cos(), length*self.sin())

class Vector:
    def __init__(self, magnitude: float, angle: Angle):
        self.magnitude = magnitude
        self.angle = angle
        
    def get_x(self)->float:
        return self.magnitude*self.angle.cos()
    def get_y(self)->float:
        return self.magnitude*self.angle.sin()
    
    def get_point(self)->Point:
        return Point(self.get_x(), self.get_y())
    

class Orientation:
    def __init__(self, x: float, y: float, angle: Angle):
        self.x = x
        self.y = y
        self.angle = angle
        
    def init(point: Point, angle: Angle)->'Orientation':
        return Orientation(point.x, point.y, angle)
    
    def get_point(self) -> Point:
        return Point(self.x, self.y)
    def get_angle(self) -> Angle:
        return self.angle
    
    def translate_by(self, new: Point) -> "Orientation":
        return Orientation.init(self.get_point().plus(new), self.angle)
    def rotate_by(self, new: Angle) -> "Orientation":
        return Orientation.init(self.get_point(), self.angle.plus(new))