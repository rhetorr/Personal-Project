import pygame

from util.mathextra.Location import Point


_ASSETS_PATH = "main/game/assets/"

def surface_size(surface: pygame.Surface)->Point:
    return Point(surface.get_width(), surface.get_height())
