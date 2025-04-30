import pygame
from Constants import *

class DonkeyKong(pygame.sprite.Sprite):
    speed_add = 0
    def __init__(self, pos, floor_Group) -> None:
        super().__init__()
        self.image_r = pygame.image.load(DONKEY_KONG_R_URL)
        self.image_r = pygame.transform.scale(self.image_r, (DONKEY_KONG_SIZE, DONKEY_KONG_SIZE))
        self.image_l = pygame.image.load(DONKEY_KONG_L_URL)
        self.image_l = pygame.transform.scale(self.image_l, (DONKEY_KONG_SIZE, DONKEY_KONG_SIZE))
        self.image = self.image_r
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.floor_Group = floor_Group
        self.speed_x = DONKEY_KONG_SPEED_X
        self.speed_y = DONKEY_KONG_SPEED_Y      
        self.speed_dir = 1  
    
    def check_floor_collision(self) -> None:
        # Check if collides with any floor sprite
        hits = pygame.sprite.spritecollide(self, self.floor_Group, doKill=False)
        return len(hits) > 0
    
    def update(self) -> None:
        self.speed_y += GRAVITY
        self.rect.y += self.speed_y

        for segment_sprite in self.floor_Group:            
            if self.rect.colliderect(segment_sprite.rect):
                # Falling: Collided with ground
                self.rect.y = segment_sprite.rect.y - self.rect.height
                self.speed_y = 0

        if self.rect.right > MAIN_WIDTH:                 
            self.image = self.image_l   
            self.speed_dir = -self.speed_dir
        if self.rect.left < 0:       
            self.image = self.image_r     
            self.speed_dir = -self.speed_dir
    
        self.rect.x += (self.speed_x + DonkeyKong.speed_add) * self.speed_dir
                