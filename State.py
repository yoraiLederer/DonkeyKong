import numpy as np
from Constants import *
from DonkeyKong import DonkeyKong
from Mario import Mario
from FloorTile import FloorTile
from Ladder import Ladder
from Barrel import Barrel
from  Gate import Gate
import random
import torch

class State:
    def __init__(self):
        self.make_board_groups()
        self.score = 0     
        self.lives_left = MARIO_LIVES
        self.random_interval = 0
        self.start_time = pygame.time.get_ticks()
        self.touched_gate = False
        self.step_to_barrel=7
        self.Board_infra = torch.tensor([160,100,260,120,280,100,620,120,0,260,940,280,960,260,1020,280,80,380,180,400,200,380,1220,400,0,500,920,520,940,500,1020,520,80,640,200,660,220,640,1220,660,0,780,1220,800,
                                     260,80,280,260,940,240,960,380,180,360,200,500,920,480,940,640,200,620,220,780], dtype=torch.float32)

        self.platforms_bottoms = {      # y-coord
            6: 0,
            5: 100,
            4: 260,
            3: 380,
            2: 500,
            1: 640, 
            0: 800
            }
        
        self.platforms_ends = {
            5: (160, 620),
            4: (0, 1020),
            3: (80, 1220),
            2: (0, 1020),
            1: (80, 1220), 
            0: (0, 1220)
        }

        self.platforms_ladders = {      # x-coord
            5: -1,
            4: 270,
            3: 950,
            2: 190,
            1: 930,
            0: 210, 
            }
        
        

    def make_board_groups (self):
        
        self.floor_Group = pygame.sprite.Group()
        self.ladder_Group = pygame.sprite.Group()
        self.barrel_Group = pygame.sprite.Group()  
        
        self.gate = Gate(self.floor_Group)
        self.gate_Group = pygame.sprite.GroupSingle(self.gate)

        self.donkey_kong = DonkeyKong((MAIN_CENTER //2, MAIN_HEIGHT-TILE_SIZE), self.floor_Group)
        self.donkey_kong_Group = pygame.sprite.GroupSingle(self.donkey_kong)
        
        self.mario = Mario((SCREEN_WIDTH-100, MAIN_HEIGHT-TILE_SIZE), self.floor_Group, self.ladder_Group)
        self.mario_Group = pygame.sprite.GroupSingle(self.mario)      
        
        self.barrel_img = pygame.image.load(BARREL_URL)
        self.barrel_img = pygame.transform.scale(self.barrel_img, (BARREL_SIZE, BARREL_SIZE))
        self.floor_img = pygame.image.load(FLOOR_URL)
        self.floor_img = pygame.transform.scale(self.floor_img, (TILE_SIZE, TILE_SIZE))
        self.ladder_img = pygame.image.load(LADDER_URL)
        self.ladder_img = pygame.transform.scale(self.ladder_img, (LADDER_SIZE, LADDER_SIZE))
        self.barrels_timer = pygame.time.get_ticks()  
        
        num_rows, num_cols = BOARD_ARR.shape
        # Iterate over the items
        for row in range(num_rows):
            for col in range(num_cols):
                value = BOARD_ARR[row, col]
                if value == FLOOR_TILE:
                    self.floor_Group.add(FloorTile(self.floor_img, (col * TILE_SIZE, row * TILE_SIZE)))
                if value == LADDER:
                    self.ladder_Group.add(Ladder(self.ladder_img, (col * TILE_SIZE, row * TILE_SIZE)))   

    def To_tensor(self):                # 160 + 4 + 4 = 168
        # Barrels                                                          # 40 * 4 = 160
        state_list = []
        barrel = 0                                           
        for sprite in self.barrel_Group:
            state_list.append(sprite.rect.centerx / MAIN_WIDTH)
            state_list.append(sprite.rect.centery / MAIN_HEIGHT)
            state_list.append(sprite.speed_dir)    #v_x
            state_list.append(sprite.velocity_y)    #v_y
            barrel += 1
        for i in range(MAX_BARREL - barrel):
            state_list.append(0)
            state_list.append(0)
            state_list.append(0)
            state_list.append(0)

        # donkey kong        
        state_list.append(self.donkey_kong.rect.centerx/ MAIN_WIDTH)                # 4
        state_list.append(self.donkey_kong.rect.centery / MAIN_HEIGHT)
        state_list.append(self.donkey_kong.speed_dir)
        state_list.append(self.donkey_kong.speed_y)
        # mario
        state_list.append(self.mario.rect.centerx / MAIN_WIDTH)
        state_list.append(self.mario.rect.centery / MAIN_HEIGHT)
        state_list.append(self.mario.velocity_x)                        # 4
        state_list.append(self.mario.velocity_y)
        # mario v_x
        # mario v_y
                                  
        tensor1 = torch.tensor(state_list, dtype=torch.float32)
        tensor = torch.cat((tensor1,self.Board_infra))
        return tensor

    def get_platform_num (self, y):
        for platform, y_max in self.platforms_bottoms.items():
            if y < y_max:
                return platform
        return 0  # y >= 800 → platform 0

    def get_platform_offset(self, platform_num, y):
        bottom = self.platforms_bottoms[platform_num]
        top =  self.platforms_bottoms[platform_num + 1]
        return (y-bottom) / (top-bottom)

    def get_tensor (self):
        '''
        mario platform
        mario platform offset
        mario on ladder
        mario jumping - in the air
        mario dist to up ladder in last pltform dist to target - no dist to down ladder
        mario dist to left end of platform
        mario dist to right end of platform
        donkey dist to mario
        donkey platformm
        barrel dist to mario - if not the same platform dist very big
        barrel platform
        barrel offset
        # input - 12 
        '''
        state_list = []

        #mario platform
        mario_bottom = self.mario.rect.bottom
        mario_platform = self.get_platform_num(mario_bottom)
        mario_x = self.mario.rect.centerx
        state_list.append(mario_platform)                                             # platform_num 0 - 5
        state_list.append(self.get_platform_offset(mario_platform, mario_bottom))           # platform_offset [0,1]
        state_list.append(int(self.mario.is_on_ladder))                         # on lader (0,1)
        state_list.append(int(self.mario.is_jumping))                           # jumping (0,1)
        state_list.append((self.platforms_ladders[mario_platform] - mario_x)/MAIN_WIDTH  )  # distance to ladder [-1, 1]
        state_list.append((self.platforms_ends[mario_platform][0] - mario_x)/MAIN_WIDTH  )  # distance to left platform [-1, 0]
        state_list.append((self.platforms_ends[mario_platform][1] - mario_x)/MAIN_WIDTH  )  # distance to right platform [0, 1]

        #Donkey_kong
        donkey_x = self.donkey_kong.rect.centerx
        donkey_platform = 0
        state_list.append((donkey_x - mario_x)/ MAIN_WIDTH)     # dist to mario
        state_list.append(donkey_platform)                      # donkey_platform

        #barrel
        first_barrel = next(iter(self.barrel_Group), None)
        if first_barrel:
            barrel_x = first_barrel.rect.centerx
            barrel_y = first_barrel.rect.centery
            barrel_platform = self.get_platform_num(barrel_x)
            if barrel_platform == mario_platform:
                state_list.append((barrel_x - mario_x)/ MAIN_WIDTH)     # dist to barrel
            else:
                state_list.append(2)                                    # dist to barrel - not in my platform
            state_list.append(barrel_platform)                          # platform
            state_list.append(self.get_platform_offset(barrel_platform, barrel_y)) # platform - offset
        else:
            state_list.append(0)        # no barrel
            state_list.append(0)        # no barrel
            state_list.append(0)        # no barrel
        
        state_tensor = torch.tensor(state_list, dtype=torch.float32)
        return state_tensor


    def move(self, action):
        
        if action == 1:
            self.mario.jump()
        elif action == 2:
            self.mario.move_left()
        elif action == 3:
            self.mario.move_right()
        elif action == 4:
            self.mario.go_up()
        elif action == 5:
            self.mario.go_down()
        elif action == 0:
            self.mario.stop_moving()
        
        self.update_groups()    
        self.step_to_barrel -= 1

    def update_groups(self):
        self.barrel_Group.update()
        self.floor_Group.update()
        self.ladder_Group.update()
        self.mario_Group.update()
        self.donkey_kong_Group.update()
        self.gate_Group.update()
    
    def restart(self, new_game=True):
        if new_game:
            self.score = 0  
            self.lives_left = MARIO_LIVES

        self.gate.rect.x = 500
        self.gate.rect.y = 0
        self.donkey_kong.rect.midbottom = (MAIN_CENTER //2, MAIN_HEIGHT-TILE_SIZE)
        self.mario.rect.midbottom = (SCREEN_WIDTH-100, MAIN_HEIGHT-TILE_SIZE)        
        self.barrel_Group.empty()
        self.step_to_barrel = 7

    def add_new_barrel(self):        
        # Add a new barrel at regular intervals
        barrels_on_screen = len(self.barrel_Group)
        if self.step_to_barrel < 0:
            self.step_to_barrel = 7
        if barrels_on_screen < MAX_BARREL and self.step_to_barrel == 0:
            self.barrel_Group.add(Barrel(self.barrel_img, (0,200), self.floor_Group))
            self.step_to_barrel = random.randint(20, 150)

        
        # barrels_on_screen = 0        
        # current_time = pygame.time.get_ticks()
        # elapsed_time = current_time - self.start_time
        # if MAX_BARREL != barrels_on_screen:
        #     if elapsed_time >= self.random_interval:
        #         self.barrel_Group.add(Barrel(self.barrel_img, (0,200), self.floor_Group))
        #         barrels_on_screen+1
        #         self.barrels_timer = current_time
        #         # Reset the timer for the next random interval
        #         self.start_time = current_time
        #         self.random_interval = random.randint(600, 3500)  

    
    def got_hit(self):        
        donkey_kong_touched = pygame.sprite.groupcollide(self.mario_Group, self.donkey_kong_Group ,False, False, collided= pygame.sprite.collide_mask) 
        barrel_touched = pygame.sprite.groupcollide(self.mario_Group, self.barrel_Group, False, False, collided= pygame.sprite.collide_mask) 
        return len(donkey_kong_touched) > 0 or len(barrel_touched) > 0
        
    def reached_gate(self):        
        gate_touched = pygame.sprite.groupcollide(self.mario_Group, self.gate_Group ,False, False, collided= pygame.sprite.collide_mask) 
        return len(gate_touched) > 0