#include <iostream>
#include "pairinggameuniversal.h"

#define N_PLAYERS 8

int main()
{
    std::vector<std::string> player_roles = {"DEF1", "C_ATCK1_1", "C_ATCK1_2", "ATCK1", "DEF2", "C_ATCK2_1", "C_ATCK2_2", "ATCK2", "DEF3", "C_ATCK3_1", "C_ATCK3_2", "ATCK3", "REJ", "CHAMP"};
    std::vector<std::string> sequence = {""};
    std::map<std::string, bool> rolloffs;

    /*
    pgu::TeamState teamA(N_PLAYERS, player_roles);
    teamA.set_role("DEF1",1);
    printf("%s",teamA.__str().c_str());
    int player_check_id = 1;
    printf("Player %i %s\n", player_check_id, teamA.is_player_free(player_check_id) ? "is free" : "isn't free");
    teamA.remove_role("DEF2");
    */

    pgu::GameRules game_rules(N_PLAYERS, player_roles, sequence, rolloffs);
    pgu::PairingGameUniversal pairing_game (game_rules);

    return 0;
}
