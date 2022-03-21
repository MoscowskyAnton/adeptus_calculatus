TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
#CONFIG -= qt

SOURCES += \
        ../Pairing8/gamestate8.cpp \
        ../Pairing8/paringgame8.cpp \
        ../Pairing8/scoresheet.cpp \
        ../Pairing8/scoresheettables.cpp \
        ../Pairing8/tablesstate.cpp \
        main.cpp

HEADERS += \
    ../Pairing8/gamestate8.h \
    ../Pairing8/paringgame8.h \
    ../Pairing8/scoresheet.h \
    ../Pairing8/scoresheettables.h \
    ../Pairing8/tablesstate.h
