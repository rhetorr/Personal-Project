import pygame

class ImageHelpers():
    def __init__(self, path: str):
        self._path_ = path
    def get(self, filename: str):
        return pygame.image.load(self._path_ + filename)
    def resize(self, surface: pygame.Surface, x: float, y: float):
        return pygame.transform.scale(surface, (x,y))
    def scale_by(self, surface: pygame.Surface, scalar: float):
        return pygame.transform.scale_by(surface, scalar)
    def scale(self, surface: pygame.Surface, x_scalar: float, y_scalar: float):
        return self.resize(surface, (surface.get_width()*x_scalar), (surface.get_height()*y_scalar))