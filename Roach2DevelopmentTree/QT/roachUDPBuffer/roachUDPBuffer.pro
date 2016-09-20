#-------------------------------------------------
#
# Project created by QtCreator 2015-10-29T10:27:04
#
#-------------------------------------------------

QT       += core

QT       -= gui

TARGET = roachUDPBuffer
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += main.cpp \
    ../readRoachStream/packetFifo.cpp \
    pipereader.cpp \
    pipewriter.cpp

HEADERS += \
    ../readRoachStream/packetFifo.h \
    pipereader.h \
    pipewriter.h
