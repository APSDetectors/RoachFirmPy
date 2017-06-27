import itertools
from collections import OrderedDict

'''

execfile('debug.py')

execfile('sim928.py')


plotAllRes2File('/home/oxygen31/TMADDEN/ROACH2/datafiles/jul7_2016/res1-5bblb.pdf')

/home/oxygen31/TMADDEN/ROACH2/datafiles/jul5_2016

calcBBLOFromRFFreqs( arange(3000e6, 3200e6,20e6))

vlist = arange(10,0,-0.02)


vlist = arange(0,10,0.02)


rffreq = 5096e6
rffreq = 5111e6
rffreq = 5199e6


hdf=hdfSerdes()
sim=sim928()
sim.open()
sim.getId()


fname = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul19/vsweep_5199_0u10000b20_1.h5'
vs = voltSweepFast(vlist,rffreq,fname)

lsUniqueTimeStamps(vs)

aaa = getEventsByTimeStamp(vs,7700,isplot=True,fignum=8)

sim.close()

hdf=hdfSerdes()
hdf.open('../../datafiles/jul14/vsweep_4.h5','w')
hdf.write(vs,'vsweep')
hdf.close()

figure(1)
clf()
st =82 * 95
ed = 95+st

plot(vs[640][192]['stream_phase'][st:ed])

'''

from matplotlib.backends.backend_pdf import PdfPages


'''

execfile('debug.py')

for m in measure.measspecs.mlist_trans: 
    m.reslist[0].plotFreq(isclf=0,is_pl_trot=False)

res = MKID_list[0].reslist[0]


execfile('debug.py')


'''


def IVCurveAverageRawData(fname):

    hdf = h5py.File(fname,'r+')
    for chan in hdf['iqdata_raw'].keys():

        alldata= {}
        seg_phase=[]
        vdata=[]


        
        #num events from file
        numevts = len(hdf['iqdata_raw'][chan]['keystr_timestamp'])
        #per voltage... 
        vlist_ = hdf['iqdata_raw'][chan]['keystr_timestamp'][::100]
        
        #get ACTUAL unique voltages in the file. 
        vlist = list(OrderedDict.fromkeys(vlist_).keys())
        #actual num of voltages.
        nvolts = len(vlist)
        
        #approx len of data pervioltate, 
        datpvolts=numevts/nvolts
        #when searching large hdf datasets, we decimate data by this to be sure we can find evetns with given voltage.
        searchsize = datpvolts/2
       
        

        start_volt_index=[0] * nvolts
        last_index = 0
        k=1
        for v in vlist[1:]:
            print v
            segment = hdf['iqdata_raw'][chan]['keystr_timestamp'][last_index: (last_index + datpvolts + searchsize)]
            next_index = where(segment==v)[0][0]
            start_volt_index[k] = last_index + next_index
            last_index = start_volt_index[k]
            k = k+1

        
        ivcurve = [0.0]*nvolts
        start_volt_index.append(numevts)
        k=0
        for v in vlist:
            st = start_volt_index[k]
            ed = start_volt_index[k+1]
            segment_ = hdf['iqdata_raw'][chan]['keystr_flux_ramp_phase_unwrap'][st:ed]
            segment = segment_[cal_ivstream_voltagestep_delay:]
            ivcurve[k] = mean(segment)
            k=k+1

        hdf['iqdata_raw'][chan].create_dataset('vlist',data=vlist)
        hdf['iqdata_raw'][chan].create_dataset('ivcurve',data=ivcurve)

    hdf.flush()
    hdf.close()

            
def sweepAtten():
    for aa in numpy.arange(0.0,31.0,0.5):
        fa.if_board.at.attenU6 = int(0.0-aa)
        fa.if_board.at.attenU7 = 0
        fa.if_board.progAtten(fa.if_board.at)
        #fa.if_board.progRFSwitches(fa.if_board.rf)
        #fa.if_board.progIfBoard()

        print 'Atten u6 = %f'%aa
        time.sleep(.5)
  

def setAtten(aa):
        fa.if_board.at.attenU6 = aa
        fa.if_board.at.attenU7 = 0
        fa.if_board.progAtten(fa.if_board.at)
        #fa.if_board.progRFSwitches(fa.if_board.rf)
        #fa.if_board.progIfBoard()

  

