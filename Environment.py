import pygame
import numpy as np
from Constants import *
from State import State
from DonkeyKong import DonkeyKong
from Mario import Mario
from FloorTile import FloorTile
from Ladder import Ladder
from Barrel import Barrel
from  Gate import Gate
import random

class Environment:
    def __init__(self, delay = 2000) -> None:
        self.state = State() 
        self.delay = delay   
        self.reward = 0
        self.gate_reward = 10
        self.hit_reward = -5
        self.close_to_lader_reward = 2
        self.max_floor = 0
        self.jump_reward = 2

    def move(self, action):
        self.state.move(action) 
    
    def get_reward(self, action, state, next_state):
        on_ladder_idx = 2
        dist_ladder_idx = 4
        reward = 0     
        if self.state.reached_gate():
            return self.gate_reward
        if self.state.got_hit():
            reward += self.hit_reward
            self.state.score += 1
        
        if state[on_ladder_idx] == 0:
            if state[dist_ladder_idx] < 0 and action == 2:
                reward += self.close_to_lader_reward
            elif state[dist_ladder_idx] > 0 and action == 3:
                reward += self.close_to_lader_reward
            else:
                reward -= self.close_to_lader_reward
        else:
            if action == 4:
                reward += self.close_to_lader_reward
            else:
                reward -= self.close_to_lader_reward


        DANGER_ZONE = 0.060   # ~16*7/2/1200
        barrel_dist = state[9]   
        if  0 < barrel_dist < DANGER_ZONE: # Mario in danger zobe
            if state[3] == 0:  # not in Jumping mode 
                if action == 1: # jumping
                    reward += self.jump_reward
                else:
                    reward -= self.jump_reward
            else:
                if action == 1:  # if in the air don't jump again
                    reward -= self.jump_reward
        else:
            if action == 1:   # don't jump
                reward -=self.jump_reward
        return reward   
        

    def play(self, game_bonus_sound=None, got_hit_sound=None):
        if self.state.reached_gate():
            # game_bonus_sound.play()
            # pygame.time.delay(self.delay)  
            self.state.lives_left -= 1
            # Barrel.speed_add =  self.state.score
            self.state.restart(new_game=False)
            

        else:        
        # got_hit = self.state.got_hit()
        # if got_hit:            
        #     # got_hit_sound.play()    
        #     pygame.time.delay(self.delay)  
        #     self.state.lives_left -= 1           
        #     # self.state.restart(new_game=False)
        #     # Barrel.speed_add = 0
        #     # self.reward = self.hit_reward
        #     print("hit\n")

            self.state.add_new_barrel()

        return self.state.lives_left == 0

 
    
