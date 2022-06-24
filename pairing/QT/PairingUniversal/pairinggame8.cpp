#include "pairinggame8.h"
#include <algorithm>

namespace pgu_8 {

    SetDefender::SetDefender(std::string name, pgu::PairingGameUniversal *parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase) : pgu::GameStep(name, parent_game, maximizing_team, affected_team, {"DEF"+phase}){
        this->phase = phase;
    }

    std::vector<std::pair<int, std::vector<int>>> SetDefender::make(int alpha, int beta){
        pgu::TeamState* ts;
        affected_team == pgu::TEAM_A ? ts = parent_game->teamA : ts = parent_game->teamB;

        std::vector<std::pair<int, std::vector<int>>> scores;
        int m_score;
        maximizing_team == pgu::TEAM_A ? m_score = parent_game->score_sheet->min_teamA_score : m_score = parent_game->score_sheet->max_teamA_score;
        for( int i = 0; i < ts->get_n_players(); i++){
            if(affected_team == pgu::TEAM_B){
                if( !phase.compare("1"))
                    printf("DefB [%s] \n", phase.c_str());
            }

            if(ts->is_player_free(i)){
                ts->set_role(roles[0], i);

                int score = parent_game->next_step()->make(alpha, beta).begin()->first;
                std::vector<int> selected_player = {i};
                scores.push_back({score,{selected_player}});
                ts->remove_role(roles[0]);
                parent_game->desrease_step();
                if(maximizing_team == pgu::TEAM_A){
                    m_score = std::max(m_score, score);
                    if(alpha_beta_prune && proceed_alpha_beta_max(m_score, alpha, beta))
                        break;
                }
                else{
                    m_score = std::min(m_score, score);
                    if(alpha_beta_prune && proceed_alpha_beta_min(score, alpha, beta))
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

    SetAtackers::SetAtackers(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase) : GameStep(name, parent_game, maximizing_team, affected_team, {"C_ATCK"+phase+"_1", "C_ATCK"+phase+"_2"}){}

    std::vector<std::pair<int, std::vector<int>>> SetAtackers::make(int alpha, int beta){
        pgu::TeamState* ts;
        affected_team == pgu::TEAM_A  ? ts = parent_game->teamA : ts = parent_game->teamB;

        int m_score;
        maximizing_team == pgu::TEAM_A ? m_score = parent_game->score_sheet->min_teamA_score : m_score = parent_game->score_sheet->max_teamA_score;
        std::vector<std::pair<int, std::vector<int>>> scores;

        for( int i = 0; i < ts->get_n_players(); i++){
            if(ts->is_player_free(i)){
                for( int j = i+1; j < ts->get_n_players(); j++){
                    if(ts->is_player_free(j)){
                        ts->set_role(roles[0], i);
                        ts->set_role(roles[1], j);

                        int score = parent_game->next_step()->make(alpha, beta).begin()->first;
                        std::vector<int> selected_players = {i, j};
                        scores.push_back({score,{selected_players}});
                        ts->remove_role(roles[0]);
                        ts->remove_role(roles[1]);
                        parent_game->desrease_step();

                        if(maximizing_team == pgu::TEAM_A){
                            m_score = std::max(m_score, score);
                            if(alpha_beta_prune && proceed_alpha_beta_max(m_score, alpha, beta))
                                break;
                        }
                        else{
                            m_score = std::min(m_score, score);
                            if(alpha_beta_prune && proceed_alpha_beta_min(m_score, alpha, beta))
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

    ChooseAtacker::ChooseAtacker(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase, std::vector<std::string> roles) : GameStep(name, parent_game, maximizing_team, affected_team, roles){
        this->phase = phase;
    }

    std::vector<std::pair<int, std::vector<int>>> ChooseAtacker::make(int alpha, int beta){
        pgu::TeamState* ts;
        affected_team == pgu::TEAM_A ? ts = parent_game->teamA : ts = parent_game->teamB; // swapped back!

        std::vector<std::pair<int, std::vector<int>>> scores;
        int m_score;
        maximizing_team == pgu::TEAM_A ? m_score = parent_game->score_sheet->min_teamA_score : m_score = parent_game->score_sheet->max_teamA_score;

        for( int i = 1, j = 2; i < 3; i++, j--){
            std::string c_role1 = "C_ATCK"+phase+"_"+std::to_string(i);
            std::string c_role2 = "C_ATCK"+phase+"_"+std::to_string(j);
            ts->set_role(roles[0], ts->players[c_role1]);
            if( ! roles[1].empty() )
                ts->set_role(roles[1], ts->players[c_role2]);
            int p_role = ts->remove_role(c_role2);

            int score = parent_game->next_step()->make(alpha, beta).begin()->first;
            std::vector<int> selected_player = {ts->players[c_role1], ts->players[c_role2]};
            scores.push_back({score,{selected_player}});
            ts->remove_role(roles[0]);
            if( ! roles[1].empty() )
                ts->remove_role(roles[1]);
            ts->set_role(c_role2, p_role);
            parent_game->desrease_step();
            if(maximizing_team == pgu::TEAM_A){
                m_score = std::max(m_score, score);
                if(alpha_beta_prune && proceed_alpha_beta_max(m_score, alpha, beta))
                    break;
            }
            else{
                m_score = std::min(m_score, score);
                if(alpha_beta_prune && proceed_alpha_beta_min(m_score, alpha, beta))
                    break;
            }
        }
        if(maximizing_team == pgu::TEAM_A)
            std::sort(scores.rbegin(), scores.rend());
        else
            std::sort(scores.begin(), scores.end());
        return scores;
    }

    ChooseTable::ChooseTable(std::string name, pgu::PairingGameUniversal *parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase, std::vector<std::string> roles) : pgu::GameStep(name, parent_game, maximizing_team, affected_team, roles){}

    std::vector<std::pair<int, std::vector<int>>> ChooseTable::make(int alpha, int beta){
        pgu::TeamState* ts;
        affected_team == pgu::TEAM_A  ? ts = parent_game->teamA : ts = parent_game->teamB;

        std::vector<std::pair<int, std::vector<int>>> scores;
        int m_score;
        maximizing_team == pgu::TEAM_A ? m_score = parent_game->score_sheet->min_teamA_score : m_score = parent_game->score_sheet->max_teamA_score;

        pgu::TablesState *tbls = ((PairingGame8*)parent_game)->tables_state;
        std::vector<int> free_table_types = tbls->get_free_types();

        std::string teamA_player;
        if( affected_team == pgu::TEAM_A ){
            teamA_player = roles[0];
        }
        else if(affected_team == pgu::TEAM_B){
            teamA_player = roles[1];
        }

        for(auto &table_type: free_table_types){
            tbls->set_table_by_type(table_type, teamA_player);
            int score = parent_game->next_step()->make(alpha, beta).begin()->first;
            std::vector<int> selected_table_type = {table_type};
            scores.push_back({score,{selected_table_type}});
            tbls->remove_table_by_player(teamA_player);
            parent_game->desrease_step();
            if(maximizing_team == pgu::TEAM_A){
                m_score = std::max(m_score, score);
                if(alpha_beta_prune && proceed_alpha_beta_max(m_score, alpha, beta))
                    break;
            }
            else{
                m_score = std::min(m_score, score);
                if(alpha_beta_prune && proceed_alpha_beta_min(score, alpha, beta))
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

    PairingGame8::PairingGame8(const std::vector<std::string> &player_roles, pgu::ScoreSheet* score_sheet, pgu::TablesState *tables_state) : pgu::PairingGameUniversal(8, player_roles, score_sheet){
        this->tables_state = tables_state;
    }

    int PairingGame8::calc_score(){
        int score = 0;

        score += score_sheet->get(teamA->players["DEF1"], teamB->players["ATCK1"], tables_state->get_table_type_by_player("DEF1"));
        score += score_sheet->get(teamA->players["ATCK1"], teamB->players["DEF1"], tables_state->get_table_type_by_player("ATCK1"));

        score += score_sheet->get(teamA->players["DEF2"], teamB->players["ATCK2"], tables_state->get_table_type_by_player("DEF2"));
        score += score_sheet->get(teamA->players["ATCK2"], teamB->players["DEF2"], tables_state->get_table_type_by_player("ATCK2"));

        score += score_sheet->get(teamA->players["DEF3"], teamB->players["ATCK3"], tables_state->get_table_type_by_player("DEF3"));
        score += score_sheet->get(teamA->players["ATCK3"], teamB->players["DEF3"], tables_state->get_table_type_by_player("ATCK3"));

        score += score_sheet->get(teamA->players["REJ"], teamB->players["REJ"], tables_state->get_table_type_by_player("REJ"));
        score += score_sheet->get(teamA->players["CHAMP"], teamB->players["CHAMP"], tables_state->get_table_type_by_player("CHAMP"));

        return score;
    }

    void PairingGame8::make_first_step(bool teamA_won_roll_off){
        int alpha = score_sheet->min_teamA_score;
        int beta = score_sheet->max_teamA_score;

        printf("%s",score_sheet->__str().c_str());

        std::vector<std::pair<int, std::vector<int>>> result = sequence[0]->make(alpha, beta);
        printf("%s\n", pgu::result_to_str(result).c_str());
    }

    void PairingGame8::make_first_first_step(bool teamA_won_roll_off){
        int alpha = score_sheet->min_teamA_score;
        int beta = score_sheet->max_teamA_score;

        printf("%s",score_sheet->__str().c_str());

        teamA->set_role("DEF1", 0);
        current_step = 1;
        std::vector<std::pair<int, std::vector<int>>> result = sequence[1]->make(alpha, beta);
        printf("%s\n", pgu::result_to_str(result).c_str());
    }

    void PairingGame8::play_with_input(bool teamA_won_roll_off){
        int alpha = score_sheet->min_teamA_score;
        int beta = score_sheet->max_teamA_score;

        printf("%s",score_sheet->__str().c_str());

        current_step = 0;
        for( auto &seq : sequence){
            printf("++ %s\n",seq->name.c_str());
            std::vector<std::pair<int, std::vector<int>>> result = seq->make(alpha, beta);
            printf("%s\n", pgu::result_to_str(result).c_str());

            if( seq->name.find("table") == std::string::npos ){
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
            }
            else{
                tables_state->set_table_by_type(result[0].second[0], seq->roles[0]);
            }
            current_step++;
        }
        printf("%s\n",final_standings_str().c_str());
    }

    std::string PairingGame8::final_standings_str(){
        std::string str = "Final standings:\n";

        str += std::to_string(teamA->players["DEF1"])+"-"+std::to_string(teamB->players["ATCK1"])+" on "+std::to_string(tables_state->get_table_type_by_player("DEF1"))+":"+std::to_string(score_sheet->get(teamA->players["DEF1"],teamB->players["ATCK1"],tables_state->get_table_type_by_player("DEF1")))+"\n";
        str += std::to_string(teamA->players["ATCK1"])+"-"+std::to_string(teamB->players["DEF1"])+" on "+std::to_string(tables_state->get_table_type_by_player("ATCK1"))+":"+std::to_string(score_sheet->get(teamA->players["ATCK1"],teamB->players["DEF1"],tables_state->get_table_type_by_player("ATCK1")))+"\n";

        str += std::to_string(teamA->players["DEF1"])+"-"+std::to_string(teamB->players["ATCK2"])+" on "+std::to_string(tables_state->get_table_type_by_player("DEF2"))+":"+std::to_string(score_sheet->get(teamA->players["DEF2"],teamB->players["ATCK2"],tables_state->get_table_type_by_player("DEF2")))+"\n";
        str += std::to_string(teamA->players["ATCK1"])+"-"+std::to_string(teamB->players["DEF2"])+" on "+std::to_string(tables_state->get_table_type_by_player("ATCK2"))+":"+std::to_string(score_sheet->get(teamA->players["ATCK2"],teamB->players["DEF2"],tables_state->get_table_type_by_player("ATCK2")))+"\n";

        str += std::to_string(teamA->players["DEF3"])+"-"+std::to_string(teamB->players["ATCK3"])+" on "+std::to_string(tables_state->get_table_type_by_player("DEF3"))+":"+std::to_string(score_sheet->get(teamA->players["DEF3"],teamB->players["ATCK3"],tables_state->get_table_type_by_player("DEF3")))+"\n";
        str += std::to_string(teamA->players["ATCK3"])+"-"+std::to_string(teamB->players["DEF3"])+" on "+std::to_string(tables_state->get_table_type_by_player("ATCK3"))+":"+std::to_string(score_sheet->get(teamA->players["ATCK3"],teamB->players["DEF3"],tables_state->get_table_type_by_player("ATCK3")))+"\n";

        str += std::to_string(teamA->players["REJ"])+"-"+std::to_string(teamB->players["REJ"])+" on "+std::to_string(tables_state->get_table_type_by_player("REJ"))+":"+std::to_string(score_sheet->get(teamA->players["REJ"],teamB->players["REJ"],tables_state->get_table_type_by_player("REJ")))+"\n";
        str += std::to_string(teamA->players["CHAMP"])+"-"+std::to_string(teamB->players["CHAMP"])+" on "+std::to_string(tables_state->get_table_type_by_player("CHAMP"))+":"+std::to_string(score_sheet->get(teamA->players["CHAMP"],teamB->players["CHAMP"],tables_state->get_table_type_by_player("CHAMP")))+"\n";

        int score = calc_score();
        str += "Total: "+std::to_string(score)+"-"+std::to_string((score_sheet->max_teamA_score + score_sheet->min_teamA_score) - score)+"\n";
        return str;
    }

    PairingGame8* init_machine(bool alpha_beta_pruning, bool teamA_won_roll_off){
        bool TAWFRF = teamA_won_roll_off; // team A won roll-off

        int n_tables = 1;

        pgu::ScoreSheet * score_sheet = new pgu::ScoreSheet(8,n_tables,-2,2,true);
        pgu::TablesState * tbl_s = new pgu::TablesState(8, n_tables);
        PairingGame8* pairing_game_8 = new PairingGame8({"DEF1", "C_ATCK1_1", "C_ATCK1_2", "ATCK1", "DEF2", "C_ATCK2_1", "C_ATCK2_2", "ATCK2", "DEF3", "C_ATCK3_1", "C_ATCK3_2", "ATCK3", "REJ", "CHAMP"}, score_sheet, tbl_s);

        // steps
        SetDefender* set_defender_A1 = new SetDefender("Set defender A1", pairing_game_8, pgu::TEAM_A, pgu::TEAM_A, "1");
        SetDefender* set_defender_B1 = new SetDefender("Set defender B1", pairing_game_8, pgu::TEAM_B, pgu::TEAM_B, "1");
        SetAtackers* set_atackers_A1 = new SetAtackers("Set atackers A1", pairing_game_8, pgu::TEAM_A, pgu::TEAM_A, "1");
        SetAtackers* set_atackers_B1 = new SetAtackers("Set atackers B1", pairing_game_8, pgu::TEAM_B, pgu::TEAM_B, "1");
        ChooseAtacker* choose_atacker_A1 = new ChooseAtacker("Choose atacker A1", pairing_game_8, pgu::TEAM_A, pgu::TEAM_B, "1", {"ATCK1", ""});
        ChooseAtacker* choose_atacker_B1 = new ChooseAtacker("Choose atacker B1", pairing_game_8, pgu::TEAM_B, pgu::TEAM_A, "1", {"ATCK1", ""});
        ChooseTable* choose_table_1_1 = new ChooseTable("Choose table 1 1", pairing_game_8, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, "1", {"DEF1","ATCK1"});
        ChooseTable* choose_table_1_2 = new ChooseTable("Choose table 1 2", pairing_game_8, TAWFRF ? pgu::TEAM_B : pgu::TEAM_A, TAWFRF ? pgu::TEAM_B : pgu::TEAM_A, "1", {"DEF1","ATCK1"});

        SetDefender* set_defender_A2 = new SetDefender("Set defender A2", pairing_game_8, pgu::TEAM_A, pgu::TEAM_A, "2");
        SetDefender* set_defender_B2 = new SetDefender("Set defender B2", pairing_game_8, pgu::TEAM_B, pgu::TEAM_B, "2");
        SetAtackers* set_atackers_A2 = new SetAtackers("Set atackers A2", pairing_game_8, pgu::TEAM_A, pgu::TEAM_A, "2");
        SetAtackers* set_atackers_B2 = new SetAtackers("Set atackers B2", pairing_game_8, pgu::TEAM_B, pgu::TEAM_B, "2");
        ChooseAtacker* choose_atacker_A2 = new ChooseAtacker("Choose atacker A2", pairing_game_8, pgu::TEAM_A, pgu::TEAM_B, "2", {"ATCK2", ""});
        ChooseAtacker* choose_atacker_B2 = new ChooseAtacker("Choose atacker B2", pairing_game_8, pgu::TEAM_B, pgu::TEAM_A, "2", {"ATCK2", ""});
        ChooseTable* choose_table_2_1 = new ChooseTable("Choose table 2 1", pairing_game_8, TAWFRF ? pgu::TEAM_B : pgu::TEAM_A, TAWFRF ? pgu::TEAM_B : pgu::TEAM_A, "2", {"DEF2","ATCK2"});
        ChooseTable* choose_table_2_2 = new ChooseTable("Choose table 2 2", pairing_game_8, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, "2", {"DEF2","ATCK2"});

        SetDefender* set_defender_A3 = new SetDefender("Set defender A3", pairing_game_8, pgu::TEAM_A, pgu::TEAM_A, "3");
        SetDefender* set_defender_B3 = new SetDefender("Set defender B3", pairing_game_8, pgu::TEAM_B, pgu::TEAM_B, "3");
        SetAtackers* set_atackers_A3 = new SetAtackers("Set atackers A3", pairing_game_8, pgu::TEAM_A, pgu::TEAM_A, "3");
        SetAtackers* set_atackers_B3 = new SetAtackers("Set atackers B3", pairing_game_8, pgu::TEAM_B, pgu::TEAM_B, "3");
        ChooseAtacker* choose_atacker_A3 = new ChooseAtacker("Choose atacker A3", pairing_game_8, pgu::TEAM_A, pgu::TEAM_B, "3", {"ATCK3", "REJ"});
        ChooseAtacker* choose_atacker_B3 = new ChooseAtacker("Choose atacker B3", pairing_game_8, pgu::TEAM_B, pgu::TEAM_A, "3", {"ATCK3", "REJ"});
        ChooseTable* choose_table_3_1 = new ChooseTable("Choose table 3 1", pairing_game_8, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, "3", {"DEF3","ATCK3"});
        ChooseTable* choose_table_3_2 = new ChooseTable("Choose table 3 2", pairing_game_8, TAWFRF ? pgu::TEAM_B : pgu::TEAM_A, TAWFRF ? pgu::TEAM_B : pgu::TEAM_A, "3", {"DEF3","ATCK3"});
        ChooseTable* choose_table_3_3 = new ChooseTable("Choose table 3 3", pairing_game_8, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, TAWFRF ? pgu::TEAM_A : pgu::TEAM_B, "3", {"REJ","REJ"});
        ChooseTable* choose_table_3_4 = new ChooseTable("Choose table 3 4", pairing_game_8, pgu::TEAM_A, pgu::TEAM_A, "3", {"CHAMP","CHAMP"});
        Finale* finale = new Finale("Finale", pairing_game_8);

        std::vector<pgu::GameStep*> sequence = {set_defender_A1, set_defender_B1, set_atackers_A1, set_atackers_B1, choose_atacker_A1, choose_atacker_B1, choose_table_1_1, choose_table_1_2,
                                               set_defender_A2, set_defender_B2, set_atackers_A2, set_atackers_B2, choose_atacker_A2, choose_atacker_B2, choose_table_2_1, choose_table_2_2,
                                               set_defender_A3, set_defender_B3, set_atackers_A3, set_atackers_B3, choose_atacker_A3, choose_atacker_B3, choose_table_3_1, choose_table_3_2,
                                               choose_table_3_3, choose_table_3_4, finale};
        pairing_game_8->set_seq(sequence);

        pairing_game_8->set_alpha_beta_pruning(alpha_beta_pruning);

        return pairing_game_8;
    }



}
