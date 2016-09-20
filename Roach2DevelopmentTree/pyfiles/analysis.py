"""

execfile('analysis.py')



phsine = calcFluxRampPhase(0,0,4)

blip_index = 100+1000


res = MKID_list[0].reslist[0]


ramp_freq = 7812.5
samp_rate = 128e6 / res.fftsynctime[2]
blip_len = 4
blip_period = (samp_rate / ramp_freq )
segment_len = blip_period- blip_len
nsegments = 1000

figure(101)
clf()
figure(102)
clf()

seg_phase = []

for k in range(nsegments):
    st = (blip_index+blip_len)
    ed = st + segment_len
    segment =  removePhaseJumps( phsine[st:ed] )    
    figure(101)
    plot(segment)
    blip_index = blip_index + blip_period
    S = fft.fft(segment - mean(segment))
    figure(102)
    plot(abs(S))
    bin = numpy.argmax(abs(S)[:blip_period/2])
    phase = numpy.angle(S[bin])
    seg_phase.append(phase)
  

nsegments  = len(iq[192]['event_len'])
figure(101);clf()
figure(102);clf()
seg_phase=[]
for k in range(nsegments):
    segment =  getSegment2(iq,192,k)
    figure(101)
    plot(segment)   
    S = fft.fft(segment - mean(segment))
    figure(102)
    plot(abs(S))
    bin = numpy.argmax(abs(S)[:20])
    phase = numpy.angle(S[bin])
    seg_phase.append(phase)
  

figure(103)
clf()
seg_phase2 = removePhaseJumps(seg_phase)
plot(seg_phase)

##########

clf()
plot(res.iqnoise[1][192]['stream_mag'][0:2000])

clf()
plot(segment)

plot(removePhaseJumps(segment))

###################3

phsine = calcFluxRampPhase(0,1,3)
phsine = removePhaseJumps(phsine)

blip = 173
seglen = 45

figure(200)
clf()

nsegs = len(phsine)/seglen - 2

for i in range(0,nsegs,100):
    ss = getSegment(phsine,i,seglen,blip)
    plot(ss)

execfile('analysis.py')

anal_vsweep(fname)

fname = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul14/vsweep_10_1.h5'

fname = '../../datafiles/jul14/vsweep_1.h5'

fname = '../../datafiles/jul14/vsweep_4.h5'

fname = '../../datafiles/jul14/vsweep_10_1.h5'



execfile('analysis.py')



fname  = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul15/vsweep_testB_3.h5'

fname  = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul15/vsweep_testB_4.h5'


aaa = getEventsByTimeStamp(vs,3200,isplot=True,fignum=8)

vsa = anal_vsweep_fast(fname)

vsa = list(vsa)
hdf.open(fname.replace('.h5','_vsa.h5'),'w')
hdf.write(vsa,'vsa')
hdf.close()



rffreq = array([5096e6,5111e6,5199e6])
#vlist = arange(10,0,-0.02)
vlist = arange(0,10,0.02)
fname =  '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul19/vsweep_mult_0u10000b20_1.h5'

vs = voltSweepFast(vlist,rffreq,fname)

vsa = anal_vsweep_fast(fname)
hdf.open(fname.replace('.h5','_vsa.h5'),'w')
hdf.write(vsa,'vsa')
hdf.close()



"""


from matplotlib.backends.backend_pdf import PdfPages

#dd=fa.dataread
#dd.iqdata=events




    



