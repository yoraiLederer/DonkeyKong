import pygame
import numpy as np
from Constants import *


class Graphics:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))# Set window title
        pygame.display.set_caption(MAIN_CAPTION)
        
        self.header_surf = pygame.Surface((HEADER_WIDTH, HEADER_HEIGHT))
        self.main_surf = pygame.Surface((MAIN_WIDTH, MAIN_HEIGHT))
        
        self.header_surf.fill(HEADER_COLOR)
        self.main_surf.fill(MAIN_COLOR)

        self.screen.blit(self.header_surf, (HEADER_RECT.left, HEADER_RECT.top))
        self.screen.blit(self.main_surf, (MAIN_RECT.left, MAIN_RECT.top))
        
        self.load_sounds()        
        # self.game_started_sound.play()

    def load_sounds(self):
        self.game_started_sound = pygame.mixer.Sound(GAME_STARTED_SOUND_URL)
        self.game_bonus_sound = pygame.mixer.Sound(GAME_BONUS_SOUND_URL)
        self.got_hit_sound = pygame.mixer.Sound(GOT_HIT_SOUND_URL)
        self.game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND_URL)

    def clear_screen(self):        
        self.header_surf.fill(HEADER_COLOR)
        self.main_surf.fill(MAIN_COLOR)

    def draw(self, state):        
        state.barrel_Group.draw(self.main_surf)
        state.floor_Group.draw(self.main_surf)
        state.ladder_Group.draw(self.main_surf)
        state.mario_Group.draw(self.main_surf)
        state.donkey_kong_Group.draw(self.main_surf)
        state.gate_Group.draw(self.main_surf)

        self.screen.blit(self.header_surf, (HEADER_RECT.left, HEADER_RECT.top))
        self.screen.blit(self.main_surf, (MAIN_RECT.left, MAIN_RECT.top))

    
    def game_over(self, score):
        self.header_surf.fill(WHITE)
        # self.game_over_sound.play()
        self.write_text(self.header_surf, "Game Ended - Score: " + str (score), (300, 10), RED)
        self.write_text(self.header_surf, "Another Game? (y/n)", (700, 10), RED)
        self.screen.blit(self.header_surf, (0,0))
        pygame.display.update()
        # pygame.time.delay(2000)  

    def write_text(self, surface, text, pos=(10, 10), color=BLUE):
        font = pygame.font.SysFont("helvetica", 28, True)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)
