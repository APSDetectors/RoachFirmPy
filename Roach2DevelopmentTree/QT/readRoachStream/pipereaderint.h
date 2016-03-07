#ifndef PIPEREADERINT_H
#define PIPEREADERINT_H

#include <QObject>
#include "dataqueue.h"
#include <QFile>
class pipeReaderInt : public QObject
{
    Q_OBJECT
public:
    explicit pipeReaderInt(QString fname,QObject *parent = 0);

public slots:
  virtual void openPipe(void);
  virtual void closePipe(void);

   virtual void getData(void);



signals:
  void newDataReady();


protected:
  bool is_got_close_message;

    QFile in_pipe;
  bool is_pipe_open;

  dataQueue qa;
  dataQueue qb;

    
};

#endif // PIPEREADERINT_H