def voltSweepT(
    vlist=None,
    rffreq=[5095.4e6],
    fnames=None,
    BB=None,
    LO = None,
    amp=None,
    lock = None,
    callback=None,
    issync = 0,
    evtsize2=100,
    syncdelay=0):

    fa.is_running=True

    if vlist==None:
        vlist = numpy.arange(10.0,0.0,-0.1)

    ev=0
    #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.

    fa.an.setOnOff(1)  
    #get sync from ext ramp gen.
    fa.rampgen.setSyncSource(0)
    #trigger on ramp gen pulses
    fa.rampgen.setIsSync(issync)
    #meas sync freq, and set up event size (or flux ramp event size) number of samples.
    fa.rampgen.setChannelizerFifoSync()
    fa.chanzer.setReadFifoSize(evtsize2)


    fa.phaser1.zeroPhaseIncs()
    fa.phaser2.zeroPhaseIncs()
    fa.phaser3.zeroPhaseIncs()
    fa.phaser4.zeroPhaseIncs()

    fa.chanzer.setSyncDelay(syncdelay)

    time.sleep(0.5)

    sim.setOutOn(1)
    #fa.capture.setStream2Disk(1, fnames)

    if BB==None:
        [LO,BB]=fa.calcBBLOFromRFFreqs(rffreq)

    fa.setCarrier(LO)
    if amp==None:
        amp = fa.calcAmp(len(rffreq))



    fa.sourceCapture(
        BB,
        amp,        
        whichbins='Freqs',
        is_trig=False,
        stream_fname = fnames)


    volts = vlist[0]
    sim.setVolts(volts)
    roach.write_int('sw_timestamp',int(1000*volts))
    roach.write_int('sw_timestamp2',int(1000*volts))
    fa.rfft.trigFFT()
    #wait for the capture to start
    time.sleep(0.01)

    if lock!=None: lock.release()

    for volts in vlist:
        fa.temp_volts = volts
        sim.setVolts(volts)
        #embed voltage into roach data stream so we associate the voltage with the data.
        print volts
        
        if lock!=None: lock.acquire()            
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))
        if lock!=None: lock.release()
        #fa.chanzer.flushFifos()

        time.sleep(0.3)
        if callback!=None:
            callback()

        if not fa.is_running:
            break


    if lock!=None: lock.acquire()     
    fa.stopCapture()
    ev =fa.getIQ(dsname = fnames,issave = False,is_decimate = True,max_read_size = 10000)
    sim.setOutOn(0)
    fa.an.setOnOff(0)    

    os.rename(fnames+'_B.h5',fnames)

    for ch in ev.keys():        
        #LO = fa.carrierfreq - fa.rfft.bin_to_srcfreq[ ev[ch]['bin'][0] ]
        ev[ch]['rffreq'] = LO



    if fnames!=None:
       hdf=hdfSerdes()
       hdf.open(fnames,'a')

       dat = fa.getUsefulMetaData()
       hdf.write(dat,'metadata')
       hdf.close()


    return(ev)







def stsd(fname):

    dat = {
    'measspecs.rffreqs': measure.measspecs.rffreqs,
    'measspecs.mlist_raw1': measure.measspecs.mlist_raw1 ,
    'measspecs.andata_1': measure.measspecs.andata_1 ,      
    'measure.iqcenterdata': measure.iqcenterdata ,
    'measspecs.mlist_trans': measure.measspecs.mlist_trans ,
    'measspecs.andata_trans': measure.measspecs.andata_trans }


    hdf= hdfSerdes()
    hdf.open(fname,'w')
    hdf.write(dat,'sweepProgTranslatorData')
    hdf.close()









def reconnRoach():
    global roach
    
    roach=katcpNc()
    roach.startNc()

    fa.capture=dataCapture()
    fa.an = anritsu(fa.is_anritsu_lo)
    

def plotFreq(res,isclf=1,isnoise=1,fnum=0,is_pl_trot = True):


   
    IQ=res.iqdata
    freqs=res.freqs

    IQp=res.RectToPolar(IQ)

    figure(1+fnum)
    if isclf:clf()



    dbref = -40

    subplot(4,2,1)
    title("Delay=%dns"%(floor(res.delay*1e9)))
    dat=20*log(IQp[0]) - dbref
    plot(freqs,dat)

    toprange = 10+10.0*ceil(max(dat)/10.0)
    botrange = -10+10.0*ceil(min(dat)/10.0)
    ylim(botrange,toprange)
    grid(True)

    ylabel('20Log10 Mag.')
    subplot(4,2,3)
    plot(freqs,res.removeTwoPi(IQp[1]))
    ylabel('Phase')
    subplot(4,2,5)
    plot(freqs,IQ[0])
    ylabel('I')
    subplot(4,2,7)
    plot(freqs,IQ[1])
    ylabel('Q')
    draw()

    figure(1+fnum)
