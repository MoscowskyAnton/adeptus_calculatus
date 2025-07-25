# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 23:07:32 2025

@author: 79165
"""
import numpy as np
import copy
from functools import partial


class PairingGameState(object):
    
    FREE = 'F'
    TAKEN = 'T'
    DEF = 'D'
    ATACK = 'A'
    REJ = 'R'
    
    def __init__(self, N_players):
        # [(playerA, playerB, table#)]
        self.formed_pairs = []
        self.N_players = N_players
        
        self.players_status = [[], []]
        for p in range(N_players):
            self.players_status[0].append('F')
            self.players_status[1].append('F')
            
        self.tables_status = ['F'] * N_players
        
    def __str__(self):
        team0 = ' '.join(self.players_status[0])
        team1 = ' '.join(self.players_status[1])
        table = ' '.join(self.tables_status)
        return f"T0: {team0}\nT1: {team1}\nTB: {table}"
    
    def copy(self):
        return copy.deepcopy(self)
        
    def is_game_over(self):
        return len(self.formed_pairs) == self.N_players
        
    def get_free_players(self, team):
        return self.get_status_players(team, 'F')
    
    def get_status_players(self, team, status):
        return [i for i, s in enumerate(self.players_status[team]) if s == status]
    
    def get_free_tables(self):
        return [i for i, s in enumerate(self.tables_status) if s == 'F']
        

class PairingGame(object):
    """
    scores - N_players * N_players * table_types
    tables - N_players * N_players (of table types)
    """
    def __init__(self, N_players, scores, tables):
        self.N_players = N_players
        self.scores = scores
        self.tables = tables
        
        self.initial_state = PairingGameState(self.N_players)
    
        
        
    def get_available_atackers_pairs(self, team, state):
        free = state.get_free_players(team)
        atackers = []
        for i, a1 in enumerate(free):
            for a2 in free[i+1:]:
                atackers.append((a1, a2))
        return atackers
    
    def set_atackers_pair(self, team, state, atackers_pair):
        for a in atackers_pair:
            if state.players_status[team][a] != 'F':
                raise ValueError(f"Atacker {a} is already taken for team {team}, status = {state.players_status[team][a]}")
        state.players_status[team][atackers_pair[0]] = 'A'
        state.players_status[team][atackers_pair[1]] = 'A'
        

    """
    choosed = player id
    """
    def choose_atacker(self, team, state, choosed_atacker):
        # if choosed_atacker not in [0, 1]:
            # raise ValueError(f"choose_atacker must take values 0\1, not {choosed_atacker}")
        #print(state)
        atackers = state.get_status_players(team-1, 'A') #other team!
        if len(atackers) != 2:
            raise ValueError(f"Atackers count must be 2, not {len(atackers)}")
        if choosed_atacker not in atackers:
            raise ValueError(f"No atacker {choosed_atacker} between real atackers {atackers}")
        
        atackers.remove(choosed_atacker)
        rej = atackers[0]
        
        state.players_status[team-1][rej] = 'R' # just mark other as rejected
        #return     
        
    def set_table_for_defender(self, team, state, table_no):
        state.tables_status[table_no] = 'T'
        
        defender = state.get_status_players(team, 'D')
        if len(defender) != 1:
            raise ValueError(f"Must be only 1 defender on this step, not {len(defender)}")
        defender = defender[0]
        
        atacker = state.get_status_players(team-1, 'A')
        if len(atacker) != 1:
            raise ValueError(f"Must be only 1 atacker on this step, not {len(atacker)}")
        atacker = atacker[0]
        
        state.players_status[team][defender] = 'T'
        state.players_status[team-1][atacker] = 'T'
        
        if team == 0:
            state.formed_pairs.append((defender, atacker, table_no))
        else:
            state.formed_pairs.append((atacker, defender, table_no))
            
    def return_rej_to_deck(self, team, state):
        rej = state.get_status_players(team, 'R')
        if len(rej) != 1:
            raise ValueError(f"More than 1 rejected {len(rej)} - something get wrong")
        rej = rej[0]
        state.players_status[team][rej] = 'F'
        
    """
    table_for_rej - table ID!
    team is for compability
    """
    def finalize_game_champ_with_champ(self, state, table_for_rej, team):
        rej0 = state.get_status_players(0, 'R')[0]
        rej1 = state.get_status_players(1, 'R')[0]
        
        champ0 = state.get_status_players(0, 'F')[0]
        champ1 = state.get_status_players(1, 'F')[0]
        
        free_tables = state.get_free_tables()
        if len(free_tables) != 2:
            raise ValueError(f"Len of free tables must be 2, not {len(free_tables)}!")
        if not table_for_rej in free_tables:
            raise ValueError(f"No table {table_for_rej} between free tables {free_tables}")
        
        #print(free_tables)
        free_tables.remove(table_for_rej)
        champ_table = free_tables[0]
        #print(champ_table)
        state.formed_pairs.append((rej0, rej1, table_for_rej))
        state.formed_pairs.append((champ0, champ1, champ_table))

    def get_available_defenders(self, team, state):
        return state.get_free_players(team)
    
    def set_defender(self, team, state, defender):
        if state.players_status[team][defender] != 'F':
            raise ValueError(f"Defender {defender} is already taken for team {team}, status = {state.players_status[team][defender]}")
        state.players_status[team][defender] = 'D'
        #return True
        
    def get_score(self, state):
        if len(state.formed_pairs) != self.N_players:
            raise ValueError(f"Not all pairs are formed (only {len(state.formed_pairs)} of {self.N_players})")
        score = 0
        for (a, b, t) in state.formed_pairs:
            t_type = self.tables[a, t]
            score += self.scores[a, b, t_type]
        return score
    
    ### actions for solvers
    
    def get_all_set_defender_actions(self, state, team):
        possible_defenders = self.get_available_defenders(team, state)
        
        #action = partial(self.set_defender, team = team) 
        action = self.set_defender
        params = [{"defender": d, "team": team} for d in possible_defenders]
        return action, params
    
    def get_all_set_table_for_defender(self, state, team):
        tables = state.get_free_tables()
        #action = partial(self.set_table_for_defender, team = team)
        action = self.set_table_for_defender
        params = [{"table_no": table_no, "team": team} for table_no in tables]
        return action, params
    
    def get_all_set_attacker_actions(self, state, team):
        atack_pairs = self.get_available_atackers_pairs(team, state)
        
        #action = partial(self.set_atackers_pair, team = team)
        action = self.set_atackers_pair
        params = [{"atackers_pair": pair, "team": team} for pair in atack_pairs]
        return action, params
    
    def get_all_choose_atacker_action(self, state, team):
        #action = partial(self.choose_atacker, team = team)
        #print(state)
        atackers = state.get_status_players(team-1, 'A')
        action = self.choose_atacker
        params = [{"choosed_atacker": choosed, "team": team} for choosed in atackers]
        return action, params
    
    def get_all_choose_atacker_action_and_return_rej(self, state, team):
        
        def choose_and_return_rej(state, team, choosed_atacker):
            self.choose_atacker(team, state, choosed_atacker)
            self.return_rej_to_deck(team-1, state)
        
        #action = partial(choose_and_return_rej, team = team)
        action = choose_and_return_rej
        atackers = state.get_status_players(team-1, 'A')
        params = [{"choosed_atacker": choosed, "team": team} for choosed in atackers]
        
        return action, params
    
    def get_all_finalize_game_actions_champ_with_champ(self, state, team):
        action = self.finalize_game_champ_with_champ
        free_tables = state.get_free_tables()
        params = [{"table_for_rej": t, "team": team} for t in free_tables]
        return action, params
    
    
    
def generate_input_data(N_players, N_table_types, min_max = (-2, 2)):
    scores = np.random.randint(min_max[0], min_max[1]+1, size = (N_players, N_players, N_table_types))
    tables = np.random.randint(0, N_table_types, size = (N_players, N_players) ) 
    return scores, tables
    
class Solver(object):
    def __init__(self):
        pass
    
    def solve(self, game):
        raise NotImplementedError("solve function not implemented!")

if __name__ == '__main__':
    
    scores, tables = generate_input_data(4, 3)
    print(scores, tables)
    four_game = PairingGame(4, scores, tables)
    state = four_game.initial_state
    print(state)
    
    print(four_game.get_all_set_defender_actions(state, 0))
    
    print(four_game.get_available_defenders(0, state))
    four_game.set_defender(0, state, 1)
    four_game.set_defender(1, state, 2)
    atacker_pairs = four_game.get_available_atackers_pairs(1, state)
    print(atacker_pairs)
    four_game.set_atackers_pair(1, state, atacker_pairs[1])
    print(state)
    