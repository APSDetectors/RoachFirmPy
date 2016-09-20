#ifndef FILESAVER_H
#define FILESAVER_H

#include <QObject>
#include <QDir>
#include <QThread>

#include "roachparser.h"

class fileSaver : public QObject
{
    Q_OBJECT
public:
    explicit fileSaver(QObject *parent = 0);
    void setEventSource(roachParser *parse);
signals:
    void saveDone(QString s);
public slots:

    void setFileName(QString fname_);
    void setIsStream(bool is_stream_);
    void saveNow(void);
    void doSaveThread(void);
    void doSaveAll(void);


  private:
    roachParser *parser;
    QHash<int,QHash<QString,QList<float> > > *events;
    QString fname;
    bool is_stream;
};

#endif // FILESAVER_H
