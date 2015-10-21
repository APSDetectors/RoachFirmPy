#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    polltimer(),
    my_gui(),
  myudp()
{
    ui->setupUi(this);



    connect(&polltimer, SIGNAL(timeout()), this, SLOT(on_pushButton_getStat_clicked()));


    connect(&myudp,
            SIGNAL(newData(QByteArray ,QHostAddress ,quint16 )),
            this,
            SLOT(newData(QByteArray ,QHostAddress ,quint16 )));

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_spinBox_sendPackLength_valueChanged(int arg1)
{
    my_gui.txframelength=arg1;

    if (my_gui.which_xmit==0)
        my_gui.roachWriteInt("testData_framelength",arg1);
    else
        my_gui.roachWriteInt("testData1_framelength",arg1);
}

void MainWindow::on_lineEdit_destIP_textChanged(const QString &arg1)
{
    strcpy(my_gui.txdestipstr,arg1.toStdString().c_str());
    my_gui.txdestip=my_gui.ipStrToInt(arg1);
    printf("%s --> 0x%x\n",my_gui.txdestipstr, my_gui.txdestip);

    if (my_gui.which_xmit==0)
        my_gui.roachWriteInt("txdestip",my_gui.txdestip);
    else
        my_gui.roachWriteInt("txdestip1",my_gui.txdestip);
}

void MainWindow::on_lineEdit_destPort_textChanged(const QString &arg1)
{
    my_gui.txdestport = arg1.toInt();
     if (my_gui.which_xmit==0)
        my_gui.roachWriteInt("txdestport",my_gui.txdestport);
    else
          my_gui.roachWriteInt("txdestport1",my_gui.txdestport);
}

void MainWindow::on_checkBox_streamUDP_clicked(bool checked)
{
    if (checked)
        my_gui.txstream=1;
    else
         my_gui.txstream=0;

   if (my_gui.which_xmit==0)
   {
    my_gui.setControl0();


    //!! tell python
    my_gui.roachWriteInt("control0",my_gui.control0);
   }
   else
   {
       my_gui.setControl1();


       //!! tell python
       my_gui.roachWriteInt("control1",my_gui.control1);
   }


}

void MainWindow::on_pushButton_sendOnePack_clicked()
{
    on_spinBox_sendPackLength_valueChanged(
                ui->spinBox_sendPackLength->value());

    on_lineEdit_destIP_textChanged(
                ui->lineEdit_destIP->text());

    on_lineEdit_destPort_textChanged(
                ui->lineEdit_destPort->text());

    if (my_gui.which_xmit==0)
    {



    my_gui.txpacket=1;
     my_gui.setControl0();//!! need to add txpacket to control0

     //!!do python

     my_gui.roachWriteInt("control0",my_gui.control0);



     my_gui.txpacket=0;
      my_gui.setControl0();
      //!!do python
      my_gui.roachWriteInt("control0",my_gui.control0);

    }
    else
    {
        my_gui.txpacket=1;
         my_gui.setControl1();//!! need to add txpacket to control0

         //!!do python

         my_gui.roachWriteInt("control1",my_gui.control1);



         my_gui.txpacket=0;
          my_gui.setControl1();
          //!!do python
          my_gui.roachWriteInt("control1",my_gui.control1);
    }

}

void MainWindow::on_checkBox_rstXaui_clicked(bool checked)
{
    if (checked)
        my_gui.xauireset=1;
    else
        my_gui.xauireset=0;

      if (my_gui.which_xmit==0)
    {
          my_gui.setControl0();


    //!! tell python
    my_gui.roachWriteInt("control0",my_gui.control0);
    }
      else
      {
                my_gui.setControl1();


          //!! tell python
          my_gui.roachWriteInt("control1",my_gui.control1);
      }

}

void MainWindow::on_pushButton_saveDataToRAM_clicked()
{
    //!! get text from the window
    QString text = ui->textEdit_dataToSend->toPlainText();


    // copy text to my gui,
    strcpy((char*)my_gui.xmitdata,text.toStdString().c_str());

    //tell python to update RAM
    //!!do python
    if (my_gui.which_xmit==0)
        my_gui.roachWrite("testData_xmitdata64",my_gui.xmitdata);
    else
        my_gui.roachWrite("testData1_xmitdata64",my_gui.xmitdata);
}

void MainWindow::on_pushButton_readRcvRam_clicked()
{
   QString data;

    if (my_gui.which_xmit==0)
       data = my_gui.roachRead("capture_rcvdata",1024);
    else
        data = my_gui.roachRead("capture1_rcvdata",1024);

   QString mytext;

   int linelen=32;
   //lines...
   for (int k = 0; k<50;k++)
   {
       mytext = mytext + data.mid(k*linelen,linelen);
       mytext = mytext+ "\n";

   }
   ui->label_RcvData->setText(mytext);
printf("%s\n",mytext.toStdString().c_str());


}

void MainWindow::on_pushButton_getStat_clicked()
{
    my_gui.getStatusRegs();
    QString txt;

    txt = QString("LEDTx0: %1\n").arg((unsigned int)my_gui.LedTx0&0xffffff);
    txt = txt + QString("LEDUp0: %1\n").arg((unsigned int)my_gui.LedUp0&0xffffff);
    txt = txt + QString("LEDRx1: %1\n").arg((unsigned int)my_gui.LedRx1&0xffffff);
    txt = txt + QString("LEDUp1: %1\n").arg((unsigned int)my_gui.LedUp1&0xffffff);
    txt = txt + QString("Stat0: %1\n").arg(my_gui.statPort0);
    txt = txt + QString("Stat1: %1\n").arg(my_gui.statPort1);

    txt = txt + QString("RdIsP: %1\n").arg(my_gui.RdIsPacket_dbgCount&0xffffff);
    txt = txt + QString("RxVld1: %1\n").arg(my_gui.RxVld1_dbgCount&0xffffff);
    txt = txt + QString("TxEOF0: %1\n").arg(my_gui.TxEOF0_dbgCount&0xffffff);
    txt = txt + QString("rmemad: %1\n").arg(my_gui.capture_rcvmemaddr);
    txt = txt + QString("frlen: %1\n").arg(my_gui.testData_framelength);





    ui->label_statMessages->setText(txt);

    txt=QString(my_gui.rcv_src_ip_str);
    ui->label_rcvFromIP->setText(txt);

    txt=QString("%1").arg(my_gui.rcv_src_port);

    ui->label_rcvFromIP->setText(txt);


}

void MainWindow::on_lineEdit_pyPipeInName_textChanged(const QString &arg1)
{
    strcpy(my_gui.pypipe_in,arg1.toStdString().c_str());

}

void MainWindow::on_lineEdit_pyPipeOutName_textChanged(const QString &arg1)
{
    strcpy(my_gui.pypipe_out,arg1.toStdString().c_str());
}

void MainWindow::on_checkBox_openPyPipe_clicked(bool checked)
{
    my_gui.is_pipe_open=checked;
    // open or close the py pipe

    if (my_gui.is_pipe_open)
     {

        my_gui.openPipes();
        ui->lineEdit_destIP->setText("192.168.1.102");
        ui->lineEdit_destPort->setText("54321");
        ui->spinBox_sendPackLength->setValue(5);
     }
    else
        my_gui.closePipes();
}

void MainWindow::on_pushButton_setupPy_clicked()
{
    my_gui.setupPython();


}

void MainWindow::on_pushButton_listReg_clicked()
{
    QString cmd;


    cmd = QString("roach2.readAllReg()");

    my_gui.writeLine(cmd);
}

void MainWindow::on_checkBox_poll_clicked(bool checked)
{

   if (checked)
    {
       polltimer.start(1000);
    }
   else
   {
       polltimer.stop();
   }
}

void MainWindow::on_pushButton_rewindRam_clicked()
{

    if (my_gui.which_xmit==0)
    {
        my_gui.rewindram=1;

    my_gui.setControl0();
    my_gui.roachWriteInt("control0",my_gui.control0);

    my_gui.rewindram=0;

    my_gui.setControl0();
    my_gui.roachWriteInt("control0",my_gui.control0);
    }
    else
    {
        my_gui.rewindram=1;

    my_gui.setControl1();
    my_gui.roachWriteInt("control1",my_gui.control1);

    my_gui.rewindram=0;

    my_gui.setControl1();
    my_gui.roachWriteInt("control1",my_gui.control1);
    }

}

void MainWindow::on_checkBox_listenOnCPU_clicked(bool checked)
{
    if (checked)
    {
        QString ip;
        unsigned short port;

        ip=ui->lineEdit_listenIP->text();
        port = ui->lineEdit_listenPort->text().toUShort();

        myudp.initSocket(ip,port);


        printf("Maingwindow: Started Socket\n");
    }
    else
    {
        myudp.closeSock();
    }
}

void MainWindow::newData(QByteArray data,QHostAddress addr,quint16 port)
{



    QString mytext;

    mytext = QString(data);

    ui->label_RcvData->setText(mytext);
 printf("%s\n",mytext.toStdString().c_str());


}

void MainWindow::on_pushButton_deMAC_clicked()
{
    QString device = ui->comboBox_whichXmit->currentText();
    QString cmd = QString("roach2.stopEth('%1')").arg(device);
    my_gui.writeLine(cmd);

}

void MainWindow::on_pushButton_reMAC_clicked()
{
    QString device = ui->comboBox_whichXmit->currentText();
    QString ip = ui->lineEdit_roachIP->text();
    QString port = ui->lineEdit_roachPort->text();
    QString mac = ui->lineEdit_roachMAC->text();

    QString cmd = QString("roach2.setupEth('%1','%2',%3,'%4')").arg(device).arg(ip).arg(port).arg(mac);
    my_gui.writeLine(cmd);
}

void MainWindow::on_pushButton_MACInfo_clicked()
{
    QString cmd = QString("roach2.infoEth()");
    my_gui.writeLine(cmd);
}

void MainWindow::on_pushButton_reBof_clicked()
{

    QString bof = ui->lineEdit_bofFile->text();

    QString cmd = QString("roach2.sendBof('%1')").arg(bof);
    my_gui.writeLine(cmd);


}

void MainWindow::on_comboBox_whichXmit_currentIndexChanged(int index)
{
    my_gui.which_xmit=index;
}

void MainWindow::on_pushButton_restart_clicked()
{
    QString cmd = QString("roach2.restart()");
    my_gui.writeLine(cmd);
}
