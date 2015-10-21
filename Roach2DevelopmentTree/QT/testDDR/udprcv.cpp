#include "udprcv.h"
#include <QStringList>
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "error.h"
#include "errno.h"
#include "string.h"
udpRcv::udpRcv(QObject *parent) :
    QObject(parent),
     udpthread()

{
  mysock=0;
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
#ifdef USE_QTSOCKET
    printf("using QT sockets\n");
    mysock = new QUdpSocket();


    mysock->bind(QHostAddress(ip),port,QUdpSocket::DontShareAddress);



    printf("Made udp socket\n");
    is_running=false;

        connect(mysock, SIGNAL(readyRead()),
                this, SLOT(readData()));

 #else
    struct sockaddr_in servaddr,cliaddr;
       socklen_t len;
       char mesg[1000];
       printf("using C sockets\n");

    mysock=socket(AF_INET,SOCK_DGRAM,0);

    bzero(&servaddr,sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    //servaddr.sin_addr.s_addr=ipStrToInt(ip);


    inet_aton(ip.toStdString().c_str(),(in_addr*) &servaddr.sin_addr.s_addr);


    servaddr.sin_port=htons(port);


    if (setsockopt(mysock, SOL_SOCKET, SO_BINDTODEVICE,"eth2",sizeof("eth2")) )
    {
        printf("ERROR- %s\n",strerror(errno));
    }
    else
    {
        printf("Prob bound to eth2\n");
    }

    bind(mysock,(struct sockaddr *)&servaddr,sizeof(servaddr));




    moveToThread(&udpthread);
    udpthread.start();

    QMetaObject::invokeMethod(
                this,
                "readData",
                Qt::AutoConnection);

#endif



}

void udpRcv::closeSock()
{
    printf("Delete socket\n");

    if (mysock==0)
        return;
#ifdef USE_QTSOCKET

    mysock->close();
    delete mysock;


#else

    close(mysock);

#endif


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

#ifdef USE_QTSOCKET
    while (mysock->hasPendingDatagrams()) {
           QByteArray datagram;
           datagram.resize(mysock->pendingDatagramSize());
           QHostAddress sender;
           quint16 senderPort;

           mysock->readDatagram(datagram.data(), datagram.size(),
                                   &sender, &senderPort);

           for (int k =0; k<datagram.size();k++)
               printf("%c",datagram.data()[k]);

           emit newData(datagram,sender, senderPort);

       }




#else
    int n;

    while(is_running)
    {
       len = sizeof(cliaddr);
       n = recvfrom(mysock,mesg,1000,0,(struct sockaddr *)&cliaddr,&len);

       printf("-------------------------------------------------------\n");
       mesg[n] = 0;
       printf("Received the following:\n");
       printf("%s",mesg);

       QByteArray datagram=QByteArray((const char*)mesg);
       QHostAddress ip=QHostAddress((quint32)cliaddr.sin_addr.s_addr);
       int port = (quint16)cliaddr.sin_port;

       emit newData(datagram,ip,port);
    }
#endif


}