def anal_vsweep_fast(fname):


    hdf=hdfSerdes()
    hdf.open(fname,'r')
    events = hdf.read()
    hdf.close()

    figure(1)
    clf()
    figure(2)
    clf()
    figure(3)
    clf()
    alldata= {}
    
    
    for ch in events.keys():


        seg_phase=[]
        vdata=[]
        voltlist = lsUniqueTimeStamps(events,chan=ch)

        #disregard 1st so many events after voltage change. may be bad data.
        nthrowaway=100

        for volts in sort(voltlist.keys()):

            #typle  mags:list of arrays,, phases:llist of arrays, k:where in stream last found.  
            evts = getEventsByTimeStamp(events,volts ,chan=ch)
            st_search=evts[2]
            #num ev found at that voltage
            nev = len(evts[0])

            print "volts: %f nev: %d"%(volts,nev)
            #get 1 event from the list.

            if nev>nthrowaway:
                seg=evts[1][nthrowaway]

                figure(1)
                plot(seg)  
                S = fft.fft(seg - mean(seg))
                figure(2)
                plot(abs(S))
                bin = numpy.argmax(abs(S)[:20])
                phase = numpy.angle(S[bin])
                seg_phase.append(phase)
                vdata.append(volts)


        figure(3)

        seg_phase2 = removePhaseJumps(seg_phase)
        plot(vdata,seg_phase2)
        #plot(vdata,seg_phase2,'x')
        
        alldata[ch]=[vdata, seg_phase2, events[ch]['rffreq']]


    return( alldata )





def lsUniqueTimeStamps(events,chan=192):
    
    unq_ts = sort(list(set(events[chan]['timestamp'] )))
    ts_ct = {}
    for ut in unq_ts:
        ts_ct[ut]=list(events[chan]['timestamp']).count(ut)
    
    return(ts_ct )
    


def getEventsByTimeStamp(events,tsfind,startindex=0,chan=192,isplot=False,fignum=8):


    magev=[]
    phsev = []
    
    foundindex = 0
    for k in range(startindex, len(events[chan]['timestamp'])):
        ts = events[chan]['timestamp'][k]
        if ts==tsfind:
            #assume all event_len are all the same. 
            evlen = events[chan]['event_len'][k]
            mm=  events[chan]['stream_mag'][ (k*evlen):((k+1)*evlen)]
            pp=  events[chan]['stream_phase'][ (k*evlen):((k+1)*evlen)]
            foundindex=k
            magev.append(mm)
            phsev.append(mm)
     
    if isplot:
        figure(fignum)       
        
        for k in range(len(magev)):
            subplot(2,1,1)
            plot(magev[k])
            subplot(2,1,2)
            plot(phsev[k])
            
            
            
    return( (magev,phsev,k) )









def anal2pdf():


    pp = PdfPages('../../datafiles/jul14/analplots.pdf')
   
    
    fnames = [
    '../../datafiles/jul14/vsweep_10_1.h5',
    '../../datafiles/jul14/vsweep_10_1b.h5',
    '../../datafiles/jul14/vsweep_10_2.h5',
    '../../datafiles/jul14/vsweep_10_3.h5',
    '../../datafiles/jul14/vsweep_10_4.h5',
    '../../datafiles/jul14/vsweep_10_5.h5',
    '../../datafiles/jul14/vsweep_10_6.h5']
   
    
    for fn in fnames:
       anal_vsweep(fn)
       figure(1)
       suptitle('Voltage sweep, 5096MHz, raw phase(Y), time_samples(X)')
       f=gcf()
       f.savefig(pp,format='pdf')
    
       figure(3)
       suptitle('Voltage sweep, 5096MHz, radians(Y) vs mV(X)')
       f=gcf()
       f.savefig(pp,format='pdf')
    
    pp.close()
    

def anal_vsweep(fname):


    hdf=hdfSerdes()
    hdf.open(fname,'r')
    vs = hdf.read()
    hdf.close()

    kz=  sort(vs.keys())

    figure(1)
    clf()
    figure(2)
    clf()
    seg_phase=[]
    vdata=[]
    
    for k in kz:
        if 192 in vs[k].keys():
          phdata = vs[k][192]['stream_phase']    
          seg = getSegment(phdata, 100, 95, 52)
          figure(1)
          plot(seg)  
          S = fft.fft(seg - mean(seg))
          figure(2)
          plot(abs(S))
          bin = numpy.argmax(abs(S)[:20])
          phase = numpy.angle(S[bin])
          seg_phase.append(phase)
          vdata.append(k)
        else: print "missing data for %d mV"%k


    figure(3)
    clf()
    seg_phase2 = removePhaseJumps(seg_phase)
    plot(vdata,seg_phase2)
    plot(vdata,seg_phase2,'rx')

    return( (vdata, seg_phase2) )


