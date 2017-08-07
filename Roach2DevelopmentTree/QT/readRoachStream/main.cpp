

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
#include "filesaver.h"
#include "hdffilesaver.h"

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


    //
    // Create fifo to store UDP raw data packets.
    //
    data_fifo.fillFifo(arguments.q_length,arguments.q_packetlen);

//!! nc -ul 192.168.1.102 50000 | ./testEnet

    //
    // set up udp receiver, and its own thread.
    //
    udpRcv myudp(&data_fifo);

    QThread udpth;
    myudp.moveToThread(&udpth);
    udpth.start(QThread::TimeCriticalPriority);

    //
    //set up packet parser, that splits udp data into two streams.
    //
    packetParse pparse(&data_fifo);
    QThread pparse_th;
    pparse.moveToThread(&pparse_th);
    pparse_th.start();

    dataQueue *stream_a = pparse.getOutQueueA();
    dataQueue *stream_b = pparse.getOutQueueB();

    //
    // set up two parsers.
    //


    roachParser parser_a(stream_a);
    roachParser parser_b(stream_b,128);

    QThread parseth_a;
    QThread parseth_b;

    parser_a.moveToThread(&parseth_a);
    parser_b.moveToThread(&parseth_b);

    //parser_a.setIsDumpInputDbg(true);
    //parser_b.setIsDumpInputDbg(true);
   parseth_a.start();
    parseth_b.start();


    //
    // Set up two file savers, one per parser.
    // streams to files.
    //
    //fileSaver fsave_a;
    //fileSaver fsave_b;
    hdfFileSaver fsave_a;
    hdfFileSaver fsave_b;

    fsave_a.setEventSource(&parser_a);
    fsave_b.setEventSource(&parser_b);


    QThread fsaveth_a;
    QThread fsaveth_b;

    fsave_a.moveToThread(&fsaveth_a);
    fsave_b.moveToThread(&fsaveth_b);
    fsaveth_a.start();
    fsaveth_b.start();



    //
    // Tell gui about all the objects we have.
    //


    w.setUdp(&myudp);
    w.addParser(&parser_a);
    w.addParser(&parser_b);
    w.setPacketParser(&pparse);
    w.setPacketFifo(&data_fifo);
    w.addSaver(&fsave_a);
    w.addSaver(&fsave_b);

    // start up the udp parser
    QMetaObject::invokeMethod(
                &pparse,
                "writeStreams",
                Qt::QueuedConnection);

    // connect udp parser output to the roach parsers.

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

    // timer for periodically updating gui
    QTimer disp_timer;
    disp_timer.start(200);
    w.connect(&disp_timer,SIGNAL(timeout()),SLOT(updateGui()),Qt::QueuedConnection);


    //
    // text commander. it is a text command interface that listens to a pipe.
    // text commands are sent to this pipe from other programs, to remote control
    // the gui of this program. python can then hit buttons or call any slot
    // in the q obhects here.
    //
    textCommander cmd(arguments.cmd_in_pipe_name,arguments.cmd_out_pipe_name);
    cmd.addNameObject("parser_a",&parser_a);
    cmd.addNameObject("parser_b",&parser_b);

    cmd.addNameObject("saver_a",&fsave_a);
    cmd.addNameObject("saver_b",&fsave_b);

    cmd.addNameObject("pparse",&pparse);
   // cmd.addNameObject("piperead",&piperead);
    cmd.addNameObject("w",&w);
    cmd.setAppName("roachstream");


    bool isc = cmd.connect(&fsave_a,SIGNAL(saveDone(QString)),SLOT(sendCommand(QString)),Qt::DirectConnection);

    isc = cmd.connect(&fsave_b,SIGNAL(saveDone(QString)),SLOT(sendCommand(QString)),Qt::DirectConnection);

#if 1
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

#endif

    w.show();
    
    return a.exec();
}
