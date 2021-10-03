#include "paringgame8.h"
#include "stdio.h"
#include <QRandomGenerator>

//#define DEBUG_STEPS

ParingGame8::ParingGame8(ScoreSheetTables* ss, TablesState* ts)
{
    SS = ss;
    TS = ts;
}

void ParingGame8::reset(){
    teamA.reset();
    teamB.reset();
}

int ParingGame8::get_score(){
    int score = 0;
    for( int i = 0 ; i < 3; i++){
        score += SS->ind(teamA.stages[i].defender, teamB.stages[i].choosed_atacker, TS->tables_types[TS->teamAdefenderTable[i]]);
        score += SS->ind(teamA.stages[i].choosed_atacker, teamB.stages[i].defender, TS->tables_types[TS->teamBdefenderTable[i]]);
    }
    score += SS->ind(teamA.rejected_last_atacker, teamB.rejected_last_atacker, TS->tables_types[TS->rejectedPlayersTable]);
    score += SS->ind(teamA.champion, teamB.champion, TS->tables_types[TS->championsPlayersTable]);
    return score;
}

void ParingGame8::print_results(){
    int tsc = get_score();
    printf("teamA: %i teamB: %i\n", tsc, (SS->max_team_score + SS->min_team_score) - tsc);

    for(int i = 0 ; i < 3; i++){
        printf("A(%i)def vs B(%i)at = %i\n",teamA.stages[i].defender, teamB.stages[i].choosed_atacker, SS->ind(teamA.stages[i].defender, teamB.stages[i].choosed_atacker, TS->tables_types[TS->teamAdefenderTable[i]]));
        printf("A(%i)at vs B(%i)def = %i\n",teamA.stages[i].choosed_atacker, teamB.stages[i].defender, SS->ind(teamA.stages[i].choosed_atacker, teamB.stages[i].defender, TS->tables_types[TS->teamBdefenderTable[i]]));
    }
    printf("A(%i)rej vs B(%i)rej = %i\n",teamA.rejected_last_atacker, teamB.rejected_last_atacker, SS->ind(teamA.rejected_last_atacker, teamB.rejected_last_atacker, TS->tables_types[TS->rejectedPlayersTable]));
    printf("A(%i)champ vs B(%i)champ = %i\n",teamA.champion, teamB.champion, SS->ind(teamA.champion, teamB.champion, TS->tables_types[TS->championsPlayersTable]));
}

void ParingGame8::make_random_move(char team_name, int stage, int phase){
    GameState8* team;
    GameState8* team_;
    if( team_name == 'A'){
        team = &teamA;
        team_= &teamB;
    }
    else{
        team = &teamB;
        team_ = &teamA;
    }
    if( phase == DEFENDER){
        int def = team->get_free_player();
        team->set_defender(stage, def);
    }
    else if( phase == ATACKERS){
        int a1, a2;
        team->get_pair_free_players(&a1,&a2);
        team->set_atackers(stage, a1, a2);
    }
    else if( phase == CHOOSE){
        int choosed = QRandomGenerator::global()->bounded(0,2);
        team_->choose_atacker(stage, choosed);
    }
    else{
        printf("ERROR! Unknown stage %i", phase);
    }
}

void ParingGame8::play_random(){
    for( int i = 0 ; i < 3; i++){
        make_random_move('A', i, DEFENDER);
        make_random_move('B', i, DEFENDER);

        make_random_move('A', i, ATACKERS);
        make_random_move('B', i, ATACKERS);

        make_random_move('B', i, CHOOSE);
        make_random_move('A', i, CHOOSE);
    }
}

