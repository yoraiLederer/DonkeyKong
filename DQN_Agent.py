import torch
import random
import math
from DQN import DQN
from Constants import *


class DQN_Agent:
    def __init__(self, parametes_path = None, train = True, env= None, devive = torch.device('cpu')):
        self.DQN = DQN(device=devive)
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.train = train
        self.setTrainMode()

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_action (self, state, epoch = 0, events= None, train = True) -> tuple:
        actions = [0,1,2,3,4,5]
        if self.train and train:
            epsilon = self.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                return random.choice(actions)
        
        with torch.no_grad():
            Q_values = self.DQN(state)
        max_index = torch.argmax(Q_values)
        return actions[max_index]

    def get_Actions_Values (self, states):
        with torch.no_grad():
            Q_values = self.DQN(states)
            max_values, max_indices = torch.max(Q_values,dim=1) # best_values, best_actions
        
        return max_indices.reshape(-1,1), max_values.reshape(-1,1)

    def Q (self, states, actions):
        Q_values = self.DQN(states) 
        rows = torch.arange(Q_values.shape[0]).reshape(-1,1)
        cols = actions.reshape(-1,1)
        return Q_values[rows, cols]

    def epsilon_greedy(self,epoch, start = 0.3, final=0.01, decay=10):
        # res = final + (start - final) * math.exp(-1 * epoch/decay)
        if epoch < decay:
            return start - (start - final) * epoch/decay
        return final
    

    def another_game(self):
       return True
  
    def loadModel (self, file):
        self.model = torch.load(file)
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def fix_update (self, dqn, tau=0.001):
        self.DQN.load_state_dict(dqn.state_dict())

    def soft_update (self, dqn, tau=0.001):
        with torch.no_grad():
            for dqn_hat_param, dqn_param in zip(self.DQN.parameters(), dqn.parameters()):
                dqn_hat_param.data.copy_(tau * dqn_param.data + (1.0 - tau) * dqn_hat_param.data)


    def __call__(self, events= None, state=None):
        return self.get_Action(state)