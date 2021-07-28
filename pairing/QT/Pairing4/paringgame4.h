#ifndef PARINGGAME4_H
#define PARINGGAME4_H
#include "scoresheettables.h"
#include "gamestate4.h"
#include "tablesstate.h"
#include "string"

#define STAGES_NUM 1
#define PLAYERS_NUM 4

enum STAGES{ FIRST_AND_ONLY };
enum PHASES{ DEFENDER, ATACKERS, CHOOSE, TABLE_DEF, TABLE_REJ};

class ParingGame4
{
public:
    ParingGame4(ScoreSheetTables*, TablesState*);

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
    int input_defender(GameState4* team);
    void input_atakers(GameState4* team, int*a1, int*a2);
    int input_choose(GameState4* team, int stage);
    int input_table();
    bool input_rolloff(std::string rolloff);

    void reset();

    TablesState* TS;
    ScoreSheetTables* SS;
    GameState4 teamA;
    GameState4 teamB;
private:
};

#endif // PARINGGAME4_H
