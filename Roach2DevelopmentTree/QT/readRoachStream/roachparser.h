#ifndef ROACHPARSER_H
#define ROACHPARSER_H

#include <QObject>
#include <QDataStream>
#include <QHash>
#include <QList>
#include <QString>

class roachParser : public QObject
{
    Q_OBJECT
public:
    explicit roachParser(QDataStream *data_source_,QObject *parent = 0);
    

    void addNewChannel(int channel);




signals:
    
public slots:
    void parseStream(void);
    void mapChanToBin(int channel, int bin);
    void clearMaps(void);
    void clearEvents(void);

protected:

    //  events  [23]   ["bin"]=[1]
    //                      ["timestamps]=[,,,,,,]
    //                      ["is_pulse"] = [1,0,0,1,....]
    //                       ["stream_mag"]=[.234,.432....]
    //                       ["stream_phase"]=[.234,.432....]

    QHash<int,QHash<QString,QList<float>* >* > *events;

    QHash<int, QList<int>* > *chan_to_bin;
    QHash<int, float > *chan_to_srcfreq;

    QDataStream *data_source;

    float getFreqFromBin(int bin);
    void defaultChanMap(void);


    bool isneg_freq;
    float fftLenf;
    int fftLen;
    float dac_clk;
    


    int searches;
    int carryover;
    int evtcnt;
    int nbad_events;

};

#endif // ROACHPARSER_H
