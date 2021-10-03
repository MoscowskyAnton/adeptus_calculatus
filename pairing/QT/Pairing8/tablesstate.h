#ifndef TABLESSTATE_H
#define TABLESSTATE_H


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
    int* tables_types;

    int* teamAdefenderTable;// = -1;
    int* teamBdefenderTable;// = -1;
    int rejectedPlayersTable = -1;
    int championsPlayersTable = -1;

    void selectDefenderTable(char team, int table_id, int stage);
    void unselectDefenderTable(char team, int stage);
    void selectRejectedTable(int table_id);
    void unselectRejectedTable();
    void print();
};

#endif // TABLESSTATE_H
