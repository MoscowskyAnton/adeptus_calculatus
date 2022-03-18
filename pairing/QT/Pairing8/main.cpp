#include <QCoreApplication>
#include "scoresheettables.h"
#include "paringgame8.h"
#include "stdio.h"
#include "tablesstate.h"
#include <chrono>
#include <iostream>


int main(int argc, char *argv[])
{
    //QCoreApplication a(argc, argv);


    int scores[8][8] = {{1,0,-2,-1,0,0,2,2},
                    {-1,-1,-1,-1,-2,-2,-1,-1},
                    {1,1,-1,-1,0,-1,1,1},
                    {0,0,-1,-2,-1,-1,0,0},
                    {2,0,-1,-2,1,-2,1,2},
                    {-1,-1,-2,-2,-1,0,1,0},
                    {-1,-1,-1,-2,-1,-1,-1,-1},
                    {1,1,-2,-1,1,0,1,1}};
    int*** sheet;
    sheet = new int**[8];
    for( int i = 0 ; i < 8 ; i++)
        sheet[i] = new int*[1];
        sheet[i][0] = scores[i];

    ScoreSheetTables ss(8, 3, -2, 2);

    ss.print();
    printf("Mean %f\n",ss.mean());

    TablesState ts(3, 8, true, false);
    ts.print();

    ParingGame8 pg(&ss, &ts);
    //pg.teamA.set_defender(FIRST, 0);

    int score, alpha = ss.min_team_score, beta = ss.max_team_score, s1, s2;
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    pg.max(DEFENDER, FIRST, alpha, beta, &score, &s1, &s2);
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Time difference = " << std::chrono::duration_cast<std::chrono::minutes>(end - begin).count() << "[min]" << std::endl;
    printf("Score = %i", score);
    //pg.play_random();
    //pg.play_with_input();


    /*
    pg.play_optimal();

    pg.print_results();
    int optimal_score = pg.get_score();
    int N = 10;
    int random_scores[N];

    for(int i = 0 ; i < N; i++){
        pg.reset();
        pg.play_optimal_vs_random();
        pg.print_results();
        random_scores[i] = pg.get_score();
    }

    printf("Optimal score: %i\n",optimal_score);
    printf("Random scroes: ");
    for(int i = 0 ; i < N; i++){
        printf("%i ",random_scores[i]);
    }
*/
    return 0;//a.exec();
}
