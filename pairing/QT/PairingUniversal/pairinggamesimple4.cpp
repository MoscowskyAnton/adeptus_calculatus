#include "pairinggamesimple4.h"

namespace pgu_simple4 {

    SetDefender::SetDefender(std::string name, pgu::PairingGameUniversal* parent_game, bool team) : GameStep(name, parent_game, team){

    }

    int SetDefender::make(int alpha, int beta){
        const std::string role = "DEF";
        pgu::TeamState* ts;
        team ? ts = parent_game->teamA : ts = parent_game->teamB;
        int new_score;
        team ? new_score = -1000 : new_score = 1000; // TODO init correctly
        for( int i = 0; i < ts->get_n_players(); i++){
            if(ts->is_player_free(i)){
                ts->set_role(role, i);
                int score = parent_game->next_step()->make(alpha, beta);
                ts->remove_role(role);
                if(team){
                    if(new_score > score)
                        new_score = score;
                    if(proceed_alpha_beta_max(score, new_score, alpha, beta) && alpha_beta_prune)
                        break;
                }
                else{
                    if(new_score < score)
                        new_score = score;
                    if(proceed_alpha_beta_min(score, new_score, alpha, beta) && alpha_beta_prune)
                        break;
                }
            }
        }
        return new_score;
    }


}
