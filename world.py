import numpy as np
import time

startState=(4,4,4,4,4,4,0,4,4,4,4,4,4,0,True)

def transition(state,action):
    #state: enter a 15-bit tuple state (e.g. (0,0,0,0,0,0,0,24,0,0,0,0,0,0,0,0,24,True)), indicating that the number of gems in each of the 12 non-scoring plates are 0, the two scoring plates have 24 balls each, and it is player1's turn to act 
    #action: a value from 0-5. player1's turn is 0-5 from bottom left to bottom right; player2's turn is 0-5 from top right to top left
    
    
    newstate=list(state)
    newstate[-1]=not newstate[-1]
    if state[-1]:
        point=action+1
        times=state[action]
        newstate[action]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point<6) and (newstate[12-point]>0):
                newstate[6]+=1+newstate[12-point]
                newstate[12-point]=0
                break
            newstate[point]+=1
            point+=1
            if point==14:
                point=0
    else:
        point=action+8
        times=state[action+7]
        newstate[action+7]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point>6) and (newstate[12-point]>0):
                newstate[13]+=1+newstate[12-point]
                newstate[12-point]=0
                break
            newstate[point]+=1
            point+=1
            if point==14:
                point=0
    return tuple(newstate)
    #newstate is the new state

def transitionIterating(state,action):
    print("iter")
    newstate=list(state)
    newstate[-1]=not newstate[-1]
    if state[-1]:
        point=action+1
        times=state[action]
        newstate[action]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point<6) and (newstate[12-point]>0):
                time.sleep(0.5)
                yield newstate,action,point,1
                newstate[6]+=1+newstate[12-point]
                buf=newstate[12-point]
                time.sleep(0.5)
                yield newstate,point,6,1
                print("iter2")
                newstate[12-point]=0
                yield newstate,12-point,6,buf
                print("iter3")
                break
            newstate[point]+=1
            time.sleep(0.5)
            yield newstate,action,point,1
            print("iter7")
            point+=1
            if point==14:
                point=0
    else:
        point=action+8
        times=state[action+7]
        newstate[action+7]=0
        for i in range(times):
            if (i==times-1) and (newstate[point]==0) and (point>6) and (newstate[12-point]>0):
                time.sleep(0.5)
                yield newstate,action+7,point,1
                print("iter4")
                newstate[13]+=1+newstate[12-point]
                buf=newstate[12-point]
                time.sleep(0.5)
                yield newstate,point,13,1
                print("iter5")
                newstate[12-point]=0
                yield newstate,12-point,13,buf
                print("iter6")
                break
            newstate[point]+=1
            time.sleep(0.5)
            yield newstate,action+7,point,1
            print("iter8")
            point+=1
            if point==14:
                point=0

def getLegalActions(state):  #Given state, return a list of legal actions (taking values from 0-5)
    actions=[]
    if state[-1]==True:
        for i in range(0,6):
            if state[i]>0:
                actions.append(i)
    else:
        for i in range(7,13):
            if state[i]>0:
                actions.append(i-7)
    return actions


def isTerminal(state):  #Given state, determine if it is a terminated state
    if (np.sum(state[:6])==0) or (np.sum(state[7:13])==0):
        return True
    return False

def getSum(state):   #Returns the sum of all gems on player1's side and the sum of all gems on player2's side, which is used to determine the winner
    return np.sum(state[:7]),np.sum(state[7:-1])