#        if isclf:clf()
    subplot(1,2,2)
    plot(IQ[0],IQ[1])




    for iqpr in res.iqnoise:

        try:
            iqp = [ iqpr[192]['stream_mag'] , iqpr[192]['stream_phase'] ]
            iq = res.PolarToRect( iqp )
           

            figure(1+fnum)
            subplot(1,2,2)
            plot(iq[0][1000:2000],iq[1][1000:2000],'.')
           
          
          
        except:
            print "No raw nosie data"




def hackResNoisePhase(res,addph):

 

    for noise_trace in res.iqnoise:

        #calc phase delay
        if True:

            #add delay to phase term of noise
            noise_trace[192]['stream_phase'] = \
                noise_trace[192]['stream_phase'] + addph
           
        else:
            print "problem w/ noise traice/ no 192" 





def loadTransSwNoise(fnameS,fnameN):

    hdf=hdfSerdes()
    
    hdf.open(fnameS,'r')
    sw = hdf.read()
    hdf.close()
    
    hdf.open(fnameN,'r')
    nz = hdf.read()
    hdf.close()
    

    fa.iqdata_raw = nz['iqdata_raw']
    
    measure.measspecs.mlist_raw0=sw['measspecs.mlist_raw0']
    measure.measspecs.mlist_raw1=sw['measspecs.mlist_raw1']
    measure.measspecs.mlist_trans=sw['measspecs.mlist_trans']


def saveTranslatorSweepData(fname):

    dat = {
    'measure.measspecs.rffreqsrough':measure.measspecs.rffreqsrough,
    'measure.measspecs.rffreqs': measure.measspecs.rffreqs,
    'measure.measspecs.mlist_raw0': measure.measspecs.mlist_raw0 ,
    'measure.measspecs.andata_0': measure.measspecs.andata_0 ,
    'measure.measspecs.mlist_raw1': measure.measspecs.mlist_raw1 ,
    'measure.measspecs.andata_1': measure.measspecs.andata_1 ,      
    'measure.iqcenterdata': measure.iqcenterdata ,
    'measure.measspecs.mlist_trans': measure.measspecs.mlist_trans ,
    'measure.measspecs.andata_trans': measure.measspecs.andata_trans }


    hdf= hdfSerdes()
    hdf.open(fname,'w')
    hdf.write(dat,'sweepProgTranslatorData')
    hdf.close()


def toMatlabText(data):
    txt = 'data = [\n'
    for d in data:
        txt = txt + '%i,\n'%d
    txt = txt + '0]\n'
    return(txt)



def reorderChansTrans():
    
    
    xy = []
    for k in fa.chanzer.chan_to_translate.keys():
        xy.append(fa.chanzer.chan_to_translate[k])
    
  
    random.shuffle(xy)
    
    i=0
    for k in fa.chanzer.chan_to_translate.keys():
        fa.chanzer.chan_to_translate[k] =xy[i]
        i=i+1
        
    
    


def readTransTable(chan=192):
    
    i =roach.read_int('FRD1_trIQ_tr',chan-128)
    ilo = i&0xffff
    ihi = (i&0xffff0000) >> 16
    flo = fa.dataread.convToFloat([ilo],(1,16,14))
    fhi = fa.dataread.convToFloat([ihi],(1,16,14))
    return(  (i, ihi, ilo, fhi, flo)   )

def testSweepers():
    pass
    
'''
fa.chanzer.setFluxRampDemod(
            is_demod=0,
            is_incl_raw_trans=2, 
            evt_len=100,
            num_cycles=2.0)

fa.chanzer.setFluxRampDemod(
            is_demod=0,
            is_incl_raw_trans=1, 
            evt_len=100,
            num_cycles=2.0)

fa.sweep(
    span_Hz=4e6, 
    center_Hz=-1, 
    pts=256,
    amplitude = 30000/4,
    defaultFRD=0)

for k in fa.iqdata_raw.keys():
    print k
    figure(11)
    subplot(2,1,1)
    plot(fa.iqdata_raw[k]['stream_mag'][:1000])
    subplot(2,1,2)
    plot(fa.iqdata_raw[k]['stream_phase'][:1000])
    figure(12)
    iq=fa.dataread.PolarToRect([fa.iqdata_raw[k]['stream_mag'][:256], fa.iqdata_raw[k]['stream_phase'][:256]  ])
    plot(iq[0],iq[1])
    
    
'''