//
// MAX
//
void ParingGame8::max(int stage, int phase, int alpha, int beta, int *score, int *selected_player1, int *selected_player2){
    *score = SS->min_team_score;

    if(phase == DEFENDER){
        for(int i = 0 ; i < 8; i++){
            if( stage == FIRST){
              printf("Calculating defender %i for team A on stage %i\n",i,stage);
            }
            if(teamA.free[i]){
                teamA.set_defender(stage, i);
                int new_score, s1, s2;
                min(stage, phase, alpha, beta, &new_score, &s1, &s2);
                if( new_score > *score){
                    *score = new_score;
                    *selected_player1 = i;
                }
                teamA.unset_defender(stage);
                if(*score >= beta){
                    break;
                }
                if(*score > alpha){
                    alpha = *score;
                }
            }
        }
    }
    else if(phase == ATACKERS){
        for(int i = 0; i < 8; i++){
            for(int j = i+1; j < 8; j++){
                if( teamA.free[i] && teamA.free[j]){
                    teamA.set_atackers(stage,i,j);
                    int new_score, s1, s2;
                    min(stage, phase, alpha, beta, &new_score, &s1, &s2);
                    if( new_score > *score){
                        *score = new_score;
                        *selected_player1 = i;
                        *selected_player2 = j;
                    }
                    teamA.unset_atackers(stage);
                    if(*score >= beta){
                        break;
                    }
                    if(*score > alpha){
                        alpha = *score;
                    }
                }
            }
        }
    }
    else if(phase == CHOOSE){
        for(int i = 0; i < 2; i++){
            teamB.choose_atacker(stage, i);
            int new_score, s1, s2;
            min(stage, phase, alpha, beta, &new_score, &s1, &s2);
            if( new_score > *score){
                *score = new_score;
                *selected_player1 = i;
            }
            teamB.unchoose_atacker(stage);
            if(*score >= beta){
                break;
            }
            if(*score > alpha){
                alpha = *score;
            }
        }
    }
    else if(phase == TABLE_CHOOSE){
        if( stage < 3){
            for(int i = 0 ; i < TS->tables_number; i++){
                if( TS->tables_free[i] ){
                    TS->selectDefenderTable('A', i, stage);
                    int new_score, s1, s2;
                    if( stage == 2 && !TS->teamA_won_1_rolloff){
                        max(TS->teamA_won_1_rolloff ? stage : stage+1, phase, alpha, beta, &new_score, &s1, &s2);
                    }
                    else
                        min(TS->teamA_won_1_rolloff ? stage : stage+1, phase, alpha, beta, &new_score, &s1, &s2);
                    if( new_score > *score){
                        *score = new_score;
                        *selected_player1 = i;
                    }
                    TS->unselectDefenderTable('A', stage);
                    if(*score >= beta){
                        break;
                    }
                    if(*score > alpha){
                        alpha = *score;
                    }
                }
            }
        }
        // last choose
        else{
            for(int i = 0 ; i < TS->tables_number; i++){
                if( TS->tables_free[i] ){
                    TS->selectRejectedTable(i);
                    int new_score;
                    new_score = get_score();
                    if( new_score > *score){
                        *score = new_score;
                        *selected_player1 = i;
                    }
                    TS->unselectRejectedTable();
                    if(*score >= beta){
                        break;
                    }
                    if(*score > alpha){
                        alpha = *score;
                    }
#ifdef DEBUG_STEPS
                    printf("A END!\n");
#endif
                }
            }
        }
    }
    else{
        printf("ERROR! Unknown phase %i",phase);
    }
}

