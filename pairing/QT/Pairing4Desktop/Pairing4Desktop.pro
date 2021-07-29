QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    ../Pairing4/gamestate4.cpp \
    ../Pairing4/paringgame4.cpp \
    ../Pairing4/scoresheettables.cpp \
    ../Pairing4/tablesstate.cpp \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    ../Pairing4/gamestate4.h \
    ../Pairing4/paringgame4.h \
    ../Pairing4/scoresheettables.h \
    ../Pairing4/tablesstate.h \
    mainwindow.h

FORMS += \
    mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

DESTDIR   = $$PWD/bin

build_pass:CONFIG(release, debug|release){
    QMAKE_POST_LINK += windeployqt --release --compiler-runtime $$DESTDIR/Pairing4Desktop.exe
}
