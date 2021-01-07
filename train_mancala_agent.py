'''
Descripttion : 
Author       : Fu Yuqian
Date         : 2020-12-10 14:15:40
LastEditors  : Fu Yuqian
LastEditTime : 2020-12-19 16:00:47
'''
# -*- coding: utf-8 -*-

import os
import logging
from mancala import Mancala_RL
from agent import ReinforceAgent

def train_agent(n_games=1, games_per_checkpoint=1, model_save_path='model/mancala_agent.pkl'):
    
    # If model already exists, expand on it, otherwise start fresh
    loaded_agent = ReinforceAgent(load_agent_path = model_save_path)
    environment = Mancala_RL(loaded_agent)

    while n_games>0:
        environment.play_game(reinforcement_learning=True)
        # Checkpoint
        if n_games%games_per_checkpoint == 0:
            environment.mancala_agent.save_agent(model_save_path)
            logging.info('Saved RL Agent Model!')
            print('Remaining Games: ', n_games)
        n_games -= 1
        
    # Save final agent model
    environment.mancala_agent.save_agent(model_save_path)
        
    return environment


if __name__ == "__main__":
    environment = train_agent(n_games = 500000, games_per_checkpoint=10000)
    
    