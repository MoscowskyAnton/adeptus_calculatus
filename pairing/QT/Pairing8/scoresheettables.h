#ifndef SCORESHEETTABLES_H
#define SCORESHEETTABLES_H


class ScoreSheetTables
{
public:
    ScoreSheetTables();

    // makes an random score sheet
    ScoreSheetTables(int players, int tables_types, float min = 0, float max = 20);
    ScoreSheetTables(int*** sheet, int playres, int tables_types, float min = 0, float max = 20);

    int ind(int, int, int);
    float mean();

    void print();

    int players;
    int tables_types;
    int min_player_score;
    int max_player_score;
    int min_team_score;
    int max_team_score;

private:
    int*** scores;
};


#endif // SCORESHEETTABLES_H
