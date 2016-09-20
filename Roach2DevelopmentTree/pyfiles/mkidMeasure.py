
"""
execfile('mkidMeasure.py')

makeGlobalObjs()


execfile('mkidMeasure.py')

measure = mkidMeasure(na,fit)



mkid = measure.newMkid(5262e6)


m=measSpecs()

measure.powersweepSetup(m)

measure.powerSweep()


"""


execfile('katcpNc.py')

execfile('fftAnalyzerR2.py')

execfile('fitters.py')

execfile('resonator.py')

global na
global fit
global roach
global measure

def sweepCallback():
    pass
    
    
def makeGlobalObjs():

    global na
    global fa
    global fit
    global roach
    global measure
    

    roach=katcpNc()
    roach.startNc()

    na = fftAnalyzerR2(roach)
    fa = na
    fit = fitters()
    
    measure = mkidMeasure(na,fit)


class measSpecs:
    def __init__(self):

        
        
        self.attInStart=5
        self.attStart=5
        self.attEnd=10
        self.numSweeps=1   
        self.attIncr= 2
        self.resonator_span = 2e6
        self.num_res_freq_points = 128
        
         #copy and clear the markerlist so it plots correctly
        self.atU6=5
        self.mlist=  [MKID(fc=3e9) , MKID(fc=3.5e9), MKID(fc=4e9) ]
        
        #take one noise trace per resonator. or we can take several, spaced narrowly around the res center freq.
        #best to have this an odd number, so the middle one is the res center. we ise the max phase val for center freq.
        self.num_noise_traces = 1
        # if we take several res, we will take them centered around the res center freq, and this Hz apart.
        self.noise_trace_spacing_Hz = 20000.0
        
        #time in sec to take nosie data
        self.noise_time_sec = 2.0
        
        self.noise_numffts=250000
        
        
        self.vlist = arange(10,0,-0.02)

    
