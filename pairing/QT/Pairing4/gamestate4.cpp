#include "gamestate4.h"
#include <QRandomGenerator>

GameState4::GameState4()
{
    reset();
}

void GameState4::reset(){
    free = new bool[4];
    for(int i = 0 ; i < 4; i++)
        free[i] = true;
    stages = new GameStage[1];
    rejected_last_atacker =-1;
    champion = -1;
}

void GameState4::set_defender(int stage, int player)
{
    free[player] = false;
    stages[stage].defender = player;
}

void GameState4::unset_defender(int stage)
{
    free[stages[stage].defender] = true;
    stages[stage].defender = -1;
}

void GameState4::set_atackers(int stage, int player1, int player2)
{
    free[player1] = false;
    free[player2] = false;
    stages[stage].atacker1 = player1;
    stages[stage].atacker2 = player2;
}

void GameState4::unset_atackers(int stage)
{
    free[stages[stage].atacker1] = true;
    free[stages[stage].atacker2] = true;
    stages[stage].atacker1 = -1;
    stages[stage].atacker2 = -1;
}

void GameState4::choose_atacker(int stage, int choosed_player)
{
    if( choosed_player == 0){
        free[stages[stage].atacker1] = false;
        free[stages[stage].atacker2] = true;

        stages[stage].choosed_atacker = stages[stage].atacker1;
        //if(stage > 1){
            rejected_last_atacker = stages[stage].atacker2;
            free[rejected_last_atacker] = false;
            // set champion
            for( int i = 0 ; i < 4; i++){
                if( free[i] ){
                    free[i] = false;
                    champion = i;
                }
            }
        //}
    }
    else{
        free[stages[stage].atacker2] = false;
        free[stages[stage].atacker1] = true;

        stages[stage].choosed_atacker = stages[stage].atacker2;
        //if(stage > 1){
            rejected_last_atacker = stages[stage].atacker1;
            free[rejected_last_atacker] = false;
            // set champion
            for( int i = 0 ; i <4; i++){
                if( free[i] ){
                    free[i] = false;
                    champion = i;
                }
            }
        //}
    }
}

void GameState4::unchoose_atacker(int stage){
    free[stages[stage].choosed_atacker] = true;
    stages[stage].choosed_atacker = -1;

    //if(stage > 1){
        free[champion] = true;
        free[rejected_last_atacker] = true;
        champion = -1;
        rejected_last_atacker =-1;
    //}
}

int GameState4::get_free_player(){
    while(true){
        int i = QRandomGenerator::global()->bounded(0,4);
        if(free[i]){
            return i;
        }
    }
}

void GameState4::get_pair_free_players(int *i, int *j){
    while(true){
        *i = QRandomGenerator::global()->bounded(0,4);
        *j = QRandomGenerator::global()->bounded(0,4);
        if( *i!=*j && free[*i] && free[*j])
            break;
    }
}
