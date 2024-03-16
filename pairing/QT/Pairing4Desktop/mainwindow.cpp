#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QRandomGenerator>
#include <QMessageBox>
#include <QFileDialog>
#include <QTextStream>
#include <QFile>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    SB_scores = {
                    {{ui->ssb000,ui->ssb001,ui->ssb002},{ui->ssb010,ui->ssb011,ui->ssb012},{ui->ssb020,ui->ssb021,ui->ssb022},{ui->ssb030,ui->ssb031,ui->ssb032}},
                    {{ui->ssb100,ui->ssb101,ui->ssb102},{ui->ssb110,ui->ssb111,ui->ssb112},{ui->ssb120,ui->ssb121,ui->ssb122},{ui->ssb130,ui->ssb131,ui->ssb132}},
                    {{ui->ssb200,ui->ssb201,ui->ssb202},{ui->ssb210,ui->ssb211,ui->ssb212},{ui->ssb220,ui->ssb221,ui->ssb222},{ui->ssb230,ui->ssb231,ui->ssb232}},
                    {{ui->ssb300,ui->ssb301,ui->ssb302},{ui->ssb310,ui->ssb311,ui->ssb312},{ui->ssb320,ui->ssb321,ui->ssb322},{ui->ssb330,ui->ssb331,ui->ssb332}}
                };

    CB_tables = {ui->cb_table1, ui->cb_table2, ui->cb_table3, ui->cb_table4};

    LE_Anames = {ui->le_a0, ui->le_a1, ui->le_a2, ui->le_a3};
    LE_Bnames = {ui->leB0name, ui->leB1name, ui->leB2name, ui->leB3name};
    LE_Bfactions = {ui->leB0faction, ui->leB1faction, ui->leB2faction, ui->leB3faction};

    PB_A_defs = {ui->pb_Adef0, ui->pb_Adef1, ui->pb_Adef2, ui->pb_Adef3};
    PB_A_attacks = {ui->pb_Aatt0, ui->pb_Aatt1, ui->pb_Aatt2};
    PB_A_choose = {ui->pb_Achoose0, ui->pb_Achoose1};

    PB_A_def_tables = {ui->pb_Adef_table0, ui->pb_Adef_table1, ui->pb_Adef_table2, ui->pb_Adef_table3};
    PB_A_rej_tables = {ui->pb_Arej_table0, ui->pb_Arej_table1};

    PB_B_defs = {ui->pb_Bdef0, ui->pb_Bdef1, ui->pb_Bdef2, ui->pb_Bdef3};
    PB_B_attacks = {ui->pb_Batt0, ui->pb_Batt1, ui->pb_Batt2};
    PB_B_choose = {ui->pb_Bchoose0, ui->pb_Bchoose1};

    PB_B_def_tables = {ui->pb_Bdef_table0, ui->pb_Bdef_table1, ui->pb_Bdef_table2, ui->pb_Bdef_table3};
    PB_B_rej_tables = {ui->pb_Brej_table0, ui->pb_Brej_table1};

    PB_finals = {ui->pb_final0, ui->pb_final1, ui->pb_final2, ui->pb_final3};

    LE_tables = {ui->le_t1, ui->le_t2, ui->le_t3, ui->le_t4};

    L_final_tables = {ui->l_final0, ui->l_final1, ui->l_final2, ui->l_final3};

    int i=0;
    for( QLineEdit* let: LE_tables){
        let->setText(QString::number(++i));
    }

    set_sb_scores_limits();
    set_cb_tables_values();

    lock_A_defs(false);
    lock_A_attacks(false);
    lock_A_choose(false);
    lock_A_defs_tables(false);
    lock_A_rej_tables(false);

    lock_B_defs(false);
    lock_B_attacks(false);
    lock_B_choose(false);
    lock_B_defs_tables(false);
    lock_B_rej_tables(false);

    ui->cb_2nd_rolloff->setDisabled(true);

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::set_sb_scores_limits(){
    for(std::vector<std::vector<QSpinBox*>> z: SB_scores){
        for( std::vector<QSpinBox*> y: z){
            for( QSpinBox* x: y){
                x->setMaximum(ui->sb_max_score->value());
                x->setMinimum(ui->sb_min_score->value());
            }
        }
    }
}

void MainWindow::on_sb_min_score_valueChanged(int arg1)
{
    set_sb_scores_limits();
}

void MainWindow::on_sb_max_score_valueChanged(int arg1)
{
    set_sb_scores_limits();
}

