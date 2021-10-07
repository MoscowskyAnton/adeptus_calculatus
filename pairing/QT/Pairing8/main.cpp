#include <QCoreApplication>
#include "scoresheettables.h"
#include "paringgame8.h"
#include "stdio.h"
#include "tablesstate.h"
#include <QThread>
#include <vector>
#include <map>

class Worker : public QObject
{
    Q_OBJECT
public:
    Worker(){

    }

    Worker(ScoreSheetTables sst, TablesState ts){
        pg = new ParingGame8(&sst, &ts);
    }

    ~Worker(){
    }

private:
    ParingGame8* pg;

public slots:
    void doWork(const int &player) {
        QString result;
        /* ... here is the expensive or blocking operation ... */
        pg->teamA.set_defender(FIRST, player);
        int score, alpha, beta, s1, s2;
        alpha = pg->SS->min_team_score;
        beta = pg->SS->max_team_score;
        pg->min(FIRST, DEFENDER, alpha, beta, &score, &s1, &s2);
        emit resultReady(score, player);
    }

signals:
    void resultReady(const int, const int);
};

void Worker::resultReady(const int a, const int b){}

class Controller : public QObject
{
    Q_OBJECT
    //QThread workerThread;
    std::vector<QThread> workerThreads;
public:
    std::vector<Worker*> workers;

    std::map<int, int> st_stage_results;

    Controller(){

    }

    Controller(ScoreSheetTables sst, TablesState ts) {
        //handleResults[0] = handleResults0;

        workerThreads = std::vector<QThread>(8);

        for(int i = 0 ; i < 8 ; i++){
            Worker *worker = new Worker(sst, ts);
            worker->moveToThread(&workerThreads[i]);
            connect(&workerThreads[i], &QThread::finished, worker, &QObject::deleteLater);
            workers.push_back(worker);
            //connect(this, &Controller::operate, worker, &Worker::doWork);
            //connect(worker, &Worker::resultReady, this, &Controller::handleResults_base);
        }

        connect(this, &Controller::operate0, workers[0], &Worker::doWork);
        connect(this, &Controller::operate1, workers[1], &Worker::doWork);
        connect(this, &Controller::operate2, workers[2], &Worker::doWork);
        connect(this, &Controller::operate3, workers[3], &Worker::doWork);
        connect(this, &Controller::operate4, workers[4], &Worker::doWork);
        connect(this, &Controller::operate5, workers[5], &Worker::doWork);
        connect(this, &Controller::operate6, workers[6], &Worker::doWork);
        connect(this, &Controller::operate7, workers[7], &Worker::doWork);

        connect(workers[0], &Worker::resultReady, this, &Controller::handleResults0);
        connect(workers[1], &Worker::resultReady, this, &Controller::handleResults1);
        connect(workers[2], &Worker::resultReady, this, &Controller::handleResults2);
        connect(workers[3], &Worker::resultReady, this, &Controller::handleResults3);
        connect(workers[4], &Worker::resultReady, this, &Controller::handleResults4);
        connect(workers[5], &Worker::resultReady, this, &Controller::handleResults5);
        connect(workers[6], &Worker::resultReady, this, &Controller::handleResults6);
        connect(workers[7], &Worker::resultReady, this, &Controller::handleResults7);

        for(int i = 0 ; i < 8 ; i++)
            workerThreads[i].start();
    }

    ~Controller() {
        for( int i = 0 ; i < 8 ; i++){
            workerThreads[i].quit();
            workerThreads[i].wait();
        }
    }
    void handleResults_base(const int & score, const int& player);
    void run();

    //void (*handleResults[8])(const int&, const int &);

public slots:
    void handleResults0(const int & s, const int & p){handleResults_base(s, p);}
    void handleResults1(const int & s, const int & p){handleResults_base(s, p);}
    void handleResults2(const int & s, const int & p){handleResults_base(s, p);}
    void handleResults3(const int & s, const int & p){handleResults_base(s, p);}
    void handleResults4(const int & s, const int & p){handleResults_base(s, p);}
    void handleResults5(const int & s, const int & p){handleResults_base(s, p);}
    void handleResults6(const int & s, const int & p){handleResults_base(s, p);}
    void handleResults7(const int & s, const int & p){handleResults_base(s, p);}
signals:
    void operate0(const int &){}
    void operate1(const int &){}
    void operate2(const int &){}
    void operate3(const int &){}
    void operate4(const int &){}
    void operate5(const int &){}
    void operate6(const int &){}
    void operate7(const int &){}
};

void Controller::handleResults_base(const int&score, const int& player){
    printf("Player %i score %i",player, score);
    st_stage_results.insert(std::pair<int, int>(score, player));

}

void Controller::run(){
    while(true){
        if(st_stage_results.size() == 8)
            break;
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);


    int scores[8][8] = {{1,0,-2,-1,0,0,2,2},
                    {-1,-1,-1,-1,-2,-2,-1,-1},
                    {1,1,-1,-1,0,-1,1,1},
                    {0,0,-1,-2,-1,-1,0,0},
                    {2,0,-1,-2,1,-2,1,2},
                    {-1,-1,-2,-2,-1,0,1,0},
                    {-1,-1,-1,-2,-1,-1,-1,-1},
                    {1,1,-2,-1,1,0,1,1}};
    int** sheet;
    sheet = new int*[8];
    for( int i = 0 ; i < 8 ; i++)
        sheet[i] = scores[i];

    ScoreSheetTables ss(8, 3, -2, 2);

    ss.print();
    printf("Mean %f\n",ss.mean());

    TablesState ts(3, 8, true, false);
    ts.print();

    Controller controller(ss, ts);
    //Controller controller();

//    emit controller.operate0(0);
//    emit controller.operate1(1);
//    emit controller.operate2(2);
//    emit controller.operate3(3);
//    emit controller.operate4(4);
//    emit controller.operate5(5);
//    emit controller.operate6(6);
//    emit controller.operate7(7);
//    controller.run();

    //ParingGame8 pg(&ss, &ts);

    //int score, alpha = ss.min_team_score, beta = ss.max_team_score, s1, s2;
    //pg.max(DEFENDER, FIRST, alpha, beta, &score, &s1, &s2);
    //printf("Score = %i", score);
    //pg.play_random();
    //pg.play_with_input();


    /*
    pg.play_optimal();

    pg.print_results();
    int optimal_score = pg.get_score();
    int N = 10;
    int random_scores[N];

    for(int i = 0 ; i < N; i++){
        pg.reset();
        pg.play_optimal_vs_random();
        pg.print_results();
        random_scores[i] = pg.get_score();
    }

    printf("Optimal score: %i\n",optimal_score);
    printf("Random scroes: ");
    for(int i = 0 ; i < N; i++){
        printf("%i ",random_scores[i]);
    }
*/
    return a.exec();
}
