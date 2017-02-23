#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFile>
#include <QFileDialog>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    polltimer(),
    my_gui(),
    parsers(),
    plottime(),
    ratetime()

{
    ui->setupUi(this);

    n_datagrams_last=0;
    //loadGuiSettings();

    //connect(&polltimer, SIGNAL(timeout()), this, SLOT(on_pushButton_getStat_clicked()));


    scope=0;
    myudp=0;
    mypparse=0;


    plottime.start();
piperead=0;

     data_fifo=0;

     ui->label_builddate->setText(QString("%1T%2").arg(__DATE__).arg(__TIME__));

}



MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::addParser(roachParser *p)
{
    parsers.append(p);
}


void MainWindow::addSaver(fileSaver *fs)
{
    savers.append(fs);

}

void MainWindow::updateGui(void)
{

    QString txt;

    if (parsers.length()==2)
    {

        txt =txt +  QString("Events:\n%1\n").arg(parsers[0]->evtcnt);
        txt = txt +  QString("Searchs:\n%1\n").arg(parsers[0]->searches);
        txt = txt +  QString("BadEvts:\n%1\n").arg(parsers[0]->nbad_events);
        txt = txt +  QString("NoData:\n%1\n").arg(parsers[0]->no_bytes_avail);
        txt = txt +  QString("Qlen:\n%1\n").arg(parsers[0]->data_source->length());
        txt = txt +  QString("nparse:\n%1\n").arg(parsers[0]->num_parse_calls);

        txt = txt +  QString("ndone_parse:\n%1\n").arg(parsers[0]->ndone_parse);
        txt = txt +  QString("Queued Lists:\n%1\n").arg(parsers[0]->getListQueueLength());
        txt = txt +  QString("Pulses:\n%1\n").arg(parsers[0]->pulse_counter);

        ui->label_parserA->setText(txt);

        txt.clear();

        txt  = txt + QString("Events:\n%1\n").arg(parsers[1]->evtcnt);
        txt  = txt + QString("Searchs:\n%1\n").arg(parsers[1]->searches);
        txt  = txt + QString("BadEvts:\n%1\n").arg(parsers[1]->nbad_events);
        txt = txt +  QString("NoData:\n%1\n").arg(parsers[1]->no_bytes_avail);
        txt = txt +  QString("Qlen:\n%1\n").arg(parsers[1]->data_source->length());
        txt = txt +  QString("nparse:\n%1\n").arg(parsers[1]->num_parse_calls);
        txt = txt +  QString("ndone_parse:\n%1\n").arg(parsers[1]->ndone_parse);
        txt = txt +  QString("Queued Lists:\n%1\n").arg(parsers[1]->getListQueueLength());
        txt = txt +  QString("Pulses:\n%1\n").arg(parsers[1]->pulse_counter);

        ui->label_parserB->setText(txt);


        if (scope && plottime.elapsed()>500)
        {

            plottime.restart();
            int plsize = 10000;
            QVector<double> x(plsize),y(plsize);
            int chan = 0;
            int lnx =(*(parsers[1]->events))[chan]["stream_mag"].length();
           // int lnx =parsers[1]->(*events)[chan]["stream_mag"].length();
            int ptx;
            if (lnx>plsize)
            {
                int kk=0;
                for (ptx=(lnx-plsize);ptx<lnx;ptx++)
                {
                    x[kk]=(double)kk;
                    y[kk]=(double)(*(parsers[1]->events))[chan]["stream_mag"][ptx];
                    kk++;
                }
            }
          scope->plotNow(x,y);
        }







    }


    if (mypparse && data_fifo)
    {

        QHash<QString,int> *clist = mypparse->getCounters();
        txt.clear();

        txt  = txt + QString("Searches:\n%1\n").arg( (*clist)["searches"] );
        txt  = txt + QString("Fnd ZZ:\n%1\n").arg( (*clist)["num_found_zzz"]);
        txt  = txt + QString("GoodPacks:\n%1\n").arg( (*clist)["num_good_packets"]);
        txt = txt +  QString("NPacks:\n%1\n").arg( (*clist)["n_datagrams"]);

        txt = txt +  QString("num_data_words:\n%1\n").arg( (*clist)["num_data_words"]);
        txt = txt +  QString("bind_stat:\n%1\n").arg( (*clist)["bind_stat"]);
        txt = txt +  QString("datagramlen:\n%1\n").arg( (*clist)["datagramlen"]);

        txt = txt +  QString("packet_num_a:\n%1\n").arg( (*clist)["packet_num_a"]);
        txt = txt +  QString("packinc_a:\n%1\n").arg( (*clist)["packinc_a"]);
        txt = txt +  QString("lost_packets:\n%1\n").arg( (*clist)["lost_packets"]);
        txt = txt +  QString("ne_packnab:\n%1\n").arg( (*clist)["ne_packnab"]);

        txt = txt +  QString("packetQ Len:\n%1\n").arg( data_fifo->length());
        txt = txt +  QString("n_datagrams :\n%1\n").arg( myudp->n_datagrams);
        txt = txt +  QString("n_packets :\n%1\n").arg( myudp->n_packets);
        txt = txt +  QString("n_nomemory :\n%1\n").arg( myudp->n_nomemory);
        txt = txt +  QString("dgramlen :\n%1\n").arg( myudp->dgramlen);


        float sec =0.001 *  (float)ratetime.elapsed();
        ratetime.restart();
        int delta_dgrams = myudp->n_packets - n_datagrams_last;
        n_datagrams_last = myudp->n_packets;

        float datarate =(( (float) delta_dgrams ) * (float )( myudp->dgramlen)  )/ (sec*1e6);
        txt = txt +  QString("datarate:\n%1 MB/s\n").arg( datarate);

        ui->label_udpStat->setText(txt);

        int k=0;
        txt.clear();


#if 0
        while (k< ((*clist)["datagramlen"] ))
        {
            //baddatagram
            //lastdatagram
            txt=txt + QString("%1%2 %3%4 %5%6 %7%8\n").
                    arg(255&(mypparse->lastdatagram[k]),2,16).
                    arg(255&(mypparse->lastdatagram[k+1]),2,16).
                    arg(255&(mypparse->lastdatagram[k+2]),2,16).
                    arg(255&(mypparse->lastdatagram[k+3]),2,16).
                    arg(255&(mypparse->lastdatagram[k+4]),2,16).
                    arg(255&(mypparse->lastdatagram[k+5]),2,16).
                    arg(255&(mypparse->lastdatagram[k+6]),2,16).
                    arg(255&(mypparse->lastdatagram[k+7]),2,16);
            k=k+8;

        }

   #endif

        ui->label_RcvData->setText(txt);

    }

}

