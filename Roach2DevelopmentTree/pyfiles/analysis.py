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

from collections import OrderedDict

from matplotlib.backends.backend_pdf import PdfPages

#dd=fa.dataread
#dd.iqdata=events

'''

execfile('analysis.py')




'''



'''

execfile('analysis.py')

frdnoise()

'''

##########################################3
#
#given file w/ iqcfrd data,. closed loop, we find noise of frd data from raoch fw frd ckt.
# then using iqc data, we calc frd in python, and copmpare noise to what hw gave.
# gove open hdf file, h5py handle
# h = h5py.File(fn,'r')
# fn = '/home/beams0/TMADDEN/ROACH2/datafiles/Feb22_2017/noise_frdiqc_l160r10kd54p4_cl_1.h5'
############################################

def testhwfrd(h):
    
    evtlen =  h['iqdata_raw']['keyint_192']['keystr_event_len'][0]
    datlen = len(h['iqdata_raw']['keyint_192']['keystr_stream_phase'])
    numevts = len(h['iqdata_raw']['keyint_192']['keystr_timestamp'])

    numevts = 10000
    frdbin = 4
    frdsw = zeros(numevts)
    for k in range(numevts):
        st = int(k*evtlen)
        ed = int(st+evtlen)
        dat = h['iqdata_raw']['keyint_192']['keystr_stream_phase'][st:ed]
        F = fft.fft(dat)
        frdsw[k] = angle(F[4])
        

    frdhw = h['iqdata_raw']['keyint_192']['keystr_flux_ramp_phase'][0:numevts]

    
    figure(1)
    clf()
    subplot(2,1,1)
    plot(frdsw)
    plot(frdhw)
    subplot(2,1,2)
    plot(frdhw-frdsw)
    
    figure(2)




######################################    
# fn='/home/beams0/TMADDEN/ROACH2/datafiles/Feb22_2017/noise_rawfrd_l160r10kd54p4_cl_1.h5'
# h = h5py.File(fn,'r')
#
#
##########################################

def testhwfrd2(h):
    
    evtlen =  h['iqdata_raw']['keyint_192']['keystr_event_len'][0]
    datlen = len(h['iqdata_raw']['keyint_192']['keystr_stream_phase'])
    numevts = len(h['iqdata_raw']['keyint_192']['keystr_timestamp'])

    xc =0.24964919791690368
    yc= 0.21232281595341021
    
    #numevts = 10000
    print numevts
    
    frdbin = 4
    frdsw = zeros(numevts)
    for k in range(numevts):
        st = int(k*evtlen)
        ed = int(st+evtlen)
        phs = h['iqdata_raw']['keyint_192']['keystr_stream_phase'][st:ed]
        mag = h['iqdata_raw']['keyint_192']['keystr_stream_mag'][st:ed]
        iq = fa.dataread.PolarToRect( [mag,phs] )
        iq[0] = iq[0] - xc
        iq[1] = iq[1] - yc
        pm2=fa.dataread.RectToPolar(iq)         
        dat = pm2[1]
        F = fft.fft(dat)
        frdsw[k] = angle(F[4])
        

    frdhw = h['iqdata_raw']['keyint_192']['keystr_flux_ramp_phase'][0:numevts]

    
    frdhw = frdhw / (2.0*pi)
    frdsw = frdsw / (2.0*pi)
    
    figure(1)
    clf()
    subplot(2,1,1)
    plot(frdsw)
    plot(frdhw)
    subplot(2,1,2)
    plot(frdhw-frdsw)
    
    figure(2)
    nhw = scipy.signal.welch(frdhw,nperseg=8192)
    nsw = scipy.signal.welch(frdsw,nperseg=8192)
    plot(nhw[0],nhw[1])
    plot(nsw[0],nsw[1])
    yscale('log')
    xscale('log')



############################
#
# analyze linearty from tes iv curve, use raw or iqc data,. muyst be iopen loop data. 
# does frd in pty code. tells which frd settings have best lin perf.
#
################################3        
        
