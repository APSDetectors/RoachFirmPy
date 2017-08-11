#ifndef ROACHPARSER_H
#define ROACHPARSER_H

#include <QObject>
#include <QDataStream>
#include <QHash>
#include <QList>
#include <QString>
#include <QFile>
#include <QMutex>

#include "dataqueue.h"
#include "roachscope.h"

//define if we have newer fw in roach that gives 24 bit FRD data.
// if not defined there is 16 bit frd data for older and more tested FW.
//#define FW_FRD_24BIT 1


class roachParser : public QObject
{
    Q_OBJECT
public:
    explicit roachParser(dataQueue *data_source_,int chanoffs = 0, QObject *parent = 0);
    

    virtual void addNewChannel(int channel);

    int getListQueueLength(void);

    void polar2Rect(double radius, double radians,double &xc, double &yc);
    void rect2Polar(double xc, double yc, double &radius, double &radians);

    void translate(int channel,double xin,double yin, double &xout, double &yout);

    void unwrapPhase(double *phase, int len);
    void DFT(double *xin, int len, double bin, double *xout, double *yout );
    void demodFluxRamp(int channel,float *mag, float *phase, int len, double *phaseout);
    void addPhaseDelay(int chan, int len, float *phase);


    bool pulseDetectRaw(int chan, double phase_sum,int outmem_datalen);
    bool pulseDetectFRD(int chan, double flux_ramp_fl);


    QHash<int,QHash<QString,QList<float> > >* getEventList(void);
    bool pushEventList(QHash<int,QHash<QString,QList<float> > >* events_);

    roachScope *dbgscope;



    //// calss vars
    bool is_pulse_detect;

    int pulse_state;

    int save_counter;
     int  save_max_count;
     int pulse_counter;
     double pulse_thresh;

     bool is_pulse_detect_frd;
     enum{
         delete_data=0,
         save_data=1,
         num_phase_ave = 1000
     };

     //phase average for each channel
    QHash<int,double> *pulse_det_phaseave;
    //number of phases we have averaged to compute phase average.
    QHash<int,int> *pulse_det_phaseavecount;

    // pulse et state for each channel
    QHash<int,int> *pulse_det_state;
     QHash<int,int> *pulse_det_savecount;

     ////


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
    void resetPulseCount(void);

    void setIsPulseDetect(bool is_);
    void setIsPulseDetectFRD(bool is_);
    void setPulseThresh(double thr_);

    void parseStream(void);
    void mapChanToBin(QString chanbin);
    void mapChanToBin2(int channel, int bin );

    void setCircleCoord(QString circle_);

    void clearMaps(void);
    void clearEvents(void);
    void stopParse(void);


    void printMaps(void);
    void queueEvents(void);

    void setFluxBin(double bin_);
    void setIsFluxDemod(bool is_);
    void setTimeDelay(QString chan_phasedelay);

public:

    //  events  [23]   ["bin"]=[1]
    //                      ["timestamps]=[,,,,,,]
    //                      ["is_pulse"] = [1,0,0,1,....]
    //                       ["stream_mag"]=[.234,.432....]
    //                       ["stream_phase"]=[.234,.432....]

    //this is a data structure for our parsed data. it is organized as aovce
    QHash<int,QHash<QString,QList<float> > > *events;
    //!!QHash<int,QHash<QString,QList<float> > > events;

    // map of hannelizer channel from 1 to 256 mapped to fft bin.
    QHash<int, int > chan_to_bin;
    //map of channelizer chan to source freq.
    QHash<int, float > *chan_to_srcfreq;

    dataQueue *data_source;

    QQueue<quint32> new_data;
    QQueue<quint32> carryover;


    // when the events fills up to so many events, we dump it in a queue.
    //the another thread can get at it to save or delete or someting.
    // when events is queued, a new events is created on new pointer
    QMutex queue_mutex;
    QQueue<QHash<int,QHash<QString,QList<float> > > *> event_queue;
    QHash<int,float> *phase_tracks;


    float getFreqFromBin(int bin);
    void defaultChanMap(void);


    void makeFakeEvent(
            int chan,
            int timestamp,
            int is_pulse,
            int bin,
            int outmem_datalen,
            bool is_get_raw_evt_data,
            float flux_ramp_fl,
            int event_type
            );


    void makeFakeEventStream(void);


    void convToFloat(
            int *indata,
            int datalen,
            float *outdata,
            int nfrac_bits, //num fraction bits
            int num_bits,  // total num bits
            int sign_bit);   //is sign bit. 1 if there is a sign bit, else 0

    void setIsDumpInputDbg(bool is_);


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

#ifdef FW_FRD_24BIT
    //datatype for mag/ph data
    enum {
        frd_sign=1,
        frd_nbits=24,
        frd_nfrac_bits=22
    };
#else
    //datatype for mag/ph data
    enum {
        frd_sign=1,
        frd_nbits=16,
        frd_nfrac_bits=13
    };
#endif

    enum
    {max_list_length = 10000,
    max_evt_q_length = 500000
         };


    // generate an ID for each parser created.
    static int parser_counter;
    //index for this parser. sort if an ID.
    int parser_number;

    // true to dump input data to file for debugging
    bool is_dump_input_dbg;

    //file in which to dump debug data from input queue
    QFile *dbg_file;



    //how many phi-0's in one segment of phase data
    double flux_bin;
    //true to demod the flux ramp
    bool is_demod_fluxramp;


};

#endif // ROACHPARSER_H
