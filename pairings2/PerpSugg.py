# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 15:01:01 2025

@author: 79165
"""

import random
from collections import defaultdict
from itertools import product
import numpy as np

class PairingGameState:
    def __init__(self, team1_pool, team2_pool, assigned_pairs, tables_assigned,
                 stage=1, step=1, winner_team=1, first_table_picker=1):
        self.team1_pool = team1_pool  # set/list of player IDs
        self.team2_pool = team2_pool
        self.assigned_pairs = assigned_pairs  # dict: table -> (player1, player2)
        self.tables_assigned = tables_assigned  # set of assigned tables
        self.stage = stage
        self.step = step
        self.winner_team = winner_team
        self.first_table_picker = first_table_picker
        # Additional state variables as needed
    
    def get_legal_actions(self, team):
        # Return list of legal moves for the given team at current step
        # e.g. select defender, select attackers, select attacker to play, select table
        # This depends on the current step and the players/tables available
        pass

    def apply_joint_action(self, joint_action):
        # joint_action: tuple (team1_action, team2_action)
        # Apply both teams' actions simultaneously, update pools, pairs, tables, stage, step
        # Return new PairingGameState instance
        pass

    def is_terminal(self):
        # Return True if all stages completed and all players assigned
        pass

    def get_score(self):
        # Compute total score from assigned_pairs and tables using your 8x8x8 score array
        pass

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = {}  # joint_action -> child_node
        self.visits = 0
        self.value = 0.0
        self.joint_action_stats = defaultdict(lambda: {'visits': 0, 'value': 0.0})
        self.untried_joint_actions = self._generate_joint_actions()

    def _generate_joint_actions(self):
        # Generate all joint actions (team1_action, team2_action) from legal moves
        team1_actions = self.state.get_legal_actions(team=1)
        team2_actions = self.state.get_legal_actions(team=2)
        return list(product(team1_actions, team2_actions))

    def is_fully_expanded(self):
        return len(self.untried_joint_actions) == 0

    def expand(self):
        joint_action = self.untried_joint_actions.pop()
        next_state = self.state.apply_joint_action(joint_action)
        child_node = MCTSNode(next_state, parent=self)
        self.children[joint_action] = child_node
        return child_node, joint_action

    def select_joint_action(self, c_param=1.4):
        # Implement selection with exploration-exploitation balance (e.g., UCT adapted for joint actions)
        def uct(joint_action):
            stats = self.joint_action_stats[joint_action]
            if stats['visits'] == 0:
                return float('inf')
            exploitation = stats['value'] / stats['visits']
            exploration = c_param * ( (2 * math.log(self.visits)) / stats['visits'] )**0.5
            return exploitation + exploration
        return max(self.children.keys(), key=uct)

    def update_stats(self, joint_action, reward):
        stats = self.joint_action_stats[joint_action]
        stats['visits'] += 1
        stats['value'] += reward
        self.visits += 1

def rollout(state):
    # Simulate random or heuristic joint actions until terminal state
    current_state = state
    while not current_state.is_terminal():
        team1_actions = current_state.get_legal_actions(1)
        team2_actions = current_state.get_legal_actions(2)
        action1 = random.choice(team1_actions)
        action2 = random.choice(team2_actions)
        current_state = current_state.apply_joint_action((action1, action2))
    return current_state.get_score()

def mcts(root_state, iterations=1000):
    root = MCTSNode(root_state)
    for _ in range(iterations):
        node = root
        path = []

        # Selection & Expansion
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                node, joint_action = node.expand()
                path.append((node, joint_action))
                break
            else:
                joint_action = node.select_joint_action()
                node = node.children[joint_action]
                path.append((node, joint_action))

        # Simulation
        reward = rollout(node.state)

        # Backpropagation (from root team's perspective)
        for n, joint_action in reversed(path):
            n.update_stats(joint_action, reward)

    # Choose best joint action at root
    best_action = max(root.joint_action_stats.items(), key=lambda x: x[1]['value']/x[1]['visits'])[0]
    return best_action

