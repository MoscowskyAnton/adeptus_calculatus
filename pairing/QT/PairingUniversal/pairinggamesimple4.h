#ifndef PAIRINGGAMESIMPLE4_H
#define PAIRINGGAMESIMPLE4_H

#include "pairinggameuniversal.h"

namespace pgu_simple4 {

    class SetDefender : public pgu::GameStep{
    public:
        SetDefender(std::string name, pgu::PairingGameUniversal* parent_game, bool team);

        int make(int alpha, int beta);

    private:

    };


    pgu::PairingGameUniversal pairing_game_simple4(4,{"DEF", "C_ATCK1", "C_ATCK2", "ATCK", "REJ", "CHAMP"},{},std::map<std::string, bool>());

    SetDefender set_defender_A("Set defender A",&pairing_game_simple4, pgu::TEAM_A);
    SetDefender set_defender_B("Set defender B",&pairing_game_simple4, pgu::TEAM_B);


    std::vector<pgu::GameStep*> sequence = {&set_defender_A, &set_defender_B};



}

#endif // PAIRINGGAMESIMPLE4_H