void MainWindow::set_cb_tables_values(){
    for( QComboBox* x: CB_tables){
        x->addItem("OPEN");
        x->addItem("MIDDLE");
        x->addItem("CLOSED");
    }
}


void MainWindow::on_actionFill_random_triggered()
{
    for(std::vector<std::vector<QSpinBox*>> z: SB_scores){
        for( std::vector<QSpinBox*> y: z){
            for( QSpinBox* x: y){
                x->setValue(QRandomGenerator::global()->bounded(ui->sb_min_score->value(), ui->sb_max_score->value()+1));
            }
        }
    }
    for( QComboBox* x: CB_tables){
        x->setCurrentIndex(QRandomGenerator::global()->bounded(0,TABLE_TYPES_NUM));
    }
    ui->l_filename->setText("No file selected");

}


void MainWindow::on_actionAbout_triggered()
{
    QMessageBox::about(this, "About", "Warhammer 40k pairing machine\n Verson "+QString(VERSION)+"\n By Anton 'Strohkopf' Moscowsky\nSource: https://github.com/MoscowskyAnton/adeptus_calculatus");
}


void MainWindow::on_pb_lock_clicked()
{
    ui->pb_lock->setDisabled(true);
    lock_state = !lock_state;
    for(std::vector<std::vector<QSpinBox*>> z: SB_scores){
        for( std::vector<QSpinBox*> y: z){
            for( QSpinBox* x: y){
                x->setDisabled(lock_state);
            }
        }
    }
    for( QComboBox* x: CB_tables){
        x->setDisabled(lock_state);
    }
    for( int i = 0 ; i < PLAYERS_NUM; i++){
        LE_Anames[i]->setDisabled(lock_state);
        LE_Bnames[i]->setDisabled(lock_state);
        LE_Bfactions[i]->setDisabled(lock_state);
    }
    ui->sb_max_score->setDisabled(lock_state);
    ui->sb_min_score->setDisabled(lock_state);
    ui->pb_lock->setText(lock_state ? "Unlock" : "Lock");
    ui->cb_1st_rolloff->setDisabled(lock_state);
    ui->cb_2nd_rolloff->setDisabled(true);
    second_roll_off_checkable = false;
    ui->cb_2nd_rolloff->setChecked(false);

    ui->actionFill_random->setDisabled(lock_state);
    ui->actionOpen_file->setDisabled(lock_state);

    lock_A_attacks(false);
    lock_A_choose(false);
    lock_A_defs_tables(false);
    lock_A_rej_tables(false);

    lock_le_tables(!lock_state);

    lock_B_defs(false);
    lock_B_attacks(false);
    lock_B_choose(false);
    lock_B_defs_tables(false);
    lock_B_rej_tables(false);
    if(lock_state){
        fill_sst();
        fill_ts();
        PG4 = new ParingGame4(SST, TS);
        calculate_A_defs();
    }
    else{
        clear_bp_defs('A');
        clear_bp_attacks('A');
        clear_bp_choose('A');
        clear_bp_def_tables('A');
        clear_bp_rej_tables('A');
        clear_bp_defs('B');
        clear_bp_attacks('B');
        clear_bp_choose('B');
        clear_bp_def_tables('B');
        clear_bp_rej_tables('B');
        A_atackers.clear();
        B_atackers.clear();
        last_tables.clear();
        ui->le_final_score->setText("");
        clear_finals();
    }

    ui->pb_lock->setDisabled(false);
    lock_A_defs(lock_state);
}

void MainWindow::calculate_A_defs(){
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->min_team_score, mi=0;
    for(int i = 0 ; i < PLAYERS_NUM; i++){
        PG4->teamA.set_defender(0, i);
        int score, s1, s2;
        PG4->min(0, DEFENDER, alpha, beta, &score, &s1, &s2);
        PB_A_defs[i]->setText(LE_Anames[i]->text() == "" ? "Player 0\n"+QString::number(score) : LE_Anames[i]->text()+"\n"+QString::number(score));
        PG4->teamA.unset_defender(0);
        if(score >= ms){
            if(score > ms){
                for( int s = mi+1; s --> 0;)
                    set_pb_font(PB_A_defs[s],"");
            }
            set_pb_font(PB_A_defs[i],"bold");
            mi = i;
            ms = score;
        }
    }
}

