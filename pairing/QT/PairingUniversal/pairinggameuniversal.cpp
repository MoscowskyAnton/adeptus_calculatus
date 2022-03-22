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
        if(player_id < 0 || player_id >= (int)n_players)
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

    GameStep::GameStep(std::string name, PairingGameUniversal* parent_game, bool team){
        this->name = name;
        this->parent_game = parent_game;
        this->team = team;
    }

    bool GameStep::proceed_alpha_beta_max(int score, int &new_score, int &alpha, int &beta){
        if(score >= beta){
            return true;
        }
        if(score > alpha){
            alpha = score;
        }
        return false;
    }

    bool GameStep::proceed_alpha_beta_min(int score, int &new_score, int &alpha, int &beta){
        if(score <= alpha){
            return true;
        }
        if(score < beta){
            beta = score;
        }
        return false;
    }

    PairingGameUniversal::PairingGameUniversal(size_t n_players, const std::vector<std::string> &player_roles, const std::vector<GameStep*> &sequence, const std::map<std::string, bool> &rolloffs){
        this->n_players = n_players;
        this->player_roles = player_roles;
        this->sequence = sequence;

        teamA = new TeamState(n_players, player_roles);
        teamB = new TeamState(n_players, player_roles);
    }

    GameStep *PairingGameUniversal::next_step(){
        return sequence[current_step+1];
    }

}
