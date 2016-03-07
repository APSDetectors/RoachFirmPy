#include "roachparser.h"
#include <math.h>
#include "dataqueue.h"
#include <iostream>
#include <QVector>
#include <QDir>

roachParser::roachParser(dataQueue *data_source_, int chanoffs, QObject *parent) :
    QObject(parent),
    events(),
    new_data(),
    carryover(),
    chan_to_bin()

{
    channel_offset = chanoffs;
    num_parse_calls=0;
    ndone_parse=0;
    dbgscope=0;
    //events = 0;

    data_source = data_source_;


    chan_to_srcfreq=0;

    clearMaps();
    clearEvents();

    is_dump_fifos=false;

     isneg_freq=true;
     fftLenf=512.0;
     fftLen=512;
     dac_clk=512e6;


     searches=0;
     //carryover=0;
     evtcnt=0;
     nbad_events=0;
     no_bytes_avail=0;

}




void roachParser::defaultChanMap(void)
{
    clearMaps();
    for (int c=0; c< 256; c++)
    {
        mapChanToBin2(c,c*2);
        (*chan_to_srcfreq)[c]  = getFreqFromBin(c*2);

     }

}


// expect this as chan:bin, chan:bin, etc.
// " 128:492, 129,400  "
void roachParser::mapChanToBin2(int channel, int bin )
{
    fprintf(stderr,"Mapping Chan %d to Bin %d\n",channel, bin);

    chan_to_bin[channel]=bin;

}

// expect this as chan:bin, chan:bin, etc.
// " 128:492, 129,400  "
void roachParser::mapChanToBin(QString chanbin)
{
    int p;
    int channel;
    int bin;

    QStringList pairs = chanbin.split(",");

    for ( p = 0; p<pairs.length();p++)
    {

        QStringList pair_ = pairs[p].split(":");
        if (pair_[0]!="")
        {
            channel = pair_[0].toInt();
            bin = pair_[1].toInt();
            mapChanToBin2(channel,bin);
        }

    }
}

void roachParser::printMaps(void)
{
    QList<int> keys = chan_to_bin.keys();

    int len=keys.length();

    for (int k=0; k<len;k++)
    {
        //delete lists

        int bin = chan_to_bin[keys[k]];
        int channel = keys[k];
                fprintf(stderr,"Channel %d Bin %d\n",channel,bin);

    }
}

void roachParser::clearMaps(void)
{
    chan_to_bin.clear();

    if (chan_to_srcfreq==0)
        chan_to_srcfreq= new QHash<int, float >();
    else
    {
        delete(chan_to_srcfreq);
        chan_to_srcfreq= new QHash<int, float >();

    }

}

void roachParser::clearEvents(void)
{
    searches=0;
    //carryover=0;
    evtcnt=0;
    nbad_events=0;

    events.clear();
    new_data.clear();

    data_source->clear();

/**
    if (events==0)
        events = new QHash<int,QHash<QString,QList<float>* >* >();
    else
    {
        QList<int> keys = events->keys();

        int len=keys.length();

        for (int k=0; k<len;k++)
        {
            //delete lists
            delete (  (*(*events)[ keys[k] ])["bin"] );
            delete (  (*(*events)[ keys[k] ])["timestamp"] );
            delete (  (*(*events)[ keys[k] ])["is_pulse"] );
            delete (  (*(*events)[ keys[k] ])["stream_mag"] );
            delete (  (*(*events)[ keys[k] ])["stream_phase"] );
            //delete dict that held lists
            delete( (*events)[ keys[k] ]  );
        }

        //delete dict that held dicts
        delete(events);

        //make a fresh dict
        events = new QHash<int,QHash<QString,QList<float>* >* >();
    }

    */
}


void roachParser::addNewChannel(int channel)
{

    if (!events.contains(channel))
    {

        events[channel]=QHash<QString, QList<float> >();
        events[channel]["bin"]=QList<float>();
        events[channel]["timestamp"]= QList<float>();
        events[channel]["is_pulse"]= QList<float>();
        events[channel]["stream_mag"]= QList<float>();
        events[channel]["stream_phase"]= QList<float>();
        /**

        (*events)[channel]=new QHash<QString, QList<float>* >();
        (*(*events)[channel])["bin"]=new QList<float>();
        (*(*events)[channel])["timestamp"]=new QList<float>();
        (*(*events)[channel])["is_pulse"]=new QList<float>();
        (*(*events)[channel])["stream_mag"]=new QList<float>();
        (*(*events)[channel])["stream_phase"]=new QList<float>();
        */


    }
}

