from world import *
from gameControler import *
from math import fabs

import numpy as np
import torch 
from torch.utils import data
from torch.autograd import Variable
from utilityTrain import CNNnet

class minimaxAgent:
    HUMAN=0
    MINIMAX=1
    ABPRUNE=2
    MEANVALUE=3
    def __init__(self,playerType=MEANVALUE,ply=2):#Player no., player category,minimax depth
        self.num=True
        self.opp=2
        self.type=playerType
        self.ply=ply
        self.opp=False
    def minimaxMove(self,state,ply):
        score=-999
        turn=self
        #state=game.getState()
        best_move=0
        for move in getLegalActions(state):
            if ply==0:
                return move
            next_state=transition(state,move)
           # opp=minimaxAgent(self.opp,self.type,self.ply)
            opp=minimaxAgent()
            s=opp.minValue(next_state,ply-1,turn)
            if s>score:
                score=s
                best_move=move
        return best_move

    def maxValue(self,state,ply,turn):
        if isTerminal(state):
            p1_sum,p2_sum=getSum(state)
            if p1_sum>p2_sum:
                return 999
            else:
                return -999
        if ply==0:
            return turn.score(state)
        score_min=-999
        for move in getLegalActions(state):
          #  opponent=minimaxAgent(self.opp,self.type,self.ply)
            opp = minimaxAgent()
            next_state=transition(state,move)
            s=self.minValue(next_state,ply-1,turn)
            if s>score_min:
                score_min=s
        return score_min

    def minValue(self,state,ply,turn):
        if isTerminal(state):
            p1_sum,p2_sum=getSum(state)
            if p1_sum<p2_sum:
                return 999
            else:
                return -999
        if ply==0:
            return turn.score(state)
        score_max=999
        for move in getLegalActions(state):
            #opponent=minimaxAgent(self.opp,self.type,self.ply)
            opp = minimaxAgent()
            next_state=transition(state,move)
            s=self.maxValue(next_state,ply-1,turn)
            if s<score_max:
                score_max=s
        return score_max

    def randomMove(self,state,ply):
        score = -999
        self.num=state[-1]
        turn = self
        # state=game.getState()
        best_move = 0
      #  w=[1.0/6]*6
        w=[0.05,0.05,0.1,0.15,0.15,0.5]
        for move in getLegalActions(state):
            if ply == 0:
                return move
            next_state = transition(state, move)
            # opp=minimaxAgent(self.opp,self.type,self.ply)
            opp = minimaxAgent()
            s = opp.randomLevel(next_state, ply - 1, turn,w)
            if s > score:
                score = s
                best_move = move
        return best_move

    def randomLevel(self,state,ply,turn,w):
        if isTerminal(state):
            p1_sum,p2_sum=getSum(state)
            if p1_sum>p2_sum:
                return 20
            else:
                return -20
        if ply==0:
            return turn.score(state)
        score=[]
        for move in getLegalActions(state):
          #  opponent=minimaxAgent(self.opp,self.type,self.ply)
            opp = minimaxAgent()
            next_state=transition(state,move)
            s=self.randomLevel(next_state,ply-1,turn,w)
            score.append(s)
        score=np.array(score)
        if state[-1]==self.num:
            rank=np.argsort(score)
            return (score[rank][-1])
        else:
            rank=np.argsort(-score)
            return (score[rank]*np.array(w[6-len(score):])).sum()*6/len(score)

    def alphabetamove(self,state,ply):
        best_move=-1
        alpha=-999
        beta=999
        score=-999
        turn=self
        #state=game.getState()
        for move in getLegalActions(state):
            if isTerminal(state):
                return -1
            next_state=transition(state,move)
            opp=minimaxAgent()
            s=opp.minABValue(next_state,ply-1,turn,alpha,beta)
            if s>score:
                best_move=move
                score=s
            alpha=max(score,alpha)
        return move

    def minABValue(self,state,ply,turn,alpha,beta):
        if isTerminal(state):
            p1_sum, p2_sum = getSum(state)
            if p1_sum < p2_sum:
                return 999
            else:
                return -999
        if ply==0:
            return turn.score(state)
        score=999
        for move in getLegalActions(state):
            opponent=minimaxAgent()
            next_state=transition(state,move)
            s=opponent.maxABValue(next_state,ply-1,turn,alpha,beta)
            if s<score:
                score=s
            if score<=alpha:
                return score
            beta=min(beta,score)
        return  score

    def maxABValue(self, state, ply, turn, alpha, beta):
        if isTerminal(state):
            p1_sum, p2_sum = getSum(state)
            if p1_sum > p2_sum:
                return 999
            else:
                return -999
        if ply == 0:
            return turn.score(state)
        score = -999
        for move in getLegalActions(state):
            opponent = minimaxAgent()
            next_state = transition(state, move)
            s = opponent.minABValue(next_state, ply - 1, turn, alpha, beta)
            if s > score:
                score = s
            if score >= beta:
                return score
            alpha = max(alpha, score)
        return score

    def score(self,state):
        p1_sum, p2_sum = getSum(state)
        p1_bag=state[6]
        p2_bag=state[13]
        grid_empty = sum(np.array(state[:-1]) == 0)
        polar=0
        if p1_sum<p2_sum:
            polar=-1
        else:
            polar=1

        # if state[-1] == True:
        #     return (p1_bag - p2_bag)
        # else:
        #     return -(p1_bag - p2_bag)

        if p1_bag+p2_bag<30:
            if state[-1]==True:
                return (p1_bag-p2_bag)
            else:
                return -(p1_bag - p2_bag)
        else:
            if p1_sum-p2_sum==0:
                return 0
            if state[-1]==True:
                return (p1_sum-p2_sum)*(1+polar*grid_empty*1.0/fabs(p1_sum-p2_sum))
            else:
                return -(p1_sum-p2_sum)*(1+polar*grid_empty*1.0/fabs(p1_sum-p2_sum))
       #return (p1_sum-p2_sum)*(1+grid_empty*1.0/fabs(p1_sum-p2_sum))

    def play(self,state):
        if self.type==self.MINIMAX:
            return self.minimaxMove(state,self.ply)
        elif self.type==self.ABPRUNE:
            return self.alphabetamove(state,self.ply)
        elif self.type==self.MEANVALUE:
            return self.randomMove(state,self.ply)

class minimaxAgentML(minimaxAgent):
    HUMAN=0
    MINIMAX=1
    ABPRUNE=2
    MEANVALUE=3
    def __init__(self,playerType=MEANVALUE,ply=2):
        super().__init__(playerType,ply)
        self.model = torch.load('model')

    def normalization(self,state):
        state=np.array([state])
        means=np.array([[1.6831783766488317,1.920861792019031,2.0142274382885192,2.099035853596613,2.223753461124363,\
            2.3957063177909617,11.785342967427546,1.6735022578976735,1.916759244860047,2.0219108486903,2.095517344002846,2.2175399572616663,2.4000639932270524,11.760987284327173]])
        stds=np.array([[2.2965555781311355,2.5959722979902446,2.6847805719174693,2.745832204831912,2.8541587526372196,\
            2.979194156904659,6.298355040135411,2.3016301665931884,2.5987004084829355,2.6955533493313037,2.738373835337156,2.8395994049082107,2.9842425056695507,6.301167592999449]])
        state=(state-means)/stds
        n=np.ones((128,1,1))
        state=state*n
        return state.tolist()


    def score(self,state):
        state1=list(state[:-1])
        state1=self.normalization(state1)
        out = self.model(torch.tensor(state1))
        if state[-1]:
            return out[0][0].item()
        else:
            return -out[0][0].item()