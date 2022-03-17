#include <iostream>
#include "../Pairing8/scoresheettables.h"
#include "../Pairing8/paringgame8.h"
#include "stdio.h"
#include "../Pairing8/tablesstate.h"

#include <thread>
#include <future>

#include <vector>
#include <map>
#include <chrono>

#define STEP_1_THREADS 8
#define TABLE_TYPES_NUM 2

using namespace std;

int simplefunc(std::string a)
{
    return a.size();
}

int main()
{


    ScoreSheetTables ss(8, TABLE_TYPES_NUM, -2, 2);
    ss.print();
    printf("Mean %f\n",ss.mean());

    TablesState ts(TABLE_TYPES_NUM, 8, true, false);
    ts.print();

    /*
    map<int, string> playersA = {{0,"Starrok"},
                                 {1, "Aberrat"},
                                 {2, "Strohkopf"},
                                 {3,"Servius"},
                                 {4,"Candid"},
                                 {5, "Burrito"},
                                 {6,"Sharlatan"},
                                 {7,"Uzh"}};
    */
    vector<string> playersA = {"Starrok", "Aberrat", "Strohkopf", "Servius", "Candid", "Burrito", "Sharlatan", "Uzh"};


    vector<ParingGame8*> pgs;
    int alpha = ss.min_team_score, beta = ss.max_team_score;
    int global_alpha = ss.min_team_score;
    int scores[STEP_1_THREADS];
    int best_score = ss.min_team_score;
    ParingGame8 pg_main(&ss, &ts);

    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    vector<thread*> threads;

    printf("First round calculating... (may take couple of minutes)\n");
    for( int i = 0; i < STEP_1_THREADS ; i++){
        TablesState* ts_copy = new TablesState(ts);
        ScoreSheetTables *sst_copy = new ScoreSheetTables(ss);
        ParingGame8* pg = new ParingGame8(sst_copy, ts_copy);
        pg->teamA.set_defender(FIRST,i);
        pg->global_alpha = &global_alpha;
        pgs.push_back(pg);
        int s1, s2;
        //printf("Launching %i item...\n",i);
        thread* th = new thread(&ParingGame8::min, pgs[i], FIRST, DEFENDER, alpha, beta, scores+i, &s1, &s2);
        threads.push_back(th);
    }

    for( int i = 0; i < STEP_1_THREADS ; i++){
        threads[i]->join();
        printf("[%i: %s]: %i\n", i, playersA[i].c_str(),*(scores+i));
        if( best_score < *(scores+i) )
            best_score = *(scores+i);
    }
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "First step took " << std::chrono::duration_cast<std::chrono::minutes>(end - begin).count() << "[min]" << std::endl;

    printf("Please choose TeamA first defender, recomended players with highest score (%i):",best_score);
    for( int i = 0 ; i < 8 ; i++){
        if( *(scores+i) == best_score)
            printf("[%i: %s], ",i, playersA[i].c_str());
    }
    //printf("\n");
    int d1a = pg_main.input_defender(&(pg_main.teamA));
    pg_main.teamA.set_defender(FIRST, d1a);
    printf("Please choose TeamB first defender");
    int d1b = pg_main.input_defender(&(pg_main.teamB));
    pg_main.teamB.set_defender(FIRST, d1b);

    int score, s1, s2;
    pg_main.max(FIRST, ATACKERS, alpha, beta, &score, &s1, &s2);
    printf("Team A: recomend to atack with %i and %i, score will be %i", s1, s2, score);
    int a11a, a12a;
    pg_main.input_atakers(&(pg_main.teamA),&a11a, &a12a);
    pg_main.teamA.set_atackers(FIRST, a11a, a12a);

    printf("Set TeamB atackers");
    int a11b, a12b;
    pg_main.input_atakers(&(pg_main.teamB),&a11b, &a12b);
    pg_main.teamB.set_atackers(FIRST, a11b, a12b);

    pg_main.max(FIRST, CHOOSE, alpha, beta, &score, &s1, &s2);
    printf("TeamA: recomend to choose player %i, score will be %i", s1, score);

    return 0;
}
