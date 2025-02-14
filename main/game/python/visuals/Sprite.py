import math
import pygame
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers
from util.RectHelpers import RectHelpers
from util.GUIPriority import GUIPriority

class Sprite(RectHelpers):
    def __init__(self, size: tuple, priority: GUIPriority):
        super().__init__(-size[0]-100, -size[1]-100, size[0], size[1])
        super().__delattr__("__rect_value__")
        self.priority = priority
        self.sprite = pygame.surface.Surface(size)
        self.img_help = ImageHelpers(VisualsUtil._ASSETS_PATH)
        self.__saved_x__ = 0
        self.__saved_y__ = 0
        self._shown_ = False
    def from_image(self, name):
        self.sprite = self.img_help.resize(self.img_help.get(name), self.width, self.height)
        return self
    def render(self, window: pygame.Surface):
        window.blit(self.sprite, (self.x,self.y))
    def hide(self):
        if self._shown_:
            self.__saved_x__ = self.x
            self.__saved_y__ = self.y
            self.x = -self.width-100
            self.y = -self.height-100
        return self
    def show(self):
        if not self._shown_:
            self.x = self.__saved_x__
            self.y = self.__saved_y__
        return self
    def at(self, x, y):
        if self._shown_:
            self.x = x
            self.y = y
        else:
            self.__saved_x__ = x
            self.__saved_y__ = y
        return self