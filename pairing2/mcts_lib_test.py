from mcts import mcts
import numpy as np

class GameState():
    
    def __init__(self):
        
        self.playersA = np.array([0] * 8, dtype = bool)
        self.playersB = np.array([0] * 8, dtype = bool)
        self.tables = np.array([0] * 8, dtype = bool)
        self.tables_types = np.array([0] * 3, dtype = int)
        
    
    def getPossibleActions(self):
        pass
    
    def takeAction(self, action):
        pass
    
    def isTerminal(self):
        pass
    
    def getReward(self):
        pass
    
class Action():
    
    def __init__():
        pass
    
    
if __name__ == '__main__':    
    
    
    
    initialState = GameState()
    searcher = mcts(timeLimit=1000)
    action = searcher.search(initialState=initialState)
