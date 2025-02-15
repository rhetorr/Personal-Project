import pygame

from util.mathextra.Location import Point

class ImageHelpers():
    def __init__(self, path: str):
        self._path_ = path
    def get(self, filename: str):
        return pygame.image.load(self._path_ + filename)
    def resize(self, surface: pygame.Surface, size: Point):
        return pygame.transform.scale(surface, size.tuple())
    def scale_by(self, surface: pygame.Surface, scalar: float):
        return pygame.transform.scale_by(surface, scalar)
    def scale(self, surface: pygame.Surface, scalars: Point):
        return self.resize(surface, Point(surface.get_width(), surface.get_height()).times(scalars))