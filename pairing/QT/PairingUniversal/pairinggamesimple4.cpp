#include "pairinggamesimple4.h"
#include <algorithm>

namespace pgu_simple4 {   

SetDefender::SetDefender(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team) : GameStep(name, parent_game, maximizing_team, affected_team, {"DEF"}){}

    std::vector<std::pair<int, std::vector<int>>> SetDefender::make(int alpha, int beta){
        pgu::TeamState* ts;
        affected_team == pgu::TEAM_A ? ts = parent_game->teamA : ts = parent_game->teamB;

        std::vector<std::pair<int, std::vector<int>>> scores;
        int score;
        for( int i = 0; i < ts->get_n_players(); i++){
            if(ts->is_player_free(i)){
                ts->set_role(roles[0], i);

                score = parent_game->next_step()->make(alpha, beta).begin()->first;
                std::vector<int> selected_player = {i};
                scores.push_back({score,{selected_player}});
                ts->remove_role(roles[0]);
                parent_game->desrease_step();
                if(maximizing_team == pgu::TEAM_A){
                    if(proceed_alpha_beta_max(score, alpha, beta) && alpha_beta_prune)
                        break;
                }
                else{                    
                    if(proceed_alpha_beta_min(score, alpha, beta) && alpha_beta_prune)
                        break;
                }
            }
        }
        if(maximizing_team == pgu::TEAM_A)
            std::sort(scores.rbegin(), scores.rend());
        else
            std::sort(scores.begin(), scores.end());
        return scores;
    }

    SetAtackers::SetAtackers(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team) : GameStep(name, parent_game, maximizing_team, affected_team, {"C_ATCK1", "C_ATCK2"}){}

    std::vector<std::pair<int, std::vector<int>>> SetAtackers::make(int alpha, int beta){
        pgu::TeamState* ts;
        affected_team == pgu::TEAM_A  ? ts = parent_game->teamA : ts = parent_game->teamB;

        int score;
        std::vector<std::pair<int, std::vector<int>>> scores;

        for( int i = 0; i < ts->get_n_players(); i++){
            if(ts->is_player_free(i)){
                for( int j = i+1; j < ts->get_n_players(); j++){
                    if(ts->is_player_free(j)){
                        ts->set_role(roles[0], i);
                        ts->set_role(roles[1], j);

                        score = parent_game->next_step()->make(alpha, beta).begin()->first;
                        std::vector<int> selected_players = {i, j};
                        scores.push_back({score,{selected_players}});
                        ts->remove_role(roles[0]);
                        ts->remove_role(roles[1]);
                        parent_game->desrease_step();

                        if(maximizing_team == pgu::TEAM_A){
                            if(proceed_alpha_beta_max(score, alpha, beta) && alpha_beta_prune)
                                break;
                        }
                        else{
                            if(proceed_alpha_beta_min(score, alpha, beta) && alpha_beta_prune)
                                break;
                        }
                    }
                }
            }
        }
        if(maximizing_team == pgu::TEAM_A)
            std::sort(scores.rbegin(), scores.rend());
        else
            std::sort(scores.begin(), scores.end());
        return scores;
    }

    ChooseAtacker::ChooseAtacker(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team) : GameStep(name, parent_game, maximizing_team, affected_team, {"ATCK", "REJ"}){}

    std::vector<std::pair<int, std::vector<int>>> ChooseAtacker::make(int alpha, int beta){
        pgu::TeamState* ts;
        affected_team == pgu::TEAM_A ? ts = parent_game->teamA : ts = parent_game->teamB; // swapped back!

        std::vector<std::pair<int, std::vector<int>>> scores;
        int score;

        for( int i = 1, j = 2; i < 3; i++, j--){
            std::string c_role1 = "C_ATCK"+std::to_string(i);
            std::string c_role2 = "C_ATCK"+std::to_string(j);
            ts->set_role(roles[0], ts->players[c_role1]);
            ts->set_role(roles[1], ts->players[c_role2]);

            score = parent_game->next_step()->make(alpha, beta).begin()->first;
            std::vector<int> selected_player = {ts->players[c_role1], ts->players[c_role2]};
            scores.push_back({score,{selected_player}});
            ts->remove_role(roles[0]);
            ts->remove_role(roles[1]);
            parent_game->desrease_step();
            if(maximizing_team == pgu::TEAM_A){
                if(proceed_alpha_beta_max(score, alpha, beta) && alpha_beta_prune)
                    break;
            }
            else{
                if(proceed_alpha_beta_min(score, alpha, beta) && alpha_beta_prune)
                    break;
            }
        }
        if(maximizing_team == pgu::TEAM_A)
            std::sort(scores.rbegin(), scores.rend());
        else
            std::sort(scores.begin(), scores.end());
        return scores;
    }

    Finale::Finale(std::string name, pgu::PairingGameUniversal* parent_game) : pgu::GameStep(name, parent_game, pgu::NONE_TEAM, pgu::BOTH_TEAMS, {"CHAMP"}){}

