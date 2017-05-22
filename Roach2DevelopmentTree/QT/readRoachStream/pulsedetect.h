#ifndef PULSEDETECT_H
#define PULSEDETECT_H

#include <QObject>
#include "roachparser.h"
class pulseDetect : public roachParser
{
    Q_OBJECT
public:
    explicit pulseDetect(QObject *parent = 0);
    

    //void addNewChannel(int channel,QHash<int,QHash<QString,QList<float> > >*evt );



    virtual void addNewChannel(int channel);


    void scanForPulsesFRD();

    void pulseDetectThread(void);
    bool getIsGotNoiseAverage(int chan);
    void getAverageNoiseValue(int chan);

    void savePulse(int chan, int st, int end);


signals:
    
public slots:
    


protected:

    roachParser *parser;
    bool is_stream;


    enum{
        pre_pulse_samples=100,
        post_pulse_samples=100
    };

     ////

    QHash<int,QHash<QString,QList<float> > > *in_events;

};

#endif // PULSEDETECT_H
