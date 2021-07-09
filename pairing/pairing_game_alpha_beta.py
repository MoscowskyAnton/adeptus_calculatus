#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from pairing_core import PairingTable, PairingGame
import time

class PairingGameAlphaBeta(object):
    
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
        sc = self.get_score()
        print("Total score A {} : {} B".format(sc, self.PT.max_team_score - sc))
        
        print("DefA ({}) vs AtackB ({}) - {}".format(self.team_A_def, self.team_B_choosed_atacker, self.PT[self.team_A_def, self.team_B_choosed_atacker]))
        
        print("AtackA ({}) vs DefB ({}) - {}".format( self.team_A_choosed_atacker, self.team_B_def, self.PT[ self.team_A_choosed_atacker,self.team_B_def]))
        
        print("RejA ({}) vs RejB ({}) - {}".format(self.team_A_reject_atacker, self.team_B_reject_atacker, self.PT[self.team_A_reject_atacker, self.team_B_reject_atacker]))
        
        print("ChampA ({}) vs ChampB ({}) - {}".format(self.team_A_champion, self.team_B_champion, self.PT[self.team_A_champion, self.team_B_champion]))
        
    def set_def(self, team, player_i):
        if team == 'A':
            self.team_A_def = player_i
            self.team_A_state[player_i] = False
        elif team == 'B':
            self.team_B_def = player_i
            self.team_B_state[player_i] = False
    
    def release_def(self, team):
        if team == 'A':
            defender = self.team_A_def
            self.team_A_def = None
            self.team_A_state[defender] = True
        elif team == 'B':
            defender = self.team_B_def
            self.team_B_def = None
            self.team_B_state[defender] = True
        return defender
    
    def set_atackers(self, team, a1, a2, also_champ = False):
        if team == 'A':
            self.team_A_atackers = [a1, a2]
            self.team_A_state[a1] = False
            self.team_A_state[a2] = False
            if also_champ:
                self.team_A_champion = self.team_A_state.index(True)
                self.team_A_state[self.team_A_champion] = False
                
        elif team == 'B':
            self.team_B_atackers = [a1, a2]
            self.team_B_state[a1] = False
            self.team_B_state[a2] = False
            if also_champ:
                self.team_B_champion = self.team_B_state.index(True)
                self.team_B_state[self.team_B_champion] = False
            
    def release_atackers(self, team, also_champ = False):
        if team == 'A':
            atackers = self.team_A_atackers
            self.team_A_state[atackers[0]] = True
            self.team_A_state[atackers[1]] = True
            self.team_A_atackers = None
            if also_champ:
                self.team_A_state[self.team_A_champion] = True
                self.team_A_champion = None
        elif team == 'B':
            atackers = self.team_B_atackers
            self.team_B_state[atackers[0]] = True
            self.team_B_state[atackers[1]] = True
            self.team_B_atackers = None
            if also_champ:
                self.team_B_state[self.team_B_champion] = True
                self.team_B_champion = None
        return atackers
    
    def choose_atacker(self, team, choosed_player, rejected_player = None):
        if team == 'B':
            self.team_B_choosed_atacker = choosed_player
            if not rejected_player is None:
                self.team_B_reject_atacker = rejected_player
            else:
                self.team_B_reject_atacker = [x for x in self.team_B_atackers if x != self.team_B_choosed_atacker][0]
                
            # state should be alredy false
        elif team == 'A':
            self.team_A_choosed_atacker = choosed_player
            if not rejected_player is None:
                self.team_A_reject_atacker = rejected_player
            else:
                self.team_A_reject_atacker = [x for x in self.team_A_atackers if x != self.team_A_choosed_atacker][0]
    
    def unchoose_atacker(self, team):
        if team == 'A':
            self.team_A_choosed_atacker = None
            self.team_A_reject_atacker = None
        elif team == 'B':
            self.team_B_choosed_atacker = None
            self.team_B_reject_atacker = None
        
              
    # team A turn
    def max(self, state, alpha, beta):
        total_score = self.PT.min_team_score
        player_selected = None
        
        if state == 'def':
            for player_i, player_free in enumerate(self.team_A_state):
                if player_free:
                    self.set_def('A', player_i)
                    sc, pl = self.min(state, alpha, beta)
                    if sc >= total_score:
                        total_score = sc
                        player_selected = player_i
                    self.release_def('A')
                        
                    if total_score > beta:
                        print('Beta cut off {} vs {}'.format(total_score, beta))
                        return total_score, player_selected
                    
                    if total_score > alpha:
                        alpha = total_score
                    #if total_score <= alpha:
                        #return total_score, player_selected
                    
                    #if total_score < beta:
                        #beta = total_score
                    
        elif state == 'atacks':
            for player_ii, player_i_free in enumerate(self.team_A_state):
                for player_jj, player_j_free in enumerate(self.team_A_state):
                    if player_ii > player_jj and player_i_free and player_j_free:
                        
                        self.set_atackers('A', player_ii, player_jj, True)
                        
                        sc, pl = self.min(state, alpha, beta)
                        if sc >= total_score:
                            total_score = sc
                            player_selected = [player_ii, player_jj]
                            
                        self.release_atackers('A', True)
                        
                        if total_score > beta:
                            return total_score, player_selected
                    
                        if total_score > alpha:
                            alpha = total_score
                        #if total_score <= alpha:
                            #return total_score, player_selected
                    
                        #if total_score < beta:
                            #beta = total_score
            
        elif state == 'chooseAtack':
            atackers = [(self.team_B_atackers[0], self.team_B_atackers[1]),
                        (self.team_B_atackers[1], self.team_B_atackers[0])]
            for i, j in atackers:
                self.choose_atacker('B', i, j)# yes B
                
                sc, pl = self.min(state, alpha, beta)
                
                if sc >= total_score:
                    total_score = sc
                    player_selected = i
                
                self.unchoose_atacker('B')
                
                if total_score > beta:
                    return total_score, player_selected
                    
                if total_score > alpha:
                    alpha = total_score
                #if total_score <= alpha:
                    #return total_score, player_selected
                
                #if total_score < beta:
                    #beta = total_score
        
        return total_score, player_selected
     
    # team B turn
    def min(self, state, alpha, beta):
        total_score = self.PT.max_team_score
        player_selected = None
        
        if state == 'def':
            for player_i, player_free in enumerate(self.team_B_state):
                if player_free:
                    self.set_def('B', player_i)
                    sc, pl = self.max('atacks', alpha, beta)
                    
                    if sc <= total_score:
                        player_selected = player_i
                        total_score = sc
                    
                    self.release_def('B')
                    
                    if total_score < alpha:
                        print('Alpha cut-off {} vs {}'.format(total_score, alpha))
                        return total_score, player_selected
                    
                    if total_score < beta:
                        beta = total_score
                    
                    #if total_score >= beta:
                        #return total_score, player_selected
                    
                    #if total_score > alpha:
                        #alpha = total_score
                    
        elif state == 'atacks':
            for player_ii, player_i_free in enumerate(self.team_B_state):
                for player_jj, player_j_free in enumerate(self.team_B_state):
                    if player_ii > player_jj and player_i_free and player_j_free:
                        
                        self.set_atackers('B', player_ii, player_jj, True)
                        
                        sc, pl = self.max('chooseAtack', alpha, beta)
                        if sc <= total_score:
                            total_score = sc
                            player_selected = [player_ii, player_jj]
                            
                        self.release_atackers('B', True)
                        
                        if total_score < alpha:
                            return total_score, player_selected
                    
                        if total_score < beta:
                            beta = total_score
                        #if total_score >= beta:
                            #return total_score, player_selected
                    
                        #if total_score > alpha:
                            #alpha = total_score
                        
        elif state == 'chooseAtack':
            atackers = [(self.team_A_atackers[0], self.team_A_atackers[1]),
                        (self.team_A_atackers[1], self.team_A_atackers[0])]
            for i, j in atackers:
                self.choose_atacker('A', i, j) # yes, A
                
                sc = self.get_score()
                if sc <= total_score:
                    player_selected = i
                    total_score = sc
                    
                self.unchoose_atacker('A')
                
                if total_score < alpha:
                    return total_score, player_selected
                    
                if total_score < beta:
                    beta = total_score
                #if total_score >= beta:
                    #return total_score, player_selected
                    
                #if total_score > alpha:
                    #alpha = total_score
        else:
            print('ERROR! unknown phase {}'.format(phase))        
        
        return total_score, player_selected
    
    def make_optimal_move(self, team, phase):
        if phase == 'def':
            if team == 'A':
                score, defender = self.max('def', self.PT.min_team_score-1, self.PT.max_team_score+1)
            elif team == 'B':
                score, defender = self.min('def', self.PT.min_team_score-1, self.PT.max_team_score+1)
            self.set_def(team, defender)
            print('TEAM {}: recomend to set defender {} for max score {}'.format(team, defender, score))
        elif phase == 'atacks':
            if team == 'A':
                score, atackers = self.max('atacks', self.PT.min_team_score-1, self.PT.max_team_score+1)
            elif team == 'B':
                score, atackers = self.min('atacks', self.PT.min_team_score-1, self.PT.max_team_score+1)
            self.set_atackers(team, atackers[0], atackers[1], True)
            print('TEAM {}: recomend to set atackers {} for max score {}'.format(team, atackers, score))
        elif phase == 'chooseAtack':
            if team == 'A':
                score, choosed = self.max('chooseAtack', self.PT.min_team_score-1, self.PT.max_team_score+1)
                self.choose_atacker('B', choosed, None)
            elif team == 'B':
                score, choosed = self.min('chooseAtack', self.PT.min_team_score-1, self.PT.max_team_score+1)
                self.choose_atacker('A', choosed, None)
            print('TEAM {}: recomend choose player {} from oppsite atackers, for score {}'.format(team, choosed, score))
        else:
            print('ERROR! unknown phase {}'.format(phase))
        return score
    
    def random_choose_free_player(self, team):
        if team == 'A':
            while(True):
                player = np.random.randint(0,4)
                if self.team_A_state[player]:
                    return player
        elif team == 'B':
            while(True):
                player = np.random.randint(0,4)
                if self.team_B_state[player]:
                    return player
    
    def make_random_move(self, team, phase):
        if phase == 'def':
            defender = self.random_choose_free_player(team)
            self.set_def(team, defender)
            print("TEAM {} randomly set player {} as defender".format(team, defender))
        elif phase == 'atacks':
            atack1 = self.random_choose_free_player(team)
            while 1:
                atack2 = self.random_choose_free_player(team)
                if atack1 != atack2:
                    break
            self.set_atackers(team, atack1, atack2, True)
            print('TEAM {} randomly set players {} as atackers'.format(team, (atack1, atack2)))
            
        elif phase == 'chooseAtack':
            choose = np.random.randint(0,2)
            if team == 'A':
                pl = self.team_B_atackers[choose]
                self.choose_atacker('B', pl)
            elif team == 'B':
                pl = self.team_A_atackers[choose]
                self.choose_atacker('A', pl)
            print('TEAM {} randomly choosed player {} from opposite atackers'.format(team, pl))
    
    def play_optimal_way(self):
        
        self.make_optimal_move('A', 'def')
        self.make_optimal_move('B', 'def')
        self.make_optimal_move('A', 'atacks')
        self.make_optimal_move('B', 'atacks')
        self.make_optimal_move('A', 'chooseAtack')
        score = self.make_optimal_move('B', 'chooseAtack')
        
        return score
    
    def play_random(self):
        self.make_random_move('A', 'def')
        self.make_random_move('B', 'def')
        self.make_random_move('A', 'atacks')
        self.make_random_move('B', 'atacks')
        self.make_random_move('A', 'chooseAtack')
        self.make_random_move('B', 'chooseAtack')
        
    def play_optimal_vs_random(self):
        self.make_optimal_move('A', 'def')
        self.make_random_move('B', 'def')
        self.make_optimal_move('A', 'atacks')
        self.make_random_move('B', 'atacks')
        self.make_optimal_move('A', 'chooseAtack')
        self.make_random_move('B', 'chooseAtack')
    
    def play_random_vs_optimal(self):
        self.make_random_move('A', 'def')
        self.make_optimal_move('B', 'def')
        self.make_random_move('A', 'atacks')
        self.make_optimal_move('B', 'atacks')
        self.make_random_move('A', 'chooseAtack')
        self.make_optimal_move('B', 'chooseAtack')
    
if __name__ == '__main__' :
    
    N = 100
    regular = []
    alpha_beta = []
    reg_time = []
    ab_time = []
    for n in range(N):
        pt = PairingTable(np.random.randint(0,21,(4,4)), teamA_player_names = ['Starrok', 'Aberrat', 'Strohkopf', 'Servius'])
        
        pg_r = PairingGame(pt)
        
        pg = PairingGameAlphaBeta(pt)
        tock = time.time()
        pg.play_optimal_way()
        tick = time.time()
        pg_r.play_optimal_way()
        tuck = time.time()
        reg_time.append(tuck - tick)
        ab_time.append(tick - tock)
        print(pt)
        print('ALPHA BETA')
        pg.print_results()
        print('REGULAR')
        pg_r.print_results()
        
        regular.append(pg_r.get_score())
        alpha_beta.append(pg.get_score())
        
    plt.plot(np.array(regular) - np.array(alpha_beta), '.')
    #plt.plot(np.array(reg_time) - np.array(ab_time), '.')
    #plt.grid()
    #plt.title('Alpha-beta pruning time decrease')
    #plt.xlabel('# experiment')
    #plt.ylabel('Time decrease, sec')
    plt.show()
