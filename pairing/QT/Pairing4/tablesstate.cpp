#include "tablesstate.h"
#include <QRandomGenerator>

TablesState::TablesState(int tables_types_num, int tables_number, bool first_rolloff, bool second_rolloff)
{
    this->tables_types_num = tables_types_num;
    this->tables_number = tables_number;
    this->teamA_won_1_rolloff = first_rolloff;
    this->teamA_won_2_rolloff = second_rolloff;

    tables_types = new int[tables_number];
    tables_free = new bool[tables_number];
    for( int i = 0 ; i < tables_number; i++){
        tables_types[i] = QRandomGenerator::global()->bounded(0, tables_types_num);
        tables_free[i] = true;
    }
}

TablesState::TablesState(int* tables_types, int tables_types_num, int tables_number, bool first_rolloff, bool second_rolloff)
{
    this->teamA_won_1_rolloff = first_rolloff;
    this->teamA_won_2_rolloff = second_rolloff;
    this->tables_types_num = tables_types_num;
    this->tables_number = tables_number;
    this->tables_types = tables_types;
}

void TablesState::selectDefenderTable(char team, int table_id){
    if( team == 'A'){
        teamAdefenderTable = table_id;
    }
    else{
        teamBdefenderTable = table_id;
    }
    tables_free[table_id] = false;
}

void TablesState::unselectDefenderTable(char team){
    if(team == 'A'){
        tables_free[teamAdefenderTable] = true;
        teamAdefenderTable = -1;
    }
    else{
        tables_free[teamBdefenderTable] = true;
        teamBdefenderTable = -1;
    }
}

void TablesState::selectRejectedTable(int table_id){
    tables_free[table_id] = false;
    rejectedPlayersTable = table_id;
    for( int i = 0 ; i < tables_number; i++){
        if( tables_free[i]){
            championsPlayersTable = i;
            tables_free[i] = false;
            break;
        }
    }
}

void TablesState::unselectRejectedTable(){
    tables_free[rejectedPlayersTable] = true;
    tables_free[championsPlayersTable] = true;
    rejectedPlayersTable = -1;
    championsPlayersTable = -1;
}

void TablesState::print(){
    printf("-- Tables Types --\n");
    for( int i = 0 ; i < tables_number; i++){
        printf("%i ",tables_types[i]);
    }

}