def progRoachFromResonatorList():
    measure.getResonatorIQCenters()
    rffreqs = []
    for item in measure.iqcenterdata:
        rffreqs.append(item['rffreq'])

    [LO,bbfreqs] = fa.calcCarrierBBFreqs(rffreqs)
    fa.setCarrier(LO)
    amp = 30000.0 / len(rffreqs)

    fa.sourceCapture(bbfreqs,amp,is_trig = False)
    fa.stopCapture()

    for item in measure.iqcenterdata:
        item['bbfreq'] = LO - item['rffreq']
        item['bin'] = fa.rfft.getBinFromFreq(item['bbfreq'])
        item['LO'] = LO
        item['chan'] = fa.rfft.bin_to_chan[item['bin']]

        fa.chanzer.setFlxDmodTranTable(chan=item['chan'],xc=item['xc'],yc=item['yc'])

    fa.chanzer.progTranslator()
    return( {'bbfreqs':bbfreqs,'amp':amp,'LO':LO})


def plotAllRes2File(fname):
    pp = PdfPages(fname)
    for m in MKID_list:
        print '%dMHz Sweep/Noise'%(m.getFc()/1e6)
        for r in m.reslist:
            r.plotFreq()

            if True:
              figure(1)
              suptitle('%dMHz Sweep/Noise U7=%d, U28=%d, U6=%d'%(
                  r.getFc()/1e6, r.atten_U7, r.atten_U28, r.atten_U6))        
              f=gcf()
              f.savefig(pp,format='pdf')

            if True:
              figure(20)
              suptitle('%dMHz Noise Mag/Phase U7=%d, U28=%d, U6=%d'%(
                  r.getFc()/1e6, r.atten_U7, r.atten_U28, r.atten_U6))        
              f=gcf()
              f.savefig(pp,format='pdf')

            if True:
              figure(21)
              suptitle('%dMHz Noise Mag/Phase U7=%d, U28=%d, U6=%d'%(
                  r.getFc()/1e6, r.atten_U7, r.atten_U28, r.atten_U6))        

              f=gcf()
              f.savefig(pp,format='pdf')


            if True:
              figure(13)
              suptitle('%dMHz Sweep Polar U7=%d, U28=%d, U6=%d'%(
                  r.getFc()/1e6, r.atten_U7, r.atten_U28, r.atten_U6))       

              f=gcf()
              f.savefig(pp,format='pdf')

            if False:
              figure(8)
              suptitle('%dMHz IQ Velocity'%(r.getFc()/1e6))
              f=gcf()
              f.savefig(pp,format='pdf')

    pp.close()





def calcBBLOFromRFFreqs(rffreqs):

    frange = max(rffreqs) - min(rffreqs)
    if frange>230e6:
        print "cannot source this freq list- to wide BW"
        return

    LO=max(rffreqs)+10e6
    bbfreqs = LO - rffreqs

    bbfreqs = numpy.sort(bbfreqs)
    return( (LO, bbfreqs) )




def dovsweeps():


    vlist = arange(0,15.0,1)
    rffreq = 5096e6

    fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul14/vsweep_10_1b.h5'
    vs = voltSweep(vlist,rffreq,fn)



    vlist = arange(15,0.0,-1)
    rffreq = 5096e6

    fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul14/vsweep_10_2.h5'
    vs = voltSweep(vlist,rffreq,fn)

    vlist = arange(5,15,0.1)
    rffreq = 5096e6

    fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul14/vsweep_10_3.h5'
    vs = voltSweep(vlist,rffreq,fn)


    vlist = arange(5,15,0.02)
    rffreq = 5096e6

    fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul14/vsweep_10_4.h5'
    vs = voltSweep(vlist,rffreq,fn)


    vlist = arange(15,5,-0.1)
    rffreq = 5096e6

    fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul14/vsweep_10_5.h5'
    vs = voltSweep(vlist,rffreq,fn)



    vlist = arange(15,5,-0.02)
    rffreq = 5096e6

    fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/jul14/vsweep_10_6.h5'
    vs = voltSweep(vlist,rffreq,fn)


