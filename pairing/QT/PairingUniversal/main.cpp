#include <iostream>
//#include "pairinggameuniversal.h"

#include "pairinggamesimple4.h"

using namespace pgu_simple4;

int main()
{

    PairingGameSimple4* pgs4 = init_machine(false);
    pgs4->play_with_input();

    return 0;
}
