#include "mainwindow.h"
#include <QApplication>
#include "udprcv.h"
#include <QThread>
#include "guisettings.h"
#include "roachparser.h"
#include "dataqueue.h"
#include "roachscope.h"
#include "packetFifo.h"
#include "packetParse.h"
#include "../roachUDPBuffer/pipereader.h"
#include "textcommander.h"
#include <QTimer>
#include "argparse.h"

int main(int argc, char *argv[])
{
    qRegisterMetaType<QVector<double> >("QVector<double>");

    QApplication a(argc, argv);

    argParse arguments;

    arguments.parseArgs(a.arguments());


    MainWindow w;

    packetFifo data_fifo;


    //pipeReader piperead("",1472,&data_fifo);
   // QThread pt;
   // piperead.moveToThread(&pt);
   //!! pt.start();

    data_fifo.fillFifo(arguments.q_length,arguments.q_packetlen);

//!! nc -ul 192.168.1.102 50000 | ./testEnet

    udpRcv myudp(&data_fifo);

    QThread udpth;
    myudp.moveToThread(&udpth);
    udpth.start(QThread::TimeCriticalPriority);


    packetParse pparse(&data_fifo);
    QThread pparse_th;
    pparse.moveToThread(&pparse_th);
    pparse_th.start();

    dataQueue *stream_a = pparse.getOutQueueA();
    dataQueue *stream_b = pparse.getOutQueueB();

    roachParser parser_a(stream_a);
    roachParser parser_b(stream_b,128);

    QThread parseth_a;
    QThread parseth_b;

    parser_a.moveToThread(&parseth_a);
    parser_b.moveToThread(&parseth_b);

   parseth_a.start();
    parseth_b.start();


    w.setUdp(&myudp);
    w.addParser(&parser_a);
    w.addParser(&parser_b);
    w.setPacketParser(&pparse);
    w.setPacketFifo(&data_fifo);

    //w.setPipeReader(&piperead);

    /**
       pparse.connect(
                &myudp,
                SIGNAL(socketOpen()),
                SLOT(writeStreams()),
                Qt::QueuedConnection);


       pparse.connect(
                &myudp,
                SIGNAL(socketClose()),
                SLOT(stopStreams()),
                Qt::DirectConnection);

    */

    QMetaObject::invokeMethod(
                &pparse,
                "writeStreams",
                Qt::QueuedConnection);


    parser_a.connect(
                &pparse,
                SIGNAL(dataAvailA()),
                SLOT(parseStream()),
                Qt::QueuedConnection);

    parser_b.connect(
                &pparse,
                SIGNAL(dataAvailB()),
                SLOT(parseStream()),
                Qt::QueuedConnection);

    QTimer disp_timer;
    disp_timer.start(200);
    w.connect(&disp_timer,SIGNAL(timeout()),SLOT(updateGui()),Qt::QueuedConnection);


    textCommander cmd(arguments.cmd_in_pipe_name,arguments.cmd_out_pipe_name);
    cmd.addNameObject("parser_a",&parser_a);
    cmd.addNameObject("parser_b",&parser_b);
    cmd.addNameObject("pparse",&pparse);
   // cmd.addNameObject("piperead",&piperead);
    cmd.addNameObject("w",&w);
    cmd.setAppName("roachstream");


    bool isc = cmd.connect(&parser_a,SIGNAL(saveDone(QString)),SLOT(sendCommand(QString)),Qt::DirectConnection);

    isc = cmd.connect(&parser_b,SIGNAL(saveDone(QString)),SLOT(sendCommand(QString)),Qt::DirectConnection);


    QThread cmdth;
    cmd.moveToThread(&cmdth);
    cmdth.start();
    QMetaObject::invokeMethod(
             &cmd,
             "openInputPipe",
             Qt::AutoConnection);
     QMetaObject::invokeMethod(
         &cmd,
         "openOutputPipe",
         Qt::AutoConnection);
     QMetaObject::invokeMethod(
         &cmd,
         "waitNextCommand",
         Qt::AutoConnection);



    w.show();
    
    return a.exec();
}
