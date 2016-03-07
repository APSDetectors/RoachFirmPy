#include "dataqueue.h"

dataQueue::dataQueue(QObject *parent) :
    QObject(parent),
    raw_data_a()
{
}
int dataQueue::length(void)
{
    int ll;
    queue_mutex.lock();
    ll = raw_data_a.length();
    queue_mutex.unlock();
    return(ll);
}

void dataQueue::clear(void)
{
     queue_mutex.lock();
     raw_data_a.clear();
     queue_mutex.unlock();
}

quint32 dataQueue::flipEndian(quint32 in)
{
    quint32 temp;
    quint32 out;

    temp = in;

    out = (temp&0xff) << 24;
    temp = temp >> 8;

    out = out  | ((temp&0xff) << 16);
    temp = temp >> 8;

    out = out  | ((temp&0xff) << 8);
    temp = temp >> 8;

    out = out  | ((temp&0xff));

    return(out);

}

bool dataQueue::write(QByteArray &data)
{
    bool stat= true;
    queue_mutex.lock();

    if (raw_data_a.length()<buffer_max_bytes)
    {

        QDataStream d(&data,QIODevice::ReadOnly);
        int wordsavail = data.length() / 4;
        quint32 val;

        int k;
        for ( k=0;k<wordsavail;k++)
        {
            d >>val;
            //raw_data_a.enqueue(flipEndian(val));
            if (val != 0xffffffff)
                raw_data_a.enqueue(val);
        }
    }
    else
        stat=false;
    queue_mutex.unlock();

    return(stat);
}

bool dataQueue::isEmpty(void)
{
    return(raw_data_a.empty());
}

quint32 dataQueue::read(void)
{
    quint32 val;
    queue_mutex.lock();

    if (!raw_data_a.empty())
        val = raw_data_a.dequeue();
    else
        val = 0xffffffff;

    queue_mutex.unlock();
    return(val);
}

void dataQueue::read(QList<quint32> &outdata)
{
     queue_mutex.lock();
     int ll = raw_data_a.length();



     for (int k=0;k<ll;k++)
     {
         outdata.append(raw_data_a.dequeue());
     }

      queue_mutex.unlock();
}
