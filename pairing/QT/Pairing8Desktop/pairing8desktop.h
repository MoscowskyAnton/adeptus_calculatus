#ifndef PAIRING8DESKTOP_H
#define PAIRING8DESKTOP_H

#include <QMainWindow>
#include <vector>
#include "ui_pairing8desktop.h"

QT_BEGIN_NAMESPACE
namespace Ui { class Pairing8Desktop; }
QT_END_NAMESPACE

class Pairing8Desktop : public QMainWindow
{
    Q_OBJECT

public:
    Pairing8Desktop(QWidget *parent = nullptr);
    ~Pairing8Desktop();

private slots:
    void on_spinBox_min_score_valueChanged(int arg1);

    void on_spinBox_max_score_valueChanged(int arg1);

private:
    Ui::Pairing8Desktop *ui;

    std::vector<std::vector<QSpinBox*> > score_table_spins;
    std::vector<QPushButton*> teamApb;
    std::vector<QPushButton*> teamBpb;

    void update_score_limits();
};
#endif // PAIRING8DESKTOP_H
