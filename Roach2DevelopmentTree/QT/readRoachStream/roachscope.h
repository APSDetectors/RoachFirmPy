#ifndef ROACHSCOPE_H
#define ROACHSCOPE_H

#include <QMainWindow>
#include "guisettings.h"
#include <QTimer>

namespace Ui {
class roachScope;
}

class roachScope : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit roachScope(guiSettings &gui, QWidget *parent = 0);
    ~roachScope();
    
private slots:


    void on_pushButton_scopeTrig_clicked();

    void on_checkBox_scopeCapture_clicked(bool checked);

    void on_spinBox_scopeInput_valueChanged(int arg1);

    void on_pushButton_scopeData_clicked();

    void on_poll_timer();

    void on_checkBox_zoomX_clicked(bool checked);

    void on_checkBox_zoomY_clicked(bool checked);

private:
    Ui::roachScope *ui;
    guiSettings &my_gui;
    QTimer poller;

    void setZooming(void);

    bool is_zoom_x;
    bool is_zoom_y;

};

#endif // ROACHSCOPE_H
