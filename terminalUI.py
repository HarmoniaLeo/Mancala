from gameControler import game
from manualAgent import manualAgent
from randomAgent import randomAgent
from minimaxAgent import minimaxAgent,minimaxAgentML
from RL_play import reinforceAgent
from utilityTrain import CNNnet

class terminalUi:
    def manualImport(self):
        print("请输入0-5:")
        return int(input())

    def playGame(self,aGame):
        round=0
        action=-1
        end=""
        while True:
            state=aGame.getState()
            print("round {0}:move {1}\n".format(round,action))
            print("     [{12}] [{11}] [{10}] [{9}] [{8}] [{7}]     \n[{13}]                          [{6}]\n     [{0}] [{1}] [{2}] [{3}] [{4}] [{5}]     \n".format(state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],state[9],state[10],state[11],state[12],state[13]))
            round+=1
            end,action=aGame.play()
            if end!="":
                break
        state=aGame.getState()
        print("round {0}:\n".format(round))
        print("     [{12}] [{11}] [{10}] [{9}] [{8}] [{7}]     \n[{13}]                          [{6}]\n     [{0}] [{1}] [{2}] [{3}] [{4}] [{5}]     \n".format(state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],state[9],state[10],state[11],state[12],state[13]))    
        print("游戏结束:"+end)
    
    def playGame100Rounds(self,agent1,agent2):
            agent1Win=0
            for i in range(100):
                aGame=game(agent1,agent2)
                action=-1
                end=""
                while True:
                    state=aGame.getState()
                    end,action=aGame.play()
                    if end!="":
                        break
                if end=="P1 wins!":
                    agent1Win+=1
                print(i,end)
            print(float(agent1Win)/100)

    def run(self):
        agent1=randomAgent()
        agent2=randomAgent()
        while True:
            print("1.选用player1开始游戏\n2.选用player2开始游戏\n3.AI对弈\n4.设置player1的AI类型\n5.设置player2的AI类型\n6.100rounds")
            i=int(input())
            if i==4:
                print("1.随机\n2.minimax\n3.RL\n4.ML\n")
                i=int(input())
                if i==1:
                    agent1=randomAgent()
                elif i==2:
                    agent1=minimaxAgent()
                elif i==3:
                    agent1=reinforceAgent()
                elif i==4:
                    agent2=minimaxAgentML()
            elif i==5:
                print("1.随机\n2.minimax\n3.RL\n4.ML\n")
                i=int(input())
                if i==1:
                    agent2=randomAgent()
                elif i==2:
                    agent2=minimaxAgent()
                elif i==3:
                    agent2=reinforceAgent()
                elif i==4:
                    agent2=minimaxAgentML()
            elif i==1:
                aGame=game(manualAgent(self),agent2)
                self.playGame(aGame)
            elif i==2:
                aGame=game(agent1,manualAgent(self))
                self.playGame(aGame)
            elif i==3:
                aGame=game(agent1,agent2)
                self.playGame(aGame)
            elif i==6:
                self.playGame100Rounds(agent1,agent2)


terminalUi().run()