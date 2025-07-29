# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 12:32:27 2025

@author: Moskovsky_AD
"""

import numpy as np
from collections import defaultdict
from itertools import product
import PairingGame

class SM_MCTS_node:
    def __init__(self, state, solver = None, game_step_no = 0, parent = None):
        self.state = state        
        self.parent = None
        self.solver = solver
        self.game_step_no = game_step_no
        
        self.children = {}  # joint_action -> child_node
        self.visits = 0
        self.value = 0.0
        self.joint_action_stats = defaultdict(lambda: {'visits': 0, 'value': 0.0})
        
        self.simultaneous_node = False
        
        #self.untried_joint_actions = self._generate_joint_actions()
        self.action, self.untried_params = self._generate_joint_actions(self.game_step_no, self.state)
        
        
    def born_child(self, new_state):
        child = SM_MCTS_node(new_state, self.solver, self.game_step_no + 1, self)
        return child

    def _generate_joint_actions(self, game_step_no, state):        
        # Generate all joint actions         
                
        action  = self.solver.game_steps[game_step_no]['action']
        if self.solver.game_steps[game_step_no]['team'] < 2:
            # alone actions
            self.simultaneous_node = False
            return action(team = self.solver.game_steps[game_step_no]['team'], state = state)
                        
        elif self.solver.game_steps[game_step_no]['team'] == 2:
            # simultaneous action
            self.simultaneous_node = True        
            
            a0, p0 = action(team = 0, state = state)
            a1, p1 = action(team = 1, state = state)
            if a0 != a1:
                raise ValueError("Different action alarm!")
            return a0, list(product(p0, p1))
                    
        else:
            raise ValueError("WHAT? How possible more that 2 action simultaneously?!")
                    

    def apply_joint_action(self, joint_param):
        next_state = self.state.copy()
        if self.simultaneous_node:
        #if self.solver()
            self.action(state = next_state, **joint_param[0])
            self.action(state = next_state, **joint_param[1])
        else:
            self.action(state = next_state, **joint_param)
        return next_state


    def is_fully_expanded(self):
        return len(self.untried_params) == 0
    
    

    def expand(self):
        joint_param = self.untried_params.pop()
        next_state = self.apply_joint_action(joint_param)
        
        child_node = self.born_child(next_state)
        self.children[joint_param] = child_node
        return child_node, joint_param


    def select_joint_action(self, c_param=1.4):
        # Implement selection with exploration-exploitation balance (e.g., UCT adapted for joint actions)
        def uct(joint_action):
            stats = self.joint_action_stats[joint_action]
            if stats['visits'] == 0:
                return float('inf')
            exploitation = stats['value'] / stats['visits']
            exploration = c_param * ( (2 * np.log(self.visits)) / stats['visits'] )**0.5
            return exploitation + exploration
        return max(self.children.keys(), key=uct)

    def update_stats(self, joint_action, reward):
        stats = self.joint_action_stats[joint_action]
        stats['visits'] += 1
        stats['value'] += reward
        self.visits += 1
        

class SM_MCTS_solver(object):
    
    def __init__(self, game, game_steps):
        self.game = game
        self.game_steps = game_steps
        
        self.root = SM_MCTS_node(state = game.initial_state, solver = self)
            

    def run(self, root = None, iterations=1000):
        
        if root is None:
            root = self.root
            
        for _ in range(iterations):
            node = root
            path = []
    
            # Selection & Expansion
            while not node.state.is_game_over():
                if not node.is_fully_expanded():
                    node, joint_action = node.expand()
                    path.append((node, joint_action))
                    break
                else:
                    joint_action = node.select_joint_action()
                    node = node.children[joint_action]
                    path.append((node, joint_action))
    
            # Simulation
            reward = self.rollout(node)
    
            # Backpropagation (from root team's perspective)
            for n, joint_action in reversed(path):
                n.update_stats(joint_action, reward)
    
        # Choose best joint action at root
        best_action = max(root.joint_action_stats.items(), key=lambda x: x[1]['value']/x[1]['visits'])[0]
        return best_action
    
    def rollout(self, node):
        # Simulate random or heuristic joint actions until terminal state
        current_node = node
        while not current_node.state.is_game_over():
            
            next_state = current_node.apply_joint_action(np.random.choice(current_node.untried_params))
            current_node = current_node.born_child(next_state)
        return current_node.state.get_score()
    
if __name__ == '__main__':
    
    N_players = 4
    
    scores, tables = PairingGame.generate_input_data(N_players = N_players, N_table_types = 3)
    
    game = PairingGame.PairingGame(N_players, scores, tables)
    
    #table_choose = [0, 1, 1, 0, 1, 0, 1, 1]
            
    steps = [## defenders 
             {"team": 2, "action": game.get_all_set_defender_actions},
             ## atackers
             {"team": 2, "action": game.get_all_set_attacker_actions},             
             ## choose
             {"team": 2, "action": game.get_all_choose_atacker_action},
             ## tables for defs
             {"team": 0, "action": game.get_all_set_table_for_defender},
             {"team": 1, "action": game.get_all_set_table_for_defender},
             ## final
             {"team": 1, "action": game.get_all_finalize_game_actions_champ_with_champ}
             ]
    
    solver = SM_MCTS_solver(game = game, game_steps = steps)
    
    solver.run()
    
    