# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 17:25:05 2025

@author: 79165
"""
import PairingGame
import MCTS_solver
from functools import partial
import GUI_images
#import GUI_inh
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    
    scores, tables = PairingGame.generate_input_data(8, 3)
    #print(scores)
    game = PairingGame.PairingGame(8, scores, tables)
    
    # test with 1-2-2-1-2-1-2-2
    steps_actions = [# stage 1
                     partial(game.get_all_set_defender_actions, team = 0),
                     partial(game.get_all_set_defender_actions, team = 1),
                     partial(game.get_all_set_attacker_actions, team = 0),
                     partial(game.get_all_set_attacker_actions, team = 1),
                     partial(game.get_all_choose_atacker_action_and_return_rej, team = 0),
                     partial(game.get_all_choose_atacker_action_and_return_rej, team = 1),
                     partial(game.get_all_set_table_for_defender, team = 0),
                     partial(game.get_all_set_table_for_defender, team = 1),
                     # stage 2
                     partial(game.get_all_set_defender_actions, team = 0),
                     partial(game.get_all_set_defender_actions, team = 1),
                     partial(game.get_all_set_attacker_actions, team = 0),
                     partial(game.get_all_set_attacker_actions, team = 1),
                     partial(game.get_all_choose_atacker_action_and_return_rej, team = 0),
                     partial(game.get_all_choose_atacker_action_and_return_rej, team = 1),
                     partial(game.get_all_set_table_for_defender, team = 1),
                     partial(game.get_all_set_table_for_defender, team = 0),
                     # final stage
                     partial(game.get_all_set_defender_actions, team = 0),
                     partial(game.get_all_set_defender_actions, team = 1),
                     partial(game.get_all_set_attacker_actions, team = 0),
                     partial(game.get_all_set_attacker_actions, team = 1),
                     partial(game.get_all_choose_atacker_action, team = 0),
                     partial(game.get_all_choose_atacker_action, team = 1),
                     partial(game.get_all_set_table_for_defender, team = 1),
                     partial(game.get_all_set_table_for_defender, team = 0),
                     game.get_all_finalize_game_actions_champ_with_champ
                     ]
    
    
    solver = MCTS_solver.MCTS_solver(game, steps_actions)
    
    app = QApplication(sys.argv)


    window = GUI_images.MainWindow(solver)
    window.setWindowTitle("Fest pairing game")
    window.show()
    sys.exit(app.exec_())
    
    #best_action = solver.root.best_action(500)
    #print(best_action.state)