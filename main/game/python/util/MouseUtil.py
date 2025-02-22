import enum
import pygame

from util.mathextra.Location import Point

class ClickType(enum.Enum):
    IDLE = False
    PRESSED = True
    HOLDING = True
    RELEASED = False
    
    def equals(self, other: 'ClickType') -> bool:
        if not isinstance(other, ClickType):
            return False
        return self == other

class Mouse:
    def __init__(self):
        self.pos = Point(0,0)
        self.left_click = ClickType.IDLE
        self.right_click = ClickType.IDLE
        self.middle_click = ClickType.IDLE
        
        self.__left_history__ = [False, False]
        self.__right_history__ = [False, False]
        self.__middle_history__ = [False, False]
        
    def update(self):
        self.pos = self._get_pos_()
        
        self.__left_history__[1] = self.__left_history__[0]
        self.__right_history__[1] = self.__right_history__[0]
        self.__middle_history__[1] = self.__middle_history__[0]
        
        self.__left_history__[0] = self._get_left_click_()
        self.__right_history__[0] = self._get_right_click_()
        self.__middle_history__[0] = self._get_middle_click_()
        
        if not self.__left_history__[0] and not self.__left_history__[1]:
            self.left_click = ClickType.IDLE
        elif not self.__left_history__[0] and self.__left_history__[1]:
            self.left_click = ClickType.PRESSED
        elif self.__left_history__[0] and self.__left_history__[1]:
            self.left_click = ClickType.HOLDING
        elif self.__left_history__[0] and not self.__left_history__[1]:
            self.left_click = ClickType.RELEASED
            
        if not self.__right_history__[0] and not self.__right_history__[1]:
            self.right_click = ClickType.IDLE
        elif not self.__right_history__[0] and self.__right_history__[1]:
            self.right_click = ClickType.PRESSED
        elif self.__right_history__[0] and self.__right_history__[1]:
            self.right_click = ClickType.HOLDING
        elif self.__right_history__[0] and not self.__right_history__[1]:
            self.right_click = ClickType.RELEASED
            
        if not self.__middle_history__[0] and not self.__middle_history__[1]:
            self.middle_click = ClickType.IDLE
        elif not self.__middle_history__[0] and self.__middle_history__[1]:
            self.middle_click = ClickType.PRESSED
        elif self.__middle_history__[0] and self.__middle_history__[1]:
            self.middle_click = ClickType.HOLDING
        elif self.__middle_history__[0] and not self.__middle_history__[1]:
            self.middle_click = ClickType.RELEASED
    
    def _get_pos_(self):
        return Point.from_tuple(pygame.mouse.get_pos())
    
    def _get_left_click_(self):
        return pygame.mouse.get_pressed()[0]
    def _get_right_click_(self):
        return pygame.mouse.get_pressed()[2]
    def _get_middle_click_(self):
        return pygame.mouse.get_pressed()[1]