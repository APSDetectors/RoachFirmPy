#include <QCoreApplication>

#include "../readRoachStream/packetFifo.h"
#include "pipereader.h"
#include "pipewriter.h"
#include <QThread>
#include <QMetaObject>

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    
    
    packetFifo data;

    data.fillFifo(17,10000);

    pipeReader reader(QString("stdin"),1472,&data);
    pipewriter writer(QString("stdout"),1472,&data);

    QThread rt;
    reader.moveToThread(&rt);
    rt.start();

    QThread wt;
    writer.moveToThread(&wt);
    wt.start();

    QMetaObject::invokeMethod(
                &writer,
                "writePipe",
                Qt::QueuedConnection);

    QMetaObject::invokeMethod(
                &reader,
                "readPipe",
                Qt::QueuedConnection);


            return a.exec();
}