def analfrdlin(
    h,
    isplot = False,
    skipfactor = 1,
    integ_offsetlist=[0,25,50,75,100,125,150],
    lastvoltage = 4000):

    if isplot:
        figure(1)
        clf()
        figure(2)
        clf()
        figure(3)
        clf()

    alldata= {}
    
    
    ch=192

    seg_phase=[]
    vdata=[]

    #get length f our raw phase data
    datlen = len(h['iqdata_raw']['keyint_192']['keystr_stream_phase'])

    #estimate number of voltages...
    nvolts = len(arange(10.0,0.0,-0.01))
    #approx phase data per each voltage...
    datpvolts=datlen/nvolts
    
    #num events from file
    numevts = len(h['iqdata_raw']['keyint_192']['keystr_timestamp'])
    #apprix num evts per volt
    nevtpvolts = numevts/nvolts
    
    #evt len from file
    evtlen =  h['iqdata_raw']['keyint_192']['keystr_event_len'][0]
    
    #get list of all the voltages in the file, in mv, from time4stamp. nevtpvolts/10 means we csample file approx 10samples
    #per voltage... 
    vlist_ = h['iqdata_raw']['keyint_192']['keystr_timestamp'][::nevtpvolts/10]
    if isplot:
        figure(1)
        clf()
        plot(vlist_,'x')
    
    #get ACTUAL unique voltages in the file. 
    vlist = list(OrderedDict.fromkeys(vlist_).keys())
    #actual num of voltages.
    nvolts = len(vlist)
    
    #approx len of data pervioltate, 
    datpvolts=datlen/nvolts
    #when searching large hdf datasets, we decimate data by this to be sure we can find evetns with given voltage.
    searchsize = (numevts/nvolts)/10
    
    
    
    
    
    
    
    #!!skipfactor = 50

    if isplot:
        figure(4);clf()
        draw()
        figure(5)
        clf()
        draw()
        
        
    linerrcurves = {}
    for frdbin in [1,2,3,4]:
        integration_len = 40*frdbin




        
        
        #!!for integration_offset in [50,100]:
        #!!for integration_offset in [0,25,50,75,100,125,150]:
        for integration_offset in integ_offsetlist:
            print '=============='
            

            ivcurve = []
            vcurve = []
            #shoudl be nvolts
            for vindex in range(0,nvolts,skipfactor):
                cur_volt = vlist[vindex]
                if cur_volt<lastvoltage:
                    break

                print 'bin= %d integration_offset %d voltage %d mV'%\
                    (frdbin,integration_offset,cur_volt)
                #get all evt indices where we have cur_volt

                evt_indices = where(h['iqdata_raw']['keyint_192']['keystr_timestamp'][:]==cur_volt)[0]
                evt_first=evt_indices[0]
                evt_last = evt_indices[-1]

                nevts_curvolt = len(evt_indices)


                stream_st = evtlen * evt_first

                if isplot:
                    figure(2)
                    clf()

                frdevt = zeros(nevts_curvolt)

                for k in range(0,nevts_curvolt):
                    st = int(stream_st + k*evtlen)
                    st = st + integration_offset
                    ed = int(st + integration_len)
                    phasedat = h['iqdata_raw']['keyint_192']['keystr_stream_phase'][st:ed]          
                    F=fft.fft(phasedat)
                    frdevt[k] = angle(F[frdbin])
                    if isplot and (rand()<0.002):
                        plot(phasedat)
                        draw()


                frdevt = removePhaseJumps(frdevt)
                if isplot:
                    figure(3)
                    clf()
                    plot(frdevt)
                    draw()

                frd_start = 800
                frd_end = nevts_curvolt
                if frd_end>frd_start:
                    frdave = mean(frdevt[frd_start:frd_end])
                    ivcurve.append(frdave)
                    vcurve.append(cur_volt)


            ivcurve2=removePhaseJumps(ivcurve)

            vcurve=array(vcurve)
            ivcurve2=array(ivcurve2)

            if isplot:
                figure(4)
                plot(vcurve,ivcurve2)
           

            slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(vcurve,ivcurve2)
            
            if isplot:
                plot(vcurve, slope*vcurve + intercept,'r')
                draw()

                figure(5)

            linerr = ivcurve2 - (slope*vcurve + intercept)
            percentlinerr = linerr / (max(ivcurve2) - min(ivcurve2))

            if isplot:
                plot( percentlinerr)
                draw()
            #  vcurve=aa[0];ivcurve2=aa[1]

            mykey =integration_len *10000 +integration_offset
            linerrcurves[mykey]={
                'percentlinerr':percentlinerr,
                'vcurve':vcurve,
                'ivcurve2':ivcurve2,
                'slope':slope,
                'intercept':intercept,
                'integration_offset':integration_offset,
                'frdbin':frdbin,
                'integration_len':integration_len
                }
        
            pickle.dump(linerrcurves,open('frdlinanal.pik','wb'))
            
    
    maxlinerr=[]
    for lec in linerrcurves.keys():
        maxlinerr.append(max(linerrcurves[lec]['percentlinerr']))

    if isplot:    
        figure(6)
        clf()
        plot(maxlinerr)
    
    return(linerrcurves)
    
    



