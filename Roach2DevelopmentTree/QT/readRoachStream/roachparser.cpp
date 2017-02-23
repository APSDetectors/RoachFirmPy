#include "roachparser.h"
#include <math.h>
#include "dataqueue.h"
#include <iostream>
#include <QVector>
#include <QDir>

/**
 * @brief roachParser::roachParser
 * @param data_source_
 * @param chanoffs
 * @param parent
 * @return
 */
int roachParser::parser_counter = 0;

/**
 * @brief roachParser::roachParser  Constructor for roach Parser.
 * @param data_source_  Queue that provides raw binary data.
 * @param chanoffs      Each channel number is added an offset, unique to parser
 * @param parent        Set to 0
 */
roachParser::roachParser(dataQueue *data_source_, int chanoffs, QObject *parent) :
    QObject(parent),
    new_data(),
    carryover(),
    chan_to_bin()

{
    channel_offset = chanoffs;
    num_parse_calls=0;
    ndone_parse=0;
    dbgscope=0;
    events = 0;
    phase_tracks=0;

    data_source = data_source_;


    chan_to_srcfreq=0;


    pulse_det_phaseave= new QHash<int,double>;
    pulse_det_phaseavecount  = new QHash<int,int>;
    pulse_det_state  = new QHash<int,int>;
    pulse_det_savecount = new QHash<int,int>;
    is_pulse_detect_frd=false;

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

     //set this parser ID
     parser_number = parser_counter;
     parser_counter++;
is_dump_input_dbg=false;
     dbg_file=0;


       flux_bin=1.0;
       is_demod_fluxramp=false;



       //// calss vars
    is_pulse_detect=false;
       pulse_state = delete_data;
         save_counter = 0;
          save_max_count = 2;
         pulse_counter = 0;
         pulse_thresh=1.0;


}

/**
 * @brief roachParser::getEventList
 * @return
 */
QHash<int,QHash<QString,QList<float> > >* roachParser::getEventList(void)
{
    QHash<int,QHash<QString,QList<float> > >* events_ = 0;
    queue_mutex.lock();

    if (event_queue.length()>0)
        events_= event_queue.dequeue();

    queue_mutex.unlock();

    return(events_);
}

/**
 * @brief roachParser::pushEventList
 * @param events_
 * @return
 */
bool roachParser::pushEventList(QHash<int,QHash<QString,QList<float> > >* events_)
{
    bool stat = true;

    queue_mutex.lock();
    if (event_queue.length()<max_evt_q_length)
        event_queue.enqueue(events_);
    else
        stat = false;

    queue_mutex.unlock();

    return(stat);
}

/**
 * @brief roachParser::getListQueueLength
 * @return length of the queue holding lists of events
 */
int roachParser::getListQueueLength(void)
{
    int qlen = 0;
    queue_mutex.lock();
    qlen = event_queue.length();
     queue_mutex.unlock();
     return(qlen);
}

/**
 * @brief roachParser::defaultChanMap   Create default channel map. Chan c mapped to fft bin c*2
 */
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
/**
 * @brief roachParser::mapChanToBin2  Map a channel number to FFT bin number.
 * @param channel Channel number, or channel of output fifo on roach.
 * @param bin   FFT bin number
 */
void roachParser::mapChanToBin2(int channel, int bin )
{
    fprintf(stderr,"Mapping Chan %d to Bin %d\n",channel, bin);

    chan_to_bin[channel]=bin;

}

// expect this as chan:bin, chan:bin, etc.
// " 128:492, 129,400  "
/**
 * @brief roachParser::mapChanToBin Map many channels to bins listed in string pairs.
 * @param chanbin QString like "25:128,26:156"
 */
void roachParser::mapChanToBin(QString chanbin)
{
    int p;
    int channel;
    int bin;

    QStringList pairs = chanbin.split(",");

    for ( p = 0; p<pairs.length();p++)
    {

        QStringList pair_ = pairs[p].split(":");
        if (pair_[0]!="" && pair_[1]!="")
        {
            channel = pair_[0].toInt();
            bin = pair_[1].toInt();
            mapChanToBin2(channel,bin);
        }
        else
        {
            fprintf(stderr,"roachParser::mapChanToBin bad QString input from python\n");

        }

    }
}
/**
 * @brief roachParser::printMaps Print channel maps on string to stderr.
 */
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