void MainWindow::setPipeReader(pipeReader *p)
{
    piperead=p;

}


void MainWindow::setPacketFifo(packetFifo *dq)
{
    data_fifo=dq;

}

void MainWindow::setPacketParser(packetParse *pp)
{

    mypparse=pp;
}

void MainWindow::setUdp(udpRcv *u)
{
    myudp=u;
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

        myudp->initSocket(my_gui.txdestip,my_gui.txdestport);



        QMetaObject::invokeMethod(
                    myudp,
                    "readData",
                    Qt::QueuedConnection);
//!!#endif
    }
    else
    {

        myudp->closeSock();
        usleep(100000);
        //clear out fifo


        mypparse->dumpFifo();
        usleep(100000);



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

void MainWindow::on_pushButton_clearEvents_clicked()
{
     mypparse->dumpFifo();
     while(mypparse->is_dump_fifos)
         usleep(100000);

    if (parsers.length()==2)
    {

        parsers[0]->clearEvents();
        parsers[1]->clearEvents();
    }
}

void MainWindow::on_pushButton_saveEvents_clicked()
{


    QFileDialog fd(this);
    QString fname=fd.getSaveFileName();


    if (parsers.length()==2 &&fname.length()>0)
    {
        parsers[0]->queueEvents();

        parsers[1]->queueEvents();

    }
    if (savers.length()==2 && fname.length()>0)
    {
        savers[0]->setFileName(fname+"_A");
        savers[0]->doSaveAll();
        savers[1]->setFileName(fname+"_B");
        savers[1]->doSaveAll();

    }



}

void MainWindow::on_checkBox_readpipe_clicked(bool checked)
{
    if (piperead)
     piperead->isWriteFifo(checked);
}

void MainWindow::on_checkBox_writePipe_clicked(bool checked)
{
    mypparse->writeToPipe(checked);
}

void MainWindow::on_pushButton_dumpPacketFifo_clicked()
{
    mypparse->dumpFifo();
}

void MainWindow::on_lineEdit_pipeName_editingFinished()
{

}

void MainWindow::on_lineEdit_pipeName_textEdited(const QString &arg1)
{
    mypparse->setPipeName(arg1);
}

void MainWindow::on_checkBox_streamEv2Disk_clicked(bool checked)
{
    bool is_currently_streaming = savers[1]->getIsStream();

    savers[0]->setIsStream(checked);
    savers[1]->setIsStream(checked);

    //run thread if not already runnibng.
    // also run even if we have checked false. in this case it
    // runs thread one loop and quits, saving nothing.
    // it forces a signal to emit from file saver sayint its done.
    if (!is_currently_streaming)
    {
    QMetaObject::invokeMethod(
                savers[0],
                "doSaveThread",
                Qt::QueuedConnection);

    QMetaObject::invokeMethod(
                savers[1],
                "doSaveThread",
                Qt::QueuedConnection);
    }

}

void MainWindow::on_checkBox_isPulseDetect_clicked(bool checked)
{
    parsers[0]->setIsPulseDetect(checked);
    parsers[1]->setIsPulseDetect(checked);

}



void MainWindow::on_lineEdit_pulseThresh_returnPressed()
{
    parsers[0]->pulse_thresh =(ui->lineEdit_pulseThresh->text()).toDouble();
    parsers[1]->pulse_thresh =(ui->lineEdit_pulseThresh->text()).toDouble();

}

void MainWindow::on_lineEdit_pulseSaveEvts_returnPressed()
{
    int nevts = (ui->lineEdit_pulseSaveEvts->text()).toInt();
    parsers[0]->save_max_count = nevts;
            parsers[1]->save_max_count = nevts;

}

void MainWindow::on_checkBox_isPulseDetectFRD_clicked(bool checked)
{
    parsers[0]->setIsPulseDetectFRD(checked);
    parsers[1]->setIsPulseDetectFRD(checked);
}

void MainWindow::on_pushButton_fakeEvents_clicked()
{
    //parsers[0]->setIsPulseDetectFRD(checked);
    parsers[1]->makeFakeEventStream();
}
