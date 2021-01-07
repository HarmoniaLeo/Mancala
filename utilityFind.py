from world import *
import random
import os
import json
import pandas as pd

iterate=10000000
iterated=0
utilityDictionary={}

def findUtility(state):
    global iterated
    if isTerminal(state):
        num1,num2=getSum(state)
        if num1>num2:
            utility=10000
        elif num1<num2:
            utility=-10000
        else:
            utility=0
        if state not in utilityDictionary.keys():
            utilityDictionary[state[:-1]]=[utility,1]
        return utility
    while True:
        action=random.randrange(0,6,1)
        if action in getLegalActions(state):
            utility=0.95*findUtility(transition(state,action))
            break
    if state not in utilityDictionary.keys():
        utilityDictionary[state[:-1]]=[utility,1]
        iterated+=1
    else:
        utilityDictionary[state[:-1]][1]+=1
        utilityDictionary[state[:-1]][0]=(utilityDictionary[state][0]+utility)/utilityDictionary[state][1]
    return utility

if __name__ == "__main__":
    state=startState
    while iterated<iterate:
        findUtility(state)
        print(iterated)
    string=""
    for key in utilityDictionary.keys():
        for i in range(0,14):
            string+=str(key[i])
            string+="\t"
        string+=str(utilityDictionary[key][0])
        string+="\n"
    f=open("dataset.txt","wb")
    f.write(string.encode("utf-8"))