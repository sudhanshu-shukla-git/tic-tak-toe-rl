from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        #print("self.state",self.state)
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        #  Index of the 3x3 board
        #   0 | 1 | 2
        #   ----------
        #   3 | 4 | 5
        #   ----------
        #   6| 7 | 8        
        #list of all the winning positions
        win_pos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for pos in win_pos:
            state = 0
            for index in pos:
                state = state + curr_state[index]  
                if state==15: #Agent/Environment wins when the sum is 15(any row, column or diagonal)
                    return True
        return False
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]
        
        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
        #print("action_space-curr_state",curr_state)
        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """        
        #assign the new value at the next position
        curr_state[curr_action[0]] = curr_action[1]        
        return curr_state


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        #new board state after agent's action
        new_state = self.state_transition(curr_state,curr_action)        
        #reward mapping for each state
        reward_list={'Win':10,'Tie':0,'Resume':-1 }
        #check if the state is terminal 
        terminal_state = self.is_terminal(new_state)
        #get the agent's reward
        agent_reward = reward_list[terminal_state[1]]
        #if its a terminal state return the state , reward
        if terminal_state[0]:
            return (new_state,agent_reward,terminal_state[0])    
        #Incoprating Envionments move             
        valid_Actions = [i for i in self.action_space(new_state)[1]]
        if len(valid_Actions)<1:
            #print("Env valid_Actions",len(valid_Actions),valid_Actions)    
            return (new_state,agent_reward,True)    
        #print("Env valid_Actions",len(valid_Actions))    
        env_action=random.choice(valid_Actions)        
        final_state = self.state_transition(new_state,env_action)
        #print('state after env turn',final_state)
        terminal_state= self.is_terminal(final_state)
        evn_reward = reward_list[terminal_state[1]]          
        if(evn_reward==10):
            agent_reward= -10
        else:
            agent_reward=evn_reward
        
        return (final_state,agent_reward,terminal_state[0])

    def reset(self):
        return self.state
