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
        self.gate_reward = 100
        self.hit_reward = -10
        self.max_floor = 0

    def move(self, action):
        self.state.move(action) 
    
    def get_reward(self, action):
        state = self.state 
        reward = self.reward

        if self.state.reached_gate():
            return self.gate_reward
        if self.state.got_hit():
            return self.hit_reward
        if self.state.mario.rect.centery <= FLOOR5_Y:
            floor = 5
        elif self.state.mario.rect.centery <= FLOOR4_Y:
            floor = 4
        elif self.state.mario.rect.centery <= FLOOR3_Y:
            floor = 3
        elif self.state.mario.rect.centery <= FLOOR2_Y:
            floor = 2
        elif self.state.mario.rect.centery <= FLOOR1_Y:
            floor = 1        
        elif self.state.mario.rect.centery <= FLOOR0_Y:
            floor = 0

        if self.max_floor < floor:
            self.state.score += 1   
            self.max_floor += 1


        if floor == 0:
            if LADDER0_X+10<self.state.mario.rect.centerx:
                if action == 2:
                    reward += 2
                elif action == 3:
                    reward -= 1
            elif LADDER0_X-10>self.state.mario.rect.centerx:     
                if action == 2:
                    reward -= 1
                elif action == 3:
                    reward += 2
            else :
                if action == 4:
                    reward += 2
                if action == 5:
                    reward -= 1
        elif floor == 1:
            if LADDER1_X+10<self.state.mario.rect.centerx:
                if action == 2:
                    reward += 2
                elif action == 3:
                    reward -= 1
            elif LADDER1_X-10>self.state.mario.rect.centerx:     
                if action == 2:
                    reward -= 1
                elif action == 3:
                    reward += 2
            else :
                if action == 4:
                    reward += 2
                if action == 5:
                    reward -= 1

        elif floor == 2:
            if LADDER2_X+10<self.state.mario.rect.centerx:
                if action == 2:
                    reward += 2
                elif action == 3:
                    reward -= 1
            elif LADDER2_X-10>self.state.mario.rect.centerx:     
                if action == 2:
                    reward -= 1
                elif action == 3:
                    reward += 2
            else :
                if action == 4:
                    reward += 2
                if action == 5:
                    reward -= 1

        elif floor == 3:
            if LADDER3_X+10<self.state.mario.rect.centerx:
                if action == 2:
                    reward += 2
                elif action == 3:
                    reward -= 1
            elif LADDER3_X-10>self.state.mario.rect.centerx:     
                if action == 2:
                    reward -= 1
                elif action == 3:
                    reward += 2
            else :
                if action == 4:
                    reward += 2
                if action == 5:
                    reward -= 1

        elif floor == 4:
            if LADDER4_X+10<self.state.mario.rect.centerx:
                if action == 2:
                    reward += 2
                elif action == 3:
                    reward -= 1
            elif LADDER4_X-10>self.state.mario.rect.centerx:     
                if action == 2:
                    reward -= 1
                elif action == 3:
                    reward += 2
            else :
                if action == 4:
                    reward += 2
                if action == 5:
                    reward -= 1  

        elif floor == 5:
            if state.gate.rect.centerx+40<self.state.mario.rect.centerx:
                if action == 2:
                    reward += 4
                elif action == 3:
                    reward -= 2
            elif state.gate.rect.centerx-40>self.state.mario.rect.centerx:     
                if action == 2:
                    reward -= 2
                elif action == 3:
                    reward += 4                 

        return reward

    def play(self, game_bonus_sound=None, got_hit_sound=None):
        if self.state.reached_gate():
            # game_bonus_sound.play()
            pygame.time.delay(self.delay)  
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

 
    
