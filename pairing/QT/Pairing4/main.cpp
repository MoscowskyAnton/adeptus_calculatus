#include <QCoreApplication>
#include "scoresheettables.h"
#include "tablesstate.h"
#include "paringgame4.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    ScoreSheetTables SST(4, 3, -2, 2);
    SST.print();

    TablesState TS(3, 4, false, false);
    TS.print();

    ParingGame4 PG4(&SST, &TS);

    //PG4.play_optimal();
    PG4.play_with_input();
    PG4.print_results();

    return a.exec();
}
