#ifndef ROACHPARSER_H
#define ROACHPARSER_H

#include <QObject>
#include <QDataStream>
#include <QHash>
#include <QList>
#include <QString>
#include "dataqueue.h"
#include "roachscope.h"
class roachParser : public QObject
{
    Q_OBJECT
public:
    explicit roachParser(dataQueue *data_source_,int chanoffs = 0, QObject *parent = 0);
    

    void addNewChannel(int channel);


    roachScope *dbgscope;

    int queuelen;

    //parser stats, counters

    int searches;
   // int carryover;
    int evtcnt;
    int nbad_events;
    bool is_parsing;
    int no_bytes_avail;
    int num_parse_calls;
    int ndone_parse;

    int channel_offset;

 signals:
    void plotEvent();
    void saveDone(QString s);
    void parseDone(QString s);

public slots:
    void parseStream(void);
    void mapChanToBin(QString chanbin);
    void mapChanToBin2(int channel, int bin );

    void clearMaps(void);
    void clearEvents(void);
    void stopParse(void);

    void saveEvents(QString dsname);
    void printMaps(void);



public:

    //  events  [23]   ["bin"]=[1]
    //                      ["timestamps]=[,,,,,,]
    //                      ["is_pulse"] = [1,0,0,1,....]
    //                       ["stream_mag"]=[.234,.432....]
    //                       ["stream_phase"]=[.234,.432....]

   //!! QHash<int,QHash<QString,QList<float>* >* > *events;
    QHash<int,QHash<QString,QList<float> > > events;

    QHash<int, int > chan_to_bin;
    QHash<int, float > *chan_to_srcfreq;

    dataQueue *data_source;

    QQueue<quint32> new_data;
    QQueue<quint32> carryover;

    float getFreqFromBin(int bin);
    void defaultChanMap(void);

    void convToFloat(
            int *indata,
            int datalen,
            float *outdata,
            int nfrac_bits, //num fraction bits
            int num_bits,  // total num bits
            int sign_bit);   //is sign bit. 1 if there is a sign bit, else 0

    //settings for ffts
    bool isneg_freq;
    float fftLenf;
    int fftLen;
    float dac_clk;
    


    //temp memory for data
    int mag_temp[256];
    int phase_temp[256];
    float mag_tempf[256];
    float phase_tempf[256];

    volatile bool is_dump_fifos;


    //datatype for mag/ph data
    enum {
        mag_sign=0,
        mag_nbits=16,
        mag_nfrac_bits=16,
        ph_sign=1,
        ph_nbits=16,
        ph_nfrac_bits=13
    };


};

#endif // ROACHPARSER_H
