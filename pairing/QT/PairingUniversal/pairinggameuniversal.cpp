#include "pairinggameuniversal.h"
#include <algorithm>
#include <stdexcept>



namespace pgu {

    ScoreSheet::ScoreSheet(int n_players, int n_criterion, int min, int max, bool random){
        this->n_players = n_players;
        this->n_criterion = n_criterion;
        this->max = max;
        this->min = min;
        if(random)
            srand(time(NULL));

        this->max_teamA_score = max * n_players;
        this->min_teamA_score = min * n_players;

        this->scores = new int**[n_players];
        for( int i = 0 ; i < n_players; i++){
            this->scores[i] = new int*[n_players];
            for( int j =0 ; j < n_players; j++){
                this->scores[i][j] = new int[n_criterion];
                for(int k = 0 ; k < n_criterion; k++){
                    if(random){
                        this->scores[i][j][k] = min + rand() % (max-min+1);
                    }
                    else{
                        this->scores[i][j][k] = 0;
                    }
                }
            }
        }
    }

    std::string ScoreSheet::__str(){
        std::string str = "";
        for( int i = 0 ; i < n_players; i++){
            for( int j =0 ; j < n_players; j++){
                str += "[";
                for(int k = 0 ; k < n_criterion; k++){
                    str += std::to_string(scores[i][j][k])+" ";
                }
                str += "] ";
            }
            str += "\n";
        }
        return str;
    }

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

    int TeamState::remove_role(std::string role){
#ifdef DEBUG_STUFF
        if (!players.count(role))
            throw std::logic_error("no such role "+role);
        if (players[role] == -1)
            throw std::logic_error(role + " is already unset");
#endif
        int p_role = players[role];
        players[role] = -1;
        return p_role;
    }

    void TeamState::reset(){
        for(auto &player : players){
            player.second = -1;
        }
    }

    TablesState::TablesState(int n_players, int table_types){
        for( int i = 0 ; i < n_players; i++){
            tables_types.push_back(rand() % table_types);
            tables_to_players[i] = "";
        }
    }

    std::vector<int> TablesState::get_free_types(){
        std::vector<int> free_types;
        for( auto &t2p : tables_to_players){
            if( t2p.second.empty() ){
                free_types.push_back(tables_types[t2p.first]);
            }
        }
        std::sort(free_types.begin(), free_types.end());
        std::vector<int>::iterator it;
        it = std::unique(free_types.begin(), free_types.end());
        free_types.resize(std::distance(free_types.begin(),it));
        return free_types;
    }

    void TablesState::set_table_by_no(int table, std::string player){
        if( !tables_to_players[table].empty() )
            throw std::logic_error("table "+std::to_string(table)+" already taken by player "+tables_to_players[table]);
        tables_to_players[table] = player;
    }

    void TablesState::set_table_by_type(int table_type, std::string player){
        for(auto &t2p:tables_to_players){
            if( t2p.second.empty()){
                if( this->tables_types[t2p.first] == table_type){
                    tables_to_players[t2p.first] = player;
                    return;
                }
            }
        }
        throw std::logic_error("no free type "+std::to_string(table_type)+" in tables");
    }

    void TablesState::remove_table_by_player(std::string player){
        for(auto &t2p:tables_to_players){
            if( t2p.second == player){
                t2p.second = "";
                return;
            }
        }
        throw std::logic_error("no table for player role "+player+" in tables");
    }

    int TablesState::get_table_type_by_player(std::string player){
        for(auto &t2p:tables_to_players){
            if( t2p.second == player){
                return tables_types[t2p.first];
            }
        }
        throw std::logic_error("no table for player role "+player+" in tables");
    }

    GameStep::GameStep(std::string name, PairingGameUniversal* parent_game, TEAMS maximizing_team, TEAMS affected_team, std::vector<std::string> roles){
        this->name = name;
        this->parent_game = parent_game;
        this->maximizing_team = maximizing_team;
        this->affected_team = affected_team;
        this->roles = roles;
    }

    bool GameStep::proceed_alpha_beta_max(int score, int &alpha, int &beta){
        if(score >= beta){
            //printf("b");
            return true;
        }
        if(score > alpha){
            alpha = score;
        }
        return false;
    }

    bool GameStep::proceed_alpha_beta_min(int score, int &alpha, int &beta){
        // uncomenting this sometimes leads to different scores in vanila minmax and alpha-beta pruned one
        if(score <= alpha){
            //printf("a");
            return true;
        }
        if(score < beta){
            beta = score;
        }
        return false;
    }

    GameStep *PairingGameUniversal::next_step(){
        return sequence[++current_step];
    }

    PairingGameUniversal::PairingGameUniversal(size_t n_players, const std::vector<std::string> &player_roles, ScoreSheet* score_sheet){
        this->n_players = n_players;
        this->player_roles = player_roles;        
        this->score_sheet = score_sheet;

        teamA = new TeamState(n_players, player_roles);
        teamB = new TeamState(n_players, player_roles);
    }

    void PairingGameUniversal::set_alpha_beta_pruning(bool value){
        for(auto &seq : sequence)
            seq->alpha_beta_prune = value;
    }

    void PairingGameUniversal::reset_states(){
        teamA->reset();
        teamB->reset();
    }

    std::string result_to_str(const std::vector<std::pair<int, std::vector<int>>> &result){
        std::string str ="";
        for (auto const& x : result){
            str += "[(";
            for( auto const& y : x.second){
                str += std::to_string(y)+", ";
            }
            str += ("): "+std::to_string(x.first)+"] ");
        }
        return str;
    }
}
