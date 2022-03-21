#include "tablesstate.h"
#include <QRandomGenerator>

TablesState::TablesState(TablesState& ts){
    tables_types_num = ts.tables_types_num;
    tables_number = ts.tables_number;

    teamA_won_1_rolloff = ts.teamA_won_1_rolloff;
    teamA_won_2_rolloff = ts.teamA_won_2_rolloff;

    tables_free = new bool[tables_number];
    for( int i=0; i < tables_number; i++ )
        tables_free[i] = ts.tables_free[i];

    tables_types = ts.tables_types;

    free_table_types = new bool[tables_types_num];
    for( int i = 0; i < tables_types_num; i++)
        free_table_types[i] = ts.free_table_types[i];

    teamAdefenderTable = new int[3];
    teamBdefenderTable = new int[3];
    for( int i = 0 ; i < 3 ; i++){
        teamAdefenderTable[i] = -1;
        teamBdefenderTable[i] = -1;
    }

    count_table_types = ts.count_table_types;

    std::vector<int> count_table_types;

}

TablesState::TablesState(int tables_types_num, int tables_number, bool first_rolloff, bool second_rolloff)
{
    teamAdefenderTable = new int[3];
    teamBdefenderTable = new int[3];
    for( int i = 0 ; i < 3 ; i++){
        teamAdefenderTable[i] = -1;
        teamBdefenderTable[i] = -1;
    }

    this->tables_types_num = tables_types_num;
    this->tables_number = tables_number;
    this->teamA_won_1_rolloff = first_rolloff;
    this->teamA_won_2_rolloff = second_rolloff;

    tables_types = std::vector<int>(tables_number);
    tables_free = new bool[tables_number];
    free_table_types = new bool[tables_types_num];
    count_table_types = std::vector<int>(tables_types_num);

    for( int i = 0 ; i < tables_number; i++){
        tables_types[i] = QRandomGenerator::global()->bounded(0, tables_types_num);
        tables_free[i] = true;
        //free_table_types.insert(tables_types[i]);
        free_table_types[tables_types[i]] = true;
        count_table_types[tables_types[i]]++;
    }
}

TablesState::TablesState(int* tables_types, int tables_types_num, int tables_number, bool first_rolloff, bool second_rolloff)
{
    this->teamA_won_1_rolloff = first_rolloff;
    this->teamA_won_2_rolloff = second_rolloff;
    this->tables_types_num = tables_types_num;
    this->tables_number = tables_number;
    this->tables_types = std::vector<int>(tables_number);//(tables_types);
    free_table_types = new bool[tables_types_num];
    tables_free = new bool[tables_number];
    count_table_types = std::vector<int>(tables_types_num);

    for( int i = 0 ; i < tables_number; i++){
        this->tables_types[i] = tables_types[i];
        tables_free[i] = true;
        free_table_types[tables_types[i]] = true;
        count_table_types[tables_types[i]]++;
    }
}
// table_id now is table_type
void TablesState::selectDefenderTable(char team, int table_id, int stage){
    if( team == 'A'){
        teamAdefenderTable[stage] = table_id;
    }
    else{
        teamBdefenderTable[stage] = table_id;
    }
    tables_free[table_id] = false;//old
    count_table_types[table_id]--;
}

void TablesState::unselectDefenderTable(char team, int stage){
    //int index;
    if(team == 'A'){
        //index = teamAdefenderTable[stage];
        tables_free[teamAdefenderTable[stage]] = true;//old
        count_table_types[teamAdefenderTable[stage]]++;
        teamAdefenderTable[stage] = -1;
    }
    else{
        //index = teamBdefenderTable[stage];
        tables_free[teamBdefenderTable[stage]] = true;//old
        count_table_types[teamBdefenderTable[stage]]++;
        teamBdefenderTable[stage] = -1;
    }
    //free_table_types.insert(tables_types[index]);

}

void TablesState::selectRejectedTable(int table_id){
    tables_free[table_id] = false;//old
    rejectedPlayersTable = table_id;
    count_table_types[rejectedPlayersTable]--;
    for( size_t i = 0 ; i < count_table_types.size(); i++){
        if( count_table_types[i] > 0){
            championsPlayersTable = i;
            count_table_types[i]--;
            break;
        }
    }
//    for( int i = 0 ; i < tables_number; i++){
//        if( tables_free[i]){
//            championsPlayersTable = i;
//            tables_free[i] = false;
//            break;
//        }
//    }
}

void TablesState::unselectRejectedTable(){
    tables_free[rejectedPlayersTable] = true;//old
    tables_free[championsPlayersTable] = true;//old
    count_table_types[rejectedPlayersTable]++;
    count_table_types[championsPlayersTable]++;
    rejectedPlayersTable = -1;
    championsPlayersTable = -1;
}

void TablesState::print(){
    printf("-- Tables Types --\n");
    for( int i = 0 ; i < tables_number; i++){
        printf("%i ",tables_types[i]);
    }
    printf("\n");
}

bool TablesState::check_there_are_free_tables_of_type(int type){
    for( int i = 0 ; i < tables_number; i++){
        if( tables_types[i] == type and tables_free[i])
            return true;
    }
    return false;
}
