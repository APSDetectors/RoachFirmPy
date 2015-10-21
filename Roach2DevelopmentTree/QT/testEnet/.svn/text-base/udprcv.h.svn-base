#ifndef UDPRCV_H
#define UDPRCV_H

#include <QObject>

#include <QUdpSocket>
#include <QThread>


#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <arpa/inet.h>


#define USE_QTSOCKET

class udpRcv : public QObject
{
    Q_OBJECT
public:
    explicit udpRcv(QObject *parent = 0);
    
    int ipStrToInt(QString ip);


    void initSocket(QString ip, unsigned short port);

    void closeSock(void);

#ifdef USE_QTSOCKET

    QUdpSocket *mysock;

#else
    int mysock;

#endif
    volatile bool is_running;


     QThread udpthread;

signals:
    void newData(QByteArray data,QHostAddress addr,quint16 port);
    
public slots:
    void readData(void);
};

#endif // UDPRCV_H
