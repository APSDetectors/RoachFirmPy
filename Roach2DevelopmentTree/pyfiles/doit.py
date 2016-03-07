"""


execfile('doit.py')

sweep(span_Hz=300e6, center_Hz=5700e6, pts=2048)


ds=findData(192)

subplot(2,1,1)
plot(fa.carrier_freqs,
    fa.iqdata[192]['stream_mag'][ds:(ds+6000)])

subplot(2,1,2)
plot(fa.carrier_freqs,
    fa.iqdata[192]['stream_phase'][ds:(ds+6000)])



form.pool=QThreadPool()
runnable = QRunPyThread( 
    'fa.sweep(span_Hz=%f*1e6, center_Hz=%f*1e6, pts=2048)'%(sf,cf) )

status=form.pool.tryStart( runnable )





fa.an.freq_time_delay=0.02


figure(1)
clf()


"""

def findData(chan=192):
    for k in range(300):
        if fa.iqdata[chan]['stream_mag'][k] >0.001:
            return(k)
            
    return(0)



def sweep(span_Hz=100e6, center_Hz=3000e6, pts=2048):

    fa.stopCapture()

    fa.sweep_num_freqs=pts;
    #fa.sweep_samples_per_freq=floor(65536/fa.sweep_num_freqs)

    fa.fbase = 10e6
    fa.sourceCapture(
        [fa.fbase],
        20000,
        numffts = 1,
        whichbins='Freqs',
        is_trig = False)



    fa.start_carrier = center_Hz + fa.fbase-span_Hz/2.0
    fa.end_carrier = center_Hz + fa.fbase+span_Hz/2.0
    fa.inc_carrier = span_Hz/pts
    fa.carrier_freqs = arange(
        fa.start_carrier ,
        fa.end_carrier,
        fa.inc_carrier )



    fa.an.setOnOff(0)

    #take off data... we have some fifo problem... some time delay for some rheason...
    for k in range(256):        
        fa.rfft.trigFFT()




    fa.an.setOnOff(1)

    for cf in fa.carrier_freqs:

        print 'trig fft cf=%f'%cf
        fa.setCarrier(cf)

        fa.rfft.trigFFT()


    #we have taken 200 points, becaise some FWs may not have fifl readout yet we take
    #rest of points to fill memory, to make sure we have fifos readout. this is not used 
    #data for cal.


    time.sleep(.1)
    fa.an.setOnOff(0)

    fa.rfft.numFFTs(65536)
    fa.rfft.progRoach()
    fa.rfft.trigFFT()

    time.sleep(1)
    fa.stopCapture()
    time.sleep(1)    
    #now mem is fill, we can readout...
    fa.getIQ();



    stindex = fa.findSweepData()
    mags = fa.iqdata[chan]['stream_mag'][stindex : (stindex+pts)]
    phase = fa.iqdata[chan]['stream_phase'][stindex : (stindex+pts)]    

    fa.iqdata_sweep = fa.dataread.PolarToRect( [mags,phase] )
    fa.freqs_sweep = fa.carrier_freqs - fa.fbase


