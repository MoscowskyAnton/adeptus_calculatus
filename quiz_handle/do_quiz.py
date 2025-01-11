import numpy as np
import os
import matplotlib.pyplot as plt

ANSWERS = ["1. Opressor",
           "2. Relic Cannon",
           "3. MCT bug",
           "4. Cadia Creed",
           "5. Lone HWT",
           "6. Orders Abhumans",
           "7. Fire Fallback",
           "8. Leman Russ Guns",
           ]


if __name__ == '__main__':

    # preproc peoples

    def preproc_people(path):
        peoples = []
        with open(path, "r") as file:

            line = file.readline()
            peoples.append(line[:-1])
            counter = 0
            while line:
                counter += 1
                line = file.readline()
                if counter == 3 and len(line) != 0:
                    peoples.append(line[:-1])
                    counter = 0

        return peoples

    #print(preproc_people("1_correct"))

    #RESULTS = []
    RATE = {}

    for ans in ANSWERS:
        no = int(ans[0])
        p_c = preproc_people(f"{no}_correct")
        for person in p_c:
            if not person in RATE:
                RATE[person] = []
            RATE[person].append(2)

        p_i = preproc_people(f"{no}_incorrect")
        for person in p_i:
            if not person in RATE:
                RATE[person] = []
            RATE[person].append(-1)

        p_p = preproc_people(f"{no}_pass")
        for person in p_p:
            if not person in RATE:
                RATE[person] = []
            RATE[person].append(0)

        #RESULTS.append((p_c, p_i, p_p))

    print(RATE)

    SCORE = {}

    for per, rate in RATE.items():
        SCORE[per] = sum(rate)


    SCORE = dict(sorted(SCORE.items(), key=lambda item: item[1]))

    print(SCORE)

    plt.figure("score")

    cmap = plt.get_cmap('RdYlGn')
    l = len(ANSWERS)*3.
    m = min(SCORE.values())
    #plt.plot(SCORE.values(), '*')
    for i, score in enumerate(SCORE.values()):
        plt.plot(i, score, '*', color = cmap(score - m / l))

    plt.title("Результаты Викторины #quiz_codex_2025@desert_corps")
    plt.grid()
    plt.xticks(np.arange(len(SCORE)), SCORE.keys(), rotation = 90)
    plt.yticks(np.arange(m, len(ANSWERS)*2))
    plt.ylabel("score")
    plt.tight_layout()

    plt.show()






