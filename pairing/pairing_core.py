#!/usr/bin/env python
# coding: utf-8
import numpy as np

class PairingTable(object):
    
    '''
    scores - square matrix (np.array) with scores of A team (row-oriented: [i][j] - score how team A player i beat team B player j)
    min_score - minamal possible score of one player
    max_score - maximal possible score of one player
    '''
    def __init__(self, scores, min_score = 0, max_score = 20):
        if not type(scores) is np.ndarray:
            raise ValueError("PairingTable: __init__: scores must be numpy array, not {}".format(type(scores)))
        if len(scores.shape) != 2:
            raise ValueError("ParingTable: __init__: scores must be 2D -matrix, not {} dimentional".format(len(scores.shape)))
        if scores.shape[0] != scores.shape[1]:
            raise ValueError("ParingTable: __init__: scores dimentional size must be equal, but got {} and {}".format(scores.shape[0], scores.shape[1]))
                             
            
        self.scores = scores
        
        self.players_num = self.scores.shape[0]
        
        self.max_player_score = max_score
        self.min_player_score = min_score
        self.max_team_score = max_score * self.players_num
    
    def __str__(self):
        return self.scores.__str__()
    
    def __getitem__(self, indices):
        return self.scores[indices]
    
class PairingGame(object):
    
    def __init__(self, pairing_table):
        self.PT = pairing_table
        
        self.team_A_state = [False] * self.PT.players_num
        self.team_B_state = [False] * self.PT.players_num
        
        self.team_A_def = None
        self.team_B_def = None
        self.team_A_atackers = None
        self.team_B_atackers = None
        self.team_A_choosed_atacker = None
        self.team_B_choosed_atacker = None
        self.team_A_reject_atacker = None
        self.team_B_reject_atacker = None
        self.team_A_champion = None
        self.team_B_champion = None
        
        self.game_state = 0
        self.game_seq = ['def', 'atacks', 'chooseAtack']
    
    def get_score(self):
        score = 0
        score += self.PT[self.team_A_def, self.team_B_choosed_atacker]
        score += self.PT[self.team_B_def, self.team_A_choosed_atacker]
        score += self.PT[self.team_A_reject_atacker, self.team_B_reject_atacker]
        score += self.PT[self.team_A_champion, self.team_B_champion]
        return score
    
    # team A turn
    def max(self):
        total_score = 0
        player_selected = None
        
        if self.game_seq[self.game_state] == 'def':
            for player_i, player_free in enumerate(self.team_A_state):
                if player_free:
                    self.team_A_state[player_i] = True
                    self.team_A_def = player_i
                    sc, pl = self.min()
                    
                    if sc >= total_score:
                        total_score = sc
                        player_selected = pl
                    
                    self.team_A_state[player_i] = False
                    self.team_A_def = None
                    
        elif self.game_seq[self.game_state] == 'atacks':
            for player_ii, player_i_free in enumerate(self.team_A_state):
                for player_jj, player_j_free in enumerate(self.team_A_state[player_ii:]):
                    if player_i_free and player_j_free:
                        
                        self.team_A_atackers = [player_ii, player_jj]
                        self.team_A_state[player_ii] = True
                        self.team_A_state[player_jj] = True
                        self.team_A_champion = self.team_A_state.index(True)
                        self.team_A_state[self.team_A_champion] = True
                        
                        sc, pl = self.min()
                        if sc >= total_score:
                            total_score = sc
                            player_selected = pl
                            
                        self.team_A_atackers = None
                        self.team_A_state[player_ii] = False
                        self.team_A_state[player_jj] = False
                        self.team_A_state[self.team_A_champion] = False
                        self.team_A_champion = None
            
        elif self.game_seq[self.game_state] == 'chooseAtack':
            atackers = [(self.team_B_atackers[0], self.team_B_atackers[1]),
                        (self.team_B_atackers[1], self.team_B_atackers[0])]
            for i, j in atackers:
                self.team_B_choosed_atacker = i
                self.team_B_reject_atacker = j
                
                sc, pl = self.min()
                
                if sc >= total_score:
                    total_score = sc
                    player_selected - pl
                
                self.team_B_choosed_atacker = None
                self.team_B_reject_atacker = None
        
        return total_score, player_selected
    
    def min(self):
        total_score = 0
        player_selected = None
        
        if self.game_seq[self.game_state] == 'def':
            self.game_state += 1
            for player_i, player_free in enumerate(self.team_B_state):
                if player_free:
                    self.team_B_state[player_i] = True
                    self.team_B_def = player_i
                    
                    sc, pl = self.max()
                    
                    if sc >= score:
                        player_selected = pl
                    
                    self.team_B_state[player_i] = False
                    self.team_B_def = None
                    
        elif self.game_seq[self.game_state] == 'atacks':
        elif self.game_seq[self.game_state] == 'chooseAtack':
        
        return total_score, player_selected
        
    

    
if __name__ == '__main__' :
    
    pt = PairingTable(np.array([[5,10,20],[6,11,19],[7,12,18]]))
    
    print(pt[1,1])
