#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTimer>
#include "guisettings.h"
#include "udprcv.h"
#include "QThread"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    
private slots:
    void on_spinBox_sendPackLength_valueChanged(int arg1);

    void on_lineEdit_destIP_textChanged(const QString &arg1);

    void on_lineEdit_destPort_textChanged(const QString &arg1);

    void on_checkBox_streamUDP_clicked(bool checked);

    void on_pushButton_sendOnePack_clicked();

    void on_checkBox_rstXaui_clicked(bool checked);

    void on_pushButton_saveDataToRAM_clicked();

    void on_pushButton_readRcvRam_clicked();

    void on_pushButton_getStat_clicked();

    void on_lineEdit_pyPipeInName_textChanged(const QString &arg1);

    void on_lineEdit_pyPipeOutName_textChanged(const QString &arg1);

    void on_checkBox_openPyPipe_clicked(bool checked);

    void on_pushButton_setupPy_clicked();

    void on_pushButton_listReg_clicked();

    void on_checkBox_poll_clicked(bool checked);

    void on_pushButton_rewindRam_clicked();

    void on_checkBox_listenOnCPU_clicked(bool checked);

    void on_pushButton_deMAC_clicked();

    void on_pushButton_reMAC_clicked();

    void on_pushButton_MACInfo_clicked();

    void on_pushButton_reBof_clicked();

    void on_comboBox_whichXmit_currentIndexChanged(int index);

    void on_pushButton_restart_clicked();

private:
    Ui::MainWindow *ui;

    guiSettings my_gui;

    QTimer polltimer;

    udpRcv myudp;


public slots:
     void newData(QByteArray data,QHostAddress addr,quint16 port);

};

#endif // MAINWINDOW_H