######################################3
# anal open loop iqc data from roach. to get noise. frd is done in py code. assume raw open loop frd data iqc.
# tells which frd settinsg have best noise perf.
#
#########################################


def frdnoise():

    fn = '/home/beams0/TMADDEN/ROACH2/datafiles/Feb8_2017_/noise_ramp40k3.6v_ol_frdiqc_l25.h5'
    
    hdffile = h5py.File(fn,'r')
    print hdffile.keys()

    fftlen = 65536
    

    dlen = hdffile['iqdata_raw']['keyint_192']['keystr_stream_phase'].len()
    evtlen = hdffile['iqdata_raw']['keyint_192']['keystr_event_len'][0]
    nevts =dlen/evtlen
    glitchoffts = 17
    avgevt = numpy.array([0.0]*25)
    for evtnum in range(100):
    
        st = int(glitchoffts + evtnum * evtlen)
        ed = int(st+evtlen)
        evtdat = hdffile['iqdata_raw']['keyint_192']['keystr_stream_phase'][st:ed]
        avgevt = avgevt + evtdat
    
    
    avgevt = avgevt - mean(avgevt)
    figure(1)    
    clf()
    plot(avgevt)      
      
    
    F1 = numpy.fft.fft(avgevt[0:evtlen-1],1024)[:512]
    F2 = numpy.fft.fft(avgevt[1:evtlen-1],1024)[:512]
    
    F1mag = abs(F1)
    figure(2)
    clf()
    plot(F1mag)
    
    maxindex = numpy.where(F1mag==F1mag.max())
    print maxindex
    #hdffile.keys()
    
    ph1 = numpy.angle(F1[maxindex])[0]
    ph2 = numpy.angle(F2[maxindex])[0]
    radfreq = ph2 - ph1
    

    wavelen = 2.0*pi / radfreq

    print 'FRD Wavelenth = %f'%wavelen


    numwaves=[1.0,2.0,3.0,4.0]
    
    
    # take 1 osc, 2 osc or some num of osc in numwaves array
    
    noise_meas=[]
    
    for nw in numwaves:
    
        intglen = round(wavelen*nw)
        
        print 'numwaves = %f, integ len = %f'%(nw,intglen)
        
        #tiem offset from start of the captured ramp record.
        for intgoffs in range(25):
            numintgevts = 10000;
            intgdatlen = intglen *   numintgevts 
            frddat = numpy.array([0.0]*int(numintgevts))
        
            #print 'datoffset = %f'%intgoffs
            
            #step thru captured data, getting each ramp, and doing frd
            for evtnum in range(numintgevts):
    
                st = int(glitchoffts + intgoffs + evtnum * evtlen)
                ed = int(st+intglen)
                evtdat = hdffile['iqdata_raw']['keyint_192']['keystr_stream_phase'][st:ed]
                
                evtdat = evtdat - mean(evtdat)
                Ffrd = numpy.fft.fft(evtdat)
                if (rand() <0.001):
                    figure(3)
                    clf()
                    subplot(2,1,1)
                    plot(evtdat)
                    subplot(2,1,2)
                    plot(abs(Ffrd))
                    draw()
                
                frd = numpy.angle(Ffrd[nw])
                frddat[evtnum]=frd
            
            #take noise of frd data
            
            figure(4)
            clf()
            plot(frddat)
            draw()
            
            totnoise = numpy.std(frddat)
            noise_meas.append( (nw, intgoffs,totnoise )  )
  
  
    figure(5)
    clf()
    nplot = []
    for nm in noise_meas:
        nplot.append(nm[2])
    
    plot(nplot)
    yscale('log')
    return(noise_meas)
            
            
            
               

