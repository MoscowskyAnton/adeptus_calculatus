#ifndef PAIRINGGAMEUNIVERSAL_H
#define PAIRINGGAMEUNIVERSAL_H

#include <vector>
#include <string>
#include <map>

namespace pgu{

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

    private:
        int n_players;

    };

    //план: делаем для каждого типа свой подкласс, в котором есть список шагов, которые должен подтянуть основной алгоритм

    /*
     * n_players - how much players in a team
     * player_roles - which roles are available
     * sequence - how the game goes
     * roll_offs - possibly rolloffs values (true - teamA won)
     */
    class GameRules{
    public:
        GameRules(){}
        GameRules(int n_players, const std::vector<std::string> &player_roles, const std::vector<std::string> &sequence, const std::map<std::string,bool> &roll_offs);

        int n_players;
        std::vector<std::string> player_roles;
        std::vector<std::string> sequence;
    private:

        bool check();


    };

    class PairingGameUniversal
    {
    public:
        PairingGameUniversal(const GameRules &game_rules);
    private:
        TeamState* teamA;
        TeamState* teamB;

        GameRules game_rules;

    };

}
#endif // PAIRINGGAMEUNIVERSAL_H
