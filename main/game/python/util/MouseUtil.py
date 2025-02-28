import enum
import time
import pygame

from util.mathextra.Location import Point

class ClickType(enum.Enum):
    IDLE = 0
    PRESSED = 1
    HOLDING = 2
    RELEASED = 3
    
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
        # self.__right_history__[1] = self.__right_history__[0]
        # self.__middle_history__[1] = self.__middle_history__[0]
        
        self.__left_history__[0] = self._get_left_click_()
        # self.__right_history__[0] = self._get_right_click_()
        # self.__middle_history__[0] = self._get_middle_click_()
        
        if self.left(False, False):
            self.left_click = ClickType.IDLE
        elif self.left(False, True):
            self.left_click = ClickType.PRESSED
        elif self.left(True, True):
            self.left_click = ClickType.HOLDING
        elif self.left(True, False):
            self.left_click = ClickType.RELEASED
            
        # if self.right(False, False):
        #     self.right_click = ClickType.IDLE
        # elif self.right(False, True):
        #     self.right_click = ClickType.PRESSED
        # elif self.right(True, True):
        #     self.right_click = ClickType.HOLDING
        # elif self.right(True, False):
        #     self.right_click = ClickType.RELEASED
            
        # if self.middle(False, False):
        #     self.middle_click = ClickType.IDLE
        # elif self.middle(False, True):
        #     self.middle_click = ClickType.PRESSED
        # elif self.middle(True, True):
        #     self.middle_click = ClickType.HOLDING
        # elif self.middle(True, False):
        #     self.middle_click = ClickType.RELEASED
    
    def left(self, a:bool, b:bool) -> bool:
        return self.__left_history__[0]==a and self.__left_history__[1]==b
    def right(self, a:bool, b:bool) -> bool:
        return self.__right_history__[0]==a and self.__right_history__[1]==b
    def middle(self, a:bool, b:bool) -> bool:
        return self.__middle_history__[0]==a and self.__middle_history__[1]==b
    
    def _get_pos_(self):
        return Point.from_tuple(pygame.mouse.get_pos())
    
    def _get_left_click_(self):
        return pygame.mouse.get_pressed()[0]
    def _get_right_click_(self):
        return pygame.mouse.get_pressed()[2]
    def _get_middle_click_(self):
        return pygame.mouse.get_pressed()[1]