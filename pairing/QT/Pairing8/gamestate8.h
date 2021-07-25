#ifndef GAMESTATE8_H
#define GAMESTATE8_H

class GameStage
{
public:
    GameStage(){
        defender =-1;
        atacker1 =-1;
        atacker2 =-1;
        choosed_atacker =-1;
    }
    int defender;
    int atacker1;
    int atacker2;
    int choosed_atacker;
};

class GameState8
{
public:
    GameState8();

    void set_defender(int stage, int player);
    void set_atackers(int stage, int player1, int player2);
    void choose_atacker(int stage, int choosed_player);

    void unset_defender(int stage);
    void unset_atackers(int stage);
    void unchoose_atacker(int stage);

    int get_free_player();
    void get_pair_free_players(int* i, int* j);

    void reset();

    bool* free;
    GameStage* stages;
    int rejected_last_atacker;
    int champion;
};

#endif // GAMESTATE8_H
