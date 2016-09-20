#ifndef PIPEREADER_H
#define PIPEREADER_H
#include <QObject>
#include <QString>
#include "../readRoachStream/packetFifo.h"


class pipeReader : public QObject
{
 Q_OBJECT
public:
    pipeReader(QString fname,int rs,packetFifo *f);

    volatile bool is_write_fifo;

public slots:
    void readPipe(void);
    void isWriteFifo(bool i);

signals:

protected:
    FILE *fp;
    int readsize;
     packetFifo *fifo;

};

#endif // PIPEREADER_H
