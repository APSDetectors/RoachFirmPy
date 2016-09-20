
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
    
    


'''
hdf = hdfSerdes()
fn = '/home/oxygen31/TMADDEN/ROACH2/datafiles/badphase.h5'
hdf.open(fn,'r')
qq=hdf.read()
iq = qq['iq']



'''
