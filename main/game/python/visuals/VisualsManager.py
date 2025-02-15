import pygame
from GameStates import FullState, GameState, PlayState
from util.mathextra.Location import Point
from util.TextHelpers import TextHelpers
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
        self.font = TextHelpers(self.WIN, "arial", 10)
        
    def render(self, surface, coords):
        return self.WIN.blit(surface, coords)
    
    def key(self, sprite: Sprite):
        return sprite.priority.value
    
    def graphics(self, full_state: FullState, sprites: list[Sprite]):
        self.WIN.fill("white")
        for sprite in sprites:
            sprite.hide()
        match full_state.game_state:
            case GameState.LAUNCHING:
                self.font.render("LOADING...", "black", Point._key())
            case GameState.IN_GAME:
                for sprite in sprites:
                    sprite.show() if sprite.check_appear(full_state) else sprite.hide()
                    sprite.render(self.WIN)
                match full_state.play_state:
                    case PlayState.OUT_OF_BOUNDS:
                        self.font.render("bad", "black", Point._key())
                    case PlayState.MENU:
                        self.font.render("haiii", "black", Point._key())
                    case _:
                        self.font.render("wait", "black", Point._key())
            case _:
                self.WIN.fill("black")
        pygame.display.update()
        