#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTimer>
#include "guisettings.h"
#include "udprcv.h"
#include "QThread"
#include "roachscope.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    

    void saveGuiSettings(void);

    void loadGuiSettings(void);

private slots:

    void on_lineEdit_destIP_textChanged(const QString &arg1);

    void on_lineEdit_destPort_textChanged(const QString &arg1);

    void on_checkBox_streamUDP_clicked(bool checked);

    void on_checkBox_scopeOpen_clicked(bool checked);

private:
    Ui::MainWindow *ui;

    guiSettings my_gui;

    QTimer polltimer;

    udpRcv myudp;

    roachScope *scope;



};

#endif // MAINWINDOW_H
