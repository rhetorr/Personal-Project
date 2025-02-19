import pygame
from GameStates import GameStates
from visuals.Sprite import Sprite
from util.TextHelpers import TextHelpers
from util.mathextra.Location import Point

class Button(Sprite):
    def __init__(self, screen: pygame.Surface, pos: Point, size: Point, text: str, font_size: float, font="arial", bg_color="gray", bg_hover="green"):
        super().__init__(screen, size, GameStates.MENU, GameStates.SETTINGS, GameStates.LOST)
        self.at(pos)
        self.text = text
        self.bg_color = bg_color
        self.bg_hover = bg_hover
        self.font_size = font_size
        self.font = font
    
    def with_text(self, text: str):
        self.text = text
        return self
    def with_screen(self, screen: pygame.Surface):
        self.screen = screen
        return self

    def draw(self, show=True):
        if show:
            self.show()
        else:
            self.hide()
        # Draw the button background
        if self.is_hovering(Point.from_tuple(pygame.mouse.get_pos())):
            bg = pygame.draw.rect(self.screen, self.bg_hover, pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
        else:
            bg = pygame.draw.rect(self.screen, self.bg_color, pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
        
        # Draw the button text
        writer = TextHelpers(bg, self.font, self.font_size)
        writer.render(self.text, "black", Point._key())

    def is_hovering(self, mouse_pos: Point)-> bool:
        if self.x <= mouse_pos.x <= self.pos.x + self.size.x and self.pos.y <= mouse_pos.y <= self.pos.y + self.size.height:
            return True
    def is_clicked(self, mouse_pos: Point, mouse_click: bool)-> bool:
        return self.is_hovering(mouse_pos) and mouse_click