class mkidMeasure:

    def __init__(self,fftanal_, fit_):
        
        self.fa=fftanal_
        self.na = self.fa
        
        self.fit = fit_
        self.is_setTROT=True
   
        self.is_use_multiprocess=False
    
        self.sweepcount=0
    
        self.measspecs=measSpecs()
        
        self.mkid_number=0
        self.device_name="fake"
        
        
        self.start_carrier = 0;
        self.end_carrier = 0;
        self.inc_carrier = 0;
        self.carrier_freqs =numpy.array([])
        
        
        
        self.sweep_samples_per_freq=64
        self.xmission_line_delay = 30e-9
        self.freq_to_linedel_phase = dict()
        self.chan_to_linedel_phase = dict()
        
        self.is_apply_delay=True
  
    def voltSweepRes(self):
        self.thread_running=1
        mlist=sorted(self.measspecs.mlist,key=MKID.getFc)
        
        short_list=[]
        fcst=0
        

        for mkid in mlist:
            for res in mkid.reslist:
            
                vdata = self.voltSweepFast(self.measspecs.vlist,res.getFc(),None)
                res.tesSweep = vdata
                
            
        return(self.measspecs.mlist)



    def voltSweepFast(self,vlist,rffreq,fnames):

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



        if fnames!=None:
           hdf.open(fnames,'w')
           hdf.write(ev,'sweepevents')


           hdf.close()


        return(ev)



  
  
    
    def powersweepSetup(self,mspecs):
       
        self.measspecs = mspecs

        self.fa.if_board.at.atten_U6  = self.measspecs.atU6
        self.sweepcount=0
        


    def powerSweep(self):
       
        
        atin=self.measspecs.attInStart
        
        
        self.thread_running=1
        
        self.fa.if_board.at.atten_U6 = self.measspecs.atU6
        
        for atx in arange(
            self.measspecs.attStart,
            self.measspecs.attEnd+1,
            self.measspecs.attIncr):
            print 'Atten Out %f, Atten In %f'%(atx,atin)
    
    
            self.fa.if_board.at.atten_U7=atx;
            self.fa.if_board.at.atten_U28=atin
        
            self.fa.if_board.progAtten(self.fa.if_board.at);
            self.fa.if_board.progRFSwitches(self.fa.if_board.rf)
        
            time.sleep(1)
        
        

            for k in range(self.measspecs.numSweeps):
                self.sweepResonators()
                    
                sweepCallback()
                self.sweepcount=self.sweepcount+1
                if self.thread_running==0:
                    print "Ending Loop/Thraed"
                    return


            atin=atin-self.measspecs.attIncr    
    


    #take list if mkids and divide into short lists of mkids within bw of 200MHz, then sweep the
    #shorts lists. list of MKID objhects expeced
    def sweepResonators(self):
        self.thread_running=1
        mlist=sorted(self.measspecs.mlist,key=MKID.getFc)
        
        short_list=[]
        fcst=0
        

        for mkid in mlist:
             self.sweepOneResonators(
                mkid,
                self.measspecs.resonator_span,
                self.measspecs.num_res_freq_points)

            
        return(self.measspecs.mlist)
        

    #sweep group of mkids w./ ftts bu sweeping LO. res must be all in 200MHz BW.
    #res are swept at same time. traces (resonatorData) are added to MKID objs
    def sweepOneResonators(self,mkid,span,pts_):

        fc=mkid.getFc2()
  
        fa.sweep(span_Hz=span, center_Hz=fc, pts=pts_)
        

        #because this is a sweep, we need to redo the delay phase
        #calc. because getDFT_IQ does this calc, we need to undo it.
        
        #cable time delay/phase is not valid because we jerked carrier freq. So we have to recalc.
        #we remove the phase delay calc to get back to raw data.
        #the problem is that we do one getDFT_IQ and one applyDelay for all the points, meaning
        #that we ahve the wrong carrier freq for most of the tones. The carrier freq must be an 
        #array,,,The ADC dekays are left in there. the data are many spectra w. one point each
        #or many spectera w. a point per mkid, for a few points
        
        #!!if self.is_apply_delay==1:          
        #!!    self.removeLineDelay()
   
        trace=self.getResonator(mkid)
        #as resonators are out of order and sorted... we find which mkid in list goes w. this trace

        mkid.addRes(trace)
        
        sweepCallback()
        #dones nothing here- for later i FW
        #self.reprogPhaseIncs()
        
        return(mkid)


    def newMkid(self,res_freq_Hz):
        self.mkid_number=0
        self.device_name="fake"
        
        mkid = MKID(N=self.mkid_number,cname=self.device_name,fc=res_freq_Hz)
        self.mkid_number = self.mkid_number + 1
        return(mkid)
    

    def getResonator(self,mkid):
        
        res=resonatorData(mkid.resonator_num, mkid.chip_name);
        #self.rescnt=self.rescnt+1;
        
        
        #tell that we used fftanal fw for sweep
        res.sweep_fw_index=1

        
        fbase= self.na.fbase
        
        res.sweep_fbase=fbase
        res.sweep_binnumber=self.na.rfft.getBinFromFreq(fbase)
        
        res.sweep_tes_bias = fa.tes_bias
        res.sweep_bias_is_on = fa.tes_bias_on
            
        freqs = fa.freqs_sweep    
        #number of freqs where we sample ferq resp of resonator. 
        #generallt 200 for a long sweep
        num_sweep_points = len(freqs)
        
        #because we hit trigFFT one to many times, we have an offset of one sample
        #fpga_bug_offset_save = self.fpga_bug_offset
        #self.fpga_bug_offset = 1 + self.fpga_bug_offset;
        
        #get bins from raw iq data w/ no phase delay calc.
        
        #!! 
        #self.fpga_bug_offset=1;
        
        #fa.removeLineDelay()
        
        
        
        
        #self.fpga_bug_offset = fpga_bug_offset_save
        
        #now calc new bins w/ correct phase delay calc.
        
        
        #calc correct phase delay- this deals wiht the fact that we havve a swept
        #LO, and the getDFT function did not account for swept LO
        # we must call removeLineDelay before this can be corect.
        #bins=self.calcXmissnLineDelay(bins_,freqs)
        
      
        #iqp = fa.dataread.RectToPolar(self.fa.iqdata)
        
        #if self.is_apply_delay:
        #    iqp=self.calcLineSweepDelay(iqp,fbase)
         
        #bins=fa.dataread.PolarToRect(iqp)
        
      
        #bug where 1st pt in the spectrum is 0, so set it to 2nd pt.
        #bins[0][0]=bins[0][1]
        #bins[1][0]=bins[1][1]
        
        res.setData(fa.iqdata, fa.freqs_sweep, self.xmission_line_delay,self.fa.carrierfreq)
        
        
        res.iqdata_rawsweep = ccopy.deepcopy(fa.iqdata_raw)
        
        #!!!res.IQ_raw = ccopy.deepcopy(self.I_raw)
        
        res.isneg_freq=self.fa.rfft.isneg_freq
 
        #copy a bunch of fields to the res object.
        res.anritsu_power= self.fa.an.anritsu_power_
        
        
        res.atten_U6=self.fa.if_board.at.atten_U6
        res.atten_U7=self.fa.if_board.at.atten_U7
        res.atten_U28=self.fa.if_board.at.atten_U28


        res.baseband_loop=self.fa.if_board.rf.baseband_loop
        res.rf_loopback=self.fa.if_board.rf.rf_loopback
        res.clk_internal=self.fa.if_board.rf.clk_internal
        res.lo_internal=self.fa.if_board.rf.lo_internal
        res.lo_source = self.fa.if_board.rf.lo_source

        #!!
        res.dac_sine_sweep_amp = self.fa.sram.amplist[0]


        res.dftLen =self.fa.rfft.dftLen
        res.sd_mod=0

        #res.fftsynctime= self.fa.rfft.fftsynctime
        
        res.is_noise = 0
            
        res.firmware_delay=0
        
        
        res.xmission_line_delay=self.xmission_line_delay

        res.roach_fft_shift = self.fa.rfft.roach_fft_shift
            
        #!!    
        res.lut_sine_amp = self.fa.sram.amplist[0]
        
        res.IQ_raw.append(self.fa.iqdata_raw)
        
        return(res)





    def calcLineDelay(self):
    
        
        
        #we di bit want bin center freq. we want the sourced freqs...
        # we have higher freq resolution in the lut than we do in the fft.
        #sourced freqs, and hence phase delay, are based on actual sourced freq.
        #sourced freqs are not in bin centers
        
        #if self.data_mode == 2:
        #    #get center freq of bins
        #    flist = self.fa.rfft.getFreqsFromBins(self.fa.rfft.fft_bins_requested)
        
        #else:
            #get freqs we source...
        flist = self.fa.sram.frequency_list
        
        binlist = self.fa.rfft.getBinsFromFreqs(flist)
        
        flist = numpy.array(flist)

        if self.fa.rfft.isneg_freq:
            #freqs=-2*pi*  (self.carrierfreq - flist)
            freqs=2*pi*  (self.fa.carrierfreq - flist)
        else:
            freqs=2*pi*  (self.fa.carrierfreq + flist) 
        
        
        
        
        self.phasesRe=   numpy.cos(freqs*self.xmission_line_delay)
        self.phasesIm=   numpy.sin(freqs*self.xmission_line_delay)


        self.freq_to_linedel_phase = dict()
        self.chan_to_linedel_phase = dict()
        for k in range(len(flist)):
            f=flist[k]
            bin=binlist[k]
            chan = self.fa.rfft.bin_to_chan[bin]
            p=[self.phasesRe[k], self.phasesIm[k]]
            self.freq_to_linedel_phase[f] = p
            self.chan_to_linedel_phase[chan]=p
            


    def calcLineSweepDelay(self,iqp,bbfreq):
    
            
        #we di bit want bin center freq. we want the sourced freqs...
        # we have higher freq resolution in the lut than we do in the fft.
        #sourced freqs, and hence phase delay, are based on actual sourced freq.
        #sourced freqs are not in bin centers
        
        
       
        if self.fa.rfft.isneg_freq==1:
            freqs=self.carrier_freqs - bbfreq
        else:
            freqs=self.carrier_freqs + bbfreq
        
        ft=freqs*self.xmission_line_delay;
        ft = ft - floor(ft);
        
        iqp[1] = iqp[1] + 2*pi*ft;
    
        


        return(iqp)
    





       #bins_all when plotted will look like the resonator response vs freq
       #plus all the extra points we csampled. we only want the 200
       #or so points we swept with. if we take many ffts per
       # freq point then we can average these together, or just take 
       #the first one. we call a function to extract the bins we want
       #len(freqs)is 200 if we swept 200 points
    def getResSweep(self,nsp,sspf,bdata):
    
            
        #just take 1st of each poihnt.. we should average...    
        bdata[0] = bdata[0][0:(nsp*sspf):sspf]
        bdata[1] = bdata[1][0:(nsp*sspf):sspf]
        return(bdata)


        
        
    def runFits2(self):
        pass
    
    def IQvelocity(self):
        pass
        
        
    def setNoiseTime(self,sec):
        
        self.measspecs.noise_time_sec= sec +3;
        self.measspecs.noise_numffts = sec * 1000000.0;
        
          
    def runNoise(self):
        for mkid in self.measspecs.mlist:
            for res in mkid.reslist:
            
                if res.maxIQvel_freq!=0:
                    fcenter=res.maxIQvel_freq
                else:
                    fcenter = mkid.rough_cent_freq
                    
                #example for 5 traces make indices -2,-1,0,1,2    
                if self.measspecs.num_noise_traces>1:
                    nindex = int(self.measspecs.num_noise_traces/2) + \
                     numpy.arange(self.measspecs.num_noise_traces) - \
                         int(self.measspecs.num_noise_traces)
                else:
                    nindex = numpy.array([0])
                                
                #make a list of freqs centered around res center, and spaced by   measspecs.noise_trace_spacing_Hz  
                nfreqs =  fcenter +  nindex *  self.measspecs.noise_trace_spacing_Hz     
                
                for fc in nfreqs:    
                    res.is_noise = res.is_noise + 1
                    self.fa.setCarrier(fc + res.sweep_fbase)
                    #self.fa.an.setPower(-3)
                    self.fa.an.setOnOff(1)




                    self.fa.if_board.at.atten_U7=res.atten_U7;
                    self.fa.if_board.at.atten_U28=res.atten_U28
                    self.fa.if_board.at.atten_U6=res.atten_U6
                    self.fa.if_board.progAtten(self.fa.if_board.at);
                    self.fa.if_board.progRFSwitches(self.fa.if_board.rf)
        
                    #!! we shoudl not assum it is 192. ... this is generally 
                    #the case though
                    if self.is_setTROT:
                        self.fa.chanzer.setFlxDmodTranTable(
                            chan=192,xc=res.cir_xc,yc=res.cir_yc)
                        
                    res.is_prog_translator = self.is_setTROT
                    
                    
                    time.sleep(1)
        
