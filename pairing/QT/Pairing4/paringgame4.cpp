#include "paringgame4.h"
#include "stdio.h"
#include <QRandomGenerator>

ParingGame4::ParingGame4(ScoreSheetTables* ss, TablesState* ts)
{
    SS = ss;
    TS = ts;
}

void ParingGame4::reset(){
    teamA.reset();
    teamB.reset();
}

int ParingGame4::get_score(){
    int score = 0;
    for( int i = 0 ; i < STAGES_NUM; i++){
        score += SS->ind(teamA.stages[i].defender, teamB.stages[i].choosed_atacker, TS->tables_types[TS->teamAdefenderTable]);
        score += SS->ind(teamA.stages[i].choosed_atacker, teamB.stages[i].defender, TS->tables_types[TS->teamBdefenderTable]);
    }
    score += SS->ind(teamA.rejected_last_atacker, teamB.rejected_last_atacker, TS->tables_types[TS->rejectedPlayersTable]);
    score += SS->ind(teamA.champion, teamB.champion, TS->tables_types[TS->championsPlayersTable]);
    return score;
}

void ParingGame4::print_results(){
    int tsc = get_score();
    printf("teamA: %i teamB: %i\n", tsc, (SS->max_team_score + SS->min_team_score) - tsc);

    for(int i = 0 ; i < STAGES_NUM; i++){
        printf("A(%i)def vs B(%i)at on table no%i(type%i) = %i\n",teamA.stages[i].defender, teamB.stages[i].choosed_atacker, TS->teamAdefenderTable, TS->tables_types[TS->teamAdefenderTable],SS->ind(teamA.stages[i].defender, teamB.stages[i].choosed_atacker,TS->tables_types[TS->teamAdefenderTable]));
        printf("A(%i)at vs B(%i)def on table no%i(type%i) = %i\n",teamA.stages[i].choosed_atacker, teamB.stages[i].defender, TS->teamBdefenderTable, TS->tables_types[TS->teamBdefenderTable],SS->ind(teamA.stages[i].choosed_atacker, teamB.stages[i].defender,TS->tables_types[TS->teamBdefenderTable]));
    }
    printf("A(%i)rej vs B(%i)rej on table no%i(type%i) = %i\n",teamA.rejected_last_atacker, teamB.rejected_last_atacker, TS->rejectedPlayersTable, TS->tables_types[TS->rejectedPlayersTable],SS->ind(teamA.rejected_last_atacker, teamB.rejected_last_atacker,TS->tables_types[TS->rejectedPlayersTable]));
    printf("A(%i)champ vs B(%i)champ on table no%i(type%i) = %i\n",teamA.champion, teamB.champion, TS->championsPlayersTable, TS->tables_types[TS->championsPlayersTable],SS->ind(teamA.champion, teamB.champion,TS->tables_types[TS->championsPlayersTable]));
}

