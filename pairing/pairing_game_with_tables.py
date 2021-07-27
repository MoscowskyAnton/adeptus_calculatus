#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from pairing_core import PairingTable

class PairingSheetTables(PairingTable):
    
    def __init__(self, scores, tables, min_score = 0, max_score = 20, teamA_player_names = None, teamB_player_names = None):
        
        if not type(scores) is np.ndarray:
            raise ValueError("PairingSheetTables: __init__: scores must be numpy array, not {}".format(type(scores)))
        if len(scores.shape) != 3:
            raise ValueError("PairingSheetTables: __init__: scores must be 3D -matrix, not {} dimentional".format(len(scores.shape)))
        if scores.shape[0] != scores.shape[1]:
            raise ValueError("PairingSheetTables: __init__: scores dimentional size must be equal, but got {} and {}".format(scores.shape[0], scores.shape[1]))
        
        if tables.shape[0] != scores.shape[0]:
            raise ValueError("PairingSheetTables: __init__: scores dimentional size must be equal to table dimentional size, but got {} and {}".format(scores.shape[0], tables.shape[0]))
        
        self.scores = scores
        
        '''
        0 - 'OPEN'
        1 - 'HALF-CLOSED'
        2 - 'CLOSED'        
        '''
        self.tables_types = tables
        self.reset()
        
        self.teamA_player_names = teamA_player_names
        self.teamB_player_names = teamB_player_names
        
        self.players_num = self.scores.shape[0]
        
        self.max_player_score = max_score
        self.min_player_score = min_score
        self.max_team_score = max_score * self.players_num
        self.min_team_score = min_score * self.players_num
        
    def reset(self):
        self.tables_free = [True] * self.tables_types.shape[0]
        


