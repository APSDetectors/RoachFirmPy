#include "roachparser.h"

roachParser::roachParser(QDataStream *data_source_, QObject *parent) :
    QObject(parent)

{

    events = 0;

    data_source = data_source_;

    chan_to_bin =0;
    chan_to_srcfreq=0;

    clearMaps();
    clearEvents();



     isneg_freq=true;
     fftLenf=512.0;
     fftLen=512;
     dac_clk=512e6;


     searches=0;
     carryover=0;
     evtcnt=0;
     nbad_events=0;

}




void roachParser::defaultChanMap(void)
{
    clearMaps();
    for (int c=0; c< 256; c++)
    {
        mapChanToBin(c,c*2);
        (*chan_to_srcfreq)[c]  = getFreqFromBin(c*2);

     }

}

void roachParser::mapChanToBin(int channel, int bin)
{
    if (!chan_to_bin->contains(channel))
    {

        (*chan_to_bin)[channel] = new QList<int>();
    }

    if ( !(*(*chan_to_bin)[channel]).contains(bin))
        (*(*chan_to_bin)[channel]).append(bin);


}

void roachParser::clearMaps(void)
{
    if (chan_to_bin==0)
        chan_to_bin = new  QHash<int, QList<int>* >();
    else
    {
        QList<int> keys = chan_to_bin->keys();

        int len=keys.length();

        for (int k=0; k<len;k++)
        {
            //delete lists
            delete (  (*chan_to_bin)[ keys[k] ] );

        }

        //delete dict that held lists
        delete(chan_to_bin);

        chan_to_bin = new  QHash<int, QList<int>* >();
    }

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
            delete (  (*(*events)[ keys[k] ])["timestamps"] );
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
}


void roachParser::addNewChannel(int channel)
{
    if (!events->contains(channel))
    {
        (*events)[channel]=new QHash<QString, QList<float>* >();
        (*(*events)[channel])["bin"]=new QList<float>();
        (*(*events)[channel])["timestamps"]=new QList<float>();
        (*(*events)[channel])["is_pulse"]=new QList<float>();
        (*(*events)[channel])["stream_mag"]=new QList<float>();
        (*(*events)[channel])["stream_phase"]=new QList<float>();


    }
}

void roachParser::parseStream(void)
{

    searches=0;
    carryover=0;
    evtcnt=0;
    nbad_events=0;

    //#we get data in retuyrned memory in packets. we have two rams, for phase and mag
    //#phase has the header data.preceeding phse data
    //#header is 0x10000 followed by int, chan number . The length of the data is set in
    //#fifoFSMPh.m, or the firmware. it is 32 words long in the memory.
    int outmem_headerlen=2;
    //#32 ints long
    int outmem_datalen=32;
    //#mem is 32 bits wide.
    int outmem_width=32;
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

    while(true)
    {
        (*data_source) >> datalong;


         //print 'while %d magphs 0x%x'%(k,magphs[k])
         if (datalong&outmem_fff_mask == 0xaaaa)
         {
          // print "FOUND aaaa\n"

               (*data_source) >> datalong1;

               int chan=datalong1&outmem_chan_mask;
               quint32 timestamp = datalong&outmem_ts_maskhi ;

               timestamp = timestamp + ((datalong1&outmem_ts_masklow) >>9);
               quint32 is_pulse = datalong1&outmem_pulse_mask;
               /*
               dp=(magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff
               dm=((magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff0000)>>16
               dataph=self.convToFloat(dp,self.outmem_phs_datatype)
               dataph=dataph*pi
               datamag=self.convToFloat(dm,self.outmem_mag_datatype)

                               if events.has_key(chan)==False:
                                   print 'chan %d'%(chan)
                                   events[chan]=dict()
                                   events[chan]['stream']=[array([]), array([])]

                                   events[chan]['timestamp']=[]
                                   events[chan]['is_pulse']=[]
                                   events[chan]['bin']=self.chan_to_bin[chan][0]
                                   #events[chan]['bin']=-1

                               events[chan]['timestamp'].append(timestamp)
                               events[chan]['is_pulse'].append(is_pulse)
                               stm=events[chan]['stream'][0]
                               stp=events[chan]['stream'][1]
                               events[chan]['stream'][0] = numpy.append(stm,datamag )
                               events[chan]['stream'][1] = numpy.append(stp,dataph )

                               print 'chan   %d  k  %d  is_pulse  %d  timestamp  %x    '%\
                                     (chan,k,is_pulse,timestamp)

                               nextk=k+self.outmem_headerlen + self.outmem_datalen


                               k = nextk
                               evtcnt=evtcnt+1
                           else:
                               print "bad event"
                               nbad_events=nbad_events+1
                               k=k+32
                       else:
                           k=k+1
                           searches=searches+1
                           print k*/

        }
    }


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
