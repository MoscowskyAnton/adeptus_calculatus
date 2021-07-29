#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "../Pairing4/gamestate4.h"
#include "../Pairing4/paringgame4.h"
#include "../Pairing4/scoresheettables.h"
#include "../Pairing4/tablesstate.h"
#include <vector>
#include "ui_mainwindow.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

enum TABLE_TYPES{ OPEN = 0, MIDDLE, CLOSED };
#define TABLE_TYPES_NUM 3
#define PLAYERS_NUM 4
#define VERSION "1.0.0"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_sb_min_score_valueChanged(int arg1);

    void on_sb_max_score_valueChanged(int arg1);

    void on_actionFill_random_triggered();

    void on_actionAbout_triggered();

    void on_pb_lock_clicked();

    void on_pb_Adef0_clicked();

    void on_pb_Adef1_clicked();

    void on_pb_Adef2_clicked();

    void on_pb_Adef3_clicked();

    void on_pb_Bdef0_clicked();

    void on_pb_Bdef1_clicked();

    void on_pb_Bdef2_clicked();

    void on_pb_Bdef3_clicked();

    void on_pb_Aatt0_clicked();

    void on_pb_Aatt1_clicked();

    void on_pb_Aatt2_clicked();

    void on_pb_Batt0_clicked();

    void on_pb_Batt1_clicked();

    void on_pb_Batt2_clicked();

    void on_pb_Achoose0_clicked();

    void on_pb_Achoose1_clicked();

    void on_pb_Bchoose0_clicked();

    void on_pb_Bchoose1_clicked();

    void on_pb_Bdef_table0_clicked();

    void on_pb_Bdef_table1_clicked();

    void on_pb_Bdef_table2_clicked();

    void on_pb_Bdef_table3_clicked();

    void on_pb_Adef_table0_clicked();

    void on_pb_Adef_table1_clicked();

    void on_pb_Adef_table2_clicked();

    void on_pb_Adef_table3_clicked();

    void on_pb_Arej_table0_clicked();

    void on_pb_Arej_table1_clicked();

    void on_pb_Brej_table0_clicked();

    void on_pb_Brej_table1_clicked();

    void on_cb_2nd_rolloff_stateChanged(int arg1);

    void on_actionOpen_file_triggered();

private:
    Ui::MainWindow *ui;

    std::vector<std::vector<std::vector<QSpinBox*>>> SB_scores;
    std::vector<QComboBox*> CB_tables;
    std::vector<QLineEdit*> LE_Anames;
    std::vector<QLineEdit*> LE_Bnames;
    std::vector<QLineEdit*> LE_Bfactions;

    std::vector<QPushButton*> PB_A_defs;
    std::vector<QPushButton*> PB_A_attacks;
    std::vector<QPushButton*> PB_A_choose;

    std::vector<QPushButton*> PB_A_def_tables;
    std::vector<QPushButton*> PB_A_rej_tables;

    std::vector<QPushButton*> PB_B_defs;
    std::vector<QPushButton*> PB_B_attacks;
    std::vector<QPushButton*> PB_B_choose;

    std::vector<QPushButton*> PB_B_def_tables;
    std::vector<QPushButton*> PB_B_rej_tables;

    std::vector<QPushButton*> PB_finals;

    void set_sb_scores_limits();
    void set_cb_tables_values();

    bool lock_state = false;
    void lock_A_defs(bool);
    void lock_A_attacks(bool);
    void lock_A_choose(bool);
    void lock_A_defs_tables(bool);
    void lock_A_rej_tables(bool);

    void lock_B_defs(bool);
    void lock_B_attacks(bool);
    void lock_B_choose(bool);
    void lock_B_defs_tables(bool);
    void lock_B_rej_tables(bool);

    void clear_bp_defs(char team);
    void clear_bp_attacks(char team);
    void clear_bp_choose(char team);
    void clear_bp_def_tables(char team);
    void clear_bp_rej_tables(char team);

    ScoreSheetTables* SST;
    TablesState* TS;
    ParingGame4* PG4;

    void fill_sst();
    void fill_ts();

    void calculate_A_defs();

    void setAdef(int def);
    void setBdef(int def);

    std::vector<std::vector<int>> A_atackers;
    std::vector<std::vector<int>> B_atackers;

    void setAatacks(int a1, int a2);
    void setBatacks(int a1, int a2);

    void set_pb_font(QPushButton* pb, QString mode);

    void setAchoose(int ch);
    void setBchoose(int ch);

    void calcADefTables();
    void calcBDefTables();

    void setADefTables(int table);
    void setBDefTables(int table);

    void setRejectedTables();

    bool second_roll_off_checkable = false;

    void final(int rejected_table);
    std::vector<int> last_tables;

    void clear_finals();

};
#endif // MAINWINDOW_H