/**
 * @brief roachParser::clearMaps Claer channel to bin maps to empty Hash tables.
 */
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

/**
 * @brief roachParser::clearEvents Clear events list in this parser. Clear input queue.
 */
void roachParser::clearEvents(void)
{
    if (phase_tracks!=0)
    {
        phase_tracks->clear();
        delete phase_tracks;
        phase_tracks=0;
    }
    searches=0;
    //carryover=0;
    evtcnt=0;
    nbad_events=0;
    int chan;

    for ( chan=0;chan<256;chan++)
        (*pulse_det_phaseave)[chan]=0.0;

    for ( chan=0;chan<256;chan++)
        (*pulse_det_phaseavecount)[chan]=0;

    for ( chan=0;chan<256;chan++)
        (*pulse_det_state)[chan]=delete_data;

    for ( chan=0;chan<256;chan++)
        (*pulse_det_savecount)[chan]=0;

        pulse_counter=0;

    new_data.clear();

    data_source->clear();

    if (events !=0) {
    events->clear();
    delete events;
    events = 0;
    }
    //data_start_index = 0;

    while (!event_queue.empty())
    {
        events = getEventList();
        events->clear();
        events = 0;
    }
}

/**
 * @brief roachParser::addNewChannel Add new channel which roach uses for data output.
 * @param channel Channel number
 */
void roachParser::addNewChannel(int channel)
{

    if (phase_tracks == NULL)
        phase_tracks = new QHash<int,float>;

    if (!phase_tracks->contains(channel))
    {
        (*phase_tracks)[channel] = 0.0;
    }

    if (events==NULL)
        events = new QHash<int,QHash<QString,QList<float> > >;


    if (!events->contains(channel))
    {

        //make epty assoc. array, or dictionary. string indexes a list of floats
        (*events)[channel]=QHash<QString, QList<float> >();
        // the fft bin for this channel
        (*events)[channel]["bin"]=QList<float>();
        // hw timestamp of event from roach
        (*events)[channel]["timestamp"]= QList<float>();
        // 1 for this event of we are looking for sync pulse
        (*events)[channel]["is_pulse"]= QList<float>();

        //long data stream of all concat events, or groups of complex samples, fft coef.
        (*events)[channel]["stream_mag"]= QList<float>();
        (*events)[channel]["stream_phase"]= QList<float>();

        // length in samples of this event

        (*events)[channel]["event_len"]= QList<float>();
        (*events)[channel]["event_type"]= QList<float>();

        // index in the data stream array telling where next event starts.
        // we get events from roacgh, or 30 to 100 samples of data. it is put into
        // one long array of mags and phases, called events[]['stream_mag'], events[]['stream_phase']
        // to get one continuous data strean. if we wish to grab each event we can use the start index
        // in events[]["data_start_index"]
        //int data_start_index;
        //(*events)[channel]["data_start_index"]= QList<float>();

        (*events)[channel]["flux_ramp_phase"]= QList<float>();
        (*events)[channel]["flux_ramp_phase_unwrap"]= QList<float>();

        (*events)[channel]["circle_specs_xy"]= QList<float>();
        // for delay phase change due to RF cabling. 30ns etc... in radians for each channel
        (*events)[channel]["phase_delay"]= QList<float>();
        (*events)[channel]["phase_delay"].append(0.0);


    }
}

void roachParser::stopParse(void)
{
   is_parsing=false;
}

void roachParser::setIsDumpInputDbg(bool is_)
{
    is_dump_input_dbg=is_;

    if (dbg_file)
    {
        dbg_file->close();
        delete(dbg_file);
        dbg_file=0;
    }

    if (is_dump_input_dbg)
    {
        dbg_file = new QFile(QString("roachParseDbg_%1.bin").arg(parser_number));
        bool stat = dbg_file->open(QIODevice::WriteOnly);
        fprintf(stderr,"%d\n",stat);
    }


}






