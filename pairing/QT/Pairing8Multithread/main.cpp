#include <iostream>
#include "../Pairing8/scoresheettables.h"
#include "../Pairing8/paringgame8.h"
#include "stdio.h"
#include "../Pairing8/tablesstate.h"

#include <thread>
#include <future>

#include <vector>
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



    vector<ParingGame8*> pgs;
    int alpha = ss.min_team_score, beta = ss.max_team_score;
    int global_alpha = ss.min_team_score;
    int scores[STEP_1_THREADS];
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    vector<thread*> threads;
    for( int i = 0; i < STEP_1_THREADS ; i++){
        TablesState* ts_copy = new TablesState(ts);
        ScoreSheetTables *sst_copy = new ScoreSheetTables(ss);
        ParingGame8* pg = new ParingGame8(sst_copy, ts_copy);
        pg->teamA.set_defender(FIRST,i);
        pg->global_alpha = &global_alpha;
        pgs.push_back(pg);
        int score, s1, s2;
        printf("Launching %i item...\n",i);
        //auto future = async(std::launch::async, &ParingGame8::min, &pg, FIRST, DEFENDER, alpha, beta, scores+i, &s1, &s2);
        thread* th = new thread(&ParingGame8::min, pgs[i], FIRST, DEFENDER, alpha, beta, scores+i, &s1, &s2);
        threads.push_back(th);
    }

    for( int i = 0; i < STEP_1_THREADS ; i++){
        threads[i]->join();
        printf("score %i is %i\n",i,*(scores+i));
    }
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::minutes>(end - begin).count() << "[min]" << std::endl;

    return 0;
}
