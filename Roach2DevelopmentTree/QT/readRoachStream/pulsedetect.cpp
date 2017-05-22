
#include "pulsedetect.h"
#include "unistd.h"
#include "math.h"
pulseDetect::pulseDetect(QObject *parent) :
    roachParser(0,0, 0)
{
     parser = 0;
     is_stream=false;
}




void pulseDetect::pulseDetectThread(void)
{

    bool is_running = is_stream;
    int nwaits = 0;

    //we copy is_stream so we can start saving. if we turn off stream,
    // we only want to stop saving if no evetns left. else we miss end of data.
    // a feature of this is that you cannot stop saving until you stop gathering data.
    while (is_running)
    {
        in_events=parser->getEventList();
        if (in_events==0)\
        {
            // every time we have to wait for data, we inc counter.

            // wait .5sec for morre data
            usleep(500000);

            //if waited 2.5 sec end loop if user attempt stop it by is_stream=false
            if (nwaits>5)
            {
                is_running=is_stream;
            }
            else
            {
                 // every time we have to wait for data, we inc counter.
                nwaits++;

            }
        }
        else
        {
            scanForPulsesFRD();
            in_events->clear();
            delete in_events;
            in_events = 0;
            //set num of waits for data to 0.
            nwaits = 0;

        }
    }



}




/**
 * @brief fileSaver::scanForPulses
 * @param chan
 */
void pulseDetect::scanForPulsesFRD(){

    float frd;
    int k;
    float  deviation;
    int numtoave;
    int lenfrd;

    QList<int> chanlist = (*in_events).keys();

    int chan;
    int m;
    int n,p,q;
    int pulse_start;
    int pulse_end;

    for (m=0;m<chanlist.length();m++)
    {
            chan = chanlist[k];
        lenfrd = (*in_events)[chan]["flux_ramp_phase_unwrap"].length();
        //
        // Have we set the noise value for this channel?
        //
        if (!getIsGotNoiseAverage(chan))
            getAverageNoiseValue( chan);


        for ( k=0;k<lenfrd;k++)
        {
            frd = (*in_events)[chan]["flux_ramp_phase_unwrap"][k];

            deviation = fabs(frd- (*pulse_det_phaseave)[chan]);
            if (deviation > pulse_thresh)
            {
               //we are at start ofa  pulse
                for (n = k;n<lenfrd;n++)
                {
                    frd = (*in_events)[chan]["flux_ramp_phase_unwrap"][n];
                    deviation = fabs(frd- (*pulse_det_phaseave)[chan]);
                    if (deviation <= pulse_thresh)
                        break;
                }
                pulse_start=k;
                pulse_end = n;
               savePulse( chan,pulse_start , pulse_end);
                pulse_counter++;
                k = n+1;
            }//if (deviation > pulse_thresh)
        }//for ( k=0;k<lenfrd;k++)
    }//for (m=0;m<chanlist.length();m++)

    queueEvents();
}

void pulseDetect::addNewChannel(int channel)
{
    roachParser::addNewChannel(channel);
    if ( !(*events)[channel].contains("pulse_number"))
    {
        // the fft bin for this channel
        (*events)[channel]["pulse_number"]=QList<float>();
    }
}

void pulseDetect::savePulse(int chan, int st, int end)
{
    addNewChannel(chan);

    int copy_st = st -pre_pulse_samples;
    int copy_end=end + post_pulse_samples;
    int lenfrd = (*in_events)[chan]["flux_ramp_phase_unwrap"].length();

    if (copy_st <0)
        copy_st = 0;

    if (copy_end> lenfrd)
        copy_end=lenfrd-1;

    int k;

    for (k=copy_st; k<copy_end;k++)
    {
        (*events)[chan]["bin"][k]=(*in_events)[chan]["bin"][k];
        (*events)[chan]["timestamp"][k]=(*in_events)[chan]["timestamp"][k];
        (*events)[chan]["is_pulse"][k]=(*in_events)[chan]["is_pulse"][k];
        (*events)[chan]["event_len"][k]=(*in_events)[chan]["event_len"][k];
        (*events)[chan]["event_type"][k]=(*in_events)[chan]["event_type"][k];

        (*events)[chan]["flux_ramp_phase"][k]=(*in_events)[chan]["flux_ramp_phase"][k];
        (*events)[chan]["flux_ramp_phase_unwrap"][k]=(*in_events)[chan]["flux_ramp_phase_unwrap"][k];
        (*events)[chan]["circle_specs_xy"][k]=(*in_events)[chan]["circle_specs_xy"][k];
        (*events)[chan]["phase_delay"][k]=(*in_events)[chan]["phase_delay"][k];
        (*events)[chan]["pulse_number"][k]=pulse_counter;


    }





}

bool pulseDetect::getIsGotNoiseAverage(int chan)
{
    bool is_done_averaging =  (*pulse_det_phaseavecount)[chan]  >= num_phase_ave;

    return(is_done_averaging);
}

void pulseDetect::getAverageNoiseValue(int chan)
{
    float frd;
    int k;
    float  deviation;
    int numtoave;
    int lenfrd = (*events)[chan]["flux_ramp_phase_unwrap"].length();
    float flux_ramp_fl;
    //
    // Have we set the noise value for this channel?
    //

    if ( ! getIsGotNoiseAverage(chan) )
    {
        //how many noise do we have still left to average
        int numtoave = num_phase_ave - (*pulse_det_phaseavecount)[chan];
        // if num left to average larger than dataset, do not go oever len of dataset.
        if (numtoave>lenfrd)
            numtoave=lenfrd;

        for ( k=0;k<numtoave;k++)
        {
            flux_ramp_fl=(*events)[chan]["flux_ramp_phase_unwrap"][k];
            (*pulse_det_phaseave)[chan]+=flux_ramp_fl;

            (*pulse_det_phaseavecount)[chan] ++;
        }

        //finish up average...
        if ( (*pulse_det_phaseavecount)[chan]  >= num_phase_ave)
            (*pulse_det_phaseave)[chan] = (*pulse_det_phaseave)[chan] / ((double)(*pulse_det_phaseavecount)[chan]);
    }

}


