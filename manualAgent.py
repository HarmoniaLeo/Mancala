from world import getLegalActions

class manualAgent:
    def __init__(self,ui):
        self.__ui=ui

    def play(self,state):
        while True:
            action=self.__ui.manualImport()
            if action in getLegalActions(state):
                return action