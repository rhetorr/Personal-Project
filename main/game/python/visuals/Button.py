import pygame
from GameStates import GameStates
from visuals.Sprite import Sprite
from util.TextHelpers import TextHelpers
from util.mathextra.Location import Point

class Button(Sprite):
    def __init__(self, screen: pygame.Surface, pos: Point, size: Point, text: str, font_size: float = 20, bg_color="gray", bg_hover="green", font="arial"):
        super().__init__(screen, size, GameStates.MENU, GameStates.SETTINGS, GameStates.LOST)
        self.at(pos)
        self.text = text
        self.bg_color = bg_color
        self.bg_hover = bg_hover
        self.font_size = font_size
        self.font = font
        self.border_size = 2
    
    def with_text(self, text: str):
        self.text = text
        return self
    def with_screen(self, screen: pygame.Surface):
        self.__window__ = screen
        return self
    
    def with_border_size(self, size: float):
        self.border_size = size
        return self

    def render(self, border: bool = True):
        # Draw the button border
        if border:
            pygame.draw.rect(self.__window__, "black", pygame.Rect(self.pos.x-self.border_size, self.pos.y-self.border_size, self.size.x+self.border_size*2, self.size.y+self.border_size*2))
        # Draw the button background
        if self.is_hovering(Point.from_tuple(pygame.mouse.get_pos())):
            bg = pygame.draw.rect(self.__window__, self.bg_hover, pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
        else:
            bg = pygame.draw.rect(self.__window__, self.bg_color, pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
        
        # Draw the button text
        writer = TextHelpers(self.__window__, self.font, self.font_size)
        txt = writer.make_text(self.text, "black")
        writer.render(txt, Point(self.pos.x + self.size.x/2 - txt.get_width()/2, self.pos.y + self.size.y/2 - txt.get_height()/2))

    def is_hovering(self, mouse_pos: Point)-> bool:
        if self.pos.x <= mouse_pos.x <= self.pos.x + self.size.x and self.pos.y <= mouse_pos.y <= self.pos.y + self.size.y:
            return True
    def is_clicked(self, mouse_pos: Point, mouse_click: bool)-> bool:
        return self.is_hovering(mouse_pos) and mouse_click
    
    def acted_on(self) -> bool:
        return self.is_clicked(Point.from_tuple(pygame.mouse.get_pos()), pygame.mouse.get_pressed()[0])