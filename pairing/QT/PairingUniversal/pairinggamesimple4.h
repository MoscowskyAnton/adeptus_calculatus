#ifndef PAIRINGGAMESIMPLE4_H
#define PAIRINGGAMESIMPLE4_H

#include "pairinggameuniversal.h"

namespace pgu_simple4 {   

    class SetDefender : public pgu::GameStep{
    public:
        SetDefender(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    private:
    };

    class SetAtackers : public pgu::GameStep{
    public:
        SetAtackers(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    private:
    };

    class ChooseAtacker : public pgu::GameStep{
    public:
        ChooseAtacker(std::string name, pgu::PairingGameUniversal* parent_game, pgu::TEAMS maximizing_team, pgu::TEAMS affected_team);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    private:
    };

    class Finale : public pgu::GameStep{
    public:
        Finale(std::string name, pgu::PairingGameUniversal* parent_game);
        virtual std::vector<std::pair<int, std::vector<int>>> make(int alpha, int beta);
    private:
    };

    class PairingGameSimple4 : public pgu::PairingGameUniversal{
    public:
        PairingGameSimple4(const std::vector<std::string> &player_roles, pgu::ScoreSheet* score_sheet) : PairingGameUniversal(4, player_roles, score_sheet){}
        int calc_score();
        void play_with_input();
        std::string final_standings_str();

    private:
    };


    PairingGameSimple4* init_machine(bool alpha_beta_pruning = true);


}

#endif // PAIRINGGAMESIMPLE4_H
