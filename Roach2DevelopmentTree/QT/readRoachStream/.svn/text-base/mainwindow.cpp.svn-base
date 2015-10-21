#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFile>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    polltimer(),
    my_gui(),
  myudp()
{
    ui->setupUi(this);

    //loadGuiSettings();

    //connect(&polltimer, SIGNAL(timeout()), this, SLOT(on_pushButton_getStat_clicked()));


    scope=0;

}



MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::saveGuiSettings(void)
{
   /* QFile file("settings.py");
    if (file.open(QFile::WriteOnly | QFile::Truncate))
    {
        QTextStream out(&file);

        out << "pywindow=\n";
        out << "\"\"\"\n";

        out << ui->textEdit_dataToSend->toPlainText();

        out << "\n\"\"\"\n";

        out << "\n\n";

        out << "rebof=\n";

        out << "\"\"\"\n";
        out << ui->lineEdit_bofFile->text();
        out << "\n\"\"\"\n";

        file.close();
    }*/

}

void MainWindow::loadGuiSettings(void)
{
   /* QFile file("settings.py");
    if (file.open(QFile::ReadOnly))
    {
        QTextStream in(&file);
        QString line=in.readLine();
        while (!line.isNull())
        {
            if (line.contains("pywindow"))
            {
                line=in.readLine();//"""
                line=in.readLine();
                QString txt;
                while (!line.contains("\"\"\""))
                {
                    txt=txt + line + "\n";
                    line=in.readLine();
                }
                ui->textEdit_dataToSend->setText(txt);
            }
            else if (line.contains("rebof"))
            {
                line=in.readLine();//"""
                line=in.readLine();//real data
                ui->lineEdit_bofFile->setText(line);
                line=in.readLine();//"""
            }
            else
                line=in.readLine();
        }
        file.close();
    }*/
}


void MainWindow::on_lineEdit_destIP_textChanged(const QString &arg1)
{

    my_gui.txdestip=arg1;


}

void MainWindow::on_lineEdit_destPort_textChanged(const QString &arg1)
{
    my_gui.txdestport = arg1.toInt();



}

void MainWindow::on_checkBox_streamUDP_clicked(bool checked)
{
    my_gui.txstream=checked;


    //open udb port and capture data
    if (my_gui.txstream)
    {

        myudp.initSocket(my_gui.txdestip,my_gui.txdestport);
    }
    else
    {
        myudp.closeSock();
    }
}






void MainWindow::on_checkBox_scopeOpen_clicked(bool checked)
{
    if (checked)
    {
        scope=new roachScope(my_gui);
        scope->show();
    }
    else
    {
        if (scope!=0)
        {
            scope->hide();
            delete scope;
        }

        scope=0;

    }

}
