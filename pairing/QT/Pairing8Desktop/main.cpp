#include "pairing8desktop.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Pairing8Desktop w;
    w.show();
    return a.exec();
}
