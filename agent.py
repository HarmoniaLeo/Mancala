'''
Descripttion : 
Author       : Fu Yuqian
Date         : 2020-12-10 14:15:40
LastEditors  : Fu Yuqian
LastEditTime : 2020-12-19 18:21:17
'''
# -*- coding: utf-8 -*-

import random
import pickle
from world import * 

class ReinforceAgent:
    
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.4, max_actions=6, load_agent_path=None):
        try:
            with open(load_agent_path, 'rb') as infile:
                self.statemap = pickle.load(infile)
        except FileNotFoundError:
            print("No pretrained agent exists. Creating new agent")
            self.statemap = {}
        
        # Parameters not saved in pkl file
        self.max_actions = max_actions
        self.previous_state = 0
        self.previous_action = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
            
    def update_q(self, current_state, reward=0):
        
        # Assume no reward unless explicitly specified

        # Convert state to a unique identifier
        hashed_current_state = hash(''.join(map(str, current_state)))
        hashed_previous_state = hash(''.join(map(str, self.previous_state)))
        
        current_q_set = self.statemap.get(hashed_current_state)
        previous_q_set = self.statemap.get(hashed_previous_state)
        
        # Add new dictionary key/value pairs for new states seen
        if current_q_set is None:
            self.statemap[hashed_current_state] =  [0]*self.max_actions
            current_q_set = [0]*self.max_actions
        if previous_q_set is None:
            self.statemap[hashed_previous_state] =  [0]*self.max_actions
            
        # Q update formula
        q_s_a = self.statemap[hashed_previous_state][self.previous_action]
        q_s_a = q_s_a + self.alpha*(reward+self.gamma*max(current_q_set)-q_s_a)

        # Update Q
        self.statemap[hashed_previous_state][self.previous_action] = q_s_a

        # Track previous state for r=delayed reward assignment problem
        self.previous_state = current_state

        return True
    
    def take_action(self, current_state):
        
        # Random action 1-epsilon percent of the time
        if random.random()>self.epsilon:
            action = random.randint(0,5)
        else:
            # Greedy action taking
            hashed_current_state = hash(''.join(map(str, current_state)))
            current_q_set = self.statemap.get(hashed_current_state)
            if current_q_set is None:
                self.statemap[hashed_current_state] =  [0]*self.max_actions
                current_q_set = [0]*self.max_actions
            action = current_q_set.index(max(current_q_set)) # Argmax of Q
            
        self.previous_action = action
        
        # Convert computer randomness to appropriate action for mancala usage
        converted_action = action+1
        
        return converted_action
    
    def save_agent(self, save_path):
        with open(save_path, 'wb') as outfile:
            pickle.dump(self.statemap, outfile)

    def take_actionplus(self,state):
        player_turn=state[-1]
        self.state=state[0:-1]
        valid_move = False
        # while not(valid_move):
        computer_action = self.take_action(self.state)
            # move = self.convert_move(computer_action, player_turn)
            # if computer_action not in getLegalActions(state):
            #     valid_move = True
        return computer_action-1
    
    def get_state(self,player_turn):

        # Flip the board interpretation if player 2
        if player_turn == True:
            relevant_pockets = self.state[:6] + self.state[7:13]
        else:
            relevant_pockets = self.state[7:13] + self.state[:6]
        
        return relevant_pockets

    # def convert_move(self, move, player):
    #     if player == True:
    #         return move-1 # Shift left once to get the pocket position
    #     if player == False:
    #         return move+6 # Shift right 6 spaces to refer to upper board spot
    #     return False # Error case handling