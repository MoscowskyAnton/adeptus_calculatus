#include <iostream>
//#include "pairinggameuniversal.h"

#include "pairinggamesimple4.h"
#include "pairinggame8.h"
//using namespace pgu_simple4;
//using namespace pgu_8;

int main()
{
    // test simple 4
    /*
    PairingGameSimple4* pgs4 = init_machine(false);
    pgs4->play_with_input();

    pgs4->set_alpha_beta_pruning(true);
    pgs4->reset_states();

    pgs4->play_with_input();
    */


    // test 8
    bool teamA_won_roll_off = true;
    pgu_8::PairingGame8* pg8 = pgu_8::init_machine(true, teamA_won_roll_off);
    pg8->play_with_input(teamA_won_roll_off);



    return 0;
}
