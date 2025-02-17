import pygame
from GameStates import GameStates
from util.mathextra.Location import Point
from util.TextHelpers import TextHelpers
from .Sprite import Sprite
from visuals import VisualsUtil
from util.ImageHelpers import ImageHelpers

class VisualsManager:
    def __init__(self, resolution: tuple, caption: str, icon_filename: str):
        self.i_h = ImageHelpers(VisualsUtil._ASSETS_PATH)
        
        self.window = pygame.display.set_mode(resolution, vsync=1) #creating window
        pygame.display.set_caption(caption)
        self.icon = Sprite(self.window, Point.fill(100), GameStates.MENU).from_image(icon_filename)
        pygame.display.set_icon(self.icon.sprite)
        self.font = TextHelpers(self.window, "arial", 20)
        
    def render(self, surface, coords):
        return self.window.blit(surface, coords)
    
    def graphics(self, state: GameStates, player: Sprite):
        self.window.fill("white")
        player.hide()
        match state:
            case GameStates.NOT_RUNNING:
                self.font.render("EVIL!!!!!!!!!!!!!!!!!!!!!!", "black", Point._key())
            case GameStates.LAUNCHING:
                self.font.render("LOADING...", "black", Point._key())
            case GameStates.MENU:
                pygame.draw.line(self.window, "black", (self.window.get_width()/2, 0), (self.window.get_width()/2, self.window.get_height()))
                pygame.draw.line(self.window, "black", (0, self.window.get_height()/2), (self.window.get_width(), self.window.get_height()/2))
                self.icon.at(self.icon.size.mid).show().render()
            case GameStates.SETTINGS | GameStates.STARTING | GameStates.PLAYING | GameStates.LOST:
                player.show().render()
                self.font.render("wip", "black", Point._key())
            case GameStates.QUITTING:
                self.font.render("QUITTING...", "black", Point._key())
        pygame.display.update()
        