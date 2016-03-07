#ifndef packetFifo_H
#define packetFifo_H

#include <QObject>

#include <QDataStream>
#include <QQueue>

#include <stdio.h>

#include <QMutex>

struct charArrayInt
{

    unsigned char *data;
    int datalen;
    int max_datalen;
};

class packetFifo : public QObject
{
    Q_OBJECT
public:
    explicit packetFifo(QObject *parent = 0);
    




    // returns mem to write to. you tell how many butes you write.
    // write fifo cnt increments
    // rets 0 of fifo is full.
    unsigned char* getNewArray(void);
    void write(int length);

    // inc read counter. ret 0 on fifo empty.
    // ret length of data, ret data.
    unsigned char* read(int *length);

    void fillFifo(int flen, int arraylen);
    void emptyFifo();

    bool isEmpty(void);
    int length(void);

    int getMaxArrayLen(void);
    void calcEmptyFull(void);
    void clear(void);


    quint32 flipEndian(quint32 in);

signals:
    
public slots:

protected:

    charArrayInt *array_fifo;
    volatile int fifo_length;
    volatile int array_max_length;
    volatile int max_fifo_len;
    volatile int max_fifo_len2;
    volatile bool is_empty;
    volatile bool is_full;



    //read pointer w/ extra bit
    volatile int read_counter;
    // actual read piounter into the fifo.
    volatile int read_location;

    //write counter w/ extra buits
    volatile int write_counter;
    //write ponter into the array
    volatile int write_location;




    
};

#endif // packetFifo_H
