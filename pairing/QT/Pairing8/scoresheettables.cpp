#include "scoresheettables.h"
# include <stdio.h>
#include <QRandomGenerator>

ScoreSheetTables::ScoreSheetTables()
{

}

ScoreSheetTables::ScoreSheetTables(int*** sheet, int players, int tables_types, float min, float max){
    min_player_score = min;
    max_player_score = max;
    min_team_score = min * players;
    max_team_score = max * players;
    this->players = players;
    this->tables_types = tables_types;
    scores = sheet;
}

ScoreSheetTables::ScoreSheetTables(int players, int tables_types, float min, float max){
    this->players = players;
    this->tables_types = tables_types;
    min_player_score = min;
    max_player_score = max;
    min_team_score = min * players;
    max_team_score = max * players;

    scores = new int**[players];
    for( int i = 0 ; i < players; i++){
        scores[i] = new int*[players];
        for( int j = 0 ; j < players; j++)
            scores[i][j] = new int[tables_types];
    }

    for( int i = 0 ; i < players; i++){
        for( int j = 0 ; j < players; j++){
            for( int k = 0 ; k < tables_types; k++){
                scores[i][j][k] = QRandomGenerator::global()->bounded(min_player_score, max_player_score+1);
            }
        }
    }
}

int ScoreSheetTables::ind(int i, int j, int k){
    //printf("%i %i %i\n",i,j,k);
    return scores[i][j][k];
}

void ScoreSheetTables::print(){
    printf("Score sheet:\n");
    for(int i = 0 ; i < players; i++){
        printf("[");
        for(int j = 0; j < players; j++){
            printf("(");
            for( int k = 0 ; k < tables_types; k++){
                printf(" %i", ind(i,j,k));
            }
            printf(") ");
        }
        printf("]\n");
    }
    printf("\n");
}

float ScoreSheetTables::mean(){
    int sum = 0;
    for(int i = 0 ; i < players; i++){
        for(int j = 0; j < players; j++){
            for( int k = 0 ; k < tables_types; k++){
                sum += ind(i,j,k);
            }
        }
    }
    return float(sum) / (players * tables_types);
}
