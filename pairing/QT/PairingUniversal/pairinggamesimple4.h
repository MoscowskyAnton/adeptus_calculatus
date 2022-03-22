#ifndef PAIRINGGAMESIMPLE4_H
#define PAIRINGGAMESIMPLE4_H

#include "pairinggameuniversal.h"

namespace pgu_simple4 {

    class SetDefender : private pgu::GameStep{
    public:
        SetDefender(std::string name, pgu::PairingGameUniversal* parent_game, bool team);

        int make(int alpha, int beta);

    private:

    };

    pgu::PairingGameUniversal PairingGameSimple4(4,{"DEF", "C_ATCK1", "C_ATCK2", "ATCK", "REJ", "CHAMP"},{},std::map<std::string, bool>());
}

#endif // PAIRINGGAMESIMPLE4_H