def voltSweep(vlist,rffreq,fnames):

   
    #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.
    
    fa.setCarrier(rffreq+10e6)
    fa.an.setOnOff(1)
    
    #get sync from ext ramp gen.
    fa.rampgen.setSyncSource(0)
    #trigger on ramp gen pulses
    fa.rampgen.setIsSync(1)
    #meas sync freq, and set up event size (or flux ramp event size) number of samples.
    fa.rampgen.setChannelizerFifoSync()
   
    fa.phaser1.zeroPhaseIncs()
    fa.phaser2.zeroPhaseIncs()
    fa.phaser3.zeroPhaseIncs()
    fa.phaser4.zeroPhaseIncs()
   
    time.sleep(0.5)
   
    vsweepdata = {}
    sim.setOutOn(1)
    
    for volts in vlist:
        print volts
        #embed voltage into roach data stream so we associate the voltage with the data.
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))
        
        sim.setVolts(volts)
        #let volts settle
        time.sleep(0.5)
        fa.sourceCapture(
            [10e6],
            30000,
            numffts = 20000,
            whichbins='Freqs')
        
        
      
        #wait a few ms for ffts to finish
        time.sleep(1.0)
        fa.stopCapture()


        time.sleep(1.0)
        ev =fa.getIQ()
        vsweepdata[ int(1000*volts) ] = ev

    sim.setOutOn(0)
    fa.an.setOnOff(0)    
    
    hdf.open(fnames,'w')
    hdf.write(vsweepdata,'vsweep')
    hdf.close()

    
    return(vsweepdata)
    
    


def voltSweepFast(vlist,rffreq,fnames):

    ev=0
    #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.
    
    
    fa.an.setOnOff(1)
    
    #get sync from ext ramp gen.
    fa.rampgen.setSyncSource(0)
    #trigger on ramp gen pulses
    fa.rampgen.setIsSync(1)
    #meas sync freq, and set up event size (or flux ramp event size) number of samples.
    fa.rampgen.setChannelizerFifoSync()
   
    fa.phaser1.zeroPhaseIncs()
    fa.phaser2.zeroPhaseIncs()
   
    fa.phaser3.zeroPhaseIncs()
    fa.phaser4.zeroPhaseIncs()
   
    fa.chanzer.setSyncDelay(128*55)
   
    time.sleep(0.5)
   
    
   
    if True:
        sim.setOutOn(1)
        #fa.capture.setStream2Disk(1, fnames)
        
        [LO,BB]=fa.calcBBLOFromRFFreqs(rffreq)
        fa.setCarrier(LO)
        amp = 32000.0/len(rffreq)
        
        fa.sourceCapture(
            BB,
            amp,
            whichbins='Freqs')

    volts = vlist[0]
    sim.setVolts(volts)
    roach.write_int('sw_timestamp',int(1000*volts))
    roach.write_int('sw_timestamp2',int(1000*volts))
    #wait for the capture to start
    time.sleep(0.01)
    
    for volts in vlist:
        print volts
      
        
        sim.setVolts(volts)

        #embed voltage into roach data stream so we associate the voltage with the data.
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))

      
        
      

        time.sleep(0.02)

    
    
        #wait a few ms for ffts to finish
    
    if True:
        fa.stopCapture()
        ev =fa.getIQ()
   

    
    sim.setOutOn(0)
    fa.an.setOnOff(0)    
    
    
    for ch in ev.keys():
        LO = fa.carrierfreq - fa.rfft.bin_to_srcfreq[ ev[ch]['bin'][0] ]
        ev[ch]['rffreq'] = LO
    
  
    
    if True:
       hdf.open(fnames,'w')
       hdf.write(ev,'sweepevents')
     
       
       hdf.close()

    
    return(ev)
    



