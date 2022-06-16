#include <iostream>
//#include "pairinggameuniversal.h"

#include "pairinggamesimple4.h"
#include "pairinggame8.h"
#include <chrono>

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
    //pg8->play_with_input(teamA_won_roll_off);

    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    pg8->make_first_step(teamA_won_roll_off);
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();

    std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::minutes>(end - begin).count() << "[min]" << std::endl;

    return 0;
}
