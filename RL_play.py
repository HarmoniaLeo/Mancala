'''
Descripttion : 
Author       : Fu Yuqian
Date         : 2020-12-10 01:03:56
LastEditors  : Fu Yuqian
LastEditTime : 2020-12-18 21:37:05
'''
from agent import ReinforceAgent
import os
from world import getLegalActions

class reinforceAgent:
    def __init__(self) -> None:
        base_cwd = os.getcwd()
        model_dir = base_cwd + "\\model"
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        model_path = model_dir + "\\mancala_agent.pkl"
        self.loaded_agent = ReinforceAgent(load_agent_path = model_path)
    def play(self,state):
        # base_cwd = os.getcwd()
        # model_dir = base_cwd + "\\model"
        # if not os.path.exists(model_dir):
        #     os.mkdir(model_dir)
        # model_path = model_dir + "\\mancala_agent.pkl"
        # loaded_agent = ReinforceAgent(load_agent_path = model_path)
        state=list(state)
        while True:
            action=self.loaded_agent.take_actionplus(state)
            
            return action
            

        
