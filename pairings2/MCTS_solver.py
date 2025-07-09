# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 11:25:42 2025

@author: 79165
"""

import PairingGame
import numpy as np
#from collections import defaultdict
from functools import partial
import copy

class MCTS_node(object):
    def __init__(self, solver, state, parent = None, parent_action = None):
        
        self.solver = solver
        if parent is None:
            self.step = 0
        else:
            self.step = parent.step + 1
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        
        self._results = []
        #self._untried_actions = None
        self._action, self._params = self.get_legal_actions()
        self._untried_params = copy.deepcopy(self._params)
        
    def get_legal_actions(self, step = None, state = None):
        if step is None:
            step = self.step
        if state is None:
            state = self.state
        action, params = self.solver.step_actions[step](state = state)
        if len(params) == 0:
            raise ValueError(f"Len of action params is 0, step = {step}, state = {state}")
        return action, params
        
    # def untried_actions(self):
    #     self._untried_actions = self.get_legal_actions()
    #     return self._untried_actions
    
    def expand(self):
        param = self._untried_params.pop(0)
        
        next_state = self.move(self._action, param)
        
        child_node = MCTS_node(self.solver, next_state, parent=self, parent_action=param)
    
        self.children.append(child_node)
        return child_node
        
    def is_terminal_node(self):
        return self.step == len(self.solver.step_actions)-1
    
    def move(self, action, param):
        next_state = self.state.copy()
        action(state = next_state, **param)
        return next_state
    
    def rollout(self):
        current_rollout_state = self.state.copy()
        current_rollout_step = self.step
        while not current_rollout_state.is_game_over():
            
            action, possible_moves = self.get_legal_actions(step = current_rollout_step, state = current_rollout_state)
            
            move = self.rollout_policy(possible_moves)
            action(state = current_rollout_state, **move)
            current_rollout_step += 1
        #print(current_rollout_state.formed_pairs)
        score = self.solver.game.get_score(current_rollout_state) 
        #print(score)
        return score
    
    def backpropagate(self, score):
        self._number_of_visits += 1.
        self._results.append(score)
        if self.parent:
            self.parent.backpropagate(score)
            
    def is_fully_expanded(self):
        return len(self._untried_params) == 0
    
    def best_child_no(self, c_param=45):
        
        choices_weights = [np.mean(c._results) + c_param * np.sqrt((2 * np.log(self._number_of_visits)) / c._number_of_visits) for c in self.children]
        return np.argmax(choices_weights)
    
    def best_child(self, c_param=45):
        return self.children[self.best_child_no(c_param)]
    
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
    
    def best_action(self, simulation_no = 100):
        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
	
        return self.best_child(c_param=0.)

class MCTS_solver(PairingGame.Solver):
    
    def __init__(self, game, step_actions = []):
        self.game = game
        self.step_actions = step_actions
        
        self.root = MCTS_node(self, self.game.initial_state)
        
        
if __name__ == '__main__':
    
    scores, tables = PairingGame.generate_input_data(4, 3)
    #print(scores)
    game = PairingGame.PairingGame(4, scores, tables)
    
    # test with 1-2-2-2
    steps_actions = [partial(game.get_all_set_defender_actions, team = 0),
                     partial(game.get_all_set_defender_actions, team = 1),
                     partial(game.get_all_set_attacker_actions, team = 0),
                     partial(game.get_all_set_attacker_actions, team = 1),
                     partial(game.get_all_choose_atacker_action, team = 0),
                     partial(game.get_all_choose_atacker_action, team = 1),
                     partial(game.get_all_set_table_for_defender, team = 0),
                     partial(game.get_all_set_table_for_defender, team = 1),
                     #partial(game.get_all_set_defender_actions, team = 0),
                     #partial(game.get_all_set_defender_actions, team = 1),
                     #partial(game.get_all_set_attacker_actions, team = 0),
                     #partial(game.get_all_set_attacker_actions, team = 1),
                     #partial(game.get_all_choose_atacker_action, team = 0),
                     #partial(game.get_all_choose_atacker_action, team = 1),
                     #partial(game.get_all_set_table_for_defender, team = 1),
                     #partial(game.get_all_set_table_for_defender, team = 0),
                     game.get_all_finalize_game_actions_champ_with_champ
                     ]
    
    
    solver = MCTS_solver(game, steps_actions)
    
    best_action = solver.root.best_action()
    print(best_action.state)
    
    