def plfrd(chan_=192):
    ev = fa.iqdata_raw
    tslist = lsUniqueTimeStamps(ev,chan_)
    
    vsweep = []
    volts = []
    stindex = 0
    sorted_ts = sort(tslist)[::-1]
    for ts in sorted_ts:    
        [rawfrd,stindex] = getEventsByTimeStamp2(ev,ts,stindex,chan_)
        rawfrdx=pi*rawfrd[20]
        #rawfrdm = mean(rawfrd)
        vsweep.append(rawfrdx)
        volts.append(ts)
        print ts
        
    seg_phase = removePhaseJumps(vsweep)
    
    figure(11)
    
    plot(volts,seg_phase,'x')
    plot(volts,seg_phase)
    figure(12)
   
    plot(volts,vsweep,'x')
    plot(volts,vsweep)
 
    return( (volts,vsweep,seg_phase) )
    
    
def plfrd3(chan_=192):
    ev = fa.iqdata_raw
    
    rawphase = pi * ev[chan_]['flux_ramp_phase']
    print 'unwrapping'
    corphase = removePhaseJumps(rawphase)
    print 'unwrapped'
    vlist = ev[chan_]['timestamp']/1000.0
    
    
    figure(12)
    plot(vlist,corphase)


def plfrd2(chan_=192):
    ev = fa.iqdata_raw
    
    rawphase = pi * ev[chan_]['flux_ramp_phase']
    print 'unwrapping'
    corphase = removePhaseJumps(rawphase)
    print 'unwrapped'
    vlist = ev[chan_]['timestamp']/1000.0
    
    
    lastv = -1.0
    #skip 1st 500 samples on new voltage
    nskip = 500
    sumph = 0.0
    sumvnadd = 0.0
    
    stskip = 0
    stadd = 1
    
    state = 0
    skipcount=0
    k = 0
    
    seg_phase = []
    volts = []
    
    while k<len(corphase):
   
        ph = corphase[k]
        v = vlist[k]   
        
        if k%100==0:
            print k
            
        if state == stskip:
            sumph = 0.0
            sumvnadd = 0.0
            if v!=lastv:
                skipcount = 0
                state = stskip
            else:
                skipcount = skipcount +1
                if skipcount>nskip:
                    state = stadd
                else:
                    state = stskip
                    
        elif state== stadd:
            if v==lastv:
                sumvnadd =sumvnadd+1.0
                sumph=ph+sumph
            else:              
                skipcount = 0
                state = stskip
                print lastv
                sumphf = sumph / sumvnadd
                volts.append(lastv)
                seg_phase.append(sumphf)
                sumph = 0.0
                sumvnadd = 0.0
                
    
        lastv = v
        k = k+1
    
    seg_phse = numpy.array(seg_phase)
    volts = numpy.array(volts)
     
    figure(11)
    
    plot(volts,seg_phase)
  
 
    return( [volts,seg_phase])
    
    

def anal_vsweep_fast(fname=None):


    if fname!=None:
        hdf=hdfSerdes()
        hdf.open(fname,'r')
        events = hdf.read()
        hdf.close()
    else:
        events = fa.iqdata_raw

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
    elements = events[chan]['timestamp']
    return list(OrderedDict.fromkeys(elements).keys())
    
    
    

def getEventsByTimeStamp2(events,tsfind,startindex=0,chan=192):


    fluxphase=[]
    
    
    foundindex = 0
    for k in range(startindex, len(events[chan]['timestamp'])):
        ts = events[chan]['timestamp'][k]
        if ts==tsfind:
            #assume all event_len are all the same. 
            evlen = events[chan]['event_len'][k]
            frd = events[chan]['flux_ramp_phase'][k]
            
            foundindex=k
            fluxphase.append(frd)
 
    return( [numpy.array(fluxphase),foundindex])






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

    phase_sig = phase_sig[::-1]
    newphase = [0] * len(phase_sig)
    
    newphase[0] = phase_sig[0]
    
    for k in range(1,len(phase_sig)):
        newphase[k] = phase_sig[k]
        dphase = newphase[k] - newphase[k-1]
  
            
        while dphase<(-pi):
            newphase[k] = newphase[k]+2*pi
            dphase = newphase[k] - newphase[k-1]
  
  
        while dphase>pi:
            newphase[k] = newphase[k]-2*pi
            dphase = newphase[k] - newphase[k-1]
     
    newphase = newphase[::-1]
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
            res.xmission_line_delay,
            res.carrierfreq)
            
        reslist.append(newres)

    return(reslist)
