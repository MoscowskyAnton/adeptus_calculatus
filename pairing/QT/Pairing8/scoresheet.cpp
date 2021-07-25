#include "scoresheet.h"
# include <stdio.h>
#include <QRandomGenerator>

ScoreSheet::ScoreSheet()
{

}

ScoreSheet::ScoreSheet(int** sheet, int players, float min, float max){
    min_player_score = min;
    max_player_score = max;
    min_team_score = min * players;
    max_team_score = max * players;
    this->players = players;
    scores = sheet;
}

ScoreSheet::ScoreSheet(int players, float min, float max){
    this->players = players;
    min_player_score = min;
    max_player_score = max;
    min_team_score = min * players;
    max_team_score = max * players;

    scores = new int*[players];
    for( int i = 0 ; i < players; i++)
        scores[i] = new int[players];

    for( int i = 0 ; i < players; i++){
        for( int j = 0 ; j < players; j++){
            scores[i][j] = QRandomGenerator::global()->bounded(min_player_score, max_player_score+1);
        }
    }
}

int ScoreSheet::ind(int i, int j){
    return scores[i][j];
}

void ScoreSheet::print(){
    printf("Score sheet:\n");
    for(int i = 0 ; i < players; i++){
        printf("[");
        for(int j = 0; j < players; j++){
            printf(" %i", ind(i,j));
        }
        printf("]\n");
    }
    printf("\n");
}

float ScoreSheet::mean(){
    int sum = 0;
    for(int i = 0 ; i < players; i++){
        for(int j = 0; j < players; j++){
            sum += ind(i,j);
        }
    }
    return float(sum) / players;
}
