#ifndef PARINGGAME8_H
#define PARINGGAME8_H
//#include "scoresheet.h"
#include "scoresheettables.h"
#include "tablesstate.h"
#include "gamestate8.h"

enum STAGES{ FIRST, SECOND, THRID};
enum PHASES{ DEFENDER, ATACKERS, CHOOSE, TABLE_CHOOSE};

class ParingGame8
{
public:
    ParingGame8(ScoreSheetTables*, TablesState*);

    //~ParingGame8(ParingGame8 &&) = default;

    int get_score();
    void print_results();

    void make_random_move(char team, int stage, int phase);
    void play_random();

    void max(int stage, int phase, int alpha, int beta, int * score, int * selected_player1, int* selected_player2);
    void min(int stage, int phase, int alpha, int beta, int * score, int * selected_player1, int* selected_player2);

    int make_optimal_move(char team, int stage, int phase, int* selected_player1, int* selected_player2);
    void play_optimal();

    void play_optimal_vs_random();

    void play_with_input();
    int input_defender(GameState8* team);
    void input_atakers(GameState8* team, int*a1, int*a2);
    int input_choose(GameState8* team, int stage);
    int input_table();

    void reset();

    GameState8 teamA;
    GameState8 teamB;

    int* global_alpha;

private:
    ScoreSheetTables* SS;
    TablesState* TS;

};

#endif // PARINGGAME8_H
