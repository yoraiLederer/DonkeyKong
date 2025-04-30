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
        self.gate_reward = 1
        self.hit_reward = -1
        self.close_to_lader_reward = 0.2
        self.max_floor = 0

    def move(self, action):
        self.state.move(action) 
    
    def get_reward(self, action, state, next_state):
        on_ladder_idx = 2
        dist_ladder_idx = 4
        reward = 0     
        if self.state.reached_gate():
            return self.gate_reward
        if self.state.got_hit():
            return self.hit_reward
        
        if abs(state[dist_ladder_idx]) < abs(next_state[dist_ladder_idx]):
            reward -= self.close_to_lader_reward
        if abs(state[dist_ladder_idx]) > abs(next_state[dist_ladder_idx]):
            reward += self.close_to_lader_reward

        if state[on_ladder_idx] and action == 4:
            reward += self.close_to_lader_reward
        elif state[on_ladder_idx]:
            reward -= self.close_to_lader_reward
             
        return reward   
        

    def play(self, game_bonus_sound=None, got_hit_sound=None):
        if self.state.reached_gate():
            # game_bonus_sound.play()
            # pygame.time.delay(self.delay)  
            self.state.lives_left -= 1
            # Barrel.speed_add =  self.state.score
            self.state.restart(new_game=False)
            # self.reward = self.gate_reward

        
        got_hit = self.state.got_hit()
        if got_hit:            
            # got_hit_sound.play()    
            pygame.time.delay(self.delay)  
            self.state.lives_left -= 1           
            self.state.restart(new_game=False)
            Barrel.speed_add = 0
            # self.reward = self.hit_reward

        self.state.add_new_barrel()

        return self.state.lives_left == 0

 
    
