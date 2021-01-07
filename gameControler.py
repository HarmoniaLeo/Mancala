import numpy as np
from world import *
import time

class game:
    def __init__(self,agent1,agent2):
        self.agents=[agent1,agent2]
        self.state=startState
        self.pointer=0

    def getState(self):
        return self.state
    
    def judge(self):
        p1,p2=getSum(self.state)
        if p1>p2:
            return "P1 wins!"
        if p1==p2:
            return "    Draw!"
        if p1<p2:
            return "P2 wins!"

    def play(self):
        action=self.agents[self.pointer].play(self.state) #关键是这句，用state调用agent对象的play函数，然后返回action
        self.state=transition(self.state,action)
        if self.state[-1]:
            action+=7
        self.pointer+=1
        if self.pointer==2:
            self.pointer=0
        if isTerminal(self.state):
            return self.judge(),action
        else:
            return "",action
        

class gameWithGUI(game):
    def __init__(self,agent1,agent2,UI):
        self.UI=UI
        super().__init__(agent1,agent2)

    def move(self,action):
        print("move")
        f=transitionIterating(self.state,action)
        try:
            while True:
                self.state,start,end,num=next(f)
                self.UI.paintMove(start,end,num)
        except StopIteration:
            time.sleep(1)
            self.pointer+=1
            if self.pointer==2:
                self.pointer=0
            if isTerminal(self.state):
                return self.judge()
            else:
                return ""    

    def play(self):
        print("play")
        judge=""
        while True:
            if not(self.agents[self.pointer] is None):
                action=self.agents[self.pointer].play(self.state) #关键是这句，用state调用agent对象的play函数，然后返回action
                judge=self.move(action)
                if judge!="":
                    self.UI.uiTerminal(self.judge())
                    break
            else:
                self.UI.enableManualAction(self.state[-1])
                break
    
    def manPlay(self,action):
        if action in getLegalActions(self.state):
            self.UI.disableManualAction(self.state[-1])
            judge=self.move(action)
            if judge!="":
                self.UI.uiTerminal(self.judge())
            else:
                self.play()