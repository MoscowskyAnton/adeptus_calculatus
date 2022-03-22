#ifndef PAIRINGGAMEUNIVERSAL_H
#define PAIRINGGAMEUNIVERSAL_H

#include <vector>
#include <string>
#include <map>

#define DEBUG_STUFF

namespace pgu{

    enum TEAMS {NONE_TEAM, TEAM_A, TEAM_B, BOTH_TEAMS};
    //const bool TEAM_A = true;
    //const bool TEAM_B = false;

    class ScoreSheet{
    public:
        ScoreSheet(int n_players, int n_criterion, int min, int max, bool random = false);

        inline int get(int plA, int plB, int criterion){
#ifdef DEBUG_STUFF
#endif
            return scores[plA][plB][criterion];
        }
        int max_teamA_score;
        int min_teamA_score;

        std::string __str();

    private:
        int max, min;
        int n_players;
        int n_criterion;
        int ***scores;

    };

    class TeamState{
    public:
        TeamState(int n_players, const std::vector<std::string> &player_roles);

        std::map<std::string, int> players;

        bool is_player_free(int player_id);

        void set_role(std::string role, int player_id);
        void remove_role(std::string role);

        std::string __str();

        inline int get_n_players(){
            return n_players;
        }

        void reset();

    private:
        int n_players;

    };

    class PairingGameUniversal;
    class GameStep{
    public:
        GameStep(std::string name, PairingGameUniversal* parent_game, TEAMS maximizing_team, TEAMS affected_team, std::vector<std::string> roles = {});

        /*
         * returns vector of scores : vector selected stuf (players/tables/etc)
         */
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta) = 0;

        std::string name;
        bool alpha_beta_prune = false;
        TEAMS maximizing_team, affected_team;
        std::vector<std::string> roles;
    protected:
        PairingGameUniversal* parent_game;

        bool proceed_alpha_beta_max(int score, int &alpha, int &beta);
        bool proceed_alpha_beta_min(int score, int &alpha, int &beta);
    };

    //план: делаем для каждого типа свой подкласс, в котором есть список шагов, которые должен подтянуть основной алгоритм

    /*
     * n_players - how much players in a team
     * player_roles - which roles are available
     * sequence - how the game goes
     * roll_offs - possibly rolloffs values (true - teamA won)
     */

    class PairingGameUniversal
    {
        //friend void GameStep::make();
    public:
        PairingGameUniversal(size_t n_players, const std::vector<std::string> &player_roles, ScoreSheet* score_sheet);

        GameStep* next_step();

        TeamState* teamA;
        TeamState* teamB;

        ScoreSheet* score_sheet;

        virtual int calc_score() = 0;


        inline void set_seq(std::vector<GameStep*> &sequence){
            this->sequence = sequence;
        }
        inline void desrease_step(){current_step--;}

        virtual void play_with_input() = 0;


    protected:
        int n_players;
        std::vector<std::string> player_roles;
        std::map<std::string, bool> rolloffs;

        int current_step = 0;
        std::vector<GameStep*> sequence;


    };

    std::string result_to_str(const std::vector<std::pair<int, std::vector<int>>> &result);

}
#endif // PAIRINGGAMEUNIVERSAL_H
