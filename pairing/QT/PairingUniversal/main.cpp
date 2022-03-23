#include <iostream>
//#include "pairinggameuniversal.h"

#include "pairinggamesimple4.h"

using namespace pgu_simple4;

int main()
{

    PairingGameSimple4* pgs4 = init_machine(false);
    pgs4->play_with_input();

    pgs4->set_alpha_beta_pruning(true);
    pgs4->reset_states();

    pgs4->play_with_input();

    return 0;
}
