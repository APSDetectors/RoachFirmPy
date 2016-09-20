#ifndef packetParse_H
#define packetParse_H

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
#include <QTime>
#include <QFile>

#include "dataqueue.h"
#include "packetFifo.h"
#include "udprcv.h"

struct twoint
{
    int state;
    int k;
};

class packetParse : public QObject
{
    Q_OBJECT
public:
    explicit packetParse(
            packetFifo *data_fifo_,
            QObject *parent = 0);
    




    dataQueue* getOutQueueA(void);
    dataQueue* getOutQueueB(void);
    QHash<QString,int>* getCounters(void);

    volatile bool is_running;

    QByteArray data_a;
    QByteArray data_b;

     QByteArray lastdatagram;
     QByteArray baddatagram;
     QList<twoint> staterecord;
     int statereclength;
     int statereccount;

volatile bool is_dump_fifos;

signals:

    void bufferFull();
    void dataAvailA();
    void dataAvailB();

public slots:

    void resetCounters(void);
    void writeStreams();
    void stopStreams(void);
    void dumpFifo(void);
    void writeToPipe(bool is_write);
    void setPipeName(QString pipename_);

protected:

    QString pipename;
    bool is_write_pipe;
    QFile *pipefile;

    dataQueue raw_data_a;
    dataQueue raw_data_b;
    quint32 buffer_max_bytes;


    packetFifo *data_fifo;


     QHash<QString,int> packet_counters;

 //    int num_err_top;
   /**  int num_err_end;
     int num_good_packets;
     int searches;
     int num_found_zzz;
     int num_data_words;

     bool bind_stat;
     int n_datagrams;*/

     QMutex queue_mutex;

     QByteArray datagram;

     int state;
      int z_counter;
      int data_counter;
      int data_counter_a;
      int data_counter_b;
      int packet_num_a,packet_num_b;


     enum
     {
         idle,
         search_zzz,
        read_packet_number_a,
         read_packet_number_b,
         in_data_a,
         in_data_b,
        data_are_we_done,
         count_end_zzz,
         end_packet
     };


};

#endif // packetParse_H
