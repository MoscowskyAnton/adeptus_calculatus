from mcts import mcts
import numpy as np
from enum import Enum
from copy import deepcopy

GameStage = Enum('GameStage', ['DEF', 'ATTCK', 'CHOOSE', 'TABLE', 'FIN'])


SCORES = np.random.randint(-2, 3, size= (4, 4, 3))

#SEQUENCE = [(1, GameStage.DEF),
            #(-1, GameStage.DEF),
            #(1, GameStage.ATTCK),
            #(-1, GameStage.ATTCK),
            #(1, GameStage.CHOOSE),
            #(-1, GameStage.CHOOSE),
            #(1, GameStage.TABLE),
            #(-1, GameStage.TABLE),
            #(1, GameStage.DEF),
            #(-1, GameStage.DEF),
            #(1, GameStage.ATTCK),
            #(-1, GameStage.ATTCK),
            #(1, GameStage.CHOOSE),
            #(-1, GameStage.CHOOSE),
            #(-1, GameStage.TABLE),
            #(1, GameStage.TABLE),
            #(1, GameStage.FIN)]

SEQUENCE = [(1, GameStage.DEF),
            (-1, GameStage.DEF),
            (1, GameStage.ATTCK),
            (-1, GameStage.ATTCK),
            (1, GameStage.CHOOSE),
            (-1, GameStage.CHOOSE),
            (1, GameStage.TABLE),
            (-1, GameStage.TABLE),
            
            (1, GameStage.FIN)]

class Team(object):
    
    def __init__(players_num = 4):
        
        self.free_players = [i for i in range(players_num)]
        self.def = -1
        self.atacks = (-1, -1)
        
def swap_teams(team):
    if team == 0:
        return 1
    return 0

class GameState():
            
    
    def __init__(self, stage_num = 0):
        
        # GAME STATE        
        self.current_team = 0
        self.stage_num = stage_num
        
        self.teams = [Team(), Team()]        
        
        self.free_tables = [0, 1, 2, 3]#, 4, 5, 6, 7]
        self.table_types = [0, 1, 1, 2]#, 3, 3, 3, 3]
        
        self.pairings = []
        
    
    def getPossibleActions(self):
        possibleActions = []
        
        team = SEQUENCE[self.stage_num][0]
        stage_type = SEQUENCE[self.stage_num][1]
        
        if stage_type == GameStage.DEF:
            for player in self.teams[team]:
                
                action = Action(team, self.stage_num, stage_type, player)
                possibleActions.append(action)
            
        return possibleActions
    
    
    def takeAction(self, action):
        new_state = deepcopy(self)
        
        if action.stage_type == GameStage.DEF:            
            pairing = (-1, -1, -1)
            pairing[team] = action.choise1            
            new_state.pairings.append(pairing)
            
        elif action.stage_type == GameStage.ATTCK:
            new_state.teams[swap_teams(action.team)].atacks = (action.choise1, action.choise2)
            
        elif action.stage_type == GameStage.CHOOSE:            
            new_state.pairings[-1][action.team] = action.choise1
            
        elif action.stage_type == GameStage.TABLE:
            new_state.pairings[-1][2] = action.choise1
        
        return new_state
            
    
    def isTerminal(self):
        pass
    
    def getReward(self):
        pass
    
class Action():
    
    def __init__(team, game_stage, stage_type, choise1, choise2 = -1):
        
        self.team = team
        self.game_stage = game_stage
        self.stage_type = stage_type
        self.choise1 = choise1
        self.choise2  = choise2
        
    
        
    def __hash__():
        return hash((team, game_stage, choise1, choise2))
    
    
if __name__ == '__main__':    
    
    
    
    initialState = GameState()
    searcher = mcts(timeLimit=1000)
    action = searcher.search(initialState=initialState)
