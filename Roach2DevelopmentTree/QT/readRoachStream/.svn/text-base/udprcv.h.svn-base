#ifndef UDPRCV_H
#define UDPRCV_H

#include <QObject>

#include <QUdpSocket>
#include <QThread>

#include <QDataStream>
#include <QQueue>

#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <arpa/inet.h>

#include <QMutex>
#include <QHash>

#include "packetFifo.h"


//#define UDP_SPINLOCK


class udpRcv : public QObject
{
    Q_OBJECT
public:
    explicit udpRcv(
            packetFifo *data_fifo_,
            QObject *parent = 0,quint32 max_bytes_=10000000);
    
    int ipStrToInt(QString ip);


    volatile int n_datagrams;
    volatile int n_nomemory;

    bool is_running;
    volatile int n_packets;
   volatile  int dgramlen;
signals:

//    void dataAvail();
    void socketOpen();
    void socketClose();


public slots:
    void readData(void);


    void initSocket(QString ip, unsigned short port);

    void closeSock(void);

protected:

    quint32 buffer_max_bytes;


    packetFifo *data_fifo;


    int mysock;

    char bit_bucket[65536];





};

#endif // UDPRCV_H
