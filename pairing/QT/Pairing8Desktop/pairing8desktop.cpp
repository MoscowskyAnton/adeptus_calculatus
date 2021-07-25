#include "pairing8desktop.h"


Pairing8Desktop::Pairing8Desktop(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Pairing8Desktop)
{
    ui->setupUi(this);

    score_table_spins = {{ui->spinBox_0_0, ui->spinBox_0_1, ui->spinBox_0_2, ui->spinBox_0_3, ui->spinBox_0_4, ui->spinBox_0_5, ui->spinBox_0_6, ui->spinBox_0_7},
                        {ui->spinBox_1_0, ui->spinBox_1_1, ui->spinBox_1_2, ui->spinBox_1_3, ui->spinBox_1_4, ui->spinBox_1_5, ui->spinBox_1_6, ui->spinBox_1_7},
                       {ui->spinBox_2_0, ui->spinBox_2_1, ui->spinBox_2_2, ui->spinBox_2_3, ui->spinBox_2_4, ui->spinBox_2_5, ui->spinBox_2_6, ui->spinBox_2_7},
                       {ui->spinBox_3_0, ui->spinBox_3_1, ui->spinBox_3_2, ui->spinBox_3_3, ui->spinBox_3_4, ui->spinBox_3_5, ui->spinBox_3_6, ui->spinBox_3_7},
                       {ui->spinBox_4_0, ui->spinBox_4_1, ui->spinBox_4_2, ui->spinBox_4_3, ui->spinBox_4_4, ui->spinBox_4_5, ui->spinBox_4_6, ui->spinBox_4_7},
                       {ui->spinBox_5_0, ui->spinBox_5_1, ui->spinBox_5_2, ui->spinBox_5_3, ui->spinBox_5_4, ui->spinBox_5_5, ui->spinBox_5_6, ui->spinBox_5_7},
                       {ui->spinBox_6_0, ui->spinBox_6_1, ui->spinBox_6_2, ui->spinBox_6_3, ui->spinBox_6_4, ui->spinBox_6_5, ui->spinBox_6_6, ui->spinBox_6_7},
                       {ui->spinBox_7_0, ui->spinBox_7_1, ui->spinBox_7_2, ui->spinBox_7_3, ui->spinBox_7_4, ui->spinBox_7_5, ui->spinBox_7_6, ui->spinBox_7_7}};

    teamApb = {ui->pb_A0, ui->pb_A1, ui->pb_A2, ui->pb_A3, ui->pb_A4, ui->pb_A5, ui->pb_A6, ui->pb_A7};
    teamApb = {ui->pb_B0, ui->pb_B1, ui->pb_B2, ui->pb_B3, ui->pb_B4, ui->pb_B5, ui->pb_B6, ui->pb_B7};

    update_score_limits();

}

void Pairing8Desktop::update_score_limits(){
    for( std::vector<QSpinBox*> y: score_table_spins){
        for( QSpinBox* x: y){
            x->setMaximum(ui->spinBox_max_score->value());
            x->setMinimum(ui->spinBox_min_score->value());
        }
    }
}

Pairing8Desktop::~Pairing8Desktop()
{
    delete ui;
}


void Pairing8Desktop::on_spinBox_min_score_valueChanged(int arg1)
{
    update_score_limits();
}


void Pairing8Desktop::on_spinBox_max_score_valueChanged(int arg1)
{
    update_score_limits();
}

