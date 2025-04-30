import pygame
from Constants import *
import random 

class Gate(pygame.sprite.Sprite):
    speed_add = 0
    def __init__(self, floor_Group) -> None:
        super().__init__()
        self.image = pygame.image.load(GATE_URL)
        self.image = pygame.transform.scale(self.image, (GATE_SIZE, GATE_SIZE))
        self.rect = self.image.get_rect(midbottom = (500,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.floor_Group = floor_Group
        self.speed_y = 5 
    
    def update(self) -> None:
        self.speed_y += GRAVITY
        self.rect.y += self.speed_y

        for segment_sprite in self.floor_Group:            
            if self.rect.colliderect(segment_sprite.rect):
                # Falling: Collided with ground
                self.rect.y = segment_sprite.rect.y - self.rect.height
                self.speed_y = 0
