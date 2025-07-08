# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 19:52:08 2025

@author: 79165
"""

import GUI_images

class MainWindow(GUI_images.MainWindow):
    
    def __init__(self, solver):
        self.solver = solver
        
        dropdown_options_list = [[] for _ in range(self.solver.game.N_players)]
        defs_ids = self.solver.game.get_available_defenders(state = self.solver.root.state, team = 0)
        dropdown_options_list[0] = [str(id) for id in defs_ids]
        
        extra_texts_list = [""] * self.solver.game.N_players
        
        self.solver.step_actions[0]
        
        right_texts = [f"Right block text {i}" for i in range(8)]


        right_images = [
            "C:/Users/79165/YandexDisk/Fest/H&A_F1.png",  # Replace with actual image paths
            "C:/Users/79165/YandexDisk/Fest/CoB_F2.png",
            "C:/Users/79165/YandexDisk/Fest/S&D_CA1_FEST.png",
            "C:/Users/79165/YandexDisk/Fest/TP_CA8_FEST.png",
            "C:/Users/79165/YandexDisk/Fest/H&A_CA7.png",
            "C:/Users/79165/YandexDisk/Fest/CoB_CA6.png",
            "C:/Users/79165/YandexDisk/Fest/SA_CA3.png",
            "C:/Users/79165/YandexDisk/Fest/DoW_CA5.png",
            ]
        
        super().__init__(dropdown_options_list, extra_texts_list, right_texts, right_images)