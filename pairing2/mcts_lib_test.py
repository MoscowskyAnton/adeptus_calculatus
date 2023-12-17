from mcts import mcts
import numpy as np
from enum import Enum
from copy import deepcopy

GameStage = Enum('GameStage', ['DEF', 'ATTCK', 'CHOOSE', 'TABLE', 'FIN'])


SCORES = np.random.randint(-2, 3, size= (4, 4, 4))

# team stage_type pairing no 
SEQUENCE = np.array([(0, GameStage.DEF, 0),
            (1, GameStage.DEF, 1),
            (0, GameStage.ATTCK, 0),
            (1, GameStage.ATTCK, 1),
            (0, GameStage.CHOOSE, 0),
            (1, GameStage.CHOOSE, 1),
            (0, GameStage.TABLE, 0),
            (1, GameStage.TABLE, 1),
            (1, GameStage.FIN, 2)])

class Team(object):
    
    def __init__(self, players_num = 4):
        
        self.free_players = [i for i in range(players_num)]
        #self.free_players = [0, 1, 2, 3]
        #self.defn = -1
        self.atacks = [-1, -1]
        self.rej = -1
        
        
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
        
        self.pairings = np.ones((4, 3), dtype = int) * -1
        '''
        def1 atack2 t
        def2 atack1 t
        rej1 rej2 t
        champ1 champ2 t
        '''
        
    
    def getPossibleActions(self):
        possibleActions = []
        
        team = SEQUENCE[self.stage_num][0]
        stage_type = SEQUENCE[self.stage_num][1]
        
        if stage_type == GameStage.DEF:
            for player in self.teams[team].free_players:
                
                action = Action(SEQUENCE[self.stage_num], player)
                possibleActions.append(action)
                
        elif stage_type == GameStage.ATTCK:
            for i in range(len(self.teams[team].free_players)):
                for j in range(i+1, len(self.teams[team].free_players)):
                    action = Action(SEQUENCE[self.stage_num], 
                                    self.teams[team].free_players[i],
                                    self.teams[team].free_players[j])
                    possibleActions.append(action)
                    
        elif stage_type == GameStage.CHOOSE:
            for player in self.teams[swap_teams(team)].atacks: # !SWAP
                action = Action(SEQUENCE[self.stage_num], player)
                possibleActions.append(action)
                    
        elif stage_type == GameStage.TABLE or stage_type == GameStage.FIN:
            for table in self.free_tables:
                action = Action(SEQUENCE[self.stage_num], table)
                possibleActions.append(action)
            
        return possibleActions
    
    
    def takeAction(self, action):
        new_state = deepcopy(self)
        stage_type = action.sequnce[1]
        pairing_no = action.sequnce[2]
        team = action.sequnce[0]
        
        if stage_type == GameStage.DEF:            
            new_state.pairings[pairing_no][team] = action.choise1
            new_state.teams[team].free_players.remove(action.choise1)
            
        elif stage_type == GameStage.ATTCK:
            new_state.teams[team].atacks = [action.choise1, action.choise2]
            new_state.teams[team].free_players.remove(action.choise1)
            new_state.teams[team].free_players.remove(action.choise2)
            
        elif stage_type == GameStage.CHOOSE:            
            #print(action.choise1, new_state.teams[swap_teams(team)].atacks)
            new_state.pairings[pairing_no][swap_teams(team)] = action.choise1
            #new_state.teams[swap_teams(team)].free_players.remove(action.choise1)
            new_state.teams[swap_teams(team)].atacks.remove(action.choise1)
            #print(new_state.teams[swap_teams(team)].atacks)
            new_state.teams[swap_teams(team)].rej = new_state.teams[swap_teams(team)].atacks[0]
            
        elif stage_type == GameStage.TABLE:
            new_state.pairings[pairing_no][2] = action.choise1
            new_state.free_tables.remove(action.choise1)
            
        elif stage_type == GameStage.FIN:            
            
            new_state.pairings[2] = np.array([new_state.teams[0].rej, new_state.teams[1].rej, action.choise1])
            
            ch1 = new_state.teams[0].free_players[0]
            ch2 = new_state.teams[1].free_players[0]
            new_state.free_tables.remove(action.choise1)
            new_state.pairings[3] = np.array([ch1, ch2, new_state.free_tables[0]])
        
        #print(SEQUENCE[self.stage_num])
        #print(new_state.pairings)
        new_state.stage_num+=1
        
        return new_state
            
    
    def isTerminal(self):
        return not np.isin(self.pairings, -1).any()
    
    def getReward(self):
        reward = 0
        for i in [0, 2, 3]:
            #print(self.pairings[i])
            #print(self.pairings[i], SCORES[self.pairings[i]])
            #exit()
            #reward += SCORES[self.pairings[i]]
            reward += SCORES[self.pairings[i][0], 
                             self.pairings[i][1], 
                             self.pairings[i][2]]
        #print(self.pairings, SCORES.shape)
        reward += SCORES[self.pairings[1][1], 
                         self.pairings[1][0], 
                         self.pairings[1][2]]
        #print(reward)
        return reward
    
    def __eq__(self, other):
        raise NotImplementedError()
    
class Action():
    
    def __init__(self, sequnce, choise1, choise2 = -1):        
        self.sequnce = sequnce
        self.choise1 = choise1
        self.choise2  = choise2
        
    def __str__(self):
        return f'{self.sequnce}: {self.choise1} {self.choise2}'
        
    def __hash__(self):
        #return hash((team, game_stage, choise1, choise2))
        return hash((self.sequnce[0], self.sequnce[1], self.choise1, self.choise2))
    
    def __eq__(self, other):
        #raise NotImplementedError()
        return False
    
    
if __name__ == '__main__':    
    
    
    
    initialState = GameState()
    searcher = mcts(timeLimit=1000)
    action = searcher.search(initialState=initialState)
    print(action)