    std::vector<std::pair<int, std::vector<int>>> Finale::make(int alpha, int beta){
        std::vector<std::pair<int, std::vector<int>>> scores;

        int i, j;
        for( i = 0 ; i < parent_game->teamA->get_n_players(); i++){
            if( parent_game->teamA->is_player_free(i)){
                parent_game->teamA->set_role(roles[0], i);
                break;
            }
        }
        for( j = 0 ; j < parent_game->teamB->get_n_players(); j++){
            if( parent_game->teamB->is_player_free(j)){
                parent_game->teamB->set_role(roles[0], j);
                break;
            }
        }
        int score = parent_game->calc_score();
        scores.push_back({score,{i, j}});
        parent_game->teamA->remove_role(roles[0]);
        parent_game->teamB->remove_role(roles[0]);
        return scores;
    }

    int PairingGameSimple4::calc_score(){
        int score = 0;

        score += score_sheet->get(teamA->players["DEF"], teamB->players["ATCK"], 0);
        score += score_sheet->get(teamA->players["ATCK"], teamB->players["DEF"], 0);
        score += score_sheet->get(teamA->players["REJ"], teamB->players["REJ"], 0);
        score += score_sheet->get(teamA->players["CHAMP"], teamB->players["CHAMP"], 0);

        return score;
    }

    void PairingGameSimple4::play_with_input(){
        int alpha = score_sheet->min_teamA_score;
        int beta = score_sheet->max_teamA_score;

        printf("%s",score_sheet->__str().c_str());

        current_step = 0;
        for( auto &seq : sequence){
            printf("++ %s\n",seq->name.c_str());
            std::vector<std::pair<int, std::vector<int>>> result = seq->make(alpha, beta);
            printf("%s\n", pgu::result_to_str(result).c_str());

            if(seq->affected_team == pgu::TEAM_A){
                int it = 0;
                for( auto &role : seq->roles)
                    teamA->set_role(role, result[0].second[it++]);
            }
            else if(seq->affected_team == pgu::TEAM_B){
                int it = 0;
                for( auto &role : seq->roles)
                    teamB->set_role(role, result[0].second[it++]);
            }
            else if(seq->affected_team == pgu::BOTH_TEAMS){
                teamA->set_role(seq->roles[0], result[0].second[0]);
                teamB->set_role(seq->roles[0], result[0].second[1]);
            }
            current_step++;
        }
        printf("%s\n",final_standings_str().c_str());

    }

    std::string PairingGameSimple4::final_standings_str(){
        std::string str = "Final standings:\n";

        str += std::to_string(teamA->players["DEF"])+"-"+std::to_string(teamB->players["ATCK"])+":"+std::to_string(score_sheet->get(teamA->players["DEF"],teamB->players["ATCK"],0))+"\n";
        str += std::to_string(teamA->players["ATCK"])+"-"+std::to_string(teamB->players["DEF"])+":"+std::to_string(score_sheet->get(teamA->players["ATCK"],teamB->players["DEF"],0))+"\n";
        str += std::to_string(teamA->players["REJ"])+"-"+std::to_string(teamB->players["REJ"])+":"+std::to_string(score_sheet->get(teamA->players["REJ"],teamB->players["REJ"],0))+"\n";
        str += std::to_string(teamA->players["CHAMP"])+"-"+std::to_string(teamB->players["CHAMP"])+":"+std::to_string(score_sheet->get(teamA->players["CHAMP"],teamB->players["CHAMP"],0))+"\n";
        int score = calc_score();
        str += "Total: "+std::to_string(score)+"-"+std::to_string(score_sheet->max_teamA_score - score)+"\n";
        return str;
    }

    PairingGameSimple4* init_machine(bool alpha_beta_pruning){

        pgu::ScoreSheet* score_sheet = new pgu::ScoreSheet(4,1,0,20,true);

        PairingGameSimple4* pairing_game_simple4 = new PairingGameSimple4({"DEF", "C_ATCK1", "C_ATCK2", "ATCK", "REJ", "CHAMP"}, score_sheet);

        SetDefender* set_defender_A = new SetDefender("Set defender A", pairing_game_simple4, pgu::TEAM_A, pgu::TEAM_A);
        SetDefender* set_defender_B = new SetDefender("Set defender B", pairing_game_simple4, pgu::TEAM_B, pgu::TEAM_B);
        SetAtackers* set_atackers_A = new SetAtackers("Set atackers A", pairing_game_simple4, pgu::TEAM_A, pgu::TEAM_A);
        SetAtackers* set_atackers_B = new SetAtackers("Set atackers B", pairing_game_simple4, pgu::TEAM_B, pgu::TEAM_B);
        ChooseAtacker* choose_atacker_A = new ChooseAtacker("Choose atacker A", pairing_game_simple4, pgu::TEAM_A, pgu::TEAM_B);
        ChooseAtacker* choose_atacker_B = new ChooseAtacker("Choose atacker B", pairing_game_simple4, pgu::TEAM_B, pgu::TEAM_A);
        Finale* finale = new Finale("Finale", pairing_game_simple4);

        std::vector<pgu::GameStep*> sequence = {set_defender_A, set_defender_B, set_atackers_A, set_atackers_B, choose_atacker_A, choose_atacker_B, finale};
        for(auto const &seq : sequence){
            seq->alpha_beta_prune = alpha_beta_pruning;
        }

        pairing_game_simple4->set_seq(sequence);

        return pairing_game_simple4;

    }


}