//
// MIN
//
void ParingGame8::min(int stage, int phase, int alpha, int beta, int *score, int *selected_player1, int *selected_player2){
    *score = SS->max_team_score;

    if(phase == DEFENDER){
        for(int i = 0 ; i < 8; i++){
            if( stage == FIRST){
                printf("\tCalculating defender %i for team B on stage %i\n",i,stage);
            }
            if(teamB.free[i]){
                teamB.set_defender(stage, i);
                int new_score, s1, s2;
                max(stage, ATACKERS, alpha, beta, &new_score, &s1, &s2);
                if( new_score < *score){
                    *score = new_score;
                    *selected_player1 = i;
                }
                teamB.unset_defender(stage);
                if(*score <= alpha){
                    break;
                }
                if(*score < beta){
                    beta = *score;
                }
            }
        }
    }
    else if(phase == ATACKERS){
        for(int i = 0; i < 8; i++){
            for(int j = i+1; j < 8; j++){
                if( teamB.free[i] && teamB.free[j]){
                    teamB.set_atackers(stage,i,j);
                    int new_score, s1, s2;
                    max(stage, CHOOSE, alpha, beta, &new_score, &s1, &s2);
                    if( new_score < *score){
                        *score = new_score;
                        *selected_player1 = i;
                        *selected_player2 = j;
                    }
                    teamB.unset_atackers(stage);
                    if(*score <= alpha){
                        break;
                    }
                    if(*score < beta){
                        beta = *score;
                    }
                }
            }
        }
    }
    else if(phase == CHOOSE){
        for(int i = 0; i < 2; i++){
            teamA.choose_atacker(stage, i);
            int new_score, s1, s2;
            if(stage == THRID ){
                //new_score = get_score();
                if( TS->teamA_won_1_rolloff ){
                    max(0, TABLE_CHOOSE, alpha, beta, &new_score, &s1, &s2);
                }
                else{
                    min(0, TABLE_CHOOSE, alpha, beta, &new_score, &s1, &s2);
                }
            }
            else
                max(stage+1, DEFENDER, alpha, beta, &new_score, &s1, &s2);
            if( new_score < *score){
                *score = new_score;
                *selected_player1 = i;
            }
            teamA.unchoose_atacker(stage);
            if(*score <= alpha){
                break;
            }
            if(*score < beta){
                beta = *score;
            }
        }
    }
    else if(phase == TABLE_CHOOSE){
        //printf("stage %i\n",stage);
        if( stage < 3){
            for(int i = 0 ; i < TS->tables_number; i++){
                if( TS->tables_free[i] ){
                    TS->selectDefenderTable('B', i, stage);
                    int new_score, s1, s2;
                    if( stage == 2 && TS->teamA_won_1_rolloff){
                        min(TS->teamA_won_1_rolloff ? stage+1 : stage, phase, alpha, beta, &new_score, &s1, &s2);
                    }
                    else
                        max(TS->teamA_won_1_rolloff ? stage+1 : stage, phase, alpha, beta, &new_score, &s1, &s2);
                    if( new_score < *score){
                        *score = new_score;
                        *selected_player1 = i;
                    }
                    TS->unselectDefenderTable('B', stage);
                    if(*score <= alpha){
                        break;
                    }
                    if(*score < beta){
                        beta = *score;
                    }
                }
            }
        }
        // last choose
        else{
            for(int i = 0 ; i < TS->tables_number; i++){
                if( TS->tables_free[i] ){
                    TS->selectRejectedTable(i);
                    int new_score;
                    new_score = get_score();
                    if( new_score < *score){
                        *score = new_score;
                        *selected_player1 = i;
                    }
                    TS->unselectRejectedTable();
                    if(*score <= alpha){
                        break;
                    }
                    if(*score < beta){
                        beta = *score;
                    }
#ifdef DEBUG_STEPS
                    printf("B END!\n");
#endif
                }

            }
        }
    }
    else{
        printf("ERROR! Unknown phase %i",phase);
    }
}

int ParingGame8::make_optimal_move(char team, int stage, int phase, int *selected_player1, int* selected_player2){
    int alpha = SS->min_team_score;
    int beta = SS->max_team_score;

    int score, s1, s2;
    GameState8* team_, *team_2;
    if(team == 'A'){
        max(stage, phase, alpha, beta, &score, &s1, &s2);
        team_ = &teamA;
        team_2 = &teamB;
    }
    else{
        min(stage, phase, alpha, beta, &score, &s1, &s2);
        team_ = &teamB;
        team_2 = &teamA;
    }
    if(phase == DEFENDER){
        team_->set_defender(stage, s1);
    }
    else if(phase == ATACKERS){
        team_->set_atackers(stage, s1, s2);
    }
    else if(phase == CHOOSE){
        team_2->choose_atacker(stage, s1);
    }
    *selected_player1 = s1;
    *selected_player2 = s2;
    return score;

}

void ParingGame8::play_optimal(){
    int s1, s2;
    for(int i = 0 ; i < 3; i++){
        printf("Stage %i\n",i);

        make_optimal_move('A', i, DEFENDER, &s1, &s2);
        make_optimal_move('B', i, DEFENDER, &s1, &s2);

        make_optimal_move('A', i, ATACKERS, &s1, &s2);
        make_optimal_move('B', i, ATACKERS, &s1, &s2);

        make_optimal_move('A', i, CHOOSE, &s1, &s2);
        make_optimal_move('B', i, CHOOSE, &s1, &s2);
    }
}

void ParingGame8::play_optimal_vs_random(){
    int s1, s2;
    for(int i = 0 ; i < 3; i++){
        make_optimal_move('A', i, DEFENDER, &s1, &s2);
        make_random_move('B', i, DEFENDER);

        make_optimal_move('A', i, ATACKERS, &s1, &s2);
        make_random_move('B', i, ATACKERS);

        make_optimal_move('A', i, CHOOSE, &s1, &s2);
        make_random_move('B', i, CHOOSE);
    }
}