class PairingGameAlphaBetaTables(object):
    
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
        
        self.team_A_def_table_id = None
        self.team_B_def_table_id = None
        self.rejected_players_table_id = None
        self.champions_table_id = None
        
        self.team_A_won_first_table_rolloff = False
        self.team_A_won_second_table_rolloff = False
    
    def get_score(self):
        score = 0
        #print(self.team_A_atackers)
        score += self.PT[self.team_A_def, self.team_B_choosed_atacker, self.PT.tables_types[self.team_A_def_table_id] ]
        score += self.PT[self.team_A_choosed_atacker, self.team_B_def, self.PT.tables_types[self.team_B_def_table_id] ]
        score += self.PT[self.team_A_reject_atacker, self.team_B_reject_atacker, self.PT.tables_types[self.rejected_players_table_id] ]
        score += self.PT[self.team_A_champion, self.team_B_champion, self.PT.tables_types[self.champions_table_id] ]
        #print(self.team_A_def, self.team_B_choosed_atacker,self.team_B_def, self.team_A_choosed_atacker,self.team_A_reject_atacker, self.team_B_reject_atacker,self.team_A_champion, self.team_B_champion)
        #print(score)
        return score
    
    def print_results(self):
        sc = self.get_score()
        print("Total score A {} : {} B".format(sc, self.PT.max_team_score - sc))
        
        print("Table {} (type{}): DefA ({}) vs AtackB ({}) - {}".format(self.team_A_def_table_id, self.PT.tables_types[self.team_A_def_table_id], self.team_A_def, self.team_B_choosed_atacker, self.PT[self.team_A_def, self.team_B_choosed_atacker, self.PT.tables_types[self.team_A_def_table_id]]))
        
        print("Table {} (type{}): AtackA ({}) vs DefB ({}) - {}".format(self.team_B_def_table_id, self.PT.tables_types[self.team_B_def_table_id], self.team_A_choosed_atacker, self.team_B_def, self.PT[ self.team_A_choosed_atacker,self.team_B_def, self.PT.tables_types[self.team_B_def_table_id]]))
        
        print("Table {} (type{}): RejA ({}) vs RejB ({}) - {}".format(self.rejected_players_table_id, self.PT.tables_types[self.rejected_players_table_id], self.team_A_reject_atacker, self.team_B_reject_atacker, self.PT[self.team_A_reject_atacker, self.team_B_reject_atacker, self.PT.tables_types[self.rejected_players_table_id]]))
        
        print("Table {} (type{}): ChampA ({}) vs ChampB ({}) - {}".format(self.champions_table_id, self.PT.tables_types[self.champions_table_id], self.team_A_champion, self.team_B_champion, self.PT[self.team_A_champion, self.team_B_champion, self.PT.tables_types[self.champions_table_id]]))
        
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
            
    def select_defender_table(self, team, table_id):
        if team == 'A':
            self.team_A_def_table_id = table_id
        else:
            self.team_B_def_table_id = table_id
        self.PT.tables_free[table_id] = False
                
    def unselect_defender_table(self, team):
        if team == 'A':
            self.PT.tables_free[self.team_A_def_table_id] = True
            self.team_A_def_table_id = None            
        if team == 'B':
            self.PT.tables_free[self.team_B_def_table_id] = True
            self.team_B_def_table_id = None    
        
    def select_rejected_table(self, table):
        self.rejected_players_table_id = table
        self.PT.tables_free[table] = False
        self.champions_table_id = self.PT.tables_free.index(True)
        self.PT.tables_free[self.champions_table_id] = False
        
    def unselect_rejected_table(self):
        self.PT.tables_free[self.champions_table_id] = True
        self.PT.tables_free[self.rejected_players_table_id] = True        
        self.rejected_players_table_id = None
        self.champions_table_id = None        
              
    # team A turn
    def max(self, state, alpha, beta):
        total_score = self.PT.min_team_score
        player_selected = None
        
        if state == 'def':
            for player_i, player_free in enumerate(self.team_A_state):
                if player_free:
                    self.set_def('A', player_i)
                    sc, pl = self.min(state, alpha, beta)
                    if sc > total_score:
                        total_score = sc
                        player_selected = player_i
                    self.release_def('A')
                        
                    if total_score >= beta:
                        #print('Beta cut off {} vs {}'.format(total_score, beta))
                        return total_score, player_selected
                    
                    alpha = max(total_score, alpha)
                    
        elif state == 'atacks':
            for player_ii, player_i_free in enumerate(self.team_A_state):
                for player_jj, player_j_free in enumerate(self.team_A_state):
                    if player_ii > player_jj and player_i_free and player_j_free:
                        
                        self.set_atackers('A', player_ii, player_jj, True)
                        
                        sc, pl = self.min(state, alpha, beta)
                        if sc > total_score:
                            total_score = sc
                            player_selected = [player_ii, player_jj]
                            
                        self.release_atackers('A', True)
                        
                        if total_score >= beta:
                            #print('Beta cut off {} vs {}'.format(total_score, beta))
                            return total_score, player_selected
                    
                        alpha = max(total_score, alpha)

            
        elif state == 'chooseAtack':
            atackers = [(self.team_B_atackers[0], self.team_B_atackers[1]),
                        (self.team_B_atackers[1], self.team_B_atackers[0])]
            for i, j in atackers:
                self.choose_atacker('B', i, j)# yes B
                
                sc, pl = self.min(state, alpha, beta)
                
                if sc > total_score:
                    total_score = sc
                    player_selected = i
                
                self.unchoose_atacker('B')
                
                if total_score >= beta:
                    #print('Beta cut off {} vs {}'.format(total_score, beta))
                    return total_score, player_selected
                    
                alpha = max(total_score, alpha)
                
        elif state == 'selectDefenderTable':
            
            for i, table_free in enumerate(self.PT.tables_free):
                if table_free:
                    
                    #self.team_A_def_table_id = i
                    #self.PT.tables_free[i] = False
                    self.select_defender_table('A',i)
                    
                    if self.team_A_won_first_table_rolloff:
                        sc, pl = self.min(state, alpha, beta)                                            
                        
                    else:
                        if self.team_A_won_second_table_rolloff:
                            sc, pl = self.max('selectRejectedTable', alpha, beta)                                            
                        else:
                            sc, pl = self.min('selectRejectedTable', alpha, beta)                                                                                                
                                            
                    if sc > total_score:
                        total_score = sc
                        player_selected = i
                                            
                    #self.team_A_def_table_id = None
                    #self.PT.tables_free[i] = True
                    self.unselect_defender_table('A')
                
                    if total_score >= beta:
                        #print('Beta cut off {} vs {}'.format(total_score, beta))
                        return total_score, player_selected
                    
                    alpha = max(total_score, alpha)
                    
        elif state == 'selectRejectedTable':
            for i, table_free in enumerate(self.PT.tables_free):
                if table_free:
                                        
                    self.select_rejected_table(i)
                    
                    sc = self.get_score()
                    if sc > total_score:
                        player_selected = i
                        total_score = sc
                                            
                    self.unselect_rejected_table()
                    
                    if total_score >= beta:
                        return total_score, player_selected
                    
                    alpha = max(total_score, alpha)

        
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
                    
                    if sc < total_score:
                        player_selected = player_i
                        total_score = sc
                    
                    self.release_def('B')
                    
                    if total_score <= alpha:
                        #print('Alpha cut-off {} vs {}'.format(total_score, alpha))
                        return total_score, player_selected
                    
                    beta = min(beta, total_score)

                    
        elif state == 'atacks':
            for player_ii, player_i_free in enumerate(self.team_B_state):
                for player_jj, player_j_free in enumerate(self.team_B_state):
                    if player_ii > player_jj and player_i_free and player_j_free:
                        
                        self.set_atackers('B', player_ii, player_jj, True)
                        
                        sc, pl = self.max('chooseAtack', alpha, beta)
                        if sc < total_score:
                            total_score = sc
                            player_selected = [player_ii, player_jj]
                            
                        self.release_atackers('B', True)
                        
                        if total_score <= alpha:
                            #print('Alpha cut-off {} vs {}'.format(total_score, alpha))
                            return total_score, player_selected
                    
                        beta = min(beta, total_score)

                        
        elif state == 'chooseAtack':
            atackers = [(self.team_A_atackers[0], self.team_A_atackers[1]),
                        (self.team_A_atackers[1], self.team_A_atackers[0])]
            for i, j in atackers:
                self.choose_atacker('A', i, j) # yes, A
                
                #sc = self.get_score()
                if self.team_A_won_first_table_rolloff:
                    sc, pl = self.max('selectDefenderTable', alpha, beta)
                else:
                    sc, pl = self.min('selectDefenderTable', alpha, beta)
                
                if sc < total_score:
                    player_selected = i
                    total_score = sc
                    
                self.unchoose_atacker('A')
                
                if total_score <= alpha:
                    #print('Alpha cut-off {} vs {}'.format(total_score, alpha))
                    return total_score, player_selected
                  
                beta = min(beta, total_score)
                
        elif state == 'selectDefenderTable':
            
            for i, table_free in enumerate(self.PT.tables_free):
                if table_free:
                    
                    #self.team_B_def_table_id = i
                    #self.PT.tables_free[i] = False                    
                    self.select_defender_table('B', i)
                    
                    if not self.team_A_won_first_table_rolloff:
                        sc, pl = self.max(state, alpha, beta)                                            
                        
                    else:
                        if self.team_A_won_second_table_rolloff:
                            sc, pl = self.max('selectRejectedTable', alpha, beta)                                            
                        else:
                            sc, pl = self.min('selectRejectedTable', alpha, beta)                                                                                                
                                            
                    if sc < total_score:
                        total_score = sc
                        player_selected = i
                                            
                    #self.team_B_def_table_id = None
                    #self.PT.tables_free[i] = True
                    self.unselect_defender_table('B')
                
                    if total_score <= alpha:
                        #print('Alpha cut off {} vs {}'.format(total_score, beta))
                        return total_score, player_selected
                    
                    beta = min(total_score, beta)
                    
        elif state == 'selectRejectedTable':
            for i, table_free in enumerate(self.PT.tables_free):
                if table_free:
                                        
                    self.select_rejected_table(i)
                    
                    sc = self.get_score()
                    if sc < total_score:
                        player_selected = i
                        total_score = sc
                                            
                    self.unselect_rejected_table()
                    
                    if total_score <= alpha:
                        return total_score, player_selected
                    
                    beta = min(total_score, beta)
            

        else:
            print('ERROR! unknown phase {}'.format(phase))        
        
        return total_score, player_selected
    
    def make_optimal_move(self, team, phase):
        alpha_start = self.PT.min_team_score-1
        beta_start = self.PT.max_team_score+1
        if phase == 'def':
            if team == 'A':
                score, defender = self.max('def', alpha_start, beta_start)
            elif team == 'B':
                score, defender = self.min('def', alpha_start, beta_start)
            if defender is None:
                raise ValueError('Selected player is None!')
            self.set_def(team, defender)
            print('TEAM {}: recomend to set defender {} for max score {}'.format(team, defender, score))
        elif phase == 'atacks':
            if team == 'A':
                score, atackers = self.max('atacks', alpha_start, beta_start)
            elif team == 'B':
                score, atackers = self.min('atacks', alpha_start, beta_start)
            if atackers is None:
                raise ValueError('Selected player is None!')
            self.set_atackers(team, atackers[0], atackers[1], True)
            print('TEAM {}: recomend to set atackers {} for max score {}'.format(team, atackers, score))
        elif phase == 'chooseAtack':
            if team == 'A':
                score, choosed = self.max('chooseAtack', alpha_start, beta_start)
                self.choose_atacker('B', choosed, None)
            elif team == 'B':
                score, choosed = self.min('chooseAtack', alpha_start, beta_start)
                self.choose_atacker('A', choosed, None)
            if choosed is None:
                raise ValueError('Selected player is None!')
            print('TEAM {}: recomend choose player {} from oppsite atackers, for score {}'.format(team, choosed, score))
        elif phase == 'selectDefenderTable':
            if team == 'A':
                score, choosed = self.max('selectDefenderTable', alpha_start, beta_start)                
                self.select_defender_table('A',choosed)                
                print("TEAM {}: recomend select table no{}(type{}) for score {}".format(team, choosed, self.PT.tables_types[choosed], score))
            elif team == 'B':
                score, choosed = self.min('selectDefenderTable', alpha_start, beta_start)
                self.select_defender_table('B',choosed)
                #print(self.PT.tables_types.shape, choosed)
                print("TEAM {}: recomend select table no{}(type{}) for score {}".format(team, choosed, self.PT.tables_types[choosed], score))
        elif phase == 'selectRejectedTable':
            if team == 'A':
                score, choosed = self.max('selectRejectedTable', alpha_start, beta_start)
                self.select_rejected_table(choosed)
                print("TEAM {}: recomend select table no{}(type{}) for score {}".format(team, choosed, self.PT.tables_types[choosed], score))
            elif team == 'B':
                score, choosed = self.min('selectRejectedTable', alpha_start, beta_start)                
                self.select_rejected_table(choosed)
                print("TEAM {}: recomend select table no{}(type{}) for score {}".format(team, choosed, self.PT.tables_types[choosed], score))
            
            
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
        self.make_optimal_move('B', 'chooseAtack')
        if self.team_A_won_first_table_rolloff:
            self.make_optimal_move('A', 'selectDefenderTable')
            self.make_optimal_move('B', 'selectDefenderTable')
        else:
            self.make_optimal_move('B', 'selectDefenderTable')
            self.make_optimal_move('A', 'selectDefenderTable')
        if self.team_A_won_second_table_rolloff:
            score = self.make_optimal_move('A', 'selectRejectedTable')
        else:
            score = self.make_optimal_move('B', 'selectRejectedTable')
        
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
    all_scores = []
    for n in range(N):
        tables = [0,1,1,2]
        
        pt = PairingSheetTables(np.random.randint(0,21,(4,4,3)), np.array(tables), teamA_player_names = ['Starrok', 'Aberrat', 'Strohkopf', 'Servius'])    
        #print(pt)
        
        scores = []
        
        pg_1 = PairingGameAlphaBetaTables(pt)
        scores.append(pg_1.play_optimal_way())
        pg_1.print_results()
        
        pt.reset()
        pg_2 = PairingGameAlphaBetaTables(pt)
        pg_2.team_A_won_first_table_rolloff = True
        #pg_2.team_A_won_second_table_rolloff = True
        scores.append(pg_2.play_optimal_way())
        pg_2.print_results()
        
        pt.reset()
        pg_2 = PairingGameAlphaBetaTables(pt)
        #pg_2.team_A_won_first_table_rolloff = True
        pg_2.team_A_won_second_table_rolloff = True
        scores.append(pg_2.play_optimal_way())
        pg_2.print_results()
        
        pt.reset()
        pg_2 = PairingGameAlphaBetaTables(pt)
        pg_2.team_A_won_first_table_rolloff = True
        pg_2.team_A_won_second_table_rolloff = True
        scores.append(pg_2.play_optimal_way())
        pg_2.print_results()
        
        all_scores.append(scores)
    
    #print(scores)
    all_scores = np.array(all_scores)
    
    diff1 = all_scores[:,1] - all_scores[:,0]
    diff2 = all_scores[:,2] - all_scores[:,0]
    diff3 = all_scores[:,3] - all_scores[:,0]
    
    mean = [0, np.mean(diff1), np.mean(diff2), np.mean(diff3)]
    maxx = [0, np.max(diff1), np.max(diff2), np.max(diff3)]
    minn = [0, np.min(diff1), np.min(diff2), np.min(diff3)]
    q1 = [0, np.quantile(diff1, 0.25), np.quantile(diff2, 0.25), np.quantile(diff3, 0.25)]
    q3 = [0, np.quantile(diff1, 0.75), np.quantile(diff2, 0.75), np.quantile(diff3, 0.75)]
    
    plt.title('Difference in score by table choose roll-offs, average by {} tests'.format(N))
    plt.ylabel('Team A score')
    plt.xlabel('Table choose roll-off for team A')
    plt.xticks([0,1,2,3],['both loose','1 win, 2 loose','1 loose, 2 win', 'both win'])
    plt.plot(mean,'-*',label="mean")
    plt.plot(maxx,':*',label="max")
    plt.plot(minn,':*',label="min")
    plt.fill_between([0,1,2,3], q1, q3, alpha = 0.25, label="interquartile")
    plt.legend()
    plt.grid()
    plt.show()
    
    
