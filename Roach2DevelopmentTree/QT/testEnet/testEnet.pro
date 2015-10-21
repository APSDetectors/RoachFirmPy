#-------------------------------------------------
#
# Project created by QtCreator 2015-03-31T10:04:43
#
#-------------------------------------------------

QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = testEnet
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    guisettings.cpp \
    udprcv.cpp

HEADERS  += mainwindow.h \
    guisettings.h \
    udprcv.h

FORMS    += mainwindow.ui

OTHER_FILES += \
    roachsetup.py
