#ifndef UDPRCV_H
#define UDPRCV_H

#include <QObject>

#include <QUdpSocket>
#include <QThread>

#include <QDataStream>
#include <QBuffer>

#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <arpa/inet.h>


#define USE_QTSOCKET

class udpRcv : public QObject
{
    Q_OBJECT
public:
    explicit udpRcv(QObject *parent = 0,quint32 max_bytes_=10000000);
    
    int ipStrToInt(QString ip);


    void initSocket(QString ip, unsigned short port);

    void closeSock(void);


    QDataStream* getOutStream(void);



signals:
    void newData(QByteArray data,QHostAddress addr,quint16 port);
    void bufferFull();

public slots:
    void readData(void);

protected:
    QBuffer raw_data;
    quint32 buffer_max_bytes;

    volatile bool is_running;

    QUdpSocket *mysock;


     QThread udpthread;

};

#endif // UDPRCV_H
