#ifndef DATAQUEUE_H
#define DATAQUEUE_H

#include <QObject>

#include <QDataStream>
#include <QQueue>

#include <stdio.h>

#include <QMutex>
class dataQueue : public QObject
{
    Q_OBJECT
public:
    explicit dataQueue(QObject *parent = 0);
    
    bool write(QByteArray &data);
    quint32 read(void);
    void read(QList<quint32> &outdata);

    bool isEmpty(void);
    int length(void);
  QQueue<quint32> raw_data_a;
    quint32 flipEndian(quint32 in);

signals:
    
public slots:
    void clear(void);

protected:


    enum { buffer_max_bytes=10000000};


     QMutex queue_mutex;

    
};

#endif // DATAQUEUE_H
