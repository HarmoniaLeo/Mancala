import random
from world import getLegalActions

class randomAgent:
    def play(self,state):
        while True:
            action=random.randrange(0,6,1)
            if action in getLegalActions(state):
                return action