int ParingGame8::input_defender(GameState8* team){
    int defender;
    printf("\n\tSelect defender: ");
    while(true){
       scanf("%i",&defender);
       if(defender >= SS->players){
           printf("Player number must be 0-%i",SS->players);
       }
       else{
           if(team->free[defender]){
               return defender;
           }
           else{
               printf("This player already taken!");
           }
       }
    }
}

void ParingGame8::input_atakers(GameState8* team, int*a1, int*a2){
    printf("\n\tSelect atacker 1: ");
    while(true){
        scanf("%i",a1);
        if(*a1 >= SS->players){
            printf("Player number must be 0-%i",SS->players);
        }
        else{
            if(team->free[*a1]){
                break;
            }
            else{
                printf("This player already taken!");
            }
        }
    }
    printf("\n\tSelect atacker 2: ");
    while(true){
        scanf("%i",a2);
        if(*a2 >= SS->players){
            printf("Player number must be 0-%i",SS->players);
        }
        else{
            if(*a1 != *a2){
                if(team->free[*a2]){
                    return;
                }
                else{
                    printf("This player already taken!");
                }
            }
            else{
                printf("Can't select the same player, you dumb!");
            }
        }
    }
}

int ParingGame8::input_choose(GameState8* team, int stage){
    int choose;
    while(true){
        printf("\n\tChoose atacker from %i (0) and %i (1): ",team->stages[stage].atacker1, team->stages[stage].atacker2);
        scanf("%i",&choose);
        if(choose != 0 && choose != 1){
            printf("Choose must be 0 or 1");
        }
        else{
            return choose;
        }
    }
}

int ParingGame8::input_table(){
    int table;
    while(true){
        printf("\n\tChoose table for player");
        scanf("%i", &table);
        if( table >= TS->tables_number){
            printf("Table must be from 0 - %i!", TS->tables_number-1);
        }
        if( TS->tables_free[table]){
            return table;
        }
        else{
            printf("This table taken already!");
        }
    }
}

void ParingGame8::play_with_input(){
    int s1, s2, score;
    int alpha = SS->min_team_score;
    int beta = SS->max_team_score;

    for( int step = 0; step < 3; step++){
        printf("Calculating %i step...\n",step);
        //score = make_optimal_move('A', DEFENDER, FIRST, &s1, &s2);
        max(step, DEFENDER, alpha, beta, &score, &s1, &s2);
        printf("Team A: recomend to defend with player %i, score will be %i", s1, score);
        //teamA.unset_defender(FIRST);
        int ad1 = input_defender(&teamA);
        teamA.set_defender(step, ad1);

        //score = make_optimal_move('B', DEFENDER, FIRST, &s1, &s2);
        min(step, DEFENDER, alpha, beta, &score, &s1, &s2);
        printf("Team B: recomend to defend with player %i, score will be %i", s1, score);
        //teamB.unset_defender(FIRST);
        int ad2 = input_defender(&teamB);
        teamB.set_defender(step, ad2);

        //score = make_optimal_move('A', ATACKERS, FIRST, &s1, &s2);
        max(step, ATACKERS, alpha, beta, &score, &s1, &s2);
        printf("Team A: recomend to atack with %i and %i, score will be %i", s1, s2, score);
        //teamA.unset_atackers(FIRST);
        int a1, a2;
        input_atakers(&teamA, &a1, &a2);
        teamA.set_atackers(step, a1, a2);

        //score = make_optimal_move('B', ATACKERS, FIRST, &s1, &s2);
        min(step, ATACKERS, alpha, beta, &score, &s1, &s2);
        printf("Team B: recomend to atack with %i and %i, score will be %i", s1, s2, score);
        //teamB.unset_atackers(FIRST);
        input_atakers(&teamB, &a1, &a2);
        teamB.set_atackers(step, a1, a2);

        max(step, CHOOSE, alpha, beta, &score, &s1, &s2);
        printf("Team A: recomend to choose %i, score will be %i", s1, score);
        int ac1 = input_choose(&teamB, step);
        teamB.choose_atacker(step, ac1);

        min(step, CHOOSE, alpha, beta, &score, &s1, &s2);
        printf("Team B: recomend to choose %i, score will be %i", s1, score);
        int bc1 = input_choose(&teamA, step);
        teamA.choose_atacker(step, bc1);
    }
    print_results();
}