def voltSweepFast(vlist,rffreq,fnames):

    ev=0
    #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.
    
    
    fa.an.setOnOff(1)
    
    #get sync from ext ramp gen.
    fa.rampgen.setSyncSource(0)
    #trigger on ramp gen pulses
    fa.rampgen.setIsSync(1)
    #meas sync freq, and set up event size (or flux ramp event size) number of samples.
    fa.rampgen.setChannelizerFifoSync()
   
    fa.phaser1.zeroPhaseIncs()
    fa.phaser2.zeroPhaseIncs()
    fa.phaser3.zeroPhaseIncs()
    fa.phaser4.zeroPhaseIncs()
   
    fa.chanzer.setSyncDelay(128*55)
   
    time.sleep(0.5)
   
    
   
    if True:
        sim.setOutOn(1)
        #fa.capture.setStream2Disk(1, fnames)
        
        [LO,BB]=fa.calcBBLOFromRFFreqs(rffreq)
        fa.setCarrier(LO)
        amp = 32000.0/len(rffreq)
        
        fa.sourceCapture(
            BB,
            amp,
            whichbins='Freqs')

    volts = vlist[0]
    sim.setVolts(volts)
    roach.write_int('sw_timestamp',int(1000*volts))
    roach.write_int('sw_timestamp2',int(1000*volts))
    #wait for the capture to start
    time.sleep(0.01)
    
    for volts in vlist:
        print volts
      
        
        sim.setVolts(volts)

        #embed voltage into roach data stream so we associate the voltage with the data.
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))

      
        
      

        time.sleep(0.02)

    
    
        #wait a few ms for ffts to finish
    
    if True:
        fa.stopCapture()
        ev =fa.getIQ()
   

    print vlist[0], 'to', vlist[-1]     #added by Daikang 2016-07-29
    sim.setOutOn(0)
    fa.an.setOnOff(0)    
    
    
    for ch in ev.keys():
        LO = fa.carrierfreq - fa.rfft.bin_to_srcfreq[ ev[ch]['bin'][0] ]
        ev[ch]['rffreq'] = LO
    
  
    
    if True:
       hdf.open(fnames,'w')
       hdf.write(ev,'sweepevents')
     
       
       hdf.close()

    
    return(ev)
    
    

'''

execfile('debug.py')


ev = voltSweepFast2(vlist=5555,rffreq=[5100e6],fnames='testvsw.h5')
print len(ev[192]['timestamp'])



'''

def voltSweepFast2(vlist=5555,rffreq=[5100e6],fnames=None):

    if vlist==5555:
        vlist = numpy.arange(10.0,0.0,-0.1)

    ev=0
    #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.

    fa.an.setOnOff(1)  
    #get sync from ext ramp gen.
    fa.rampgen.setSyncSource(0)
    #trigger on ramp gen pulses
    fa.rampgen.setIsSync(1)
    #meas sync freq, and set up event size (or flux ramp event size) number of samples.
    fa.rampgen.setChannelizerFifoSync()

    fa.phaser1.zeroPhaseIncs()
    fa.phaser2.zeroPhaseIncs()
    fa.phaser3.zeroPhaseIncs()
    fa.phaser4.zeroPhaseIncs()

    fa.chanzer.setSyncDelay(128*55)

    time.sleep(0.5)

    #!!sim.setOutOn(1)
    #fa.capture.setStream2Disk(1, fnames)

    [LO,BB]=fa.calcBBLOFromRFFreqs(rffreq)
    fa.setCarrier(LO)
    amp = 32000.0/len(rffreq)

    fa.sourceCapture(
        BB,
        amp,
        numffts=200000,
        whichbins='Freqs',
        is_trig=False)


    volts = vlist[0]
    #!!sim.setVolts(volts)
    roach.write_int('sw_timestamp',int(1000*volts))
    roach.write_int('sw_timestamp2',int(1000*volts))
    #wait for the capture to start
    time.sleep(0.01)
    
    for volts in vlist:
        print volts
        #!!sim.setVolts(volts)
        #embed voltage into roach data stream so we associate the voltage with the data.
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))
        
        #fa.chanzer.flushFifos()
        fa.rfft.trigFFT()
        time.sleep(0.5)

    
   
    
    fa.stopCapture()
    ev =fa.getIQ()
   #!!sim.setOutOn(0)
    fa.an.setOnOff(0)    
    
    
    for ch in ev.keys():        
        #LO = fa.carrierfreq - fa.rfft.bin_to_srcfreq[ ev[ch]['bin'][0] ]
        ev[ch]['rffreq'] = LO
    
 

    if fnames!=None:
       hdf.open(fnames,'w')
       hdf.write(ev,'sweepevents')
       hdf.close()

    
    return(ev)
    
    



