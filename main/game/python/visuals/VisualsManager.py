import pygame
from GameState import GameState
from util.GUIPriority import GUIPriority
from .Sprite import Sprite
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class VisualsManager:
    def __init__(self, resolution: tuple, caption: str, icon_filename: str):
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self.WIN = pygame.display.set_mode(resolution, vsync=1) #creating window
        pygame.display.set_caption(caption)
        pygame.display.set_icon(self.i_h.get(icon_filename))
        
    def render(self, surface, coords):
        return self.WIN.blit(surface, coords)
    
    def key(self, sprite: Sprite):
        return sprite.priority.value
    
    def graphics(self, state: GameState, sprites: list[Sprite]):
        self.WIN.fill("white")
        for sprite in sprites:
            sprite.hide()
        match state:
            case GameState.LAUNCHING:
                self.WIN.fill("green")
            case GameState.IN_GAME:
                for sprite in sprites:
                    sprite.show().render(self.WIN)
            case _:
                self.WIN.fill("black")
        pygame.display.update()
        