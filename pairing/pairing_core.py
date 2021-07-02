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
        self.min_team_score = min_score * self.players_num
        
    
    def __str__(self):
        return self.scores.__str__()
    
    def __getitem__(self, indices):
        return self.scores[indices]
    
    def mean(self):
        return np.mean(self.scores)
    
class PairingGame(object):
    
    def __init__(self, pairing_table):
        self.PT = pairing_table
        
        self.reset()
        
        self.game_seq = ['def', 'atacks', 'chooseAtack']
        
    def reset(self):
        self.team_A_state = [True] * self.PT.players_num
        self.team_B_state = [True] * self.PT.players_num
        
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
    
    def get_score(self):
        score = 0
        #print(self.team_A_atackers)
        score += self.PT[self.team_A_def, self.team_B_choosed_atacker]
        score += self.PT[self.team_A_choosed_atacker, self.team_B_def]
        score += self.PT[self.team_A_reject_atacker, self.team_B_reject_atacker]
        score += self.PT[self.team_A_champion, self.team_B_champion]
        #print(self.team_A_def, self.team_B_choosed_atacker,self.team_B_def, self.team_A_choosed_atacker,self.team_A_reject_atacker, self.team_B_reject_atacker,self.team_A_champion, self.team_B_champion)
        #print(score)
        return score
    
    def print_results(self):
        print("DefA ({}) vs AtackB ({}) - {}".format(self.team_A_def, self.team_B_choosed_atacker, self.PT[self.team_A_def, self.team_B_choosed_atacker]))
        
        print("AtackA ({}) vs DefB ({}) - {}".format( self.team_A_choosed_atacker, self.team_B_def, self.PT[ self.team_A_choosed_atacker,self.team_B_def]))
        
        print("RejA ({}) vs RejB ({}) - {}".format(self.team_A_reject_atacker, self.team_B_reject_atacker, self.PT[self.team_A_reject_atacker, self.team_B_reject_atacker]))
        
        print("ChampA ({}) vs ChampB ({}) - {}".format(self.team_A_champion, self.team_B_champion, self.PT[self.team_A_champion, self.team_B_champion]))
              
    # team A turn
    def max(self, state):
        total_score = self.PT.min_team_score
        player_selected = None
        
        #if self.game_seq[self.game_state] == 'def':
        if state == 'def':
            for player_i, player_free in enumerate(self.team_A_state):
                if player_free:
                    self.team_A_state[player_i] = False
                    self.team_A_def = player_i
                    sc, pl = self.min(state)
                    
                    if sc >= total_score:
                        total_score = sc
                        player_selected = player_i
                    
                    self.team_A_state[player_i] = True
                    self.team_A_def = None
                    
        #elif self.game_seq[self.game_state] == 'atacks':
        elif state == 'atacks':
            for player_ii, player_i_free in enumerate(self.team_A_state):
                for player_jj, player_j_free in enumerate(self.team_A_state):
                    if player_ii != player_jj and player_i_free and player_j_free:
                        
                        self.team_A_atackers = [player_ii, player_jj]
                        self.team_A_state[player_ii] = False
                        self.team_A_state[player_jj] = False
                        self.team_A_champion = self.team_A_state.index(True)
                        self.team_A_state[self.team_A_champion] = False
                        
                        sc, pl = self.min(state)
                        if sc >= total_score:
                            total_score = sc
                            player_selected = [player_ii, player_jj]
                            
                        self.team_A_atackers = None
                        self.team_A_state[player_ii] = True
                        self.team_A_state[player_jj] = True
                        self.team_A_state[self.team_A_champion] = True
                        self.team_A_champion = None
            
        #elif self.game_seq[self.game_state] == 'chooseAtack':
        elif state == 'chooseAtack':
            atackers = [(self.team_B_atackers[0], self.team_B_atackers[1]),
                        (self.team_B_atackers[1], self.team_B_atackers[0])]
            for i, j in atackers:
                #print(i,j, atackers)
                self.team_B_choosed_atacker = i
                self.team_B_reject_atacker = j
                
                sc, pl = self.min(state)
                
                if sc >= total_score:
                    total_score = sc
                    player_selected = i
                
                self.team_B_choosed_atacker = None
                self.team_B_reject_atacker = None
        
        return total_score, player_selected
     
    # team B turn
    def min(self, state):
        total_score = self.PT.max_team_score
        player_selected = None
        
        #if self.game_seq[self.game_state] == 'def':
        if state == 'def':
            #self.game_state += 1
            for player_i, player_free in enumerate(self.team_B_state):
                if player_free:
                    self.team_B_state[player_i] = False
                    self.team_B_def = player_i
                    
                    sc, pl = self.max('atacks')
                    
                    if sc <= total_score:
                        player_selected = player_i
                        total_score = sc
                    
                    self.team_B_state[player_i] = True
                    self.team_B_def = None
                    
        #elif self.game_seq[self.game_state] == 'atacks':
        elif state == 'atacks':
            #self.game_state += 1
            for player_ii, player_i_free in enumerate(self.team_B_state):
                for player_jj, player_j_free in enumerate(self.team_B_state):
                    if player_ii != player_jj and player_i_free and player_j_free:
                        
                        self.team_B_atackers = [player_ii, player_jj]
                        self.team_B_state[player_ii] = False
                        self.team_B_state[player_jj] = False
                        self.team_B_champion = self.team_B_state.index(True)
                        self.team_B_state[self.team_B_champion] = False
                        #print('tba',self.team_B_atackers)
                        sc, pl = self.max('chooseAtack')
                        if sc <= total_score:
                            total_score = sc
                            player_selected = [player_ii, player_jj]
                            
                        self.team_B_atackers = None
                        self.team_B_state[player_ii] = True
                        self.team_B_state[player_jj] = True
                        self.team_B_state[self.team_B_champion] = True
                        self.team_B_champion = None
                    
        #elif self.game_seq[self.game_state] == 'chooseAtack':
        elif state == 'chooseAtack':
            #self.game_state += 1
            atackers = [(self.team_A_atackers[0], self.team_A_atackers[1]),
                        (self.team_A_atackers[1], self.team_A_atackers[0])]
            for i, j in atackers:
                #print(i,j)
                self.team_A_choosed_atacker = i
                self.team_A_reject_atacker = j
                
                sc = self.get_score()
                #print(sc, total_score)
                if sc <= total_score:
                    player_selected = i
                    total_score = sc
                
                self.team_A_choosed_atacker = None
                self.team_A_reject_atacker = None
        
        return total_score, player_selected
    
    def play_optimal_way(self):
        print(self.PT)
        print('TEAM A mean score = {}'.format(self.PT.mean()))
        
        score, defender = self.max('def')
        print('TEAM A: defend with player A{} and team A score will be {}'.format(defender, score))
        self.team_A_def = defender
        self.team_A_state[defender] = False
        
        score, defender = self.min('def')
        print('TEAM B: defend with player B{} and team A score will be {}'.format(defender, score))
        self.team_B_def = defender
        self.team_B_state[defender] = False
        
        score, atackers = self.max('atacks')
        print('TEAM A: atack with players A{} and team A score will be {}'.format(atackers, score))
        self.team_A_atackers = atackers#list(atackers)
        self.team_A_state[atackers[0]] = False
        self.team_A_state[atackers[1]] = False
        self.team_A_champion = self.team_A_state.index(True)
        self.team_A_state[self.team_A_champion] = False
        
        score, atackers = self.min('atacks')
        print('TEAM B: atack with players B{} and team A score will be {}'.format(atackers, score))
        self.team_B_atackers = atackers
        self.team_B_state[atackers[0]] = False
        self.team_B_state[atackers[1]] = False
        self.team_B_champion = self.team_B_state.index(True)
        self.team_B_state[self.team_B_champion] = False
        
        score, choose = self.max('chooseAtack')
        print('TEAM A: chooose player B{} and team A score will be {}'.format(choose, score))
        self.team_B_choosed_atacker = choose
        self.team_B_reject_atacker = [x for x in self.team_B_atackers if x != self.team_B_choosed_atacker][0]
        
        score, choose = self.min('chooseAtack')
        print('TEAM B: chooose player A{} and team A score will be {}'.format(choose, score))
        self.team_A_choosed_atacker = choose
        self.team_A_reject_atacker = [x for x in self.team_A_atackers if x != self.team_A_choosed_atacker][0]
        
        self.print_results()
        
        return score
        
if __name__ == '__main__' :
    
    '''
    pt = PairingTable(np.array([[0,5,10,20],
                                [19,9,4,0],
                                [7,8,9,10],
                                [20,20,0,0]]))
    '''
    pt = PairingTable(np.random.randint(0,21,(4,4)))
    
    pg = PairingGame(pt)
    pg.play_optimal_way()
