#include "udprcv.h"
#include <QStringList>
#include <QIODevice>
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "error.h"
#include "errno.h"
#include "string.h"
udpRcv::udpRcv(
        packetFifo *data_fifo_,
        QObject *parent,quint32 max_bytes_ ) :
    QObject(parent)



{
  mysock=0;
  buffer_max_bytes=max_bytes_;

    data_fifo=data_fifo_;

    dgramlen=0;


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



    if (mysock!=0)
    {
        fprintf(stderr,"socket alreayd open?\n");
        return;
    }
    n_nomemory=0;
    n_datagrams=0;
    n_packets=0;
    fprintf(stderr,"using posix sockets\n");

    struct sockaddr_in servaddr,cliaddr;
          socklen_t len;
          char mesg[1000];


       mysock=socket(AF_INET,SOCK_DGRAM,0);

       bzero(&servaddr,sizeof(servaddr));
       servaddr.sin_family = AF_INET;
       servaddr.sin_addr.s_addr=ipStrToInt(ip);


       inet_aton(ip.toStdString().c_str(),(in_addr*) &servaddr.sin_addr.s_addr);


       servaddr.sin_port=htons(port);


      // if (setsockopt(mysock, SOL_SOCKET, SO_BINDTODEVICE,"eth2",sizeof("eth2")) )
      // {
       //    ffprintf(stderr,stderr,"ERROR- %s\n",strerror(errno));
      // }
      // else
      // {
      //     ffprintf(stderr,stderr,"Prob bound to eth2\n");
      // }

       bind(mysock,(struct sockaddr *)&servaddr,sizeof(servaddr));


       emit(socketOpen());
}

void udpRcv::closeSock()
{


    fprintf(stderr,"req socket close\n");

is_running=false;


}


void udpRcv::readData(void)
{
    struct sockaddr_in cliaddr;
       socklen_t len;
       char mesg[8192];


    if (mysock==0)
        return;

is_running=true;

int n;
    data_fifo->clear();

    while(is_running)
    {
       len = sizeof(cliaddr);


       unsigned char *datagram=data_fifo->getNewArray();
       if (datagram)
        {


            n = recvfrom(mysock,datagram,8192,0,(struct sockaddr *)&cliaddr,&len);


               n_datagrams++;
               n_packets++;
                dgramlen = n;
                             data_fifo->write(n);

       }
       else
       {
           n_nomemory++;
        n_packets++;
           n = recvfrom(mysock,bit_bucket,8192,0,(struct sockaddr *)&cliaddr,&len);

       }



    }


 fprintf(stderr,"Delete socket\n");
    close(mysock);

    emit(socketClose());
       mysock=0;
}
