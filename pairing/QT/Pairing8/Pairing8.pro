QT -= gui

CONFIG += c++11 console
CONFIG -= app_bundle

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        gamestate8.cpp \
        main.cpp \
        paringgame8.cpp \
        scoresheet.cpp \
        scoresheettables.cpp \
        tablesstate.cpp

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    gamestate8.h \
    paringgame8.h \
    scoresheet.h \
    scoresheettables.h \
    tablesstate.h
