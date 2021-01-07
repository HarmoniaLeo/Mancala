import numpy as np
import time

startState=(4,4,4,4,4,4,0,4,4,4,4,4,4,0,True)

def transition(state,action):
    #state：输入15位元组状态（如(0,0,0,0,0,0,24,0,0,0,0,0,0,24,True)），表示此时12个小袋子中球数均为0，两边大袋子中各有24个球，而当前轮到player1行动
    #action：0-5的数值。player1的回合选取袋子操作时，从左下到右下0-5；player2的回合选取袋子操作时，从右上到左上0-5
    
    
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
    #newstate是新的状态

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

def getLegalActions(state):  #给出state，返回合法行动列表（取值在0-5）
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


def isTerminal(state):  #给出state，判断是否是终止状态
    if (np.sum(state[:6])==0) or (np.sum(state[7:13])==0):
        return True
    return False

def getSum(state):   #返回player1方所有球数总和、player2方所有球数总和，判断输赢的时候会用到
    return np.sum(state[:7]),np.sum(state[7:-1])
