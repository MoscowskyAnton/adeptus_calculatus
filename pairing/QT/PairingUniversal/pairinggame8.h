#ifndef PAIRINGGAME8_H
#define PAIRINGGAME8_H

#include "pairinggameuniversal.h"

namespace pgu_8 {

    class SetDefender : public pgu::GameStep{
    public:
        SetDefender(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    private:
        std::string phase;
    };

    class SetAtackers : public pgu::GameStep{
    public:
        SetAtackers(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    };

    class ChooseAtacker : public pgu::GameStep{
    public:
        ChooseAtacker(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase, std::vector<std::string> roles);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    private:
        std::string phase;
    };

    class ChooseTable : public pgu::GameStep{
    public:
        ChooseTable(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team, std::string phase, std::vector<std::string> roles);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    };

    class Finale : public pgu::GameStep{
    public:
        Finale(std::string name, pgu::PairingGameUniversal* parent_game);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    private:
    };

    class PairingGame8 : public pgu::PairingGameUniversal{
    public:
        PairingGame8(const std::vector<std::string> &player_roles, pgu::ScoreSheet* score_sheet, pgu::TablesState* tables_state);

        int calc_score();
        void play_with_input(bool teamA_won_roll_off);
        std::string final_standings_str();

        void make_first_step(bool teamA_won_roll_off);

        pgu::TablesState* tables_state;
    private:


    };

    PairingGame8* init_machine(bool alpha_beta_pruning, bool teamA_won_roll_off);

}

#endif // PAIRINGGAME8_H