void roachParser::stopParse(void)
{
   is_parsing=false;
}


void roachParser::saveEvents(QString dsname)
{
   QDir prnt;


       if (prnt.mkdir(dsname))
       {
           prnt.cd(dsname);

           //QHash<int,QHash<QString,QList<float> > > events;
           QList<int> keys1=events.keys();
           for (int i=0;i<keys1.length();i++)
           {
               int chan = keys1[i];
               int bin = chan_to_bin[chan];
               QString dirname = QString("chan_%1_bin_%2").arg(chan).arg(bin);
               prnt.mkdir(dirname);
               if (prnt.cd(dirname))
               {

               QList<QString> keys2=events[keys1[i]].keys();
               for (int i2=0;i2<keys2.length();i2++)
               {
                   QString fname = keys2[i2];
                   fname.prepend(prnt.absolutePath()+"/");
                   QFile file(fname);
                   file.open(QIODevice::WriteOnly);

                   //QDataStream out(&file);


                   for (int i3=0;i3< events[keys1[i]][keys2[i2]].length() ; i3++)
                   {
                       //out << events[keys1[i]][keys2[i2]][i3];
                       float v = events[keys1[i]][keys2[i2]][i3];
                       file.write((const char*)&v,sizeof(float));
                   }


                   file.close();

               }


               prnt.cdUp();
               }


           }

       }


       emit saveDone(QString("python fa saveDone 0 \n"));


}



void roachParser::parseStream(void)
{


    //#we get data in retuyrned memory in packets. we have two rams, for phase and mag
    //#phase has the header data.preceeding phse data
    //#header is 0x10000 followed by int, chan number . The length of the data is set in
    //#fifoFSMPh.m, or the firmware. it is 32 words long in the memory.
    int outmem_headerlen=2;
    //#32 ints long
    int outmem_datalen=32;
    //#mem is 32 bits wide.
    int outmem_width=32;

    int event_length=outmem_headerlen + outmem_datalen;
    //#below is sign buts, total buts, num frac buts
    //!!self.outmem_mag_datatype = [0,16,16]
    //!!self.outmem_phs_datatype = [1,16,13]

    quint32 outmem_ts_masklow = 0x0000ffff<<9;
    quint32 outmem_ts_maskhi = 0xffff0000;
    quint32 outmem_ts_norm= 65536;
    quint32 outmem_fff_mask=0xffff;
    quint32 outmem_chan_mask=0xff;
    quint32 outmem_pulse_mask=0x100;



    quint32 datalong, datalong1,datalong2;
    bool is_good_event = true;

    int chan, bin;

    //new_data.clear();
    //new_data.append(carryover);

    num_parse_calls++;


    queuelen=data_source->length();
    data_source->read(new_data);
int dbgql;


        while (new_data.length() >=event_length)
        {
            //
            datalong=new_data.dequeue();

             if ( (datalong&outmem_fff_mask) == 0xaaaa)
             {
                // fprintf(stderr, "FOUND aaaa\n");

                   datalong1 = new_data.dequeue();

                    chan=datalong1&outmem_chan_mask;
                   chan = chan + channel_offset;
                     bin = -1;

                   if (chan_to_bin.contains(chan))
                        bin = chan_to_bin[chan];

                   quint32 timestamp = datalong&outmem_ts_maskhi ;

                   timestamp = timestamp + ((datalong1&outmem_ts_masklow) >>9);
                   quint32 is_pulse = datalong1&outmem_pulse_mask;



                   int plen;
                    is_good_event = true;

                   for ( plen = 0; plen<outmem_datalen;plen++)
                   {
                        quint32 dp, dm;
                        datalong2=new_data.dequeue();

                        if (datalong2&outmem_fff_mask == 0xaaaa)
                        {

                            nbad_events++;
                            is_good_event=false;
                            break;
                        }

                        dp=datalong2&0xffff;
                        dm = (datalong2& 0xffff0000)>>16;

                        mag_temp[plen]=dm;
                        phase_temp[plen]=dp;
                   }

                  if (is_good_event)
                  {
                       // adds new chan to events if not alreayd there.
                      addNewChannel(chan);
                      //!!(*(*events)[chan])["timestamp"]->append((float)timestamp);
                      //!!(*(*events)[chan])["is_pulse"]->append((float)is_pulse);
                      //!!(*(*events)[chan])["bin"]->append(-1.0 );//!! need to look at map

                      events[chan]["timestamp"].append((float)timestamp);
                      events[chan]["is_pulse"].append((float)is_pulse);
                      events[chan]["bin"].append((float)bin );//!! need to look at map


                      convToFloat(mag_temp,
                                  outmem_datalen,
                                  mag_tempf,
                                  mag_nfrac_bits,
                                  mag_nbits,
                                  mag_sign);


                      convToFloat(phase_temp,
                                  outmem_datalen,
                                  phase_tempf,
                                  ph_nfrac_bits,
                                  ph_nbits,
                                  ph_sign);

                      for ( plen = 0; plen<outmem_datalen;plen++)
                      {
                         //!! (*(*events)[chan])["stream_mag"]->append(mag_tempf[plen] );
                          //!!(*(*events)[chan])["stream_phase"]->append(3.141592653589793 * phase_tempf[plen] );
                          events[chan]["stream_mag"].append(mag_tempf[plen] );
                          events[chan]["stream_phase"].append(3.141592653589793 * phase_tempf[plen] );
                      }

                     // fprintf(stderr,"Done Good evt\n");
                      fflush(stdout);
                       //print 'chan   %d  k  %d  is_pulse  %d  timestamp  %x    '%\
                       //      (chan,k,is_pulse,timestamp)

                       evtcnt++;


                  }//if is good event


               }//if found aaaaaa
             else
             {
                searches++;

                //fprintf(stderr,"0x%x\n",datalong);
                //fflush(stdout);

             }
        }//while


        ndone_parse++;
        emit parseDone(QString("python fa parseDone 0 \n"));

}