void roachParser::resetPulseCount(void)
{
    pulse_counter=0;

}

void roachParser::setIsPulseDetect(bool is_)
{
    is_pulse_detect=is_;
}

void roachParser::setIsPulseDetectFRD(bool is_)
{
    is_pulse_detect_frd=is_;
}


void roachParser::setPulseThresh(double thr_)
{
    pulse_thresh=thr_;
}

void roachParser::queueEvents(void)
{


    //pointer to events is dumped in queue. we dont delete, consumer will grab and delete.
    if (events!=0)
    {


        pushEventList(events);
    }
    events = 0;
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
    quint32 outmem_fff_maskhi=0xffff0000;
    quint32 outmem_chan_mask=0xff;
    quint32 outmem_pulse_mask=0x100;
    int cc;

    quint32 flux_ramp_data;
    float flux_ramp_fl;
    double phase_sum;

    quint32 datalong, datalong1,datalong2,datalongaaa;
    bool is_good_event = true;
    bool is_get_raw_evt_data = true;

    int chan, bin;
    double phaseout;
    int event_type;

    //new_data.clear();
    //new_data.append(carryover);

    num_parse_calls++;


    queuelen=data_source->length();
    data_source->read(new_data);
int dbgql;


        while (new_data.length() >=(2*event_length + 50))
        {
            //
            datalong=new_data.dequeue();
            //fprintf(stderr,"datalong- %x %x\n",datalong,(datalong&outmem_fff_maskhi)>>16);
            if (is_dump_input_dbg) dbg_file->write((const char*)&datalong,4);

            if ( ((datalong&outmem_fff_maskhi) >>16) == 0x5555)
             {

                event_length = (datalong&outmem_fff_mask) & 0xff;
                event_type = (((datalong&outmem_fff_mask)&0xff00)>>8);
                //event type
                // 0 older FW, raw event only
                // 1 raw chan event data, like older FW. aaaa, chan, data
                // 2 fluxramp, aaaa, chan
                // 3 fluxramp, aaaa, chan , raw data
                // 4 flux ramp aaa chan trans data


                // subtract off the aaaa and timestamp words, leaving only fft coef data

                if (event_type==0 || event_type==1 || event_type==4 )
                {
                    outmem_datalen = event_length-2;
                    is_get_raw_evt_data=true;
                }
                else if (event_type==3 )
                {
                    outmem_datalen= event_length;
                    is_get_raw_evt_data=true;
                }
                else
                {
                    outmem_datalen=0;
                    is_get_raw_evt_data=false;
                }



                if (event_type==2 || event_type==3|| event_type==4)
                {
                   flux_ramp_data = new_data.dequeue();
                   convToFloat((int*)&flux_ramp_data,
                               1,
                               &flux_ramp_fl,
                               ph_nfrac_bits,
                               ph_nbits,
                               ph_sign);


                    flux_ramp_fl = flux_ramp_fl * 3.141592653589793;
                }
                else
                    flux_ramp_data=0;


                // fprintf(stderr, "outmem_datalen %d\n",outmem_datalen);
                datalongaaa = new_data.dequeue();

                //fprintf(stderr, "datalongaaa %x\n",datalongaaa);

                if (is_dump_input_dbg) dbg_file->write((const char*)&datalongaaa,4);


                   datalong1 = new_data.dequeue();
                   //fprintf(stderr, "datalong1 %x\n",datalong1);
                    if (is_dump_input_dbg) dbg_file->write((const char*)&datalong1,4);

                    chan=datalong1&outmem_chan_mask;
                   chan = chan + channel_offset;
                     bin = -1;

                   if (chan_to_bin.contains(chan))
                        bin = chan_to_bin[chan];

                   quint32 timestamp = datalongaaa&outmem_ts_maskhi ;

                   timestamp = timestamp + ((datalong1&outmem_ts_masklow) >>9);
                   quint32 is_pulse = datalong1&outmem_pulse_mask;

                   //fprintf(stderr,"chan %d,timestamp %x \n",
                    //       chan, timestamp);

                   int plen;
                    is_good_event = true;

                    if (is_get_raw_evt_data)
                    {
                        if (new_data.length()>outmem_datalen)
                       {
                            for ( plen = 0; plen<outmem_datalen;plen++)
                            {
                                quint32 dp, dm;
                                datalong2=new_data.dequeue();
                                if (is_dump_input_dbg) dbg_file->write((const char*)&datalong2,4);

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
                            phase_sum=0.0;

                            for ( plen = 0; plen<outmem_datalen;plen++)
                            {

                                phase_tempf[plen] = (3.14159256*phase_tempf[plen] );
                                phase_sum +=phase_tempf[plen];
                            }




                       }
                       else
                           is_good_event= false;
                    }


                    //
                    // here we do pulse detectoion if turned on.
                    //
                    if (is_pulse_detect_frd && (event_type==2 || event_type==3 || event_type==4))
                    {
                           is_good_event= pulseDetectFRD( chan,  flux_ramp_fl);
                    }
                    else if (is_pulse_detect && is_get_raw_evt_data)
                    {
                        is_good_event=pulseDetectRaw( chan,  phase_sum, outmem_datalen);
                    }

                    //
                    //
                    //

                   if (is_good_event )
                  {
                       // adds new chan to events if not alreayd there.
                      addNewChannel(chan);


                      if ((*events)[chan]["timestamp"].length() >= max_list_length)
                      {
                          queueEvents();
                          // create new events list with current channel.
                          addNewChannel(chan);
                      }


                          (*events)[chan]["timestamp"].append((float)timestamp);
                          (*events)[chan]["is_pulse"].append((float)is_pulse);
                          (*events)[chan]["bin"].append((float)bin );//!! need to look at map
                          (*events)[chan]["event_type"].append((float)event_type );//!! need to look at map
                          (*events)[chan]["event_len"].append((float)(outmem_datalen));//!! need to look at map

                          if (is_get_raw_evt_data)
                          {

                              //!!addPhaseDelay(chan,plen,phase_tempf);
                              for ( plen = 0; plen<outmem_datalen;plen++)
                              {
                                  (*events)[chan]["stream_mag"].append(mag_tempf[plen] );
                                  (*events)[chan]["stream_phase"].append(phase_tempf[plen] );
                              }

                          }

                          if (event_type==2 || event_type==3 || event_type==4)
                          {
                              //demodFluxRamp(chan,mag_tempf, phase_tempf,outmem_datalen, &phaseout );
                              (*events)[chan]["flux_ramp_phase"].append(flux_ramp_fl);

                              float last_phase = (*phase_tracks)[chan];
                              float dphase = flux_ramp_fl - last_phase;
                              while(dphase<(-3.141592653589793))
                              {
                                  flux_ramp_fl+=6.283185307179586;
                                  dphase = flux_ramp_fl - last_phase;
                              }

                              while(dphase>3.141592653589793)
                              {
                                  flux_ramp_fl+=(-6.283185307179586);
                                  dphase = flux_ramp_fl - last_phase;
                              }

                              (*phase_tracks)[chan]=flux_ramp_fl;

                              (*events)[chan]["flux_ramp_phase_unwrap"].append(flux_ramp_fl);
                          }
                          else
                          {
                              (*events)[chan]["flux_ramp_phase"].append(-1.0);
                              (*events)[chan]["flux_ramp_phase_unwrap"].append(-1.0);
                          }



                         // fprintf(stderr,"Done Good evt\n");
                          //fflush(stdout);
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



void roachParser::makeFakeEventStream(void)
{
    int nevents = 50000;
    int stchan = 192;
    int numchans = 4;
    int cur_chan = 0;

    int stbin = 500;

    int cur_bin = 0;
    int datalen = 100;
    float phase_offset_chan;
    float phase_offset_time;
    float flux_ramp_fl;

    for (int k =0; k<nevents;k++)
    {
        phase_offset_chan =(float)cur_chan * 0.1;

        phase_offset_time =6.28*(float)k * 0.1;


        for (int m = 0;m<datalen;m++)
        {
            mag_tempf[m]= 0.01 + 0.01*((float)cur_chan);


            phase_tempf[m] =phase_offset_chan +   0.1*cos(phase_offset_time +\
                            3.14159 * 4.0 * ((float)m/(float)datalen) );
        }

        flux_ramp_fl = phase_offset_time;

    makeFakeEvent(
            (cur_chan + stchan), //int chan,
            k, //int timestamp,
            1, //int is_pulse,
            stbin - 2*cur_chan, //int bin,
            datalen, //int outmem_datalen,
            1, //bool is_get_raw_evt_data,
            flux_ramp_fl, //float flux_ramp_fl,
            3//int event_type
            );

    cur_chan = (cur_chan+1)%numchans;


    }
}


/**
 * @brief roachParser::makeFakeEvent-
 *  Make a software defined event into lists for debugging purposes. supply chan, etc. for phase and mag data
 *  put data in class vars mag_tempf, phase_tempf before calling function.
 * @param chan 0-255
 * @param timestamp 32 but int.
 * @param is_pulse 0 or 1
 * @param bin 0 to 511
 * @param outmem_datalen use 100 or around there. length of raw data in mag_tempf, phase_tempf
 * @param is_get_raw_evt_data, 1 to unclude raw mag and phase data, 0 otherwise
 * @param flux_ramp_fl  , calc ramp phase, in radian/pi
 * @param event_type, 1,2,3,4. 2,3,4 use flux ramp phase. 1 is raw data only. no fl ramp.
 */


void roachParser::makeFakeEvent(
        int chan,
        int timestamp,
        int is_pulse,
        int bin,
        int outmem_datalen,
        bool is_get_raw_evt_data,
        float flux_ramp_fl,
        int event_type
        )
{
int plen;

    // adds new chan to events if not alreayd there.
   addNewChannel(chan);


   if ((*events)[chan]["timestamp"].length() >= max_list_length)
   {
       queueEvents();
       // create new events list with current channel.
       addNewChannel(chan);
   }





           (*events)[chan]["timestamp"].append((float)timestamp);
           (*events)[chan]["is_pulse"].append((float)is_pulse);
           (*events)[chan]["bin"].append((float)bin );//!! need to look at map


           //if ((*events)[chan]["data_start_index"].length() ==0)
           //    (*events)[chan]["data_start_index"].append(0.0);
           //else
           //    (*events)[chan]["data_start_index"].append(
             //              (*events)[chan]["data_start_index"].last() +
             //                (*events)[chan]["event_len"].last());

           (*events)[chan]["event_len"].append((float)(outmem_datalen));//!! need to look at map
            (*events)[chan]["event_type"].append((float)event_type );//!! need to look at map




           if (is_get_raw_evt_data)
           {



               //!!addPhaseDelay(chan,plen,phase_tempf);
               for ( plen = 0; plen<outmem_datalen;plen++)
               {
                   (*events)[chan]["stream_mag"].append(mag_tempf[plen] );
                   (*events)[chan]["stream_phase"].append(phase_tempf[plen] );
               }

           }




           if (event_type==2 || event_type==3 || event_type==4)
           {
               //demodFluxRamp(chan,mag_tempf, phase_tempf,outmem_datalen, &phaseout );
               (*events)[chan]["flux_ramp_phase"].append(flux_ramp_fl);

              float last_phase = (*phase_tracks)[chan];
              float dphase = flux_ramp_fl - last_phase;
              while(dphase<(-3.141592653589793))
              {
                  flux_ramp_fl+=6.283185307179586;
                  dphase = flux_ramp_fl - last_phase;
              }

              while(dphase>3.141592653589793)
              {
                  flux_ramp_fl+=(-6.283185307179586);
                  dphase = flux_ramp_fl - last_phase;
              }

              (*phase_tracks)[chan]=flux_ramp_fl;

              (*events)[chan]["flux_ramp_phase_unwrap"].append(flux_ramp_fl);
           }
          else
          {
              (*events)[chan]["flux_ramp_phase"].append(-1.0);
              (*events)[chan]["flux_ramp_phase_unwrap"].append(-1.0);
          }




          // fprintf(stderr,"Done Good evt\n");
           //fflush(stdout);
            //print 'chan   %d  k  %d  is_pulse  %d  timestamp  %x    '%\
            //      (chan,k,is_pulse,timestamp)

            evtcnt++;



}






bool roachParser::pulseDetectRaw(int chan, double phase_sum,int outmem_datalen)
{
    //
    // here we do pulse detectoion if turned on.
    //
    int n;
    double deviation;
    bool is_good_event = true;
    bool is_trigger=false;

        //see if we need to averate or we collect pulses.
        if ( (*pulse_det_phaseavecount)[chan]  < num_phase_ave)
        {
            (*pulse_det_phaseave)[chan]+=phase_sum;
            (*pulse_det_phaseavecount)[chan] +=outmem_datalen;

            //finish up average...
            if ( (*pulse_det_phaseavecount)[chan]  >= num_phase_ave)
                (*pulse_det_phaseave)[chan] = (*pulse_det_phaseave)[chan] / ((double)(*pulse_det_phaseavecount)[chan]);
        }
        else
        {

            pulse_state = (*pulse_det_state)[chan];
            save_counter = (*pulse_det_savecount)[chan];

        switch(pulse_state)
        {


            case delete_data:

                  is_trigger = false;

                //determine if we have pulse in this event. set is_trigger if so.
                for ( n=0 ; n<outmem_datalen;n++)
                {
                    deviation = fabs(phase_tempf[n]- (*pulse_det_phaseave)[chan]);
                    if (deviation > pulse_thresh)
                    {
                        is_trigger = true;
                        n = outmem_datalen;
                    }
                }

                //we have a pulse. so goto save mode.
                if (is_trigger)
                {
                    is_good_event=true;
                    save_counter=save_max_count;

                    pulse_state = save_data;
                    pulse_counter++;
                }
               else
                  is_good_event =false;


                break;
        case save_data:
               if (save_counter>0)
               {

                  save_counter--;
                  is_good_event=true;
               }
               else
               {
                 pulse_state  =delete_data;

                 //after each pulse on chan x, we reaverage.
                 // the save counter max must be correct.


                     (*pulse_det_phaseave)[chan]=0.0;


                     (*pulse_det_phaseavecount)[chan]=0;


               }

            break;

        }//switch

        (*pulse_det_state)[chan] = pulse_state;
        (*pulse_det_savecount)[chan] = save_counter;


           }//else

        return(is_good_event);
}


/**
 * @brief roachParser::pulseDetectFRD
 * @param chan
 * @param phase_sum
 * @param outmem_datalen
 * @return
 */
bool roachParser::pulseDetectFRD(int chan, double flux_ramp_fl)
{
    //
    // here we do pulse detectoion if turned on.
    //
    int n;
    double deviation;
    bool is_good_event = true;
    bool is_trigger=false;

        //see if we need to averate or we collect pulses.
        if ( (*pulse_det_phaseavecount)[chan]  < num_phase_ave)
        {
            (*pulse_det_phaseave)[chan]+=flux_ramp_fl;
            (*pulse_det_phaseavecount)[chan] ++;

            //finish up average...
            if ( (*pulse_det_phaseavecount)[chan]  >= num_phase_ave)
                (*pulse_det_phaseave)[chan] = (*pulse_det_phaseave)[chan] / ((double)(*pulse_det_phaseavecount)[chan]);
        }
        else
        {

            pulse_state = (*pulse_det_state)[chan];
            save_counter = (*pulse_det_savecount)[chan];

        switch(pulse_state)
        {


            case delete_data:

                  is_trigger = false;

                //determine if we have pulse in this event. set is_trigger if so.

                deviation = fabs(flux_ramp_fl- (*pulse_det_phaseave)[chan]);
                if (deviation > pulse_thresh)
                    is_trigger=true;



                //we have a pulse. so goto save mode.
                if (is_trigger)
                {
                    is_good_event=true;
                    save_counter=save_max_count;

                    pulse_state = save_data;
                    pulse_counter++;
                }
               else
                  is_good_event =false;


                break;
        case save_data:
               if (save_counter>0)
               {

                  save_counter--;
                  is_good_event=true;
               }
               else
               {
                 pulse_state  =delete_data;

                 //after each pulse on chan x, we reaverage.
                 // the save counter max must be correct.


                     (*pulse_det_phaseave)[chan]=0.0;


                     (*pulse_det_phaseavecount)[chan]=0;


               }

            break;

        }//switch

        (*pulse_det_state)[chan] = pulse_state;
        (*pulse_det_savecount)[chan] = save_counter;


           }//else

        return(is_good_event);
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

/**
 * @brief roachParser::convToFloat convert binary fixed point data top a float
 * @param indata    array of fixed pt data
 * @param datalen   len of array
 * @param outdata   array of float data, output
 * @param nfrac_bits    num of bits in fraction
 * @param num_bits  num of bits in the total, frctino + int + significand()
 * @param sign_bit  1 if there is sign bit, 0 if not
 */
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

/**
 * @brief roachParser::setCircleCoord Given string of key val pairs chan:xc:yc , chan:xc:yc all ints
 *
 * @param circle_
 */
void roachParser::setCircleCoord(QString circle_)
{
    QStringList pairs = circle_.split(",");
    int p;
    int channel;
    float circle_xc , circle_yc;

    for ( p = 0; p<pairs.length();p++)
    {

        QStringList pair_ = pairs[p].split(":");
        if (pair_[0]!="" && pair_[1]!=""&& pair_[2]!="")
        {

            circle_xc = pair_[1].toFloat();
            circle_yc = pair_[2].toFloat();
            channel=pair_[0].toInt();
            addNewChannel(channel);
            (*events)[channel]["circle_specs_xy"].append(circle_xc);
            (*events)[channel]["circle_specs_xy"].append(circle_yc);
            fprintf(stderr, "Add circle chan: %d, xc:%f, yc:%f \n",channel, circle_xc, circle_yc);
        }
        else
        {
            fprintf(stderr, "roachParser::setCircleCoord ERROR- bad string\n");

        }

    }


}


/**
 * @brief roachParser::polar2Rect convert x,y pair into polar coord
 * @param radius input radius
 * @param radians input angle in radians
 * @param xc output x
 * @param yc outptu y
 */
void roachParser::polar2Rect(double radius, double radians,double &xc, double &yc)
{
    xc = radius * cos(radians);
    yc = radius * sin(radians);

}

/**
 * @brief roachParser::rect2Polar convert x y to polar coord
 * @param xc input x
 * @param yc    input y
 * @param radius    output radius
 * @param radians   outpu angle, radians
 */
void roachParser::rect2Polar(double xc, double yc, double &radius, double &radians)
{
    radius = sqrt( xc*xc + yc*yc);
    radians = atan2(yc,xc);
}

/**
 * @brief roachParser::translate
 * @param xin
 * @param yin
 * @param xout
 * @param yout
 */
void roachParser::translate(int channel, double xin,double yin, double &xout, double &yout)
{
    xout = xin - (*events)[channel]["circle_specs_xy"][0];
    yout = yin - (*events)[channel]["circle_specs_xy"][1];

}
/**
 * @brief roachParser::unwrapPhase
 * @param phase
 * @param len
 */
void roachParser::unwrapPhase(double *phase, int len)
{
    int k;
    double ph_z;

    ph_z = phase[0];
    for (k=1;k<len;k++)
    {
        while(phase[k] - ph_z >6)
            phase[k]=phase[k]-6.2831853071795862;

        while(phase[k] - ph_z < -6)
            phase[k]=phase[k]+6.2831853071795862;

        ph_z = phase[k];

    }
}
/**
 * @brief roachParser::DFT
 * @param xin array of real vals
 * @param len   len of array
 * @param bin   freq of the coef, in bin number, or periods per len
 * @param xout  scaler real dft coef output
 * @param yout  scalar imag dft coef output
 */
void roachParser::DFT(double *xin, int len, double bin, double *xout, double *yout )
{
    int k;
    *xout = 0.0;
    *yout = 0.0;
    for (k = 0; k< len; k++)
    {
        *xout +=  ( xin[k] * cos((double)k * 6.2831853071795862 *  (bin/(double)len) )  );

        *yout +=  (  xin[k] * sin((double)k * 6.2831853071795862 *  (bin/(double)len) ) );


    }

}

/**
 * @brief roachParser::roachParserdemodFluxRamp
 * @param mag   array of mags input
 * @param phase array of phawse input
 * @param len   len of array
 * @param phaseout  single phase scaler output
 */
void roachParser::demodFluxRamp(int channel,float *mag, float *phase, int len,  double *phaseout)
{
    int k;
    double xc,yc;
    double xct, yct;
    double rt,pht;

    double ph_t[1024];
    double dft_x,  dft_y;
    double dft_r, dft_ph;

    if (len>1023)
    {
        fprintf(stderr,"roachParser::demodFluxRamp, len >1024 ERROR\n");
        *phaseout = 0;
        return;
    }



    for (k =0; k < len; k++)
    {


        polar2Rect((double)mag[k], (double)phase[k],xc,yc);
        translate(channel,xc,yc,xct,yct);
        rect2Polar(xct,yct,rt,pht);

        ph_t[k] = pht;
    }

    unwrapPhase(ph_t,len);
    DFT(ph_t, len, flux_bin, &dft_x, &dft_y );
    rect2Polar(dft_x,dft_y, dft_r, dft_ph );
    *phaseout = dft_ph;
}

/**
 * @brief roachParser::setFluxBin Set fft bin that the flux ramp freq is in
 * @param bin_ the bin. or freq/dft len
 */
void roachParser::setFluxBin(double bin_)
{
    flux_bin=bin_;
    fprintf(stderr, "FluxRamp bin = %f \n",flux_bin);

}

/**
 * @brief roachParser::setIsFluxDemod turn on off flux reamp demod
 * @param is_ true to perform flux ramp demod during parsing roach data
 */
void roachParser::setIsFluxDemod(bool is_)
{
    is_demod_fluxramp=is_;
    fprintf(stderr, "FluxRamp demod = %d \n",is_demod_fluxramp);
}

/**
 * @brief roachParser::setTimeDelay Set time delay of RF xmission line in radians for each chan
 * @param ns_ chan_phasedelay String of pairs "chan:radians, chan:radians" etc.
 */
void roachParser::setTimeDelay(QString chan_phasedelay)
{
    QStringList pairs = chan_phasedelay.split(",");
    int p;
    int channel;
    float phase_delay;

    for ( p = 0; p<pairs.length();p++)
    {

        QStringList pair_ = pairs[p].split(":");
        if (pair_[0]!="" && pair_[1]!="")
        {

            phase_delay = pair_[1].toFloat();

            channel=pair_[0].toInt();
            addNewChannel(channel);
            (*events)[channel]["phase_delay"][0]  = phase_delay;
            fprintf(stderr, "Add delay chan: %d,  phase:%f \n",channel, phase_delay);
        }
        else
        {
            fprintf(stderr, "roachParser::setTimeDelay ERROR bad string\n");

        }

    }


}

/**
 * @brief roachParser::addPhaseDelay Add phase offset due to RF time delay of xmission line.
 * @param chan  Channel of interest
 * @param len   Lengeh of phase array
 * @param phase Phase array to add phase.
 */
void roachParser::addPhaseDelay(int chan, int len, float *phase)
{
    for (int k = 0; k<len; k++)
    {
        phase[k] = phase[k] + (*events)[chan]["phase_delay"][0];
    }
}
