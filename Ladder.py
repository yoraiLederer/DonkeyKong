import pygame
from Constants import *

class Ladder(pygame.sprite.Sprite):
    
    def __init__(self, img, pos) -> None:
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)    


