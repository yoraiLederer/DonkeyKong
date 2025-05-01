import pygame
from Constants import *

class Mario(pygame.sprite.Sprite):
    def __init__(self, pos, floor_Group, ladder_Group) -> None:
        super().__init__()
        self.image_r = pygame.image.load(MARIO_R_URL)
        self.image_r = pygame.transform.scale(self.image_r, (MARIO_SIZE, MARIO_SIZE))
        self.image_l = pygame.image.load(MARIO_L_URL)
        self.image_l = pygame.transform.scale(self.image_l, (MARIO_SIZE, MARIO_SIZE))
        self.image = self.image_r
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.floor_Group = floor_Group
        self.ladder_Group = ladder_Group
        self.lives = MARIO_LIVES
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.is_on_ladder = False 

    def jump(self):
        if not self.is_jumping and not self.is_on_ladder:
            self.velocity_y = JUMP_VELOCITY
            self.is_jumping = True

    def move_left(self):
        self.image = self.image_l
        self.velocity_x = -MARIO_SPEED_X        

    def move_right(self):        
        self.image = self.image_r
        self.velocity_x = MARIO_SPEED_X

    def stop_moving(self):
        self.velocity_x = 0
        self.velocity_y = 0

    def go_up(self):  
        if self.is_on_ladder:
            self.velocity_y = -MARIO_SPEED_Y

    def go_down(self):    
        if self.is_on_ladder:
            self.velocity_y = MARIO_SPEED_Y

    def update(self):        
        # Apply gravity
        if not self.is_on_ladder:
            self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
    
        # Check collision with ground
        for segment_sprite in self.floor_Group:            
            if self.rect.colliderect(segment_sprite.rect) and not self.is_on_ladder:
                if self.velocity_y > 0:
                    # Falling: Collided with ground
                    self.rect.y = segment_sprite.rect.y - self.rect.height
                    self.velocity_y = 0
                    self.is_jumping = False
                elif self.velocity_y < 0:
                    # Jumping: Collided with ceiling
                    self.rect.y = segment_sprite.rect.bottom
                    self.velocity_y = 0


        # Check collision with ladder
        for ladder_sprite in self.ladder_Group:
            if ladder_sprite.rect.collidepoint(self.rect.centerx, self.rect.centery):
                self.is_on_ladder = True
                # if self.action == 0:
                #     self.velocity_y = 0  # Prevent falling
                break
        else:
            self.is_on_ladder = False

        # Update horizontal position
        self.rect.x += self.velocity_x
        
        # reset velocity
        self.velocity_x = 0     

        if self.rect.left <  0:
            self.rect.left = 0

        if self.rect.bottom > 800:
            self.rect.bottom = 780

        if self.rect.right > MAIN_WIDTH:
            self.rect.right = MAIN_WIDTH 