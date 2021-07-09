#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import time
from pairing_core import PairingTable

class PairingGame8(object):
    def __init__(self, pairing_table):
        self.PT = pairing_table
        
        self.reset()
        
    def reset(self):
        
        self.team = {}
        
        self.team['A'] = {}
        self.team['B'] = {}
        
        self.team['A']['state'] = [True]*8
        self.team['B']['state'] = [True]*8
        
        for team in [self.team['A'], self.team['B']]:
            team['1_def'] = None
            team['1_atackers'] = None
            team['1_choosed_atacker'] = None
            team['2_def'] = None
            team['2_atackers'] = None
            team['2_choosed_atacker'] = None
            team['3_def'] = None
            team['3_atackers'] = None
            team['3_choosed_atacker'] = None
            team['champion'] = None
            team['rejected'] = None
            
    def get_score(self):
        if None in self.team['A'].values() or None in self.team['B'].values():
            raise ValueError('Error in (get_score) Can\'t solve score, some players are not choosen!')
        
        score = 0
    
        score += self.PT[self.team['A']['1_def'], self.team['B']['1_choosed_atacker']]
        score += self.PT[self.team['A']['1_choosed_atacker'], self.team['B']['1_def']]
        score += self.PT[self.team['A']['2_def'], self.team['B']['2_choosed_atacker']]
        score += self.PT[self.team['A']['2_choosed_atacker'], self.team['B']['2_def']]
        score += self.PT[self.team['A']['3_def'], self.team['B']['3_choosed_atacker']]
        score += self.PT[self.team['A']['3_choosed_atacker'], self.team['B']['3_def']]
        score += self.PT[self.team['A']['rejected'], self.team['B']['rejected']]
        score += self.PT[self.team['A']['champion'], self.team['B']['champion']]
        #print(score)
        return score
    
    def print_results(self):
        if None in self.team['A'].values() or None in self.team['B'].values():
            raise ValueError('Error in (print_results) can\'t print final standings - some players are not choosen!')
        
        print('A[{}] - B[{}]'.format(self.get_score(), self.PT.max_team_score - self.get_score()))
        def get_str(playerA, playerB):
            return 'A{} vs B{} - {}'.format(self.team['A'][playerA], self.team['B'][playerB], self.PT[self.team['A'][playerA], self.team['B'][playerB]])
        
        for i in [1,2,3]:
            df = '{}_def'.format(i)
            chat = '{}_choosed_atacker'.format(i)
            print(get_str(df, chat))
            print(get_str(chat, df))
        print(get_str('rejected', 'rejected'))
        print(get_str('champion', 'champion'))
        
    def get_selected(self):
        
        selectedA = [self.team['A']['1_def'],
                     self.team['A']['1_choosed_atacker'],
                     self.team['A']['2_def'],
                     self.team['A']['2_choosed_atacker'],
                     self.team['A']['3_def'],
                     self.team['A']['3_choosed_atacker'],
                     self.team['A']['rejected'],
                     self.team['A']['champion']]
        
        selectedB = [self.team['B']['1_choosed_atacker'],
                     self.team['B']['1_def'],
                     self.team['B']['2_choosed_atacker'],
                     self.team['B']['2_def'],
                     self.team['B']['3_choosed_atacker'],
                     self.team['B']['3_def'],
                     self.team['B']['rejected'],
                     self.team['B']['champion']]
        
        return selectedA, selectedB
    
    def set_defender(self, team, stage, player):
        if self.team[team]['state'][player]:
            self.team[team]['state'][player] = False
            self.team[team]['{}_def'.format(stage)] = player
        else:
            raise ValueError('Error in (set_defender) player {} of team {} already taken!'.format(team, player))
        
    def unset_defender(self, team, stage):
        name = '{}_def'.format(stage)
        defender = self.team[team][name]
        if defender is None:
            raise ValueError('Error on (unset_defender) defender has been even not selected!')
        if self.team[team]['state'][defender]:
            raise ValueError('Error on (unset_defender) defender has been already unselected!')
        self.team[team]['state'][defender] = True
        self.team[team][name] = None
        return defender # let it be
            
    def set_atackers(self, team, stage, player1, player2):
        if not self.team[team]['state'][player1]:
            raise ValueError('Error in (set_atackers) player {} of team {} already taken!'.format(team, player1))
        if not self.team[team]['state'][player2]:
            raise ValueError('Error in (set_atackers) player {} of team {} already taken!'.format(team, player2))
            
        self.team[team]['state'][player1] = False
        self.team[team]['state'][player2] = False
        self.team[team]['{}_atackers'.format(stage)] = [player1, player2]
        
    def unset_atackers(self, team, stage):
        name = '{}_atackers'.format(stage)
        atackers = self.team[team][name]
        if atackers is None:
            raise ValueError('Error on (unset_atackers) atackers have been even not selected!')
        # below doesn't work because atackers can be modified by other functions
        #for at in atackers:
            #if self.team[team]['state'][at]:
                #raise ValueError('Error on (unset_atackers) atacker has been already unselected!')
        
            
        self.team[team]['state'][atackers[0]] = True
        self.team[team]['state'][atackers[1]] = True
        self.team[team][name] = None
    
    def rev_0_1(self, val):
        if val ==  0:
            return 1
        if val == 1:
            return 0
        raise ValueError('Error in (rev_0_1) value is {} but nust be 0\\1'.format(val))
    '''
    no_atacker is 0 or 1
    '''
    def choose_atacker(self, team, stage, no_atacker):#, atackers):
        name = '{}_atackers'.format(stage)
        if self.team[team][name] is None:
            #print(self.team)
            raise ValueError('Error in (choose_atacker) atackers not selected!')
        choosed = self.team[team][name][no_atacker]
        rej = self.team[team][name][self.rev_0_1(no_atacker)]
        self.team[team]['state'][choosed] = False # maybe not needed but let it be 
        self.team[team]['{}_choosed_atacker'.format(stage)] = choosed
        if stage == 1 or stage == 2:
            self.team[team]['state'][rej] = True
        if stage == 3:
            self.team[team]['state'][rej] = False
            self.team[team]['rejected'] = rej
            # also find champions
            if sum(self.team[team]['state']) != 1:
                raise ValueError('Error in (choose_atacker) on stage 3: there are more than 1 free player!')
            last_free_player = self.team[team]['state'].index(True)
            self.team[team]['state'][last_free_player] = False
            self.team[team]['champion'] = last_free_player
            
    def unchoose_atacker(self, team, stage):
        name = '{}_choosed_atacker'.format(stage)
        choosed = self.team[team][name]
        if choosed is None:
            raise ValueError('Error in (unchoose_atacker) atacker has been even not selected')
        if self.team[team]['state'][choosed]:
            raise ValueError('Error in (unchoose_atacker) atacker has been already unselected')
        else:
            self.team[team]['state'][choosed] = True
            self.team[team][name] = None
            if stage == 3:
                # also clear champion and rejected
                champ = self.team[team]['champion']
                rej = self.team[team]['rejected']
                self.team[team]['state'][champ] = True
                self.team[team]['state'][rej] = True
                self.team[team]['champion'] = None
                self.team[team]['rejected'] = None
    
    def get_random_free_player(self, team):
        # TODO check if not all taken
        while True:
            player = np.random.randint(0,8)
            if self.team[team]['state'][player]:
                return player
                       
    def make_random_move(self, team, stage, phase):
        if phase == 'DEFENDER':
            self.set_defender(team, stage, self.get_random_free_player(team))
        elif phase == 'ATACKERS':
            while True:
                a1 = self.get_random_free_player(team)
                a2 = self.get_random_free_player(team)
                if a1 != a2:
                    break
            self.set_atackers(team, stage, a1, a2)
        elif phase == 'CHOOSE':
            self.choose_atacker(team, stage, np.random.randint(0,2))
        else:
            raise ValueError('Error in (make_random_move) unknown phase {}'.format(phase))
        
    def play_random(self):
        for stage in [1,2,3]:
            self.make_random_move('A', stage, 'DEFENDER')
            self.make_random_move('B', stage, 'DEFENDER')
            
            self.make_random_move('A', stage, 'ATACKERS')
            self.make_random_move('B', stage, 'ATACKERS')
            
            self.make_random_move('A', stage, 'CHOOSE')
            self.make_random_move('B', stage, 'CHOOSE')
        
        self.print_results()
        
    def max(self, stage, phase, alpha, beta):
        #print('A',self.team['A']['state'])
        max_score = self.PT.min_team_score
        move = None
        
        if phase == 'DEFENDER':
            for player, free in enumerate(self.team['A']['state']):
                if stage == 1:
                    print("Calculating 1 def A {}...".format(player))
                if free:
                    self.set_defender('A', stage, player)
                    score, _ = self.min(stage, phase, alpha, beta)
                    if score > max_score:
                        max_score = score
                        move = player
                    self.unset_defender('A', stage)
                    
                    if max_score >= beta:
                        #print('beta')
                        return max_score, move
                    
                    if max_score > alpha:
                        alpha = max_score
                        
        elif phase == 'ATACKERS':
            for player1, free1 in enumerate(self.team['A']['state']):
                for player2, free2 in enumerate(self.team['A']['state']):
                    if player1 > player2 and free1 and free2:
                        self.set_atackers('A', stage, player1, player2)
                        score, _ = self.min(stage, phase, alpha, beta)
                        if score > max_score:
                            max_score = score
                            move = [player1, player2]
                        self.unset_atackers('A', stage)
                        
                        if max_score >= beta:
                            #print('beta')
                            return max_score, move
                    
                        if max_score > alpha:
                            alpha = max_score
                            
        elif phase == 'CHOOSE':
            for choose in [0, 1]:
                self.choose_atacker('B', stage, choose)#sure B
                score, _ = self.min(stage, phase, alpha, beta)
                if score > max_score:
                    max_score = score
                    move = self.team['B']['{}_atackers'.format(stage)][choose]
                self.unchoose_atacker('B', stage)
                
                if max_score >= beta:
                    #print('beta')
                    return max_score, move
                    
                if max_score > alpha:
                    alpha = max_score
        else:
            raise ValueError('Error in (max) unknown phase {}'.format(phase))
        return max_score, move
        
    def min(self, stage, phase, alpha, beta):
        #print(self.team)
        #print('B',self.team['B']['state'])
        min_score = self.PT.max_team_score
        move = None
        
        if phase == 'DEFENDER':
            for player, free in enumerate(self.team['B']['state']):
                if stage == 1:
                    print("Calculating 1 def B {}...".format(player))
                if free:
                    self.set_defender('B', stage, player)
                    score, _ = self.max(stage, 'ATACKERS', alpha, beta)
                    if score < min_score:
                        min_score = score
                        move = player
                    self.unset_defender('B', stage)
                    
                    if min_score <= alpha:
                        #print('alpha')
                        return min_score, move
                    
                    if min_score < beta:
                        beta = min_score
                    
        elif phase == 'ATACKERS':
            for player1, free1 in enumerate(self.team['B']['state']):
                for player2, free2 in enumerate(self.team['B']['state']):
                    if player1 > player2 and free1 and free2:
                        self.set_atackers('B', stage, player1, player2)
                        score, _ = self.max(stage, 'CHOOSE', alpha, beta)
                        if score < min_score:
                            min_score = score
                            move = [player1, player2]
                        self.unset_atackers('B', stage)
                        
                        if min_score <= alpha:
                            #print('alpha')
                            return min_score, move
                    
                        if min_score < beta:
                            beta = min_score
        elif phase == 'CHOOSE':
            for choose in [0, 1]:
                self.choose_atacker('A', stage, choose)#sure B
                if stage == 1 or stage == 2:
                    score, _ = self.max(stage+1, 'DEFENDER', alpha, beta)
                elif stage == 3:
                    score = self.get_score()
                else:
                    raise ValueError('Error in (min) stage can be only 1,2,3')
                    
                if score < min_score:
                    min_score = score
                    move = self.team['A']['{}_atackers'.format(stage)][choose]
                self.unchoose_atacker('A', stage)
                
                if min_score <= alpha:
                    #print('alpha')
                    return min_score, move
                    
                if min_score < beta:
                    beta = min_score
        else:
            raise ValueError('Error in (min) unknown phase {}'.format(phase))
        return min_score, move
    
    def play_optimal(self):
        score, player = self.max(1,'DEFENDER', self.PT.min_team_score, self.PT.max_team_score)
        print(score, player)
        #for stage in [1,2,3]:
            #self.max(stage, 'DEFENDER')
            #self.min(stage, 'DEFENDER')
            
            #self.make_random_move('A', stage, 'ATACKERS')
            #self.make_random_move('B', stage, 'ATACKERS')
            
            #self.make_random_move('A', stage, 'CHOOSE')
            #self.make_random_move('B', stage, 'CHOOSE')
        
        #self.print_results()
        

if __name__ == '__main__' :
    pt = PairingTable(np.random.randint(0,21,(8,8)))
    
    print(pt)
    pg8 = PairingGame8(pt)
    #pg8.get_score()
    
    #pg8.set_defender('A', 1, 1)
    #pg8.set_atackers('A', 1, 3, 2)
    #pg8.choose_atacker('A',1, 1)
    
    #pg8.unchoose_atacker('A',1)
    #pg8.unset_atackers('A',1)
    #pg8.unset_defender('A',1)
    
    #print(pg8.team['A'])
    tock = time.time()
    pg8.play_optimal()
    tick = time.time()
    print("Elapsed time {} min".format((tick-tock)/60))
    
    #selA, selB = pg8.get_selected()
    
    #pt.plot(selA, selB)
    
    #plt.show()