void ParingGame4::make_random_move(char team_name, int stage, int phase){
    GameState4* team;
    GameState4* team_;
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

void ParingGame4::play_random(){
    for( int i = 0 ; i < STAGES_NUM; i++){
        make_random_move('A', i, DEFENDER);
        make_random_move('B', i, DEFENDER);

        make_random_move('A', i, ATACKERS);
        make_random_move('B', i, ATACKERS);

        make_random_move('B', i, CHOOSE);
        make_random_move('A', i, CHOOSE);
    }
}

void ParingGame4::max(int stage, int phase, int alpha, int beta, int *score, int *selected_player1, int *selected_player2){
    *score = SS->min_team_score;

    if(phase == DEFENDER){
        for(int i = 0 ; i < PLAYERS_NUM; i++){
//            if( stage == FIRST){
//                printf("Calculating defender %i for team A\n",i);
//            }
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
        for(int i = 0; i < PLAYERS_NUM; i++){
            for(int j = i+1; j < PLAYERS_NUM; j++){
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
    else if(phase == TABLE_DEF){
        for(int i = 0 ; i < TS->tables_number; i++){
            if(TS->tables_free[i]){
                TS->selectDefenderTable('A', i);
                int new_score, s1, s2;
                if(TS->teamA_won_1_rolloff){
                    min(stage, phase, alpha, beta, &new_score, &s1, &s2);
                }
                else{
                    if(TS->teamA_won_2_rolloff){
                        max(stage, TABLE_REJ, alpha, beta, &new_score, &s1, &s2);
                    }
                    else{
                        min(stage, TABLE_REJ, alpha, beta, &new_score, &s1, &s2);
                    }
                }
                if( new_score > *score){
                    *score = new_score;
                    *selected_player1 = i;
                }
                TS->unselectDefenderTable('A');
                if(*score >= beta){
                    break;
                }
                if(*score > alpha){
                    alpha = *score;
                }
            }
        }
    }
    else if(phase == TABLE_REJ){
        for(int i = 0; i < TS->tables_number; i++){
            if(TS->tables_free[i]){
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
            }
        }
    }
    else{
        printf("ERROR! Unknown phase %i",phase);
    }
}

void ParingGame4::min(int stage, int phase, int alpha, int beta, int *score, int *selected_player1, int *selected_player2){
    *score = SS->max_team_score;

    if(phase == DEFENDER){
        for(int i = 0 ; i < PLAYERS_NUM; i++){
//            if( stage == FIRST){
//                printf("\tCalculating defender %i for team B\n",i);
//            }
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
        for(int i = 0; i < PLAYERS_NUM; i++){
            for(int j = i+1; j < PLAYERS_NUM; j++){
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
//            if(stage > 1)
//                new_score = get_score();
//            else
//                max(stage+1, DEFENDER, alpha, beta, &new_score, &s1, &s2);
            if(TS->teamA_won_1_rolloff){
                max(stage, TABLE_DEF, alpha, beta, &new_score, &s1, &s2);
            }
            else{
                min(stage, TABLE_DEF, alpha, beta, &new_score, &s1, &s2);
            }
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
    else if(phase == TABLE_DEF){
        for(int i = 0 ; i < TS->tables_number; i++){
            if(TS->tables_free[i]){
                TS->selectDefenderTable('B', i);
                int new_score, s1, s2;
                if(!TS->teamA_won_1_rolloff){
                    max(stage, phase, alpha, beta, &new_score, &s1, &s2);
                }
                else{
                    if(TS->teamA_won_2_rolloff){
                        max(stage, TABLE_REJ, alpha, beta, &new_score, &s1, &s2);
                    }
                    else{
                        min(stage, TABLE_REJ, alpha, beta, &new_score, &s1, &s2);
                    }
                }
                if( new_score < *score){
                    *score = new_score;
                    *selected_player1 = i;
                }
                TS->unselectDefenderTable('B');
                if(*score <= alpha){
                    break;
                }
                if(*score < beta){
                    beta = *score;
                }
            }
        }
    }
    else if(phase == TABLE_REJ){
        for(int i = 0; i < TS->tables_number; i++){
            if(TS->tables_free[i]){
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
                    beta= *score;
                }
            }
        }
    }
    else{
        printf("ERROR! Unknown phase %i",phase);
    }
}

int ParingGame4::make_optimal_move(char team, int stage, int phase, int *selected_player1, int* selected_player2){
    int alpha = SS->min_team_score;
    int beta = SS->max_team_score;

    int score, s1, s2;
    GameState4* team_, *team_2;
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
    else if(phase == TABLE_DEF){
        TS->selectDefenderTable(team, s1);
    }
    else if(phase == TABLE_REJ){
        TS->selectRejectedTable(s1);
    }
    *selected_player1 = s1;
    *selected_player2 = s2;
    return score;
}

void ParingGame4::play_optimal(){
    int s1, s2;
    for(int i = 0 ; i < STAGES_NUM; i++){
        printf("Stage %i\n",i);

        make_optimal_move('A', i, DEFENDER, &s1, &s2);
        make_optimal_move('B', i, DEFENDER, &s1, &s2);

        make_optimal_move('A', i, ATACKERS, &s1, &s2);
        make_optimal_move('B', i, ATACKERS, &s1, &s2);

        make_optimal_move('A', i, CHOOSE, &s1, &s2);
        make_optimal_move('B', i, CHOOSE, &s1, &s2);

        if( TS->teamA_won_1_rolloff){
            make_optimal_move('A',i,TABLE_DEF,&s1, &s2);
            make_optimal_move('B',i,TABLE_DEF,&s1, &s2);
        }
        else{
            make_optimal_move('B',i,TABLE_DEF,&s1, &s2);
            make_optimal_move('A',i,TABLE_DEF,&s1, &s2);
        }
        if( TS->teamA_won_2_rolloff){
            make_optimal_move('A',i,TABLE_REJ,&s1, &s2);
        }
        else{
            make_optimal_move('B',i,TABLE_REJ,&s1, &s2);
        }
    }
}

void ParingGame4::play_optimal_vs_random(){
    int s1, s2;
    for(int i = 0 ; i < STAGES_NUM; i++){
        make_optimal_move('A', i, DEFENDER, &s1, &s2);
        make_random_move('B', i, DEFENDER);

        make_optimal_move('A', i, ATACKERS, &s1, &s2);
        make_random_move('B', i, ATACKERS);

        make_optimal_move('A', i, CHOOSE, &s1, &s2);
        make_random_move('B', i, CHOOSE);
    }
}

int ParingGame4::input_defender(GameState4* team){
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

void ParingGame4::input_atakers(GameState4* team, int*a1, int*a2){
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

int ParingGame4::input_choose(GameState4* team, int stage){
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

bool ParingGame4::input_rolloff(std::string rolloff){
    int roll;
    while(true){
        printf("\n\tInput result of %s table roll off (1 - team A won, 0 - team A lost): ", rolloff.c_str());
        scanf("%i",&roll);
        if(roll != 0 && roll != 1){
            printf("Result must be 0 or 1");
        }
        else{
            return bool(roll);
        }
    }
}

int ParingGame4::input_table(){
    int table;
    while(true){
        printf("\n\tInput selected table: ");
        scanf("%i",&table);
        if(TS->tables_free[table]){
            return table;
        }
        else{
            printf("This table already taken!");
        }
    }
}

void ParingGame4::play_with_input(){
    int s1, s2, score;
    int alpha = SS->min_team_score;
    int beta = SS->max_team_score;

    for( int step = 0; step < STAGES_NUM; step++){
        TS->teamA_won_1_rolloff = input_rolloff("fisrt");

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
        int b1, b2;
        input_atakers(&teamB, &b1, &b2);
        teamB.set_atackers(step, b1, b2);

        max(step, CHOOSE, alpha, beta, &score, &s1, &s2);
        printf("Team A: recomend to choose %i, score will be %i", s1, score);
        int ac1 = input_choose(&teamB, step);
        teamB.choose_atacker(step, ac1);

        min(step, CHOOSE, alpha, beta, &score, &s1, &s2);
        printf("Team B: recomend to choose %i, score will be %i", s1, score);
        int bc1 = input_choose(&teamA, step);
        teamA.choose_atacker(step, bc1);

        if(TS->teamA_won_1_rolloff){
            max(step, TABLE_DEF, alpha, beta, &score, &s1, &s2);
            printf("Team A: recomend to take table no%i(type%i), score will be %i", s1, TS->tables_types[s1], score);
            int dt = input_table();
            TS->selectDefenderTable('A',dt);

            min(step, TABLE_DEF, alpha, beta, &score, &s1, &s2);
            printf("Team B: recomend to take table no%i(type%i), score will be %i", s1, TS->tables_types[s1], score);
            dt = input_table();
            TS->selectDefenderTable('B',dt);
        }
        else{
            min(step, TABLE_DEF, alpha, beta, &score, &s1, &s2);
            printf("Team B: recomend to take table for defender no%i(type%i), score will be %i", s1, TS->tables_types[s1], score);
            int dt = input_table();
            TS->selectDefenderTable('A',dt);

            max(step, TABLE_DEF, alpha, beta, &score, &s1, &s2);
            printf("Team A: recomend to take table for defender no%i(type%i), score will be %i", s1, TS->tables_types[s1], score);
            dt = input_table();
            TS->selectDefenderTable('B',dt);
        }
        TS->teamA_won_2_rolloff = input_rolloff("second");
        if(TS->teamA_won_2_rolloff){
            max(step, TABLE_REJ, alpha, beta, &score, &s1, &s2);
            printf("Team A: recomend to take table for rejected no%i(type%i), score will be %i", s1, TS->tables_types[s1], score);
            int rt = input_table();
            TS->selectRejectedTable(rt);
        }
        else{
            min(step, TABLE_REJ, alpha, beta, &score, &s1, &s2);
            printf("Team B: recomend to take table for rejected no%i(type%i), score will be %i", s1, score);
            int rt = input_table();
            TS->selectRejectedTable(rt);
        }
    }
    print_results();
}
