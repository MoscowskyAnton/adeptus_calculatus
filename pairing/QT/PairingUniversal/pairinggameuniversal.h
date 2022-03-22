#ifndef PAIRINGGAMEUNIVERSAL_H
#define PAIRINGGAMEUNIVERSAL_H

#include <vector>
#include <string>
#include <map>

namespace pgu{

    const bool TEAM_A = true;
    const bool TEAM_B = false;

    class ScoreSheet{
    public:
        ScoreSheet(int n_players, int n_criterion);
    private:
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

    private:
        int n_players;

    };

    class PairingGameUniversal;
    class GameStep{
    public:
        GameStep(std::string name, PairingGameUniversal* parent_game, bool team);

        virtual int make(int alpha, int beta) = 0;

        std::string name;
        bool alpha_beta_prune = true;
    protected:
        PairingGameUniversal* parent_game;
        bool team;

        bool proceed_alpha_beta_max(int score, int &new_score, int &alpha, int &beta);
        bool proceed_alpha_beta_min(int score, int &new_score, int &alpha, int &beta);
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
        PairingGameUniversal(size_t n_players, const std::vector<std::string> &player_roles, const std::vector<GameStep*> &sequence, const std::map<std::string, bool> &rolloffs);

        GameStep* next_step();

        TeamState* teamA;
        TeamState* teamB;

    private:
        int n_players;
        std::vector<std::string> player_roles;
        std::map<std::string, bool> rolloffs;
        std::vector<GameStep*> sequence;
        int current_step = 0;


    };

}
#endif // PAIRINGGAMEUNIVERSAL_H
