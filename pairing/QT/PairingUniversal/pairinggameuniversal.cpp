#include "pairinggameuniversal.h"
#include <algorithm>
#include <stdexcept>

#define DEBUG_STUFF

namespace pgu {

    TeamState::TeamState(int n_players, const std::vector<std::string> &player_roles){
        this->n_players = n_players;
        for (auto const & role : player_roles){
            players[role] = -1;
        }
    }

    std::string TeamState::__str(){
        std::string str = "";
        for (std::pair<const std::string,int>& player: players) {
            str += (player.first + ": " + std::to_string(player.second) + "\n");
        }
        return str;
    }

    bool TeamState::is_player_free(int player_id){
#ifdef DEBUG_STUFF
        if(player_id < 0 || player_id >= n_players)
            throw std::out_of_range("player_id incorrect value "+std::to_string(player_id));
#endif
        return std::find_if(players.begin(), players.end(), [player_id](const auto& mo) {return mo.second == player_id; }) == players.end();
    }

    void TeamState::set_role(std::string role, int player_id){
#ifdef DEBUG_STUFF
        if (!players.count(role))
            throw std::logic_error("no such role "+role);
        if (players[role] != -1)
            throw std::logic_error(role + " already taken");
        if(player_id < 0 || player_id >= n_players)
            throw std::out_of_range("player_id incorrect value "+std::to_string(player_id));
#endif
        players[role] = player_id;
    }

    void TeamState::remove_role(std::string role){
#ifdef DEBUG_STUFF
        if (!players.count(role))
            throw std::logic_error("no such role "+role);
        if (players[role] == -1)
            throw std::logic_error(role + " is already unset");
#endif
        players[role] = -1;
    }

    GameRules::GameRules(int n_players, const std::vector<std::string> &player_roles, const std::vector<std::string> &sequence, const std::map<std::string, bool> &rolloffs){
        this->n_players = n_players;
        this->player_roles = player_roles;
        this->sequence = sequence;
    }

    PairingGameUniversal::PairingGameUniversal(const GameRules& game_rules){
        this->game_rules = game_rules;
        teamA = new TeamState(game_rules.n_players, game_rules.player_roles);
        teamB = new TeamState(game_rules.n_players, game_rules.player_roles);
    }

}
