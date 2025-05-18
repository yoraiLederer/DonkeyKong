import pygame
import torch
from Constants import *
from Environment import Environment
from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from Graphics import Graphics
import os
import wandb

def main (chkpt):
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    graphics = Graphics(SCREEN_WIDTH, SCREEN_HEIGHT)
    env = Environment(delay=0)    

    

    #region ###### params ############
    player = DQN_Agent()
    player_hat = DQN_Agent()
    player_hat.DQN = player.DQN.copy()
    batch_size = 50
    buffer = ReplayBuffer(path=None)
    learning_rate = 0.001
    ephocs = 1000
    start_epoch = 0
    C = 2
    loss = torch.tensor(-1)
    avg = 0
    scores, losses, avg_score = [], [], []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    # scheduler = torch.optim.lr_scheduler.StepLR(optim,100000, gamma=0.50)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[5000*1000, 10000*1000, 15000*1000], gamma=0.5)
    step = 0
    MIN_BUFFER = 100
    MAX_STEPS = 1500
    #endregion

    #region   ############# wandb init ###########################
    wandb.init(
    # set the wandb project where this run will be logged
        project="Donkey-Kong",
        id=f'Donkey-Kong{chkpt}',
        name=f"Donkey-Kong{chkpt}",
        config={
        "learning_rate": learning_rate,
        "architecture": str(player.DQN),
        "batch_size":batch_size,
        "C": C
        }
    )
    #endregion

    for epoch in range(start_epoch, ephocs):
        env.state.restart()
        done = False
        state = env.state.get_tensor() 
        step = 0
        while not done: # and step < MAX_STEPS:
            print (step, end='\r')
            step += 1
            graphics.clear_screen()
            events = pygame.event.get()
            pygame.event.pump()
            for event in events:
                if event.type == pygame.QUIT:
                    done = True
                    return
            
            ############## Sample Environement #########################
            action = player.get_action(state=state,events=events, train=True)
            env.move(action=action)
            next_state = env.state.get_tensor()
            reward = env.get_reward(action, state, next_state)
            done = env.play()
            # print (f'reward: {reward} action: {action} done: {done}') 
            buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32), 
                        next_state, torch.tensor(done, dtype=torch.float32))
            
            state = next_state
            
            graphics.write_text(graphics.header_surf, "Lives: " + str(env.state.lives_left), (300, 10))
            graphics.write_text(graphics.header_surf, "Score: " + str(env.state.score) ,(700, 10))
            graphics.draw(env.state)
            pygame.display.update()
            # clock.tick(FPS)
            
            if len(buffer) < MIN_BUFFER:
                continue
           
            ############## Train ################
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = player.Q(states, actions)
            next_actions, Q_hat_Values = player_hat.get_Actions_Values(next_states)

            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            scheduler.step()

        if epoch % C == 0:
            player_hat.DQN.load_state_dict(player.DQN.state_dict())

        #region ####### print and log   #################################
        print (f'chkpt: {chkpt} epoch: {epoch} loss: {loss:.7f} LR: {scheduler.get_last_lr()} step: {step} ' \
               f'score: {env.state.score}')
        wandb.log({
            "loss": loss,
            "score": env.state.score,
            "steps/100": step/100,
            "steps": step
        })
        step = 0
        if epoch == 50:
            player.save_param(f"Data/params{chkpt}")
       

        # if epoch % 1000 == 0 and epoch > 0:
        #     pass
        #endregion
        


        

        
if __name__ == "__main__":
    if not os.path.exists("Data/checkpoit_num"):
        torch.save(1, "Data/checkpoit_num")    
    
    chkpt = torch.load("Data/checkpoit_num", weights_only=False)
    chkpt += 1
    torch.save(chkpt, "Data/checkpoit_num")    
    main (chkpt)
    pygame.quit()