import pygame

from util.mathextra.Location import Point
from util.mathextra.MathModule import mean

class TextHelpers:
    def __init__(self, window: pygame.Surface, font, size: float):
        self.__window__ = window
        self._font_ = font
        self._size_ = size
        self.bold = False
        self.italic = False
        self.strikethrough = False
        self.underline = False
        self.__write__ = pygame.font.SysFont(self._font_, self._size_)
    def bolded(self, is_bold: bool):
        self.bold = is_bold
        return self
    def italicized(self, is_italic: bool):
        self.italic = is_italic
        return self
    def strikedthrough(self, is_strikedthrough: bool):
        self.strikethrough = is_strikedthrough
        return self
    def underlined(self, is_underlined: bool):
        self.underline = is_underlined
        return self
    def reset_format(self):
        self.bolded(False)
        self.italicized(False)
        self.strikedthrough(False)
        self.underlined(False)
        return self
    def with_font(self, font: str):
        self._font_ = font
        self.__write__ = pygame.font.SysFont(self._font_, self._size_)
        return self
    def with_size(self, size: float):
        self._size_ = size
        self.__write__ = pygame.font.SysFont(self._font_, self._size_)
        return self
    def render(self, text: str, color, pos: Point):
        self.__write__.bold = self.bold
        self.__write__.italic = self.italic
        self.__write__.strikethrough = self.strikethrough
        self.__write__.underline = self.underline
        temp = self.__write__.render(text, 1, color)
        if pos == Point._key():
            pos = Point(mean(self.__window__.get_width(),temp.get_width()),mean(self.__window__.get_height(),temp.get_height()))
        self.__window__.blit(temp, pos.tuple())
        return self
    def render_highlighted(self, text: str, color, highlight_color, pos: Point):
        self.__write__.bold = self.bold
        self.__write__.italic = self.italic
        self.__write__.strikethrough = self.strikethrough
        self.__write__.underline = self.underline
        temp = self.__write__.render(text, 1, color, highlight_color)
        if pos == Point._key():
            pos = Point(mean(self.__window__.get_width(),temp.get_width()),mean(self.__window__.get_height(),temp.get_height()))
        self.__window__.blit(temp, pos.tuple())
        return self