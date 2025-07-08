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
#define TABLE_TYPES_NUM 1

using namespace std;

int simplefunc(std::string a)
{
    return a.size();
}

int main()
{

    int scores_table[8][8] = {{1,1,1,1,0,1,-2,0},
                    {0,-2,0,-1,0,-1,-1,1},
                    {-2,-1,-2,-2,-1,-1,-2,-1},
                    {1,-1,0,0,0,0,0,-1},
                    {-1,0,-1,0,-2,-1,-1,2},
                    {1,1,1,1,0,1,0,1},
                    {-2,-1,-1,-1,-1,1,-1,1},
                    {1,1,0,0,0,0,-1,1}};


    int*** sheet = new int**[8];
    for( int i = 0 ; i < 8; i++){
        sheet[i] = new int*[8];
        for( int j = 0 ; j < 8; j++){
            sheet[i][j] = new int[1];
            sheet[i][j][0] = scores_table[i][j];
        }
    }

//    int*** sheet;
//    sheet = new int**[8];
//    for( int i = 0 ; i < 8 ; i++){
//        sheet[i] = new int*[8];
//        for(int j = 0 ; j < 8 ; j++){
//            sheet[i][j] = new int;
//            sheet[i][j][0] = scores[i][j];
//        }
//    }

    ScoreSheetTables ss(sheet, 8, TABLE_TYPES_NUM, -2, 2);
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
    //vector<string> playersB = {"B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"};

    //vector<string> playersB = {"Harlequins","Tyranids",	"Necrons",	"Grey Knights",	"Thousand Sons",	"Tau",	"Orks",	"Craftworlds"};
    //vector <string> playersB = {"Craftworlds","Tau","Space Wolves","Harly","Adeptus Mechanicus",	"Adeptus Custodes","Drukhari",	"Tyranids"};
    vector<string> playersB = {"Adeptus Astartes - Black Templars",	"Adeptus Mechanicus",	"Adeptus Custodes",	"Orks",	"Tyranids",	"CSM/CD/DG",	"Tau",	"Craftworlds"};
    //vector<string> playersB = {"Adeptus Mechanicus","Space Marines","Tau",	"Drukhari","Harlequins","Adeptus Custodes","Orks","Death Guard"};


    vector<ParingGame8*> pgs;
    int alpha = ss.min_team_score, beta = ss.max_team_score;    
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

    int score, s1, s2;
    for( int stage = FIRST ; stage <= THRID; stage++){
          printf("ENEMIES!\n");
          for ( int i = 0 ; i < playersB.size(); i++)
              printf("[%i %s] ",i, playersB[i].c_str());
          printf("\n");
        printf("======== ROUND %i =========\n",stage);
        if( stage != 0 ){
            pg_main.max(stage, DEFENDER, alpha, beta, &score, &s1, &s2);
            printf("TeamA: recomend to defend with [%i %s], score will be %i\n",s1, playersA[s1].c_str(), score);
        }
        else{
            printf("Please choose TeamA first defender, recomended players with highest score (%i):",best_score);
            for( int i = 0 ; i < 8 ; i++){
                if( *(scores+i) == best_score)
                    printf("[%i: %s], ",i, playersA[i].c_str());
            }
        }
        int d1a = pg_main.input_defender(&(pg_main.teamA));
        pg_main.teamA.set_defender(stage, d1a);

        printf("Please choose TeamB first defender");
        int d1b = pg_main.input_defender(&(pg_main.teamB));
        pg_main.teamB.set_defender(stage, d1b);


        pg_main.max(stage, ATACKERS, alpha, beta, &score, &s1, &s2);
        printf("Team A: recomend to atack with [%i: %s] and [%i: %s], score will be %i", s1, playersA[s1].c_str(), s2, playersA[s2].c_str(), score);
        //int a11a, a12a;
        int a_atackers[2];
        pg_main.input_atakers(&(pg_main.teamA), a_atackers, a_atackers+1);
        pg_main.teamA.set_atackers(stage, a_atackers[0], a_atackers[1]);

        printf("Please set TeamB atackers");
        //int a11b, a12b;
        int b_atackers[2];
        pg_main.input_atakers(&(pg_main.teamB), b_atackers, b_atackers+1);
        pg_main.teamB.set_atackers(stage, b_atackers[0], b_atackers[1]);

        pg_main.max(stage, CHOOSE, alpha, beta, &score, &s1, &s2);
        printf("TeamA: recomend to choose [%i: %s] (type %i) atacker, score will be %i", b_atackers[s1], playersB[b_atackers[s1]].c_str(), s1, score);
        int ca = pg_main.input_choose(&(pg_main.teamB), stage);
        pg_main.teamB.choose_atacker(stage, ca);

        printf("Please set TeamB choose: [%s] (type 0), [%s] (type 1)", playersA[a_atackers[0]].c_str(), playersA[a_atackers[1]].c_str());
        int cb = pg_main.input_choose(&(pg_main.teamA), stage);
        pg_main.teamA.choose_atacker(stage, cb);


    }

    return 0;
}
