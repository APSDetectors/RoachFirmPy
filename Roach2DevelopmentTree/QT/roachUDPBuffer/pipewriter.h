#ifndef PIPEWRITER_H
#define PIPEWRITER_H
#include <QObject>
#include <QString>
#include "../readRoachStream/packetFifo.h"

class pipewriter: public QObject
{
    Q_OBJECT
public:
    pipewriter(QString fname,int rs,packetFifo *f);

    packetFifo *fifo;

signals:

public slots:
    void writePipe(void);
protected:

    FILE *fp;
    int readsize;
};

#endif // PIPEWRITER_H

