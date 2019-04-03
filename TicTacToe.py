# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:05:19 2018

@author: CIMlab
"""

import numpy as np

class Env:
    def __init__(self):
        self.Reset()
        self.Tie = 0
        self.Owin = 0
        self.Xwin = 0
    
    def Reset(self):
        self.status = np.zeros((3, 3), dtype = int)
        self.RemainingSpace = 9
        #print("Game Start!")
    
    def Step(self, x, y, In):
        if self.status[x, y] != 0:
            #print("Invalid!!!", self.RemainingSpace)
            return False
        else:
            self.status[x, y] = In
            self.RemainingSpace -= 1
            self.Show()
            return True
            
    def Ref(self, Prt = False):
        
        winner = 0
        #Column Winning
        for i in range(3):
            init = self.status[i, 0]
            if init == 0:
                continue
            for j in range(1, 3):
                if self.status[i, j] != init:
                    winner = 0
                    break
                else:
                    winner = init
            if winner != 0:
                if winner == 1 and Prt:
                    print("O win!")
                    self.Owin += 1
                elif Prt:
                    print("X win!")
                    self.Xwin += 1
                return winner
        
        #Row Winning
        for i in range(3):
            init = self.status[0, i]
            if init == 0:
                continue
            for j in range(1, 3):
                if self.status[j, i] != init:
                    winner = 0
                    break
                else:
                    winner = init
            if winner != 0:
                if winner == 1 and Prt:
                    print("O win!")
                    self.Owin += 1
                elif Prt:
                    print("X win!")
                    self.Xwin += 1
                return winner
        
        
        #Cross Winning
        if self.status[1, 1] == 0:
            #Tie
            if self.RemainingSpace == 0:
                if Prt:
                    print("Tie!")
                    self.Tie += 1
                return 3
            else:
                return 0
        else:
            init = self.status[1, 1]
            if self.status[0, 0] == init == self.status[2, 2]:
                if init == 1 and Prt:
                    print("O win!")
                    self.Owin += 1
                elif Prt:
                    print("X win!")
                    self.Xwin += 1
                return init
            elif self.status[2, 0] == init == self.status[0, 2]:
                if init == 1 and Prt:
                    print("O win!")
                    self.Owin += 1
                elif Prt:
                    print("X win!")
                    self.Xwin += 1
                return init
            else:
                #Tie
                if self.RemainingSpace == 0:
                    if Prt:
                        print("Tie!")
                        self.Tie += 1
                    return 3
                else:
                    return 0
            
    def Show(self):
        show = []
        for i in range(len(self.status)):
            for j in range(len(self.status[i])):
                if self.status[i][j] == 0:
                    show.append(" ")
                elif self.status[i][j] == 1:
                    show.append("O")
                elif self.status[i][j] == 2:
                    show.append("X")
        print(" %s | %s | %s \n-----------\n %s | %s | %s \n-----------\n %s | %s | %s\n"%tuple(show))
        
            
            
class Agent:
    def __init__(self, env): 
        self.table = np.zeros((3, 3, 3, 3, 3, 3, 3, 3, 3, 9))
        self.env = env
        
        self.alpha = 0.1
        self.gamma = 0.9
    
    def GetState(self, team):
        state = sum(self.env.status.tolist(), [])
        for i in range(len(state)):
            if team == 2:
                if state[i] == 1:
                    state[i] = 2
                elif state[i] == 2:
                    state[i] = 1
                    
        return state
    
    def Decision(self, s):
        EXP = self.table[tuple(s)]
        decision = np.random.choice(np.where(EXP == np.max(EXP))[0])
        return decision
    
    def learn(self, s, s_, a, R):
        if R == 0:
            self.table[tuple(s)][a] = self.table[tuple(s)][a] + self.alpha*(R + self.gamma*np.max(self.table[tuple(s_)]) - self.table[tuple(s)][a])
        else:
            self.table[tuple(s)][a] = self.table[tuple(s)][a] + self.alpha*(R - self.table[tuple(s)][a])

def Trainer(env, epoch):
    agent = Agent(env)
    
    for i in range(epoch):
        print("Epoch", i+1)
        sX, sO, aX, aO, s_X, s_O = 0, 0, 0, 0, 0, 0
        while True:
            for i in range(2):
                if i == 0:
                    sO = agent.GetState(1)
                    step = agent.Decision(sO)
                    x, y = int(step/3), step%3
                    while not env.Step(x, y, 1):
                        agent.table[tuple(sO)][step] = -1000
                        step = agent.Decision(sO)
                        x, y = int(step/3), step%3
                        
                    aO = step
                    s_X = agent.GetState(1)
                    if sX != 0:
                        winner = env.Ref()
                        if winner == 0:
                            agent.learn(sX, s_X, aX, 0)
                        elif winner == 1:
                            agent.learn(sX, s_X, aX, -100)
                            agent.learn(sO, s_O, aO, 100)
                            break
                        elif winner == 3:
                            agent.learn(sX, s_X, aX, 10)
                            break
                    
                        
                    
                elif i == 1:
                    sX = agent.GetState(2)
                    step = agent.Decision(sX)
                    x, y = int(step/3), step%3
                    while not env.Step(x, y, 2):
                        agent.table[tuple(sX)][step] = -1000
                        step = agent.Decision(sX)
                        x, y = int(step/3), step%3
                    
                    aX = step
                    s_O = agent.GetState(2)
                    if sO != 0:
                        winner = env.Ref()
                        if winner == 0:
                            agent.learn(sO, s_O, aO, 0)
                        elif winner == 2:
                            agent.learn(sO, s_O, aO, -100)
                            agent.learn(sX, s_X, aX, 100)
                            break
                        elif winner == 3:
                            agent.learn(sO, s_O, aO, 10)
                            break
                
                
                
            if env.Ref(True) != 0:
                env.Reset()
                break
            
                    
env = Env()
Trainer(env, 1000)
print("Tie: {} O: {} X: {}".format(env.Tie, env.Owin, env.Xwin))
