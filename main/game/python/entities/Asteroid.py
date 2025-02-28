import random
import pygame
from util.mathextra.Location import Angle, Orientation, Point, Vector
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class Asteroid:
    def __init__(self, window:pygame.Surface, size: Point, res_scalar: Point):
        self.size = size.times(res_scalar)
        self.__window__ = window
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        self.windowmask = pygame.mask.from_surface(self.__window__)
        
        self.asteroid = self.i_h.resize(self.i_h.get("Asteroid.png"), self.size)
        self.asteroid_mask = pygame.mask.from_surface(self.asteroid)
        self.fire_size = self.size.times(Point(1.8, 3)).scale_by(1.1)
        self.fire = self.i_h.resize(self.i_h.get("fire.png"), self.fire_size)
        
        self.lookahead = Point(0,0)
        self.pos: Orientation = Orientation.init(size.negate().minus(Point.fill(200)), Angle.in_degrees(0))
        self.vector = Vector(0, Angle.in_degrees(180))
        self.angle_vel = Angle.in_degrees(random.randint(-20, 20) / 60) # deg/s
        self.spawned = False
        
    def render(self):
        # self.__window__.blit(self.fire, self.pos.get_point().minus(Point(150, 1.75*self.size.y)).tuple())
        # temp = self.i_h.rotate(self.asteroid, self.pos.angle)
        # TODO: commented out until you look into using mask objects from pygame for "pixel perfect collisions"
        self.__window__.blit(self.asteroid, self.pos.get_point().tuple())
        # self.asteroid.draw(, self.pos.get_point().tuple())
    def spawn(self, xpos):
        self.pos = Orientation.init(Point(xpos, -self.size.y), self.pos.angle)
        self.spawned = True
        return self
    def move_x(self, amount: float):
        self.pos.x += amount
        return self
    def move_y(self, amount: float):
        self.pos.y += amount
        return self
    def move(self, amount: Point):
        self.pos = self.pos.translate_by(amount)
        return self
    def spin(self):
        self.pos = self.pos.rotate_by(self.angle_vel)
        return self
    
    def collided(self, other: pygame.Mask, other_point: Point)->bool:
        # temp = self.rect
        # vel = self.vector.get_point().scale_by(1/60)
        # temp.x += vel.x
        # temp.y += vel.y
        # return temp.colliderect(other)
        return self.asteroid_mask.overlap(other, other_point.minus(self.lookahead).round().tuple())
    
    def move_along_path(self, dt):
        self.pos = self.pos.translate_by(self.vector.get_point().scale_by(dt))
        self.lookahead = self.pos.translate_by(self.vector.get_point().scale_by(dt))
        return self
    def reset(self):
        self.spawned = False
        self.pos = Orientation.init(self.size.negate().minus(Point.fill(200)), Angle.in_degrees(0))
        self.vector = Vector(0, Angle.in_degrees(180))
        return self