float roachParser::getFreqFromBin(int bin)
{
    float whichbinf;

     if (isneg_freq)
         whichbinf = fftLenf - (float)bin;
     else
         whichbinf=(float)bin;



    float freq=whichbinf * (dac_clk / fftLenf);

     return(freq);
}





//###########################################################################
//#
//#data type is (18,15) where we have 18 bits data, 15 fraction bits
//#converts vector of binary twos comp to floats.
//###########################################################################

void roachParser::convToFloat(
        int *indata,
        int datalen,
        float *outdata,
        int nfrac_bits, //num fraction bits
        int num_bits,  // total num bits
        int sign_bit)   //is sign bit. 1 if there is a sign bit, else 0
{
    quint32 fracmask;
    float fracnorm;
    //nfrac=2
    //nbits=1
    //sbit=0

    //#pow(2,(datatype[output][1]+1),
    //#if we have 16 fraction bits, this is
    //#pow(2,16)-1 = 0x10000 - 1 = 0xffff
    if (nfrac_bits>0)
    {
        fracmask = (1<<nfrac_bits)-1;
        fracnorm=pow(2.0,nfrac_bits);
    }
    else
    {
        fracmask = 0;
        fracnorm=1.0;
    }

    //#mask for int part not including sign bit.
    //#datatype[output][0] - datatype[output][1] - 1 is 18-15-1=2, where we have 2 bits
    //#fir int part not counting sign bit.
    int numintbits =   num_bits - (sign_bit + nfrac_bits);
    //#for 2 int buits, we take 3<<numfracbits, 3<<15
    //#this is int portion mask not incl the
    quint32 intmask;
    if (numintbits>0)
        intmask  = ((1<<numintbits)-1) << nfrac_bits ;
    else
        intmask=0;

    //#sign mask is numbuts-1
    quint32 signmask;
    float signval;

    if (sign_bit>0)
    {
        signmask =  1 << (num_bits)-1;
        signval = -1.0 * (float)signmask/fracnorm;
    }
    else
    {
        signmask=0;
        signval=0.0;
    }

    //#print 'fracmask %x fracnorm  %f numintbits  %d intmask  %x signmask  %x signval  %f '%\
    //#    (fracmask,fracnorm,numintbits,intmask,signmask,signval)

    int fracpart;
    float frac;
    int intpart;
    float intval;
    float signbit, signval_,val;

    //newdata = []
    for (int d =0; d<datalen;d++)
    {
        fracpart=indata[d] &  fracmask;
        frac =  (float)fracpart/fracnorm;

        intpart = indata[d] & intmask;
        intval = (float)intpart / fracnorm;

        //#if we have 18 bit data, sign but is but 17.
        //#signbit will be 1 or 0, below becayse of > sign
        signbit=(float)((indata[d] & signmask)>0);
        signval_ = signbit*signval;


        val = signval_ + intval + frac;

        //#print ' fracpart  %d   frac %f intpart  %d  intval %f signbit  %d signval_  %f  val %f'%\
        //#    (fracpart,frac,intpart,intval,signbit,signval_,val)

        //newdata.append(val)
        outdata[d]=val;
    }
   }


