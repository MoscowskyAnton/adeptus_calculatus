# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 17:25:05 2025

@author: 79165
"""
import PairingGame
import MCTS_solver
from functools import partial


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
    
    
    solver = MCTS_solver.MCTS_solver(game, steps_actions)
    
    best_action = solver.root.best_action()
    print(best_action.state)
    print(best_action.parent_action)