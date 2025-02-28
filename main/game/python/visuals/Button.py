import pygame
from GameStates import GameStates
from util.MouseUtil import ClickType, Mouse
from visuals.Sprite import Sprite
from util.TextHelpers import TextHelpers
from util.mathextra.Location import Point

class Button(Sprite):
    def __init__(self, screen: pygame.Surface, pos: Point, size: Point, text: str, font_size: float = 20, bg_color: pygame.Color="gray", bg_hover: pygame.Color="green", font="times new roman"):
        super().__init__(screen, size)
        self.at(pos)
        self.text = text
        self.bg_color = bg_color
        self.bg_hover = bg_hover
        self.font_size = font_size
        self.font = font
        self.border_size = 2
        
        self.use_text = True
        
    def with_image(self, filename: str):
        self.sprite = self.i_h.resize(self.i_h.get(filename), self.size.div_by(2))
        self.use_text = False
        return self
    
    def with_text(self, text: str):
        self.text = text
        self.use_text = True
        return self
    def with_screen(self, screen: pygame.Surface):
        self.__window__ = screen
        return self
    
    def with_border_size(self, size: float):
        self.border_size = size
        return self

    def render(self, mouse: Mouse, border: bool = True):
        # Draw the button border
        if border:
            pygame.draw.rect(self.__window__, "black", pygame.Rect(self.pos.x-self.border_size, self.pos.y-self.border_size, self.size.x+self.border_size*2, self.size.y+self.border_size*2))
        # Draw the button background
        if self.is_hovering(mouse.pos):
            bg = pygame.draw.rect(self.__window__, self.bg_hover, pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
        else:
            bg = pygame.draw.rect(self.__window__, self.bg_color, pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
        
        # Draw the button text/image
        if self.use_text:
            writer = TextHelpers(self.__window__, self.font, self.font_size)
            txt = writer.make_text(self.text, "black")
            writer.render(txt, Point(self.pos.x + self.size.x/2 - txt.get_width()/2, self.pos.y + self.size.y/2 - txt.get_height()/2))
        else:
            self.__window__.blit(self.sprite, Point(self.pos.x + self.size.x/2 - self.sprite.get_width()/2, self.pos.y + self.size.y/2 - self.sprite.get_height()/2).tuple())

    def is_hovering(self, mouse_pos: Point)-> bool:
        if self.pos.x <= mouse_pos.x <= self.pos.x + self.size.x and self.pos.y <= mouse_pos.y <= self.pos.y + self.size.y:
            return True
    def is_Lclicked(self, mouse: Mouse, type: ClickType = ClickType.RELEASED)-> bool:
        return self.is_hovering(mouse.pos) and mouse.left_click.equals(type)
    def is_Rclicked(self, mouse: Mouse, type: ClickType = ClickType.RELEASED)-> bool:
        return self.is_hovering(mouse.pos) and mouse.right_click.equals(type)
    def is_Mclicked(self, mouse: Mouse, type: ClickType = ClickType.RELEASED)-> bool:
        return self.is_hovering(mouse.pos) and mouse.middle_click.equals(type)
    
    def Lpressed(self, mouse: Mouse, type: ClickType = ClickType.RELEASED) -> bool:
        return self.is_Lclicked(mouse, type=type)
    def Rpressed(self, mouse: Mouse, type: ClickType = ClickType.RELEASED) -> bool:
        return self.is_Rclicked(mouse, type=type)
    def Mpressed(self, mouse: Mouse, type: ClickType = ClickType.RELEASED) -> bool:
        return self.is_Mclicked(mouse, type=type)