void MainWindow::fill_sst(){
    int*** new_sst;
    new_sst = new int**[PLAYERS_NUM];
    for(int i = 0 ; i < PLAYERS_NUM; i++){
        new_sst[i] = new int*[PLAYERS_NUM];
        for(int j = 0 ; j < PLAYERS_NUM; j++){
            new_sst[i][j] = new int[TABLE_TYPES_NUM];
            for(int k = 0 ; k < TABLE_TYPES_NUM; k++){
                new_sst[i][j][k] = SB_scores[i][j][k]->value();
            }
        }
    }
    SST = new ScoreSheetTables(new_sst, PLAYERS_NUM, TABLE_TYPES_NUM, ui->sb_min_score->value(), ui->sb_max_score->value());
}

void MainWindow::fill_ts(){
    int* new_ts = new int[PLAYERS_NUM];
    for(int i = 0 ; i < PLAYERS_NUM; i++){
        new_ts[i] = CB_tables[i]->currentIndex();
    }
    //TS = new TablesState(new_ts, TABLE_TYPES_NUM, PLAYERS_NUM, ui->cb_1st_rolloff->isChecked(), ui->cb_2nd_rolloff->isChecked());
    TS = new TablesState(new_ts, TABLE_TYPES_NUM, PLAYERS_NUM, ui->cb_1st_rolloff->isChecked(), !ui->cb_1st_rolloff->isChecked()); // GoldFish style
}