def getSegment(phdata, index, segment_len, offset):
    st = (offset +index*segment_len)
    ed = st + segment_len
    segment =  removePhaseJumps( phdata[st:ed] )    
    return(segment)


def plotSegs(iq,chan):

    figure(404)
    clf()
    nsegs = len(iq[chan]['data_start_index'])
    for index in range(1,nsegs,10):
        s = getSegment2(iq,chan,index)
        plot(s)


def getSegment2(iq,chan,index):
    st = iq[chan]['data_start_index'][index]
    ed = st + iq[chan]['event_len'][index]
    return( removePhaseJumps( iq[chan]['stream_phase'][st:ed]) )

def removePhaseJumps(phase_sig):
    newphase = [0] * len(phase_sig)
    
    newphase[0] = phase_sig[0]
    
    for k in range(1,len(phase_sig)):
        newphase[k] = phase_sig[k]
        dphase = newphase[k] - newphase[k-1]
        while dphase>pi:
            newphase[k] = newphase[k]-2*pi
            dphase = newphase[k] - newphase[k-1]
            
        while dphase<(-pi):
            newphase[k] = newphase[k]+2*pi
            dphase = newphase[k] - newphase[k-1]
        
    return(newphase)    


def calcFluxRampPhase(mkidnum,resnum,noisetrnum):
    res = MKID_list[mkidnum].reslist[resnum]


    res.setDelay(30e-9)

    if res.applied_delay ==0.0: res.applyDelay()


    res.plotFreq()

    fit.reslist=[res]
    fit.fit_circle2()

    iqnp=  [ res.iqnoise[noisetrnum][192]['stream_mag'] , res.iqnoise[noisetrnum][192]['stream_phase'] ]
    iqn= fit.PolarToRect(iqnp)


    iqn_tr = fit.trans_rot3(res, iqn)

    iqn_trp = fit.RectToPolar(iqn_tr)


    figure(100)
    clf()
    subplot(2,1,1)
    plot(iqn_trp[0][10000:10500])

    subplot(2,1,2)
    plot(iqn_trp[1][10000:10500])

    return(iqn_trp[1])



#give a resonatorData with iqdata being a wide span w/ manu MKIDs
#give center freqiencies and span.
#return resonaData list with iqdata being sub span of orig resdata obj.
def splitResonator(res,freqlist_Hz,span_Hz):
    



    res.info()

    reslist = []

    #span of res in Hz, 1/2 span actually
    hlfspan=span_Hz/2

    #Hz /index
    fresolution =  (res.freqs[-1] - res.freqs[0])/len(res.freqs) 
    
    for k in range(len(freqlist_Hz)):
    
        leftfreq = freqlist_Hz[k] - span_Hz/2
        #get freq diff from left to 1st freq, then convert to indices
        #index in freqs of left of span
        ist = (leftfreq - res.freqs[-1]) / fresolution
        
        rightfreq = freqlist_Hz[k] + span_Hz/2
        #get freq diff from left to 1st freq, then convert to indices
        #index in freqs of right of span
        ied = (rightfreq - res.freqs[-1]) / fresolution
        
        
        newres=resonatorData(k,'');
        newres.setData(
            [res.iqdata[0][ist:ied], res.iqdata[1][ist:ied]],
            res.freqs[ist:ied],
            res.delayraw,
            res.carrierfreq)
            
        reslist.append(newres)

    return(reslist)
