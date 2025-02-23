import pygame
from GameStates import GameStates
from util.mathextra.Location import Point
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers
from util.RectHelpers import RectHelpers

class Sprite(RectHelpers):
    def __init__(self, window:pygame.Surface, size: Point):
        super().__init__(size.negate().minus(Point.fill(100)), size)
        super().__delattr__("__rect_value__")
        self.sprite = pygame.surface.Surface(size.tuple())
        self.img_help = ImageHelpers(VisualsUtil._ASSETS_PATH)
        self.__saved_pos__ = Point.fill(0)
        self._shown_ = False
        self.__window__ = window
        self.size.with_mid(Point(self.__window__.get_width(), self.__window__.get_height()))
    def from_image(self, name):
        self.sprite = self.img_help.resize(self.img_help.get(name), self.size)
        return self
    def render(self):
        self.__window__.blit(self.sprite, self.pos.tuple())
    def hide(self):
        if self._shown_:
            self.__saved_pos__ = self.pos
            self.pos = self.size.negate().minus(Point.fill(100))
        return self
    def show(self):
        if not self._shown_:
            self.pos = self.__saved_pos__
        return self
    def at(self, pos: Point):
        if self._shown_:
            self.pos = pos
        else:
            self.__saved_pos__ = pos
        return self