void MainWindow::lock_A_defs(bool flag){
    for(QPushButton* pb : PB_A_defs){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_A_attacks(bool flag){
    for(QPushButton* pb : PB_A_attacks){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_A_choose(bool flag){
    for(QPushButton* pb : PB_A_choose){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_A_defs_tables(bool flag){
    for(QPushButton* pb : PB_A_def_tables){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_A_rej_tables(bool flag){
    for(QPushButton* pb : PB_A_rej_tables){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_B_defs(bool flag){
    for(QPushButton* pb : PB_B_defs){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_B_attacks(bool flag){
    for(QPushButton* pb : PB_B_attacks){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_B_choose(bool flag){
    for(QPushButton* pb : PB_B_choose){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_B_defs_tables(bool flag){
    for(QPushButton* pb : PB_B_def_tables){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_B_rej_tables(bool flag){
    for(QPushButton* pb : PB_B_rej_tables){
        pb->setDisabled(!flag);
    }
}

void MainWindow::lock_le_tables(bool flag){
    for(QLineEdit* le : LE_tables){
        le->setDisabled(!flag);
    }
}

void MainWindow::set_pb_font(QPushButton* pb, QString mode){
    QFont f = pb->font();
    if( mode == "bold")
        f.setBold(true);
    else if( mode == "italic")
        f.setItalic(true);
    else{
        // release
        f.setItalic(false);
        f.setBold(false);
    }
    pb->setFont(f);
}

void MainWindow::on_pb_Adef0_clicked()
{
    set_pb_font(ui->pb_Adef0, "italic");
    setAdef(0);
}


void MainWindow::on_pb_Adef1_clicked()
{
    set_pb_font(ui->pb_Adef1, "italic");
    setAdef(1);
}


void MainWindow::on_pb_Adef2_clicked()
{
    set_pb_font(ui->pb_Adef2, "italic");
    setAdef(2);
}


void MainWindow::on_pb_Adef3_clicked()
{
    set_pb_font(ui->pb_Adef3, "italic");
    setAdef(3);
}

void MainWindow::setAdef(int def){
    lock_A_defs(false);
    PG4->teamA.set_defender(0, def);
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->max_team_score, mi=0;
    for(int i = 0 ; i < PLAYERS_NUM; i++){
        PG4->teamB.set_defender(0, i);
        int score, s1, s2;
        PG4->max(0, ATACKERS, alpha, beta, &score, &s1, &s2);
        PB_B_defs[i]->setText(LE_Bnames[i]->text() == "" ? "Player 0\n"+QString::number(score) : LE_Bnames[i]->text()+"\n"+QString::number(score));
        PG4->teamB.unset_defender(0);
        if(score <= ms){
            if(score < ms)
                for( int s = mi+1; s --> 0;)
                    set_pb_font(PB_B_defs[s],"");
            set_pb_font(PB_B_defs[i],"bold");
            mi = i;
            ms = score;
        }
    }
    lock_B_defs(true);
}

void MainWindow::clear_bp_defs(char team){
    if(team == 'A'){
        for(QPushButton* x : PB_A_defs ){
            x->setText("");
            set_pb_font(x, "");
        }
    }
    else
        for(QPushButton* x : PB_B_defs ){
            x->setText("");
            set_pb_font(x, "");
        }
}

void MainWindow::clear_bp_attacks(char team){
    if(team == 'A'){
        for(QPushButton* x : PB_A_attacks ){
            x->setText("");
            set_pb_font(x, "");
        }
    }
    else
        for(QPushButton* x : PB_B_attacks ){
            x->setText("");
            set_pb_font(x, "");
        }
}

void MainWindow::clear_bp_choose(char team){
    if(team == 'A'){
        for(QPushButton* x : PB_A_choose ){
            x->setText("");
            set_pb_font(x, "");
        }
    }
    else
        for(QPushButton* x : PB_B_choose ){
            x->setText("");
            set_pb_font(x, "");
        }
}

void MainWindow::clear_bp_def_tables(char team){
    if(team == 'A'){
        for(QPushButton* x : PB_A_def_tables ){
            x->setText("");
            set_pb_font(x, "");
        }
    }
    else
        for(QPushButton* x : PB_B_def_tables ){
            x->setText("");
            set_pb_font(x, "");
        }
}

void MainWindow::clear_bp_rej_tables(char team){
    if(team == 'A'){
        for(QPushButton* x : PB_A_rej_tables ){
            x->setText("");
            set_pb_font(x, "");
        }
    }
    else
        for(QPushButton* x : PB_B_rej_tables ){
            x->setText("");
            set_pb_font(x, "");
        }

}

void MainWindow::on_pb_Bdef0_clicked()
{
    set_pb_font(ui->pb_Bdef0, "italic");
    setBdef(0);
}


void MainWindow::on_pb_Bdef1_clicked()
{
    set_pb_font(ui->pb_Bdef1, "italic");
    setBdef(1);
}


void MainWindow::on_pb_Bdef2_clicked()
{
    set_pb_font(ui->pb_Bdef2, "italic");
    setBdef(2);
}


void MainWindow::on_pb_Bdef3_clicked()
{
    set_pb_font(ui->pb_Bdef3, "italic");
    setBdef(3);
}

void MainWindow::setBdef(int def){
    lock_B_defs(false);
    PG4->teamB.set_defender(0, def);
    int pb_cntr = 0;
    int score, s1, s2;
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->min_team_score, mi=0;
    for(int i = 0 ; i < PLAYERS_NUM; i++){
        for(int j = i+1 ; j < PLAYERS_NUM; j++){
            if( PG4->teamA.free[i] && PG4->teamA.free[j] ){
                PG4->teamA.set_atackers(0,i,j);
                PG4->min(0, ATACKERS, alpha, beta, &score, &s1, &s2);
                QString a1 = LE_Anames[i]->text() == "" ? "Player "+QString::number(i) :LE_Anames[i]->text();
                QString a2 = LE_Anames[j]->text() == "" ? "Player "+QString::number(j) :LE_Anames[j]->text();
                PB_A_attacks[pb_cntr]->setText(a1+"\n"+a2+"\n"+QString::number(score));
                PG4->teamA.unset_atackers(0);
                if(score >= ms){
                    if(score > ms)
                        for( int s = mi+1; s --> 0;)
                            set_pb_font(PB_A_attacks[s],"");
                    set_pb_font(PB_A_attacks[pb_cntr],"bold");
                    mi = pb_cntr;
                    ms = score;
                }
                pb_cntr++;
                std::vector<int> a;
                a.push_back(i);
                a.push_back(j);
                A_atackers.push_back(a);
            }
        }
    }
    lock_A_attacks(true);
}

void MainWindow::on_pb_Aatt0_clicked()
{
    set_pb_font(ui->pb_Aatt0, "italic");
    setAatacks(A_atackers[0][0], A_atackers[0][1]);
}

void MainWindow::on_pb_Aatt1_clicked()
{
    set_pb_font(ui->pb_Aatt1, "italic");
    setAatacks(A_atackers[1][0], A_atackers[1][1]);
}

void MainWindow::on_pb_Aatt2_clicked()
{
    set_pb_font(ui->pb_Aatt2, "italic");
    setAatacks(A_atackers[2][0], A_atackers[2][1]);
}

void MainWindow::setAatacks(int a1, int a2){
    lock_A_attacks(false);
    PG4->teamA.set_atackers(0,a1,a2);
    int pb_cntr = 0;
    int score, s1, s2;
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->max_team_score, mi=0;
    for(int i = 0 ; i < PLAYERS_NUM; i++){
        for(int j = i+1 ; j < PLAYERS_NUM; j++){
            if( PG4->teamB.free[i] && PG4->teamB.free[j] ){
                PG4->teamB.set_atackers(0,i,j);
                PG4->max(0, CHOOSE, alpha, beta, &score, &s1, &s2);
                QString a1 = (LE_Bnames[i]->text() == "" ? "Pl. "+QString::number(i) :LE_Bnames[i]->text())+(LE_Bfactions[i]->text() == "" ? "" : " ("+LE_Bfactions[i]->text()+")");
                QString a2 = (LE_Bnames[j]->text() == "" ? "Pl. "+QString::number(j) :LE_Bnames[j]->text())+(LE_Bfactions[j]->text() == "" ? "" : " ("+LE_Bfactions[j]->text()+")");
                PB_B_attacks[pb_cntr]->setText(a1+"\n"+a2+"\n"+QString::number(score));
                PG4->teamB.unset_atackers(0);
                if(score <= ms){
                    if(score < ms)
                        for( int s = mi+1; s --> 0;)
                            set_pb_font(PB_B_attacks[s],"");
                    set_pb_font(PB_B_attacks[pb_cntr],"bold");
                    mi = pb_cntr;
                    ms = score;
                }
                pb_cntr++;
                std::vector<int> a;
                a.push_back(i);
                a.push_back(j);
                B_atackers.push_back(a);
            }
        }
    }
    lock_B_attacks(true);
}


void MainWindow::on_pb_Batt0_clicked()
{
    set_pb_font(ui->pb_Batt0, "italic");
    setBatacks(B_atackers[0][0], B_atackers[0][1]);
}

void MainWindow::on_pb_Batt1_clicked()
{
    set_pb_font(ui->pb_Batt1, "italic");
    setBatacks(B_atackers[1][0], B_atackers[1][1]);
}

void MainWindow::on_pb_Batt2_clicked()
{
    set_pb_font(ui->pb_Batt2, "italic");
    setBatacks(B_atackers[2][0], B_atackers[2][1]);
}

void MainWindow::setBatacks(int a1, int a2){
    lock_B_attacks(false);
    PG4->teamB.set_atackers(0, a1, a2);
    int score, s1, s2;
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->min_team_score, mi=0;
    for( int i = 0 ; i < 2; i++){
        PG4->teamB.choose_atacker(0,i);
        PG4->min(0,CHOOSE,alpha,beta,&score,&s1,&s2);

        int chosed_id = i == 0 ? PG4->teamB.stages[0].atacker1 : PG4->teamB.stages[0].atacker2;
        QString name = LE_Bnames[chosed_id]->text() == "" ? "Player "+QString::number(chosed_id) :LE_Bnames[chosed_id]->text();
        QString faction = LE_Bfactions[chosed_id]->text() == "" ? "" : "("+LE_Bfactions[chosed_id]->text()+")";
        PB_A_choose[i]->setText(name+faction+"\n"+QString::number(score));
        PG4->teamB.unchoose_atacker(0);
        if(score >= ms){
            if(score > ms)
                for( int s = mi+1; s --> 0;)
                    set_pb_font(PB_A_choose[s],"");
            set_pb_font(PB_A_choose[i],"bold");
            mi = i;
            ms = score;
        }
    }
    lock_A_choose(true);
}

void MainWindow::on_pb_Achoose0_clicked()
{
    set_pb_font(ui->pb_Achoose0, "italic");
    setAchoose(0);
}

void MainWindow::on_pb_Achoose1_clicked()
{
    set_pb_font(ui->pb_Achoose1, "italic");
    setAchoose(1);
}

void MainWindow::setAchoose(int ch){
    lock_A_choose(false);
    PG4->teamB.choose_atacker(0,ch);
    int score, s1, s2;
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->max_team_score, mi=0;
    for( int i = 0 ; i < 2; i++){
        PG4->teamA.choose_atacker(0,i);
        if(PG4->TS->teamA_won_1_rolloff)
            PG4->max(0,TABLE_DEF,alpha,beta,&score,&s1,&s2);
        else
            PG4->min(0,TABLE_DEF,alpha,beta,&score,&s1,&s2);
        int chosed_id = i == 0 ? PG4->teamA.stages[0].atacker1 : PG4->teamA.stages[0].atacker2;
        QString name = LE_Anames[chosed_id]->text() == "" ? "Player "+QString::number(chosed_id) :LE_Anames[chosed_id]->text();
        PB_B_choose[i]->setText(name+"\n"+QString::number(score));
        PG4->teamA.unchoose_atacker(0);
        if(score <= ms){
            if(score < ms)
                for( int s = mi+1; s --> 0;)
                    set_pb_font(PB_B_choose[s],"");
            set_pb_font(PB_B_choose[i],"bold");
            mi = i;
            ms = score;
        }
    }
    lock_B_choose(true);
}

void MainWindow::on_pb_Bchoose0_clicked()
{
    set_pb_font(ui->pb_Bchoose0, "italic");
    setBchoose(0);
}

void MainWindow::on_pb_Bchoose1_clicked()
{
    set_pb_font(ui->pb_Bchoose1, "italic");
    setBchoose(1);
}

void MainWindow::setBchoose(int ch){
    lock_B_choose(false);
    PG4->teamA.choose_atacker(0,ch);
    if( PG4->TS->teamA_won_1_rolloff){
        calcADefTables();
        lock_A_defs_tables(true);
    }
    else{
        calcBDefTables();
        lock_B_defs_tables(true);
    }
}

void MainWindow::calcADefTables(){
    int score, s1, s2;
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->min_team_score, mi=0;
    for( int i = 0 ; i < PLAYERS_NUM; i++){
        if(PG4->TS->tables_free[i]){            
            PG4->TS->selectDefenderTable('A',i);
            if(PG4->TS->teamA_won_1_rolloff)
                PG4->min(0,TABLE_DEF,alpha,beta,&score,&s1,&s2);
            else
                if(PG4->TS->teamA_won_2_rolloff)
                    PG4->max(0,TABLE_REJ,alpha,beta,&score,&s1,&s2);
                else
                    PG4->min(0,TABLE_REJ,alpha,beta,&score,&s1,&s2);
            //PB_A_def_tables[i]->setText("Table "+QString::number(i+1)+"\n"+QString::number(score));
            PB_A_def_tables[i]->setText(L_final_tables[i]->text()+"\n"+QString::number(score));
            PG4->TS->unselectDefenderTable('A');
            if(score >= ms){
                if(score > ms)
                    for( int s = mi+1; s --> 0;)
                        set_pb_font(PB_A_def_tables[s],"");
                set_pb_font(PB_A_def_tables[i],"bold");
                mi = i;
                ms = score;
            }
        }
        else{
            PB_A_def_tables[i]->setText("Table taken");
            PB_A_def_tables[i]->setDisabled(true);
        }
    }
}

void MainWindow::calcBDefTables(){
    int score, s1, s2;
    int alpha = SST->min_team_score;
    int beta = SST->max_team_score;
    int ms=PG4->SS->max_team_score, mi=0;
    for( int i = 0 ; i < PLAYERS_NUM; i++){
        if(PG4->TS->tables_free[i]){            
            PG4->TS->selectDefenderTable('B',i);
            if(PG4->TS->teamA_won_1_rolloff){
                if(PG4->TS->teamA_won_2_rolloff)
                    PG4->max(0,TABLE_REJ,alpha,beta,&score,&s1,&s2);
                else
                    PG4->min(0,TABLE_REJ,alpha,beta,&score,&s1,&s2);
            }
            else
                PG4->max(0,TABLE_DEF,alpha,beta,&score,&s1,&s2);
            //PB_B_def_tables[i]->setText("Table "+QString::number(i+1)+"\n"+QString::number(score));
            PB_B_def_tables[i]->setText(L_final_tables[i]->text()+"\n"+QString::number(score));
            PG4->TS->unselectDefenderTable('B');
            if(score <= ms){
                if(score < ms)
                    for( int s = mi+1; s --> 0;)
                        set_pb_font(PB_B_def_tables[s],"");
                set_pb_font(PB_B_def_tables[i],"bold");
                mi = i;
                ms = score;
            }
        }
        else{
            PB_B_def_tables[i]->setText("Table taken");
            PB_B_def_tables[i]->setDisabled(true);
        }
    }
}

void MainWindow::on_pb_Bdef_table0_clicked()
{
    set_pb_font(ui->pb_Bdef_table0, "italic");
    setBDefTables(0);
}

void MainWindow::on_pb_Bdef_table1_clicked()
{
    set_pb_font(ui->pb_Bdef_table1, "italic");
    setBDefTables(1);
}

void MainWindow::on_pb_Bdef_table2_clicked()
{
    set_pb_font(ui->pb_Bdef_table2, "italic");
    setBDefTables(2);
}

void MainWindow::on_pb_Bdef_table3_clicked()
{
    set_pb_font(ui->pb_Bdef_table3, "italic");
    setBDefTables(3);
}

void MainWindow::setADefTables(int table){
    PG4->TS->selectDefenderTable('A',table);
    if( PG4->TS->teamA_won_1_rolloff){
        lock_B_defs_tables(true);
        calcBDefTables();
    }
    else{
        //go rejected
        setRejectedTables();
        ui->cb_2nd_rolloff->setDisabled(false);
        second_roll_off_checkable = true;
    }
    lock_A_defs_tables(false);
}

void MainWindow::setBDefTables(int table){
    PG4->TS->selectDefenderTable('B',table);
    if( PG4->TS->teamA_won_1_rolloff){
        //go rejected
        setRejectedTables();
        ui->cb_2nd_rolloff->setDisabled(false);
        second_roll_off_checkable = true;
    }
    else{
        lock_A_defs_tables(true);
        calcADefTables();
    }
    lock_B_defs_tables(false);
}

void MainWindow::on_pb_Adef_table0_clicked()
{
    set_pb_font(ui->pb_Adef_table0, "italic");
    setADefTables(0);
}

void MainWindow::on_pb_Adef_table1_clicked()
{
    set_pb_font(ui->pb_Adef_table1, "italic");
    setADefTables(1);
}

void MainWindow::on_pb_Adef_table2_clicked()
{
    set_pb_font(ui->pb_Adef_table2, "italic");
    setADefTables(2);
}

void MainWindow::on_pb_Adef_table3_clicked()
{
    set_pb_font(ui->pb_Adef_table3, "italic");
    setADefTables(3);
}

void MainWindow::setRejectedTables(){
    if(PG4->TS->teamA_won_2_rolloff){
        lock_A_rej_tables(true);
        lock_B_rej_tables(false);
        int score;
        int ms=PG4->SS->min_team_score, mi=0;
        int tc = 0;
        for( int i = 0 ; i < PLAYERS_NUM; i++){
            if(PG4->TS->tables_free[i]){
                last_tables.push_back(i);
                PG4->TS->selectRejectedTable(i);
                score = PG4->get_score();
                //PB_A_rej_tables[tc]->setText("Table "+QString::number(i)+"\n"+QString::number(score));
                PB_A_rej_tables[tc]->setText(L_final_tables[i]->text()+"\n"+QString::number(score));
                PG4->TS->unselectRejectedTable();
                if(score >= ms){
                    if(score > ms)
                        for( int s = mi+1; s --> 0;)
                            set_pb_font(PB_A_rej_tables[s],"");
                    set_pb_font(PB_A_rej_tables[tc],"bold");
                    mi = tc;
                    ms = score;
                }
                tc++;
            }
        }
    }
    else{
        lock_A_rej_tables(false);
        lock_B_rej_tables(true);
        int score;
        int ms=PG4->SS->max_team_score, mi=0;
        int tc = 0;
        for( int i = 0 ; i < PLAYERS_NUM; i++){
            if(PG4->TS->tables_free[i]){
                last_tables.push_back(i);
                PG4->TS->selectRejectedTable(i);
                score = PG4->get_score();
                //PB_B_rej_tables[tc]->setText("Table "+QString::number(i)+"\n"+QString::number(score));
                PB_B_rej_tables[tc]->setText(L_final_tables[i]->text()+"\n"+QString::number(score));
                PG4->TS->unselectRejectedTable();
                if(score <= ms){
                    if(score < ms)
                        for( int s = mi+1; s --> 0;)
                            set_pb_font(PB_B_rej_tables[s],"");
                    set_pb_font(PB_B_rej_tables[tc],"bold");
                    mi = tc;
                    ms = score;
                }
                tc++;
            }
        }
    }
}

void MainWindow::on_pb_Arej_table0_clicked()
{
    set_pb_font(ui->pb_Arej_table0,"italic");
    final(last_tables[0]);
}

void MainWindow::on_pb_Arej_table1_clicked()
{
    set_pb_font(ui->pb_Arej_table1,"italic");
    final(last_tables[1]);
}

void MainWindow::on_pb_Brej_table0_clicked()
{
    set_pb_font(ui->pb_Brej_table0,"italic");
    final(last_tables[0]);
}

void MainWindow::on_pb_Brej_table1_clicked()
{
    set_pb_font(ui->pb_Brej_table1,"italic");
    final(last_tables[1]);
}

void MainWindow::on_cb_2nd_rolloff_stateChanged(int arg1)
{
    if(second_roll_off_checkable){
        PG4->TS->teamA_won_2_rolloff = bool(arg1);
        setRejectedTables();
    }
}

void MainWindow::final(int rejected_table){
    ui->cb_2nd_rolloff->setDisabled(true);
    second_roll_off_checkable = false;
    lock_A_rej_tables(false);
    lock_B_rej_tables(false);
    PG4->TS->selectRejectedTable(rejected_table);
    int score = PG4->get_score();
    ui->le_final_score->setText(QString::number(score));

    int Aid, Bid;
    for( int i = 0 ; i < PLAYERS_NUM; i++){
        if( i == PG4->TS->teamAdefenderTable){
            Aid = PG4->teamA.stages[0].defender;
            Bid = PG4->teamB.stages[0].choosed_atacker;
        }
        else if(i == PG4->TS->teamBdefenderTable){
            Bid = PG4->teamB.stages[0].defender;
            Aid = PG4->teamA.stages[0].choosed_atacker;
        }
        else if(i == PG4->TS->rejectedPlayersTable){
            Aid = PG4->teamA.rejected_last_atacker;
            //Bid = PG4->teamB.rejected_last_atacker;
            Bid = PG4->teamB.champion;
        }
        else if(i == PG4->TS->championsPlayersTable){
            Aid = PG4->teamA.champion;
            //Bid = PG4->teamB.champion;
            Bid = PG4->teamB.rejected_last_atacker;
        }
        else{
            //crap!
        }
        score = PG4->SS->ind(Aid, Bid, PG4->TS->tables_types[i]);
        QString playerA = LE_Anames[Aid]->text() == "" ? "A Player "+QString::number(Aid) : LE_Anames[Aid]->text();
        QString playerB = LE_Bnames[Bid]->text() == "" ? "B Player "+QString::number(Bid) : LE_Bnames[Bid]->text();

        PB_finals[i]->setText(playerA+"\nvs\n"+playerB+"\n"+QString::number(score));
    }
}

void MainWindow::clear_finals(){
    for( QPushButton* x: PB_finals){
        x->setText("");
    }
}

void MainWindow::on_actionOpen_file_triggered()
{
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open Scores"), "", tr("Text Files (*.txt)"));
    ui->l_filename->setText(fileName);
    QFile file(fileName);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)){
        QMessageBox::warning(this,"File error","File cannon be opened");
        return;
    }
    QTextStream in(&file);
    int cntr =0;
    QRegularExpression rx("(\\ |\\t)");
    while (!in.atEnd()) {
        QString line = in.readLine();
        // player
        if( cntr == 0 ){
            QStringList names = line.split(rx);
            for(int i = 0 ; i < PLAYERS_NUM; i++){
                if( i < names.length())
                    LE_Bnames[i]->setText(names[i]);
            }
        }
        // faction
        else if( cntr == 1){
            QStringList names = line.split(rx);
            for(int i = 0 ; i < PLAYERS_NUM; i++){
                if( i < names.length())
                    LE_Bfactions[i]->setText(names[i]);
            }
        }
        else{
            QStringList numbers = line.split(rx);
            int i = (cntr-2) / 3;
            int k = (cntr-2) - i * 3;
            for(int j = 0 ; j < PLAYERS_NUM; j++){
                //ui->l_debug->setText(QString::number(cntr-2)+"->"+QString::number(a)+" "+QString::number(b)+" "+QString::number(c));
                SB_scores[i][j][k]->setValue(numbers[j].toInt());
            }
        }
        cntr++;
    }
}

void MainWindow::on_le_t1_textChanged(const QString &arg1)
{
    ui->l_final0->setText("Table "+arg1);
}

void MainWindow::on_le_t2_textChanged(const QString &arg1)
{
    ui->l_final1->setText("Table "+arg1);
}

void MainWindow::on_le_t3_textChanged(const QString &arg1)
{
    ui->l_final2->setText("Table "+arg1);
}

void MainWindow::on_le_t4_textChanged(const QString &arg1)
{
    ui->l_final3->setText("Table "+arg1);
}

