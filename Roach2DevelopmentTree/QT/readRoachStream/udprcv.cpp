#include "udprcv.h"
#include <QStringList>
#include <QIODevice>
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "error.h"
#include "errno.h"
#include "string.h"
udpRcv::udpRcv(QObject *parent, quint32 max_bytes_) :
    QObject(parent),
     udpthread(),
     raw_data()

{
  mysock=0;
  buffer_max_bytes=max_bytes_;
}




int udpRcv::ipStrToInt(QString ip)
{
    QStringList nums=ip.split('.');

    unsigned int int_ip=0;

    int_ip = (nums[0].toInt()) << 24;
    int_ip += (nums[1].toInt()) << 16;
    int_ip += (nums[2].toInt()) << 8;
    int_ip += (nums[3].toInt());
    return(int_ip);
}



void udpRcv::initSocket(QString ip, unsigned short port)
{



    printf("using QT sockets\n");
    mysock = new QUdpSocket();


    mysock->bind(QHostAddress(ip),port,QUdpSocket::DontShareAddress);



    printf("Made udp socket\n");
    is_running=false;

   raw_data.open(QIODevice::ReadWrite);


        connect(mysock, SIGNAL(readyRead()),
                this, SLOT(readData()));



}

void udpRcv::closeSock()
{
    printf("Delete socket\n");

    raw_data.close();

    if (mysock==0)
        return;


    mysock->close();
    delete mysock;



    mysock=0;
}


void udpRcv::readData(void)
{
    struct sockaddr_in cliaddr;
       socklen_t len;
       char mesg[1000];


    if (mysock==0)
        return;
is_running=true;


    while (mysock->hasPendingDatagrams()) {
           QByteArray datagram;
           datagram.resize(mysock->pendingDatagramSize());
           QHostAddress sender;
           quint16 senderPort;

           mysock->readDatagram(datagram.data(), datagram.size(),
                                   &sender, &senderPort);

           //for (int k =0; k<datagram.size();k++)
           //    printf("%c",datagram.data()[k]);

           //!!emit newData(datagram,sender, senderPort);

           if (raw_data.size()<buffer_max_bytes)
               raw_data.write(datagram);
           else
               emit bufferFull();

       }


}



QDataStream* udpRcv::getOutStream(void)
{
    QDataStream *s = new QDataStream(&raw_data);
    return(s);
}
