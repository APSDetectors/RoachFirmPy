#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTimer>
#include "guisettings.h"
#include "udprcv.h"
#include "QThread"
#include "roachscope.h"
#include "roachparser.h"
#include "packetParse.h"
#include <QTime>
#include "../roachUDPBuffer/pipereader.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    guiSettings my_gui;


    void saveGuiSettings(void);

    void loadGuiSettings(void);
    void setUdp(udpRcv *u);
    void setPacketParser(packetParse *pp);

    void setPacketFifo(packetFifo *dq);
    void addParser(roachParser *p);
    void setPipeReader(pipeReader *p);


private slots:

    void on_lineEdit_destIP_textChanged(const QString &arg1);

    void on_lineEdit_destPort_textChanged(const QString &arg1);

    void on_checkBox_streamUDP_clicked(bool checked);

    void on_checkBox_scopeOpen_clicked(bool checked);

    void updateGui(void);

    void on_pushButton_clearEvents_clicked();

    void on_pushButton_saveEvents_clicked();



    void on_checkBox_readpipe_clicked(bool checked);

private:
    Ui::MainWindow *ui;


    QTimer polltimer;

    QTime plottime;

    QTime ratetime;
    udpRcv *myudp;
    packetParse *mypparse;

    roachScope *scope;
    QList<roachParser*> parsers;

    packetFifo *data_fifo;
    pipeReader *piperead;
    int n_datagrams_last;

};

#endif // MAINWINDOW_H