def voltSweepTEST(vlist_=None,rffreq=[5100e6],numsamples = 2000,fnames=None):

    if vlist_==None:
        vlist_ = numpy.arange(10.0,0.0,-0.1)

    ev=0
    #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.

    fa.an.setOnOff(1)  
    #get sync from ext ramp gen.
    fa.rampgen.setSyncSource(0)
    #trigger on ramp gen pulses
    fa.rampgen.setIsSync(1)
    #meas sync freq, and set up event size (or flux ramp event size) number of samples.
    fa.rampgen.setChannelizerFifoSync()

    fa.phaser1.zeroPhaseIncs()
    fa.phaser2.zeroPhaseIncs()
    fa.phaser3.zeroPhaseIncs()
    fa.phaser4.zeroPhaseIncs()

    fa.chanzer.setSyncDelay(128*55)

    time.sleep(0.5)

    #!!sim.setOutOn(1)
    #fa.capture.setStream2Disk(1, fnames)

    [LO,BB]=fa.calcBBLOFromRFFreqs(rffreq)
    fa.setCarrier(LO)
    amp = 32000.0/len(rffreq)

    fa.sourceCapture(
        BB,
        amp,
        numffts=numsamples*100,
        whichbins='Freqs',
        is_trig=False)


    volts = vlist_[0]
    #!!sim.setVolts(volts)
    roach.write_int('sw_timestamp',int(1000*volts))
    roach.write_int('sw_timestamp2',int(1000*volts))
    #wait for the capture to start
    time.sleep(0.01)

    for volts in vlist_:
        print volts
        #!!sim.setVolts(volts)
        #embed voltage into roach data stream so we associate the voltage with the data.
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))

        #fa.chanzer.flushFifos()
        fa.rfft.trigFFT()
        time.sleep(0.5)




    fa.stopCapture()
    ev =fa.getIQ()
   #!!sim.setOutOn(0)
    fa.an.setOnOff(0)    


    for ch in ev.keys():        
        #LO = fa.carrierfreq - fa.rfft.bin_to_srcfreq[ ev[ch]['bin'][0] ]
        ev[ch]['rffreq'] = LO



    if fnames!=None:
       hdf=hdfSerdes()
       hdf.open(fnames,'w')
       hdf.write(ev,'sweepevents')
       hdf.close()


    return(ev)









def voltSweep3(vlist=None,rffreq=[5100e6],numsamples = 2000,fnames=None):

    if vlist==None:
        vlist = numpy.arange(10.0,0.0,-0.1)

    ev=0
    #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.

    fa.an.setOnOff(1)  
    #get sync from ext ramp gen.
    fa.rampgen.setSyncSource(0)
    #trigger on ramp gen pulses
    fa.rampgen.setIsSync(1)
    #meas sync freq, and set up event size (or flux ramp event size) number of samples.
    fa.rampgen.setChannelizerFifoSync()

    fa.phaser1.zeroPhaseIncs()
    fa.phaser2.zeroPhaseIncs()
    fa.phaser3.zeroPhaseIncs()
    fa.phaser4.zeroPhaseIncs()

    fa.chanzer.setSyncDelay(128*55)

    time.sleep(0.5)

    sim.setOutOn(1)
    #fa.capture.setStream2Disk(1, fnames)

    [LO,BB]=fa.calcBBLOFromRFFreqs(rffreq)
    fa.setCarrier(LO)
    amp = 32000.0/len(rffreq)

    fa.sourceCapture(
        BB,
        amp,        
        whichbins='Freqs',
        is_trig=False)


    volts = vlist[0]
    sim.setVolts(volts)
    roach.write_int('sw_timestamp',int(1000*volts))
    roach.write_int('sw_timestamp2',int(1000*volts))
    fa.rfft.trigFFT()
    #wait for the capture to start
    time.sleep(0.01)

    for volts in vlist:
        print volts
        sim.setVolts(volts)
        #embed voltage into roach data stream so we associate the voltage with the data.
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))

        #fa.chanzer.flushFifos()

        time.sleep(0.3)




    fa.stopCapture()
    ev =fa.getIQ()
    sim.setOutOn(0)
    fa.an.setOnOff(0)    


    for ch in ev.keys():        
        #LO = fa.carrierfreq - fa.rfft.bin_to_srcfreq[ ev[ch]['bin'][0] ]
        ev[ch]['rffreq'] = LO



    if fnames!=None:
       hdf=hdfSerdes()
       hdf.open(fnames,'w')
       hdf.write(ev,'sweepevents')
       hdf.close()


    return(ev)




    
    


'''
hdf = hdfSerdes()
fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/badphase.h5'
hdf.open(fn,'r')
qq=hdf.read()
iq = qq['iq']



'''
