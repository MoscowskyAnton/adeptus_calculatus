#ifndef TABLESSTATE_H
#define TABLESSTATE_H

#include <set>
#include <vector>

class TablesState
{
public:
    TablesState(int tables_types_num, int tables_number, bool, bool);
    TablesState(int* tables_types, int tables_types_num, int tables_number, bool , bool);

    int tables_types_num;
    int tables_number;

    bool teamA_won_1_rolloff;
    bool teamA_won_2_rolloff;

    bool* tables_free;
    std::vector<int> tables_types;

    bool* free_table_types;

    int* teamAdefenderTable;// = -1;
    int* teamBdefenderTable;// = -1;
    int rejectedPlayersTable = -1;
    int championsPlayersTable = -1;

    std::vector<int> count_table_types;

    void selectDefenderTable(char team, int table_id, int stage);
    void unselectDefenderTable(char team, int stage);
    void selectRejectedTable(int table_id);
    void unselectRejectedTable();
    void print();

    bool check_there_are_free_tables_of_type(int type);

};

#endif // TABLESSTATE_H
