import pygame
from Constants import *

class Barrel (pygame.sprite.Sprite):
    speed_add = 0
    def __init__(self, img, pos, floor_Group) -> None:
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.floor_Group = floor_Group
        self.speed_x = BARREL_SPEED
        self.speed_y = 0
        self.max_barrel = 30
        self.speed_dir = 1
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self) -> None:
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        for segment_sprite in self.floor_Group:            
            if self.rect.colliderect(segment_sprite.rect):
                # Falling: Collided with ground
                self.rect.y = segment_sprite.rect.y - self.rect.height
                self.velocity_y = 0

        if self.rect.right > MAIN_WIDTH:            
            self.speed_dir = -self.speed_dir
        if self.rect.left < 0:            
            self.speed_dir = -self.speed_dir
            
        self.rect.x += (self.speed_x + Barrel.speed_add) * self.speed_dir
        
        if self.rect.bottom > MAIN_HEIGHT - TILE_SIZE - 1 and self.rect.left < 0:
            self.kill() 