#freqlist,amp,numffts = -1,whichbins='Freqs',is_trig = True,is_zero_phaseinc=False):

                    self.fa.sourceCapture(
                        [res.sweep_fbase],
                        res.dac_sine_sweep_amp,
                        numffts = self.measspecs.noise_numffts)
                        
                    time.sleep(self.measspecs.noise_time_sec)
                    self.fa.stopCapture()
                    time.sleep(1)

                    iq = self.fa.getIQ()
                    res.iqnoise.append( ccopy.deepcopy(self.fa.iqdata_raw) )

                    res.fftLen.append(512)
                    res.fftsynctime.append( self.fa.rfft.fftsynctime)
                    res.num_noise_traces = res.num_noise_traces +1
                    res.fftdelay.append(0)

                    res.srcfreq.append( self.fa.sram.frequency_list[0] )
                    res.fftcarrierfreq.append( self.fa.carrierfreq)
                    res.noise_rf_freq.append( 
                            self.fa.carrierfreq - self.fa.sram.frequency_list[0] )

                
                    res.noise_tes_bias.append(fa.tes_bias)
                    res.noise_tes_bias_on.append(fa.tes_bias_on)
        
       
                    
        #self.fftsynctimes=[0]
    
        
             
print "Loaded mkidMeasure.py"
             