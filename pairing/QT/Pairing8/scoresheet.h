#ifndef SCORESHEET_H
#define SCORESHEET_H


class ScoreSheet
{
public:
    ScoreSheet();

    // makes an random score sheet
    ScoreSheet(int players, float min = 0, float max = 20);
    ScoreSheet(int** sheet, int playres, float min = 0, float max = 20);

    int ind(int, int);
    float mean();

    void print();

    int players;
    int min_player_score;
    int max_player_score;
    int min_team_score;
    int max_team_score;

private:
    int** scores;
};



#endif // SCORESHEET_H
