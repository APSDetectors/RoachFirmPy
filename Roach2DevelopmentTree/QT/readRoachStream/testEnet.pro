#-------------------------------------------------
#
# Project created by QtCreator 2015-03-31T10:04:43
#
#-------------------------------------------------

QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = testEnet
TEMPLATE = app

INCLUDEPATH +=../qcustomplot-source
INCLUDEPATH +=/home/beams0/TMADDEN/swWork/hdf5/hdf5-1.8.7-linux-x86_64-static/include
LIBS +=-L/home/beams0/TMADDEN/swWork/hdf5/hdf5-1.8.7-linux-x86_64-static/lib -lhdf5 -lsz -lz
SOURCES += main.cpp\
        mainwindow.cpp \
    guisettings.cpp \
    udprcv.cpp \
    roachscope.cpp \
    ../qcustomplot-source/qcustomplot.cpp \
    roachparser.cpp \
    dataqueue.cpp \
    packetParse.cpp \
    packetFifo.cpp \
    ../roachUDPBuffer/pipereader.cpp \
    textcommander.cpp \
    argparse.cpp \
    filesaver.cpp \
    hdffilesaver.cpp \
    epicsv4support.cpp

HEADERS  += mainwindow.h \
    guisettings.h \
    udprcv.h \
    roachscope.h \
    ../qcustomplot-source/qcustomplot.h \
    roachparser.h \
    dataqueue.h \
    packetParse.h \
    packetFifo.h \
    ../roachUDPBuffer/pipereader.h \
    textcommander.h \
    argparse.h \
    filesaver.h \
    hdffilesaver.h \
    epicsv4support.h

FORMS    += mainwindow.ui \
    roachscope.ui

OTHER_FILES += \
    roachsetup.py \
    ../build-testEnet-Desktop-Debug/settings.py \
    debug.py
