"""

execfile('analysis.py')

phsine = calcFluxRampPhase(0,0,2)

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

"""



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
