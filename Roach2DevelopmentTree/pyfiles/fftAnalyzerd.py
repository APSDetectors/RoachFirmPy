print "Loading fftAnalyzerd.py"


"""


execfile('natAnalGui.py')

#works - has gain error between I and Q-0 could be puython scripts

#fwname='fftanalyzerd_2014_Apr_10_1607.bof'
#fwname = 'fftanalyzerd_2014_Apr_11_1143.bof'

fwname ='fftanalyzerd_2014_Apr_23_1437.bof'

roach=connRoach()
startFW(roach,fwname)

fa.printRegs(1)

fa.zeroCoefMem()


setupfad()

fa.stopFFTs()

fa.fftsynctime=512*5

fa.roach_num_ffts=1
fa.progRoach()

rf.baseband_loop=0
progRFSwitches(roach,rf)

#fa.setLutSize(1024*128)

fa.Q_amp_factor=-1.0
fa.Q_phase_offs=5


#fa.setLutFreqs([20e6, 400e6],2000)

#fa.setLutFreqs(arange(15e6,500e6,20e6).tolist(),1000)
fa.setLutFreqs( arange(10e6,240e6,5e6).tolist(),600)
#fa.setLutFreqs([10e6],16384)
fa.adc_nloopback=1

#fa.setLutComb(fbase,1e6,100)

#fa.setLutFreqs([10e6, 20e6, 30e6, 40e6, 50e6, 60e6, 70e6, 80e6,200e6],2000)
#fa.fftBinFlags(range(400))
fa.fftBinsFreqs()
#fa.fftBinsAll()
fa.progRoach()

fa.trigFFT()


time.sleep(1)

fa.getDFT_IQ();


figure(301); clf();plot(10e-6+fa.extractSpectrum(0)[0])

clf();ts=fa.extractTimeSeries(10e6);plot(ts[1])

ts=fa.extractTimeSeries(30e6);plot(ts[1])
ts=fa.extractTimeSeries(40e6);plot(ts[1])
ts=fa.extractTimeSeries(20e6);clf();plot(ts[1])



sp=fa.extractRecord(1)
figure(303);clf();plot(sp[0],sp[1])
	
#
#
#

dy=55e-9
fa.setDelay(dy);fa.getDFT_IQ();sp=fa.extractRecord(1);figure(303);clf();plot(sp[0],sp[1]);
figure(301);clf();
subplot(2,1,1)
plot(fa.extractSpectrum(0)[0])
subplot(2,1,2)
plot(fa.extractSpectrum(0)[1])





iq=fa.captureADC_IQ(0)
figure(303);clf();plot(iq[0][1:100]);plot(iq[1][1:100])


clf();semilogy(abs(fft.fft( iq[0] + complex(0,1)*iq[1] )))



#@
#
#

fa.getDFT_IQ();

 clf();semilogy(10e-6+fa.extractSpectrum(0)[0])

#
#
#
setupfad()


at.atten_U6=0
at.atten_U7=0
at.atten_U28=0

progAtten(roach,at)
rf.rf_loopback=1

rf.lo_internal=0
progRFSwitches(roach,rf)

#Fitted Fr 2.560060 GHz

fc= 2.560060e9
carr=2.5e9

fa.setCarrier(carr)
#fa.setLutSize(1024*1024)
#fa.setLutSize(1024*128)

fbase=fc-carr

fa.setLutFreqsBins([60e6],4,1000)
#fa.setLutFreqs([ fbase ],20000)
#fa.setLutChirp(fbase,1e6,20000)
#fa.setLutComb(fbase,1e6,100)


fa.fftBinsFreqs()
#fa.fftBinsAll()


fa.progRoach()

fa.trigFFT()
time.sleep(5)

fa.getDFT_IQ();


aa=fa.extractSpectra(100)

fa.plotSpectra1(100)

fa.plotSpectra2(100)

fa.plotTimes(.0001,.05)

clf();ts=fa.extractTimeSeries(fbase);plot(ts[0])

#
#
#


for k in range(10):
    fa.trigFFT()
    time.sleep(5)   
    fa.getDFT_IQ();
    clf();ts=fa.extractTimeSeries(fbase);plot(ts[1])
    draw()
    time.sleep(.1)



#
#
#


clf();plot(fa.lut_i[:100]);plot(fa.lut_q[:100])

clf();semilogy(1e-6+abs(fft.fft(fa.lut_i + complex(0,1)*fa.lut_q)))


#
#testing long dram stuff
#

fa.setLutSize(1024*1024)
fa.setLutFreqs([1e6],10000)
lutrb = roach.read_dram(len(fa.lut_binaryIQ))
ddrb=fa.convertFromBinary128(lutrb)


dif_i=ddrb[0]-fa.lut_i
dif_q=ddrb[1]-fa.lut_q


off=0
clf();plot(fa.lut_q[(off):(off+1000)]);plot(ddrb[1][(off):(off+1000)]);off=off+32768;print off


fa.adc_nloopback=0

ss=fa.captureADC3(0);clf();plot(ss)





#
#
#

on roach unix prompt

dd if=/proc/583/hw/ioreg/dram_memory of=maddog.bin bs=1024 count=4096
#on linux
scp root@192.168.0.67:maddog.bin .

#in py

ff=open('maddog.bin','rb')
lutf= ff.read(1024*1024*4)
ff.close()
ddrb=fa.convertFromBinary128(lutf)


dif_i=ddrb[0]-fa.lut_i
dif_q=ddrb[1]-fa.lut_q



fa.fftBinFlags(range(35,45))

 fa.progRoach()

 fa.trigFFT()

 fa.getDFT_IQ();


 clf();semilogy(fa.extractSpectrum(3)[0])




fa.fftBinFlags([40])
fa.progRoach()
fa.trigFFT()
fa.getDFT_IQ();
clf();semilogy(fa.extractSpectrum(3)[0])
[<matplotlib.lines.Line2D at 0x1d949510>]






fa.setLutFreqs([10e6, 20e6, 30e6, 40e6, 50e6],2000)
#fa.fftBinFlags(range(400))
fa.fftBinsFreqs()
fa.progRoach()

 fa.trigFFT()

 fa.getDFT_IQ();


 clf();semilogy(fa.extractSpectrum(0)[0])




fa.setLutFreqs([10e6, 20e6, 30e6, 40e6, 50e6],2000)


fa.setLutNoise()

fa.fftBinsAll()
fa.progRoach()

 fa.trigFFT()

 fa.getDFT_IQ();


 clf();semilogy(fa.extractSpectrum(0)[0])


ss=fa.extractSpectra()


#how you calc bin from sin freq.
10e6/(512e6/2048)





fa.setLutFreqs([10e6, 20e6, 30e6, 40e6, 50e6],2000)
fa.fftBinsFreqs()

 fa.fft_bin_list

fa.progRoach()

 fa.trigFFT()

 fa.getDFT_IQ();


 clf();semilogy(fa.extractSpectrum(3)[0])


nspectra= fa.memLen / len(fa.fft_bin_list)




fa.fa.Q_phase_offs=-10.0 * (3.14159/180.0)


fa.setLutFreqs([10e6, 20e6, 30e6, 40e6, 50e6],2000)
fa.fftBinsAll()
fa.progRoach()

 fa.trigFFT()

 fa.getDFT_IQ();


 clf();semilogy(fa.extractSpectrum(0)[0])




fa.adc_nloopback=1
fa.Q_phase_offs=0 * (3.14159/180.0)
fa.Q_amp_factor=0.05
fa.Q_freq_offset=0

#fa.setLutFreqs([10e6, 20e6, 30e6, 40e6, 50e6],2000)
fa.setLutFreqs([10e6],5000)
fa.fftBinsAll()
fa.progRoach()

 fa.trigFFT()

 fa.getDFT_IQ();


 clf();semilogy(fa.extractSpectrum(0)[0])








clf();plot(fa.lut_i);plot(fa.lut_q)


"""

#for making random obhects w/ fields. example a = inline()
#a.whatever =1
#a.thisthat ='dfdfd'
#pickle.dump(a,open('filelll','wb'))


class inline: pass


	
########################################################################
#
# uise fftanalyzerc.slx
#
#
#######################################################################

class fftAnalyzerd(fftAnalyzer):


	def __init__(self,r):
		fftAnalyzer.__init__(self,r)
		#when sweeping, how many ffts per freq		
		self.sweep_samples_per_freq=1


		#list of mkids we areradout out... we have to resweep them for readout so curcles line up		
		self.fft_mkid_list=[]
		
		
		#apply phase time calc on getting iq data
		self.is_apply_delay=1;
		
		#if no roach, or debugging, we can read IQ data from a dump file.
		self.is_read_dump_file = 0
		
		#1 to sweep many res at once. 0 othersize
		self.is_sweep_several=0
		
		#delay in ns of the formware calc. thsi is time delay of dac, ADC, ffts, 
		#and IF board delay. we should calc using RF loopback. 
		#measred w/ calcFFTTimeDelay 
		#this is for 2k fft
		#self.firmware_delay=748e-9
		#for 512 fft- better meas. negative because we use neg freq
		#self.firmware_delay=-1650e-9
		#dont hagve good meas of this, so forget it for now...we can work around it.
		self.firmware_delay=0.0
		
		#line delay xmission line delay
		self.xmission_line_delay = 30e-9
		#total delay
		self.delay = self.firmware_delay + self.xmission_line_delay
		
		#save objects for debugging
		self.debugobjs=[]
		self.is_debug_save_objs=0
		
		
		
		self.isneg_freq=1
		
		
		self.fftsynctime=self.dftLen*5

		#dft memlen
		self.memLen=65536
		self.memLen4=self.memLen/4
		self.memLen8=self.memLen/8


		#num ffts calc'd per trigger in roach.
		self.roach_num_ffts=65536
		
		#bit for triggering ffts
		self.start_ffts=0
		
		#reg in roach for fft shifting, fft gain
		self.roach_fft_shift=2047
		

		# for dump fifo. set to 1, then 0.
		self.dump_fifo=0
	
		#number of bins read out of all 4 outoputs of fft compboned. 
		self.numBinsStored=0
		
		#list of bins we actially stpre in readout ram after fifos, this is 1 and 0 array. 
		self.binReadRam=zeros(10)
		
		
		#for sweeping resonators w. LO
		self.start_carrier = 0.0
		self.end_carrier = 0.0
		self.inc_carrier = 0.0
		
		#to set up attens, switches, lut, fftbins on doing noise. set to 0 if we
		#wish to use current settings, as in sweeping then noise meas. 
		self.is_resetup_noise=1

		#the delay for noise sweeps..
		self.calcNsDly_php=[zeros(200),zeros(200)]
		#the delay for freq sweeps..
		self.calcSwDly_php=[zeros(200),zeros(200)]


	def setObjSpecs(self,specs):
	
	
	
		self.is_apply_delay=specs.is_apply_delay
	
		self.fpga_bug_offset= specs.fpga_bug_offset
	
		self.firmware_delay=specs.firmware_delay
		self.xmission_line_delay=specs.xmission_line_delay
		
		#wire for resettign DAC block in FW
		self.dac_reset_bit=int(specs.dac_reset_bit)
		
		#sinusoid amplitude in the DAC, as a percent. 1.0 means DAC is full scale.
		#hardcoded in netanaluzer FW
		self.dac_sine_sweep_amp = specs.dac_sine_sweep_amp
		
		#device name- a string, saved to hdf dump file...
		#!!self.device_name=specs.device_name
		
		
		#resonator number- an attribute saved w/ sweepts
		self.resonator_number=int(specs.resonator_number)
		
		
		#power in dbm for anritsu
		self.anritsu_power=specs.anritsu_power
		
		#some fw has adjustable gain on the sin output- 
		#some dont
		self.hasIQGainReg=int(specs.hasIQGainReg)
		
		#
		#!!self.debugvalue=specs.0
		
		
		
		self.carrierfreq=specs.carrierfreq


		self.statusFlags=int(specs.statusFlags)
		self.stat_sweepDone=int(specs.stat_sweepDone)
	


		#enable signal delta modulator
		self.sd_mod=int(specs.sd_mod)
		#reset master state machine
		self.msm_rst=int(specs.msm_rst)
		#trigger scan
		self.start_scan=int(specs.start_scan)
		#start dac
		self.startOutputDac=int(specs.startOutputDac)
		#manual increment of freq
		self.manualSweep=int(specs.manualSweep)
		#manual trigger of dft
		self.manDFT=int(specs.manDFT)
		
		
		#set to 1 for adc. set to 0 for loopback.
		self.adc_nloopback=int(specs.adc_nloopback)
		
		#adc mem start, clear addr
		self.adcmem_start=int(specs.adcmem_start)
		#adc wr mem
		self.adcmem_wr=int(specs.adcmem_wr)
		#adc mem select- 0...7
		self.adcmem_sel=int(specs.adcmem_sel)
		
		#force adc sync hi
		self.adcfsync=int(specs.adcfsync)
		
		#start frequency Hz
		self.startFreq_Hz=specs.startFreq_Hz
		#end freq Hz
		self.endFreq_Hz=specs.endFreq_Hz
		#freq incr Hz
		self.incrFreq_Hz=specs.incrFreq_Hz
		
		
		#sintable len
		self.sin_tablen=int(specs.sin_tablen)
		
		#start freq register
		self.startFreq=specs.startFreq
		self.endFreq=specs.endFreq
		self.freqAddend=specs.freqAddend
		self.controlReg=int(specs.controlReg)
		
		
		#for short PFB window- double length hamming window
		#overlap added. 32 or 256 depending on FW.
		#if zero, no windowing.
		#if 1 we get that hamming. need to set dftlen to 32
		self.useOverlapWind=int(specs.useOverlapWind)
		
		self.dftLen=int(specs.dftLen)
		
	
	

		#waveformme len
		self.memLenW=int(specs.memLenW)

		self.phasesRe=specs.phasesRe
		self.phasesIm=specs.phasesIm
		


		#for sweeping the power- setting the attenuator on IF
    		#output atten start
		self.attStart=specs.attStart
	    	self.attEnd=specs.attEnd
	    	self.attIncr=specs.attIncr
		#input atten start...
		self.attInStart=specs.attInStart
		
		#for cunting getting iqdata on power sweeps	    	
		self.numSweeps=int(specs.numSweeps)
		self.sweepcount=int(specs.sweepcount)
		#to plot graph on sweep grab
		self.is_plotsweep=int(specs.is_plotsweep)
		
		
		
		#where latest iqdata is stored
		self.iqdata=specs.iqdata
	
		self.I_raw=specs.I_raw
		self.Q_raw=specs.Q_raw
		
	
		#index for reading and writn ghdf files.		
		#!self.iq_index=specs.iq_index
		#!self.set_index=specs.set_index

		#for returning resonator obj, give in index.
		self.rescnt=int(specs.rescnt)
		
		
		
		#reg for 1/dftlen window length...
		self.invDftLen=int(specs.invDftLen)
		
	
		
		
		
				
		self.dac_clk=specs.dac_clk
		self.sys_clk=specs.sys_clk
		
		
		#amplitude of waves we put in lut- as a percentage. 1.0 is full scale
		self.lut_sine_amp=specs.lut_sine_amp
		
		
		#for debug...send address of dram to dac output
		self.seeaddress=int(specs.seeaddress)
		
		self.st_fft_mem=int(specs.st_fft_mem)
		self.fft_mem_we=int(specs.fft_mem_we)

		
		self.holdcounter=int(specs.holdcounter)
		
		self.resetDRAM=int(specs.resetDRAM)
	
		
		#
		# can put a phase pulse into the lut
		#give pulse amp, pulse length
		#pulse shaped like sawtooth
		# amp in degrees. length is in samples in the lut
		#
		self.test_pulse_amp=specs.test_pulse_amp
		self.test_pulse_len=int(specs.test_pulse_len)
		
		
		self.lut_length=int(specs.lut_length)
		self.lut_length2=int(specs.lut_length2)
		self.lut_length4=int(specs.lut_length4)
		self.lut_length8=int(specs.lut_length8)
		

		
		#dft memlen
		self.memLen=int(specs.memLen)
		self.memLen4=int(specs.memLen4)
		self.memLen8=int(specs.memLen8)

		#waveformme len
		self.memLenW=int(specs.memLenW)
		
		
		#len of fft on roach
		self.fftLen=int(specs.fftLen)
		#num samples on one tap from 1/4 ADC in roach board.
		self.dftLen=int(specs.dftLen)
		
	
		self.delay=specs.delay

		
		#phase offset of Q in radians. is is added phase to a sin
		self.Q_phase_offs=specs.Q_phase_offs
		
		#amp factor to mult by Q amplitude. set to 1.0 . set to 0 for no Q.
		self.Q_amp_factor=specs.Q_amp_factor
		
		#we can make Q freq different from I freq w. offset in Hz
		self.Q_freq_offset=specs.Q_freq_offset
		
		
		try:
		    self.lut_phase_list=specs.lut_phase_list.tolist()

		except:
		    self.lut_phase_list=specs.lut_phase_list
		
		
		
		try:
		    self.fft_bins_requested=specs.fft_bins_requested.tolist()

		except:
		    self.fft_bins_requested=specs.fft_bins_requested
		    
		    
		try:
		    self.fft_bin_list=specs.fft_bin_list.tolist()
		except:
		    self.fft_bin_list=specs.fft_bin_list


		try:
		    self.frequency_list=specs.frequency_list.tolist()
		except:
		    self.frequency_list=specs.frequency_list

		try:
		    self.fft_bin_flags=specs.fft_bin_flags.tolist()
		except:
		    self.fft_bin_flags=specs.fft_bin_flags
		    
		    #the delay for noise sweeps..
		try:
		    self.calcNsDly_php=specs.calcNsDly_php.tolist()
		except:
		    self.calcNsDly_php=specs.calcNsDly_php


		    #the delay for freq sweeps..
		try:
		    self.calcSwDly_php=specs.calcSwDly_php.tolist()
		except:
		    self.calcSwDly_php=specs.calcSwDly_php


		
		
		self.Q_amp_factor=specs.Q_amp_factor
		self.isneg_freq=int(specs.isneg_freq)
		
		
		self.fftsynctime=specs.fftsynctime



		#num ffts calc'd per trigger in roach.
		self.roach_num_ffts=int(specs.roach_num_ffts)
		
		#bit for triggering ffts
		self.start_ffts=int(specs.start_ffts)
		
		#reg in roach for fft shifting, fft gain
		self.roach_fft_shift=int(specs.roach_fft_shift)
		

		# for dump fifo. set to 1, then 0.
		self.dump_fifo=int(specs.dump_fifo)
	
		#number of bins read out of all 4 outoputs of fft compboned. 
		self.numBinsStored=int(specs.numBinsStored)
		
		#list of bins we actially stpre in readout ram after fifos, this is 1 and 0 array. 
		self.binReadRam=specs.binReadRam
		
		
		#for sweeping resonators w. LO
		self.start_carrier =specs.start_carrier
		self.end_carrier = specs.end_carrier 
		self.inc_carrier = specs.inc_carrier
		
		#to set up attens, switches, lut, fftbins on doing noise. set to 0 if we
		#wish to use current settings, as in sweeping then noise meas. 
		self.is_resetup_noise=int(specs.is_resetup_noise)
		
		
		
		self.lut_i=specs.lut_i
		self.lut_q=specs.lut_q
		
		
		rf.baseband_loop=int(specs.rf_baseband_loop)
		rf.clk_internal=int(specs.rf_clk_internal)
		rf.lo_internal=int(specs.rf_lo_internal)
		rf.lo_source=int(specs.rf_lo_source)
		rf.rf_loopback=int(specs.rf_loopback)

	
	 	at.atten_U6=specs.at_atten_U6
		at.atten_U7=specs.at_atten_U7
		at.atten_U28=specs.at_atten_U28


		global anritsu_freqghz_
		global anritsu_power_
		global anritsu_is_on_

		anritsu_freqghz_=specs.anritsu_freqghz_
		anritsu_power_=specs.anritsu_power_
		anritsu_is_on_=specs.anritsu_is_on_




	def getObjSpecs(self):
	
		specs=inline()
		
		
		specs.is_apply_delay=self.is_apply_delay
		specs.fpga_bug_offset= self.fpga_bug_offset
		
		specs.firmware_delay=self.firmware_delay
		specs.xmission_line_delay=self.xmission_line_delay
		
		#wire for resettign DAC block in FW
		specs.dac_reset_bit=self.dac_reset_bit
		
		#sinusoid amplitude in the DAC, as a percent. 1.0 means DAC is full scale.
		#hardcoded in netanaluzer FW
		specs.dac_sine_sweep_amp = self.dac_sine_sweep_amp
		
		#device name- a string, saved to hdf dump file...
		#specs.device_name=self.device_name
		
		
		#resonator number- an attribute saved w/ sweepts
		specs.resonator_number=self.resonator_number
		
		
		#power in dbm for anritsu
		specs.anritsu_power=self.anritsu_power
		
		#some fw has adjustable gain on the sin output- 
		#some dont
		specs.hasIQGainReg=self.hasIQGainReg
		
		#
		#!!specs.debugvalue=self.0
		
		
		
		specs.carrierfreq=self.carrierfreq


		specs.statusFlags=self.statusFlags
		specs.stat_sweepDone=self.stat_sweepDone
	


		#enable signal delta modulator
		specs.sd_mod=self.sd_mod
		#reset master state machine
		specs.msm_rst=self.msm_rst
		#trigger scan
		specs.start_scan=self.start_scan
		#start dac
		specs.startOutputDac=self.startOutputDac
		#manual increment of freq
		specs.manualSweep=self.manualSweep
		#manual trigger of dft
		specs.manDFT=self.manDFT
		
		
		#set to 1 for adc. set to 0 for loopback.
		specs.adc_nloopback=self.adc_nloopback
		
		#adc mem start, clear addr
		specs.adcmem_start=self.adcmem_start
		#adc wr mem
		specs.adcmem_wr=self.adcmem_wr
		#adc mem select- 0...7
		specs.adcmem_sel=self.adcmem_sel
		
		#force adc sync hi
		specs.adcfsync=self.adcfsync
		
		#start frequency Hz
		specs.startFreq_Hz=self.startFreq_Hz
		#end freq Hz
		specs.endFreq_Hz=self.endFreq_Hz
		#freq incr Hz
		specs.incrFreq_Hz=self.incrFreq_Hz
		
		
		#sintable len
		specs.sin_tablen=self.sin_tablen
		
		#start freq register
		specs.startFreq=self.startFreq
		specs.endFreq=self.endFreq
		specs.freqAddend=self.freqAddend
		specs.controlReg=self.controlReg
		
		
		#for short PFB window- double length hamming window
		#overlap added. 32 or 256 depending on FW.
		#if zero, no windowing.
		#if 1 we get that hamming. need to set dftlen to 32
		specs.useOverlapWind=self.useOverlapWind
		
		specs.dftLen=self.dftLen
		
	
	

		#waveformme len
		specs.memLenW=self.memLenW

		specs.phasesRe=self.phasesRe
		specs.phasesIm=self.phasesIm
		


		#for sweeping the power- setting the attenuator on IF
    		#output atten start
		specs.attStart=self.attStart
	    	specs.attEnd=self.attEnd
	    	specs.attIncr=self.attIncr
		#input atten start...
		specs.attInStart=self.attInStart
		
		#for cunting getting iqdata on power sweeps	    	
		specs.numSweeps=self.numSweeps
		specs.sweepcount=self.sweepcount
		#to plot graph on sweep grab
		specs.is_plotsweep=self.is_plotsweep
		
		
		
		#where latest iqdata is stored
		specs.iqdata=self.iqdata
	
		specs.I_raw=self.I_raw
		specs.Q_raw=self.Q_raw
		
	
		#index for reading and writn ghdf files.		
		specs.iq_index=self.iq_index
		specs.set_index=self.set_index

		#for returning resonator obj, give in index.
		specs.rescnt=self.rescnt
		
		
		
		#reg for 1/dftlen window length...
		specs.invDftLen=self.invDftLen
		
		
		
		
		
		
				
		specs.dac_clk=self.dac_clk
		specs.sys_clk=self.sys_clk
		
		
		#amplitude of waves we put in lut- as a percentage. 1.0 is full scale
		specs.lut_sine_amp=self.lut_sine_amp
		
		
		#for debug...send address of dram to dac output
		specs.seeaddress=self.seeaddress
		
		specs.st_fft_mem=self.st_fft_mem
		specs.fft_mem_we=self.fft_mem_we

		
		specs.holdcounter=self.holdcounter
		
		specs.resetDRAM=self.resetDRAM
	
		
		#
		# can put a phase pulse into the lut
		#give pulse amp, pulse length
		#pulse shaped like sawtooth
		# amp in degrees. length is in samples in the lut
		#
		specs.test_pulse_amp=self.test_pulse_amp
		specs.test_pulse_len=self.test_pulse_len
		
		
		specs.lut_length=self.lut_length
		specs.lut_length2=self.lut_length2
		specs.lut_length4=self.lut_length4
		specs.lut_length8=self.lut_length8
		

		
		#dft memlen
		specs.memLen=self.memLen
		specs.memLen4=self.memLen4
		specs.memLen8=self.memLen8

		#waveformme len
		specs.memLenW=self.memLenW
		
		
		#len of fft on roach
		specs.fftLen=self.fftLen
		#num samples on one tap from 1/4 ADC in roach board.
		specs.dftLen=self.dftLen
		
	
		specs.delay=self.delay

		
		#phase offset of Q in radians. is is added phase to a sin
		specs.Q_phase_offs=self.Q_phase_offs
		
		#amp factor to mult by Q amplitude. set to 1.0 . set to 0 for no Q.
		specs.Q_amp_factor=self.Q_amp_factor
		
		#we can make Q freq different from I freq w. offset in Hz
		specs.Q_freq_offset=self.Q_freq_offset
		
		
		
		specs.fft_bins_requested=self.fft_bins_requested
		
		#list of bins like 40,41,42,43, 128,129,130,140,1022,1023,1024,1025 for which bins
		# we read out of FFT. is is list of indices of fft_bin_flags that are
		#set to 1, and mult by 4. for all bins, for 2k fft this is same as
		#range(2048). 
		specs.fft_bin_list=self.fft_bin_list
		
		#list of freqs we wish to generate in setLutFreqs
		specs.req_frequency_list=self.req_frequency_list
		#list of freqs we ACTUALLY? generate in setLutFreqs
		specs.frequency_list=self.frequency_list
		
		specs.fft_bin_flags=self.fft_bin_flags
	
		specs.lut_phase_list=self.lut_phase_list
	
		
		
		specs.Q_amp_factor=self.Q_amp_factor
		specs.isneg_freq=self.isneg_freq
		
		
		specs.fftsynctime=self.fftsynctime

		

		#num ffts calc'd per trigger in roach.
		specs.roach_num_ffts=self.roach_num_ffts
		
		#bit for triggering ffts
		specs.start_ffts=self.start_ffts
		
		#reg in roach for fft shifting, fft gain
		specs.roach_fft_shift=self.roach_fft_shift
		

		# for dump fifo. set to 1, then 0.
		specs.dump_fifo=self.dump_fifo
	
		#number of bins read out of all 4 outoputs of fft compboned. 
		specs.numBinsStored=self.numBinsStored
		
		#list of bins we actially stpre in readout ram after fifos, this is 1 and 0 array. 
		specs.binReadRam=self.binReadRam
		
		
		#for sweeping resonators w. LO
		specs.start_carrier =self.start_carrier
		specs.end_carrier = self.end_carrier 
		specs.inc_carrier = self.inc_carrier
		
		#to set up attens, switches, lut, fftbins on doing noise. set to 0 if we
		#wish to use current settings, as in sweeping then noise meas. 
		specs.is_resetup_noise=self.is_resetup_noise
		
		
		
		specs.lut_i=self.lut_i
		specs.lut_q=self.lut_q
		
	


		#the delay for noise sweeps..
		specs.calcNsDly_php=self.calcNsDly_php
		#the delay for freq sweeps..
		specs.calcSwDly_php=self.calcSwDly_php

		
		
		
		
		specs.rf_baseband_loop=rf.baseband_loop
		specs.rf_clk_internal=rf.clk_internal
		specs.rf_lo_internal=rf.lo_internal
		specs.rf_lo_source=rf.lo_source
		
		specs.rf_loopback=rf.rf_loopback

		
		
		
	 	specs.at_atten_U6=at.atten_U6
		specs.at_atten_U7=at.atten_U7
		specs.at_atten_U28=at.atten_U28

		
		
		
		specs.anritsu_freqghz_=anritsu_freqghz_
		specs.anritsu_power_=anritsu_power_
		specs.anritsu_is_on_=anritsu_is_on_


		
		
		return(specs)






	def info(self,level):
			
		if level>=0: print 'specs.firmware_delay= %e'%(self.firmware_delay)
		if level>=0: print 'specs.xmission_line_delay= %e'%(self.xmission_line_delay)
		
		
		
		
		#wire for resettign DAC block in FW
		if level>=1: print 'specs.dac_reset_bit= %f'%(self.dac_reset_bit)
		
		#sinusoid amplitude in the DAC, as a percent. 1.0 means DAC is full scale.
		#hardcoded in netanaluzer FW
		if level>=0: print 'specs.dac_sine_sweep_amp = %f'%( self.dac_sine_sweep_amp)
		
		
		
		#resonator number- an attribute saved w/ sweepts
		if level>=2: print 'specs.resonator_number= %f'%(self.resonator_number)
		
		
		#power in dbm for anritsu
		if level>=0: print 'specs.anritsu_power= %f'%(self.anritsu_power)
		
		#some fw has adjustable gain on the sin output- 
		#some dont
		if level>=2: print 'specs.hasIQGainReg= %f'%(self.hasIQGainReg)
		
		
		if level>=0: print 'specs.carrierfreq= %f'%(self.carrierfreq)


		if level>=2: print 'specs.statusFlags= %f'%(self.statusFlags)
		if level>=2: print 'specs.stat_sweepDone= %f'%(self.stat_sweepDone)
	


		#enable signal delta modulator
		if level>=1: print 'specs.sd_mod= %f'%(self.sd_mod)
		#reset master state machine
		if level>=2: print 'specs.msm_rst= %f'%(self.msm_rst)
		#trigger scan
		if level>=2: print 'specs.start_scan= %f'%(self.start_scan)
		#start dac
		if level>=2: print 'specs.startOutputDac= %f'%(self.startOutputDac)
		#manual increment of freq
		if level>=2: print 'specs.manualSweep= %f'%(self.manualSweep)
		#manual trigger of dft
		if level>=2: print 'specs.manDFT= %f'%(self.manDFT)
		
		
		#set to 1 for adc. set to 0 for loopback.
		if level>=0: print 'specs.adc_nloopback= %f'%(self.adc_nloopback)
		
		#adc mem start, clear addr
		if level>=2: print 'specs.adcmem_start= %f'%(self.adcmem_start)
		#adc wr mem
		if level>=2: print 'specs.adcmem_wr= %f'%(self.adcmem_wr)
		#adc mem select- 0...7
		if level>=2: print 'specs.adcmem_sel= %f'%(self.adcmem_sel)
		
		#force adc sync hi
		if level>=2: print 'specs.adcfsync= %f'%(self.adcfsync)
		
		#start frequency Hz
		if level>=1: print 'specs.startFreq_Hz= %f'%(self.startFreq_Hz)
		#end freq Hz
		if level>=1: print 'specs.endFreq_Hz= %f'%(self.endFreq_Hz)
		#freq incr Hz
		if level>=1: print 'specs.incrFreq_Hz= %f'%(self.incrFreq_Hz)
		
		
		#sintable len
		if level>=0: print 'specs.sin_tablen= %f'%(self.sin_tablen)
		
		#start freq register
		if level>=2: print 'specs.startFreq= %f'%(self.startFreq)
		if level>=2: print 'specs.endFreq= %f'%(self.endFreq)
		if level>=2: print 'specs.freqAddend= %f'%(self.freqAddend)
		if level>=2: print 'specs.controlReg= %f'%(self.controlReg)
		
		
		#for short PFB window- double length hamming window
		#overlap added. 32 or 256 depending on FW.
		#if zero, no windowing.
		#if 1 we get that hamming. need to set dftlen to 32
		if level>=2: print 'specs.useOverlapWind= %f'%(self.useOverlapWind)
		
		if level>=0: print 'specs.dftLen= %f'%(self.dftLen)
		
	
	

		#waveformme len
		if level>=2: print 'specs.memLenW= %f'%(self.memLenW)

		if level>=2: print 'specs.phasesRe= %f'%(self.phasesRe)
		if level>=2: print 'specs.phasesIm= %f'%(self.phasesIm)
		


		#for sweeping the power- setting the attenuator on IF
    		#output atten start
		if level>=1: print 'specs.attStart= %f'%(self.attStart)
	    	if level>=1: print 'specs.attEnd= %f'%(self.attEnd)
	    	if level>=1: print 'specs.attIncr= %f'%(self.attIncr)
		#input atten start...
		if level>=1: print 'specs.attInStart= %f'%(self.attInStart)
		
		#for cunting getting iqdata on power sweeps	    	
		if level>=1: print 'specs.numSweeps= %f'%(self.numSweeps)
		if level>=1: print 'specs.sweepcount= %f'%(self.sweepcount)
		#to plot graph on sweep grab
		if level>=2: print 'specs.is_plotsweep= %f'%(self.is_plotsweep)
		
		
		
		#where latest iqdata is stored
		if level>=2: print 'specs.iqdata= %f'%(self.iqdata)
	
		if level>=2: print 'specs.I_raw= %f'%(self.I_raw)
		if level>=2: print 'specs.Q_raw= %f'%(self.Q_raw)
		
	
		#index for reading and writn ghdf files.		
		if level>=2: print 'specs.iq_index= %f'%(self.iq_index)
		if level>=2: print 'specs.set_index= %f'%(self.set_index)

		#for returning resonator obj, give in index.
		if level>=1: print 'specs.rescnt= %f'%(self.rescnt)
		
		
		
		#reg for 1/dftlen window length...
		if level>=1: print 'specs.invDftLen= %f'%(self.invDftLen)
		
		
		
		
		
		
				
		if level>=0: print 'specs.dac_clk= %f'%(self.dac_clk)
		if level>=0: print 'specs.sys_clk= %f'%(self.sys_clk)
		
		
		#amplitude of waves we put in lut- as a percentage. 1.0 is full scale
		if level>=0: print 'specs.lut_sine_amp= %f'%(self.lut_sine_amp)
		
		
		#for debug...send address of dram to dac output
		if level>=1: print 'specs.seeaddress= %f'%(self.seeaddress)
		
		if level>=1: print 'specs.st_fft_mem= %f'%(self.st_fft_mem)
		if level>=1: print 'specs.fft_mem_we= %f'%(self.fft_mem_we)

		
		if level>=1: print 'specs.holdcounter= %f'%(self.holdcounter)
		
		if level>=1: print 'specs.resetDRAM= %f'%(self.resetDRAM)
	
		
		#
		# can put a phase pulse into the lut
		#give pulse amp, pulse length
		#pulse shaped like sawtooth
		# amp in degrees. length is in samples in the lut
		#
		if level>=2: print 'specs.test_pulse_amp= %f'%(self.test_pulse_amp)
		if level>=2: print 'specs.test_pulse_len= %f'%(self.test_pulse_len)
		
		
		if level>=0: print 'specs.lut_length= %f'%(self.lut_length)
		if level>=2: print 'specs.lut_length2= %f'%(self.lut_length2)
		if level>=2: print 'specs.lut_length4= %f'%(self.lut_length4)
		if level>=2: print 'specs.lut_length8= %f'%(self.lut_length8)
		

		
		#dft memlen
		if level>=2: print 'specs.memLen= %f'%(self.memLen)
		if level>=2: print 'specs.memLen4= %f'%(self.memLen4)
		if level>=2: print 'specs.memLen8= %f'%(self.memLen8)

		#waveformme len
		if level>=2: print 'specs.memLenW= %f'%(self.memLenW)
		
		
		#len of fft on roach
		if level>=0: print 'specs.fftLen= %f'%(self.fftLen)
		#num samples on one tap from 1/4 ADC in roach board.
		if level>=0: print 'specs.dftLen= %f'%(self.dftLen)
		
	
		if level>=0: print 'specs.delay= %f'%(self.delay)

		
		#phase offset of Q in radians. is is added phase to a sin
		if level>=1: print 'specs.Q_phase_offs= %f'%(self.Q_phase_offs)
		
		#amp factor to mult by Q amplitude. set to 1.0 . set to 0 for no Q.
		if level>=1: print 'specs.Q_amp_factor= %f'%(self.Q_amp_factor)
		
		#we can make Q freq different from I freq w. offset in Hz
		if level>=1: print 'specs.Q_freq_offset= %f'%(self.Q_freq_offset)
		
		
		
		if level>=2: 
		    print('specs.fft_bins_requested= '),
		    print self.fft_bins_requested
		
		#list of bins like 40,41,42,43, 128,129,130,140,1022,1023,1024,1025 for which bins
		# we read out of FFT. is is list of indices of fft_bin_flags that are
		#set to 1, and mult by 4. for all bins, for 2k fft this is same as
		#range(2048). 
		if level>=1:
		   print('specs.fft_bin_list'),;print self.fft_bin_list
		
		#list of freqs we wish to generate in setLutFreqs
		if level>=0: 
		    print('specs.req_frequency_list'),
		    print self.req_frequency_list
		
		#list of freqs we ACTUALLY? generate in setLutFreqs
		if level>=0: 
		    print('specs.frequency_list'),
		    print self.frequency_list
		
		if level>=2: print 'specs.fft_bin_flags= %f'%(self.fft_bin_flags)
	
	
	
		
		
		if level>=2: print 'specs.Q_amp_factor= %f'%(self.Q_amp_factor)
		if level>=0: print 'specs.isneg_freq= %f'%(self.isneg_freq)
		
		
		if level>=0: print 'specs.fftsynctime= %f'%(self.fftsynctime)

		

		#num ffts calc'd per trigger in roach.
		if level>=1: print 'specs.roach_num_ffts= %f'%(self.roach_num_ffts)
		
		#bit for triggering ffts
		if level>=2: print 'specs.start_ffts= %f'%(self.start_ffts)
		
		#reg in roach for fft shifting, fft gain
		if level>=0: print 'specs.roach_fft_shift= %f'%(self.roach_fft_shift)
		

		# for dump fifo. set to 1, then 0.
		if level>=2: print 'specs.dump_fifo= %f'%(self.dump_fifo)
	
		#number of bins read out of all 4 outoputs of fft compboned. 
		if level>=2: print 'specs.numBinsStored= %f'%(self.numBinsStored)
		
		#list of bins we actially stpre in readout ram after fifos, this is 1 and 0 array. 
		if level>=2: print 'specs.binReadRam= %f'%(self.binReadRam)
		
		
		#for sweeping resonators w. LO
		if level>=0: print 'specs.start_carrier = %f'%(self.start_carrier)
		if level>=0: print 'specs.end_carrier = %f'%( self.end_carrier )
		if level>=0: print 'specs.inc_carrier = %f'%( self.inc_carrier)
		
		#to set up attens, switches, lut, fftbins on doing noise. set to 0 if we
		#wish to use current settings, as in sweeping then noise meas. 
		if level>=0: print 'specs.is_resetup_noise= %f'%(self.is_resetup_noise)
		
		
		
		if level>=2: print 'specs.lut_i= %f'%(self.lut_i)
		if level>=2: print 'specs.lut_q= %f'%(self.lut_q)
		
	


		#the delay for noise sweeps..
		if level>=2: print 'specs.calcNsDly_php= %f'%(self.calcNsDly_php)
		#the delay for freq sweeps..
		if level>=2: print 'specs.calcSwDly_php= %f'%(self.calcSwDly_php)

		


		if level>=0: print 'rf.baseband_loop %f'%(rf.baseband_loop)
		if level>=0: print 'rf.clk_internal %f'%(rf.clk_internal)
		if level>=0: print 'rf.lo_internal %f'%(rf.lo_internal)
		if level>=0: print 'rf.lo_source %f'%(rf.lo_source)
		if level>=0: print 'rf.loopback %f'%(rf.rf_loopback)




	
		if level>=0: print 'at.atten_U6 %f'%(at.atten_U6)
		if level>=0: print 'at.atten_U7 %f'%(at.atten_U7)
		if level>=0: print 'at.atten_U28 %f'%(at.atten_U28)


		if level>=0: print 'anritsu_freqghz_= %f'%(anritsu_freqghz_)
		if level>=0: print 'anritsu_power_= %f'%(anritsu_power_)
		if level>=0: print 'anritsu_is_on_= %f'%(anritsu_is_on_)










	def dbgclear(self):
			
		self.debugobjs=[]


	def dbgsave(self,filename):
	    pickle.dump(self.debugobjs,open(filename,'wb'))
	    
	    
	def dbgload(self,filename):
	    class inline:pass
	    self.debugobjs = pickle.load(open(filename,'rb'))
	    
	   
	   
	def dbgappend(self,obj):
	    if self.is_debug_save_objs==1:
	        self.debugobjs.append(ccopy.deepcopy(obj))
	    





	    
	         
	#take list if mkids and divide into short lists of mkids within bw of 200MHz, then sweep the
	#shorts lists. list of MKID objhects expeced
	def noiseResonators(self,mlist1,numtraces):

		mlist=sorted(mlist1,key=MKID.getFc)
		
		self.thread_running=1
		
		for mkid in mlist:	  
		    for resdata in mkid.reslist:
		        try:
			    #if resdata.is_noise==0:
			    self.resonatorNoise(resdata,numtraces)
			    
			    if self.thread_running==0:
			        print "Ending Loop/Thraed"
			        return
			except:
			    print "problem taking noise on resdata MKID Fc=%f"%(mkid.getFc())
			
	   		    traceback.print_exc()
			
		
			
		    
		
			
	def resonatorNoise(self, resdata,numtraces):
	
		resdata.noise_fw_index=1;


		fc=resdata.skewcircle_fr
		
		if fc==0:
			fc=resdata.rough_cent_freq
			print "Warning: using rough cent freq for noise"

		#fbase=self.frequency_list[0]
		fbase=resdata.sweep_fbase
		
		
		if self.is_resetup_noise==1:
		    #set attens to same as in the  original sweep
		    at.atten_U6=resdata.atten_U6
		    at.atten_U7=resdata.atten_U7
		    at.atten_U28=resdata.atten_U28

		    progAtten(roach,at)

		    rf.lo_internal=int(resdata.lo_internal)
		    progRFSwitches(roach,rf)

		   
		    
		    

		if resdata.isneg_freq==1:
		    carr= fc + fbase
		else:
		    carr=fc-fbase

		
		self.setCarrier(carr)

		self.stopFFTs()
		
		if self.is_resetup_noise==1:
		    self.setLutFreqs([ fbase ],resdata.lut_sine_amp*32768)
		    self.fftBinsFreqs()
		    self.roach_fft_shift=resdata.roach_fft_shift
		    
		self.fftsynctime=self.dftLen
		self.roach_num_ffts=65536
		    
		self.progRoach()
		#self.resetDAC()
		

		self.dbgappend(('resonatorNoise,fa',self.getObjSpecs()))
		self.dbgappend(('resonatorNoise,printRegs',self.printRegs(0,0)))


		progAtten(roach,at)
		progRFSwitches(roach,rf)


		for t in range(numtraces):
		    time.sleep(1.0)
		    self.trigFFT()
		    time.sleep(1.0)

		    self.getDFT_IQ();
		    #getDFT adds phase delay... not sure if it is correct..
		    #maks sure that the phse delay is the same we used in the
		    #sweep. so we must get the phse delay from resonator sweep
		    #remove delay implsed by getDFT_IQ
		    
		    #!!self.removeDelay();
		    #get delay data from resonator when we did sweep
		    

		    if resdata.num_noise_traces==0:
			resdata.fftLen=[]
			resdata.fftsynctime=[]
			resdata.fftdelay=[]
			resdata.iqnoise=[]
			resdata.iqnoise_raw=[]
			resdata.binnumber=[]
			resdata.srcfreq=[]
			resdata.noisetrace_len=[]
			resdata.fftcarrierfreq=[]


		    ##
		    ##
		    ##


		    ts=self.extractTimeSeries(self.getLegalFreqs([fbase])[0])
		    
		    #!!ts=self.calcFWDelay(ts_,fbase)
		    
		    #1st and lst noise is bad... so take them out...
		    ll=len(ts[0])
		    ts[0] = ts[0][1:(ll-2)]
		    ts[1] = ts[1][1:(ll-2)]
		    
	    	    tsr=self.PolarToRect(ts)

		    resdata.num_noise_traces=resdata.num_noise_traces+1
		    resdata.is_noise = resdata.num_noise_traces
		    resdata.fftLen.append(self.fftLen)
		    resdata.fftsynctime.append(self.fftsynctime)
		    resdata.fftdelay.append(self.delay)
		    resdata.iqnoise.append(tsr)
		    resdata.iqnoise_raw.append(ccopy.deepcopy(self.I_raw))

		    resdata.binnumber.append(self.getBinFromFreq(fbase))
		    resdata.srcfreq.append(fbase)
		    resdata.noisetrace_len.append(len(tsr[0]))
		    resdata.fftcarrierfreq.append(self.carrierfreq)
		    resdata.carrierfreq=self.carrierfreq
		    
		    self.setSweepResonator(resdata)
		    
    		    sweepCallback()
		    if self.thread_running==0:
				print "Ending Loop/Thraed"
				return

		
	#iq is noise trace or sweep trace- freq is one freq or a vector.
	#,ust be baseband freq, not rf freq.
	def calcFWDelay(self,iq,freq):
	
		
		
		if self.isneg_freq:
		    ff=-2*pi*  freq
		else:
		    ff=2*pi*  freq
		
		phasesRe= numpy.cos(ff*self.firmware_delay)
		phasesIm= numpy.sin(ff*self.firmware_delay)
		phasep=self.RectToPolar([phasesRe,phasesIm]);
		
		self.calcNsDly_php=phasep
		
		self.dbgappend( ('calcFWDelay,fa',self.getObjSpecs()) )

		
		iqp=self.RectToPolar(iq)
		
		#phasep[1] is a scalar. 
		#iqp is vector.
		iqp[1] =iqp[1] + phasep[1]
		iqp[1] = self.removeTwoPi(iqp[1])
		
		iq=self.PolarToRect(iqp)
		
		
		
		return(iq)
		
	
	
		
			
	
	def sweepAndReadout(self,mlist1):
		

		span=1e6
		pts=50
		cnt=0
		
			

		self.fft_mkid_list=[]
		for m in mlist1:
		   
	            ff=m.getFc2()
		    
		    self.fft_mkid_list.append(MKID(cnt, self.device_name,ff))
		    cnt=cnt+1

		isss_save=self.is_sweep_several
		self.is_sweep_several=1    
		self.sweepResonators(self.fft_mkid_list,span,pts)


		self.is_sweep_several= isss_save 

		for m in self.fft_mkid_list: #loops through list of resonators
		    fit.resonator=m.reslist[0]
		    fit.reslist=m.reslist
		    fit.fit_circle2(); #fit a circle to data
		    fit.trans_rot2(); #move coordinate system to center of circle
		    fit.IQvelocityCalc()

	
	
		
		
		self.roach_num_ffts=65536/len(self.fft_mkid_list)
		self.fftsynctime=self.dftLen
		
		self.progRoach()


		#use the 1st mkid to find correct carrier... no recalc yet a bit bad...
		#assume neg sideband...
		carr=self.fft_mkid_list[0].reslist[0].maxIQvel_freq + self.fft_mkid_list[0].reslist[0].sweep_fbase

		self.setCarrier(carr)
		self.TgrabData(10000)
		
		return(self.fft_mkid_list)		

	#take list if mkids and divide into short lists of mkids within bw of 200MHz, then sweep the
	#shorts lists. list of MKID objhects expeced
	def sweepResonators(self,mlist1,span,pts):
	        self.thread_running=1
		mlist=sorted(mlist1,key=MKID.getFc)
		
		short_list=[]
		fcst=0
		
		#sweep in a group. do several res at once.put several res into sublists
		#and sweep several at once. res in sublist mare in a 200MHz bandwidth
		#some wierd bug.. so disabled...
		
		if self.is_sweep_several:  
		
		    for mkid in mlist:
			if fcst==0:
		            fcst=mkid.getFc()

			if mkid.getFc()-fcst<200e6:
		            short_list.append(mkid)
			else:
		            self.sweepResonators2(short_list,span,pts)
			    short_list=[mkid]
			    fcst=0	
			    if self.thread_running==0:
				    print "Ending Loop/Thraed"
				    return

		    if len(short_list)>0:
			self.sweepResonators2(short_list,span,pts)
			
			
		#sweep one res at a time.	
		else:
			
		    for mkid in mlist:
		         self.sweepResonators2([mkid],span,pts)
			
		    
		return(mlist1)
		

	#sweep group of mkids w./ ftts bu sweeping LO. res must be all in 200MHz BW.
	#res are swept at same time. traces (resonatorData) are added to MKID objs
	def sweepResonators2(self,mkid_list,span,pts):

		

		self.stopFFTs()

		#self.zeroCoefMem()
		self.clearFIFOs();
		self.rewindFFTMem()
		self.fftBinsFreqs()

		
		
		self.sweep_num_freqs=pts;
		#self.sweep_samples_per_freq=floor(65536/self.sweep_num_freqs)
		
		
		self.roach_num_ffts=self.sweep_samples_per_freq
		self.fftsynctime=self.dftLen
		
		self.progRoach()


		###

		fc_s=[]
		for mkid in mkid_list:

		    #get rough ctne freq, or fitted freq, if available
   		    fc=mkid.getFc2()

		    fc_s.append(fc)


		fc_s=numpy.sort(fc_s)

		frange=max(fc_s) - min(fc_s)
		if (frange>200e6):
		    print "resonators too far apart, cannot sweep all of them"
		    return


		# we have wierd number so we don't have nice number of sines. We always then have some freq error based
		#based on wave tablelen. could use 10MJz, bit too nice.
		carr=max(fc_s)+10109375

		freqs=carr-fc_s
		freqs = freqs[::-1]

		print "carrier freq %d"%(carr)
		print "Base Freqs"
		print freqs
		print "Res Freqs "
		print fc_s


		###


		self.setLutFreqs(freqs,32500.0/len(freqs))

		self.fftBinsFreqs()
		#so new fw w/ phase corrector does not mess up phase... on older fw
		#does nothing.
		#self.zeroPhaseIncs()

		self.progRoach()

		self.start_carrier = carr-span/2.0
		self.end_carrier = carr+span/2.0
		self.inc_carrier = span/pts
		
		
		self.dbgappend(('sweepResonators2,fa',self.getObjSpecs()))
		self.dbgappend(('sweepResonators2,printRegs',self.printRegs(0,0)))
		
		time.sleep(1.0)
		
		progAtten(roach,at)
		progRFSwitches(roach,rf)
		
		first_trig=1;
		
		for cf in arange(
			self.start_carrier ,
			self.end_carrier,
			self.inc_carrier ):

		    self.setCarrier(cf)
		    
		    self.dbgappend(('carrier,anritsupwr',self.carrierfreq,self.anritsu_power))
		    
		    print carr
		    #progAtten(roach,at)
		    #progRFSwitches(roach,rf)
		    #self.resetDAC()
		    time.sleep(0.1)
		    
		    if first_trig==1:
		        self.trigFFT()
			first_trig=0
		    else:
		        self.retrigFFT()
			
		    time.sleep(0.1)
		    
		    if self.thread_running==0:
				print "Ending Loop/Thraed"
				return

		#we have taken 200 points, becaise some FWs may not have fifl readout yet we take
		#rest of points to fill memory, to make sure we have fifos readout. this is not used 
		#data for cal.

		
		self.roach_num_ffts=65536
		
		
		self.progRoach()
		self.retrigFFT()
			
		#now mem is fill, we can readout...
		self.getDFT_IQ();



		#because this is a sweep, we need to redo the delay phase
		#calc. because getDFT_IQ does this calc, we need to undo it.
		
		#cable time delay/phase is not valid because we jerked carrier freq. So we have to recalc.
		#we remove the phase delay calc to get back to raw data.
		#the problem is that we do one getDFT_IQ and one applyDelay for all the points, meaning
		#that we ahve the wrong carrier freq for most of the tones. The carrier freq must be an 
		#array,,,The ADC dekays are left in there. the data are many spectra w. one point each
		#or many spectera w. a point per mkid, for a few points
		
		if self.is_apply_delay==1:		  
		    self.removeLineDelay()
		
		
		print "carrier freq %d"%(carr)
		print "Base Freqs"
		print freqs
		print "Res Freqs "
		print fc_s


		
		
		for fbase in self.frequency_list:
		    trace=self.getResonator(fbase)
		    #as resonators are out of order and sorted... we find which mkid in list goes w. this trace
		    
		    res_fc=median(trace.freqs)
		    
		    #start w. bug error, and assume trace goes to mkid 0.
		    err=[0,100e9]
		    #test all mkids
		    for k in range(len(mkid_list)):
		    	mkid=mkid_list[k]
			#calc diff in freq between trace and the mkid cent freq.
		        df=abs(mkid.rough_cent_freq - res_fc)
			#if diff in freq<error, then mkid k is better choice for this trace
			if err[1]>df:
			    err=[k,df]
			    
		    
		    mkid_list[err[0]].addRes(trace)
			
		    
		
		sweepCallback()
		#dones nothing here- for later i FW
		#self.reprogPhaseIncs()
		
		return(mkid_list)



	def getResonator(self,fbase):
		res=resonatorData(self.resonator_number, self.device_name);
		self.rescnt=self.rescnt+1;
		
		
		#tell that we used fftanal fw for sweep
		res.sweep_fw_index=1

		
		fbase= self.getLegalFreqs([fbase])[0]
		
		res.sweep_fbase=fbase
		res.sweep_binnumber=self.getBinFromFreq(fbase)
		
		
		carrfs=arange(self.start_carrier,self.end_carrier, self.inc_carrier)
		if self.isneg_freq==1:
		    freqs=carrfs - fbase
		else:
		    freqs=carrfs +fbase	
		    
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
		
		bins_all=self.extractBinSeries(fbase)
		
		#self.fpga_bug_offset=0;
		
		
		#bins_all when plotted will look like the resonator response vs freq
		#plus all the extra points we csampled. we only want the 200
		#or so points we swept with. if we take many ffts per
		# freq point then we can average these together, or just take 
		#the first one. we call a function to extract the bins we want
		#len(freqs)is 200 if we swept 200 points
		bins_=self.getResSweep(
			num_sweep_points,
			self.sweep_samples_per_freq,
			bins_all)
		
		
		
		#self.fpga_bug_offset = fpga_bug_offset_save
		
		#now calc new bins w/ correct phase delay calc.
		
		
		#calc correct phase delay- this deals wiht the fact that we havve a swept
		#LO, and the getDFT function did not account for swept LO
		# we must call removeLineDelay before this can be corect.
		#bins=self.calcXmissnLineDelay(bins_,freqs)
		
		iqp=fa.RectToPolar(bins_)
		
		if self.is_apply_delay==1:
		    iqp=fa.calcLineSweepDelay(iqp,fbase)
		 
		bins=fa.PolarToRect(iqp)
		
		
		
		
		
		#bug where 1st pt in the spectrum is 0, so set it to 2nd pt.
		bins[0][0]=bins[0][1]
		bins[1][0]=bins[1][1]
		
		res.setData(bins, freqs, self.delay,self.carrierfreq)
		
		res.IQ_raw = ccopy.deepcopy(self.I_raw)
		
		res.isneg_freq=self.isneg_freq
		
		#if self.isneg_freq==1:
		#	res.fliplr()
		
		
		
		
		#copy a bunch of fields to the res object.
		res.anritsu_power= self.anritsu_power
		
		
		res.atten_U6=at.atten_U6
		res.atten_U7=at.atten_U7
		res.atten_U28=at.atten_U28


		res.baseband_loop=rf.baseband_loop
		res.rf_loopback=rf.rf_loopback
		res.clk_internal=rf.clk_internal
		res.lo_internal=rf.lo_internal
		res.lo_source = rf.lo_source


		res.dac_sine_sweep_amp = self.dac_sine_sweep_amp


		res.dftLen =self.dftLen
		res.sd_mod=self.sd_mod

		res.fftsynctime= self.fftsynctime
		
		res.is_noise = 0
		    
		res.firmware_delay=self.firmware_delay
		
		
		res.xmission_line_delay=self.xmission_line_delay

		res.roach_fft_shift = self.roach_fft_shift
			
		res.lut_sine_amp = self.lut_sine_amp
		
			
		return(res)








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












	#given an rf freq, take carrierfreq, and figure out which baseband freq is doing thisone.
	#it sources approx freq... find the one...
	def findBasebandFreq(self,rffreq):
	
		if self.isneg_freq==1:
		    fbase=self.carrierfreq - rffreq
		else:
		    fbase = rffreq - self.carrierfreq
		    
		
		
		maxdf=[0.0,1e9]
		
		for f in self.frequency_list:
		    df=abs(f-fbase)
		    
		    if df<maxdf[1]: 
		        maxdf[1]=df;
			maxdf[0]=f
			
		return(maxdf[0])
		
		
		



	def powerSweep(self,attInSt,attSt,attEd,step,sweeps,span,mkidlist):

	    
	    self.attInStart=attInSt
	    self.attStart=attSt
	    self.attEnd=attEd
	    self.numSweeps=sweeps
	    self.res_span = span
	    self.attIncr= step
	
	    self.markerlistx=mkidlist
	    
	    self.dbgappend(('PowerSweep'))
	    
            print "Starting FFT  Power Sweep " 
            self.powerSweep3()



	def powerSweep3(self):
	    self.thread_running=1
	    #markerlist is really MKID objhects

	    self.thread_running=1
	    
	    
	    atin=self.attInStart
	    
	    
	    
	    
	    
	    for atx in arange(self.attStart,self.attEnd+1,self.attIncr):
		print 'Atten Out %f, Atten In %f'%(atx,atin)
	
		#at.atten_U6=0;
		at.atten_U7=atx;
		at.atten_U28=atin
		
		progAtten(roach,at);
		progRFSwitches(roach,rf)
		
		time.sleep(1)
		
		
		
		for k in range(self.numSweeps):
			self.sweepResonators(self.markerlistx,self.res_span,200)
			sweepCallback()
			self.sweepcount=self.sweepcount+1
			if self.thread_running==0:
				print "Ending Loop/Thraed"
				return
		
		
		atin=atin-self.attIncr	
	



	#iqdata has raw fft coeff. we have mixed up bins, and several spectra stored.
	# we extract spectra, and put into a 2k array so it looks like a spectruym
	#spec_num is time offset, which spectrum in the iqdata array
	#return POLAR coords
	def extractSpectrum(self,spec_num):
	

	    recordlen=self.getRecordLen()

	    spectrum_R=zeros(self.fftLen)
	    spectrum_I=zeros(self.fftLen)

	    st=spec_num*recordlen;
	    ed=st + recordlen;
	    record_R=self.iqdata[0][ st:ed]
	    record_I=self.iqdata[1][ st:ed]

		#dreop the 1st record.. get wierd phase paroblem
	    for k in range(recordlen):
		    i=self.fft_bins_requested[k];
		    spectrum_R[i]=record_R[k]
		    spectrum_I[i]=record_I[k]

	    

	    #put in freq order. We have carrier or DC at bin fftLen/2. bins 0-fftLen/2 are
	    #right of DC. bins fftLen/2 are reverszed order (they are negative freqs), and put on left of DC.
	    left=spectrum_R[(self.fftLen/2):]
	    right=spectrum_R[:(self.fftLen/2)]
	    spectrum_R=numpy.concatenate((left,right))
	    

	    left=spectrum_I[(self.fftLen/2):]
	    right=spectrum_I[:(self.fftLen/2)]
	    spectrum_I=numpy.concatenate((left,right))

	    sP=self.RectToPolar([spectrum_R,spectrum_I])
	    #return([spectrum_R,spectrum_I])
	    return(sP)


	#say we readback 20 bins. then we make time series of one of these bins.
	#We supply freq, that is the freq in Hz we soured. If we are actually reading ot that bin,
	#then we retrive all samples of that bin and return in polar coord
	def extractTimeSeries(self,freq):

	    binIQ=self.extractBinSeries(freq)

	    #convert to polar, mag and phase
	    bP=self.RectToPolar(binIQ)

	    #
	    # Calc extected phase inc per fft, and remove it., then we can see only freq changes, phase changes
	    #
	    phaseperfft=self.getPhasePerFFT(freq)


	    phaseterm = bP[1]

	    ramp = phaseperfft * arange(len(phaseterm))

	    if self.isneg_freq==0:
	        phaseterm=phaseterm-ramp
	    
	    else:
	        phaseterm=phaseterm+ramp
		
	    #sub 1st point, to offset from 0 phase
	    #phaseterm = phaseterm-numpy.median(phaseterm)
	    #make phase around pi, so we dont wrap to 6.28 when removing multipiples of 2pi	    
	    #phaseterm = phaseterm+pi
	
		#take out multiples of 2pi
	    phaseterm= 2*pi * (  (phaseterm/(2.0*pi) )- floor(phaseterm/(2.0*pi))  )
	    #now make around 0 radians
	    #phaseterm=phaseterm-pi

	    


	    bP[1] = phaseterm
	    
	    #bP[0]= bP[0] - bP[0][0]
	    
	    return(bP)	    


	#set in sec
	#sets delay in sec and calcs the delay phase vector
	def setDelay(self,d):
		#760e9 is ADC/DAC time delay in ns- we add that to xmission line dly
		#this is for ADCDAC and FFT andpol;yphase filter 
		self.xmission_line_delay=d
		self.delay=d+self.firmware_delay

		self.calcLineFPGADelay()


	#calcs the delay phase vector used when applyDelay
	
	def calcLineFPGADelay(self):
	
		
		
		#we di bit want bin center freq. we want the sourced freqs...
		# we have higher freq resolution in the lut than we do in the fft.
		#sourced freqs, and hence phase delay, are based on actual sourced freq.
		#sourced freqs are not in bin centers
		
		
		#get center freq of bins
		flist1 = self.getFreqsFromBins(self.fft_bins_requested)
		
		#get freqs we source...
		flist2 = self.frequency_list
		
		#if we are asking for all bins, then let flist be the ffr bins.
		if len(flist1)>len(flist2):
		    flist = flist1
		else:
		    #if we are getting just freqs of interest, then we use the sourced frequencuies
		    flist = flist2
		
		
		flist = numpy.array(flist)

		if self.isneg_freq:
		    #freqs=-2*pi*  (self.carrierfreq - flist)
		    freqs=2*pi*  (self.carrierfreq - flist)
		else:
		    freqs=2*pi*  (self.carrierfreq + flist) 
		
		
		
		#calc phase shift for baseband.We assyme all delay for FW is in DAC, and not in DAC +ADC
		#what if freqs are negative? If we have pos freqs, we use negative sideband...
		#phasesRe_fw= numpy.cos(flist*self.firmware_delay)
		#phasesIm_fw= numpy.sin(flist*self.firmware_delay)
		
		
		
		
		#phFwP=self.RectToPolar([phasesRe_fw, phasesIm_fw])
		
		
		
		#phasesRe_xl= numpy.cos(freqs*self.xmission_line_delay)
		#phasesIm_xl= numpy.sin(freqs*self.xmission_line_delay)

		#phXlP=self.RectToPolar([phasesRe_xl,phasesIm_xl  ])
		
		
		
		#phases=phXlP[1] +  phFwP[1]
		
		#the mags should all be one, for both fw and xl, so just use xl mags..
		#phasesP=[ phXlP[0] ,phases]
		#phasesR=self.PolarToRect(phasesP)
		self.phasesRe=numpy.cos(freqs*self.xmission_line_delay + flist*self.firmware_delay)
		self.phasesIm = numpy.sin(freqs*self.xmission_line_delay + flist*self.firmware_delay)
		
		

	def calcLineDelay(self):
	
		
		
		#we di bit want bin center freq. we want the sourced freqs...
		# we have higher freq resolution in the lut than we do in the fft.
		#sourced freqs, and hence phase delay, are based on actual sourced freq.
		#sourced freqs are not in bin centers
		
		
		#get center freq of bins
		flist1 = self.getFreqsFromBins(self.fft_bins_requested)
		
		#get freqs we source...
		flist2 = self.frequency_list
		
		#if we are asking for all bins, then let flist be the ffr bins.
		if len(flist1)>len(flist2):
		    flist = flist1
		else:
		    #if we are getting just freqs of interest, then we use the sourced frequencuies
		    flist = flist2
		
		
		flist = numpy.array(flist)

		if self.isneg_freq:
		    #freqs=-2*pi*  (self.carrierfreq - flist)
		    freqs=2*pi*  (self.carrierfreq - flist)
		else:
		    freqs=2*pi*  (self.carrierfreq + flist) 
		
		
		
	
		
		self.phasesRe=   numpy.cos(freqs*self.xmission_line_delay)
		self.phasesIm=   numpy.sin(freqs*self.xmission_line_delay)




	def calcLineSweepDelay(self,iqp,bbfreq):
	
			
		#we di bit want bin center freq. we want the sourced freqs...
		# we have higher freq resolution in the lut than we do in the fft.
		#sourced freqs, and hence phase delay, are based on actual sourced freq.
		#sourced freqs are not in bin centers
		
		
		carr=arange(self.start_carrier,self.end_carrier,self.inc_carrier)
		if self.isneg_freq==1:
			freqs=carr - bbfreq
		else:
			freqs=carr + bbfreq
		
		ft=freqs*self.xmission_line_delay;
		ft = ft - floor(ft);
		
		iqp[1] = iqp[1] + 2*pi*ft;

		return(iqp)
	



	

	############################################3
	#
	########################################33			
		
	def getRecordLen(self):
	    recordlen=len(self.fft_bins_requested)
	    return(recordlen)
	    	


	#say we readback 20 bins. then we make time series of one of these bins.
	#We supply freq, that is the freq in Hz we soured. If we are actually reading ot that bin,
	#then we retrive all samples of that bin and return in polar coord
	def extractBinSeries(self,freq):

	    freq=self.getLegalFreqs([freq])[0]
	    #recordlen=self.getRecordLen()

	    
	    
 	    nspectra= self.getNumSpectra()
		
	    #find which bin in fft this freq cooresponds to
	    whichbin=self.getBinFromFreq(freq)

	    
	    
	    #look in bin list to make sure it is in there. if so, get the index in the binlist.
	    #the index will be offset in the records returned by roach.

	    aa=where(array(self.fft_bins_requested)==whichbin)[0]
	    if len(aa)==0:
		print "Error- that freq not in the binlist"
		return

	    binindex = aa[0]


	    binR=zeros(nspectra)
	    binI=zeros(nspectra)

	    #
	    #extract the bin we want and make into a array, R and I.
	    #

	    for spec in range(0,nspectra):
		#st=spec*recordlen
		#ed=st+recordlen
		#record_R=self.iqdata[0][ st:ed]
		#record_I=self.iqdata[1][ st:ed]
		record=self.extractRecord(spec)
		try:
		    binR[spec]=record[0][binindex]
		    binI[spec]=record[1][binindex]
	        except:
		    binR[spec]=0
		    binI[spec]=0

	    return([binR,binI])






	#mem 0,1 are i0,1,2,3. iqsel gets 0 or 1, 2 or 3. mem 2,3 is q0,1,2,3.
	#ireturns [i,q]. you pick 0,1,2,3 for which i and q output.
	def captureADC_IQ(self,iqsel):
	
		if (iqsel==0 or iqsel==2):
		    self.trigADCMem(0);
		else:
		    self.trigADCMem(1);
		
		
		if (iqsel==0 or iqsel==1):
		    i=self.readADC(0)
		else:
		    i=self.readADC(1)
		    
		
		if (iqsel==0 or iqsel==1):
		    q=self.readADC(2)
		else:
		    q=self.readADC(3)
			    
		return([i,q])
		
	
	def zeroCoefMem(self):
	
		roachlock.acquire()
		bzeros=self.convertToBinary(zeros(self.memLen))
		try:
		    self.roach.write('MemRecordReal_%s'%(ramname),bzeros)
		    self.roach.write('MemRecordImag_%s'%(ramname),bzeros)
		except:
		    print "zeromem error"
		    
		roachlock.release()
	
	def getDFTdata(self,output):

		#for debugging so we can see last read from mem
      		global aa;
		
		#I even re, even im, odd re, odd im
		regnames=[
		'MemRecordReal_%s'%(ramname),
		'MemRecordImag_%s'%(ramname),
		]
		
		aa=struct.unpack('>'+'I'*self.memLen,roach.read(regnames[output],4*self.memLen))
		
#aa=struct.unpack('>'+'I'*fa.memLen,roach.read(regnames[output],4*(fa.dftLen/4)))
		
		dftmem=[]
		odd=output&0x1
		
		for i in range(self.memLen):
		
			
			fracpart=int(aa[i]&0x0001ffff)
			signbit=int(aa[i]&0x00020000)
			
			
			val = -1.0*float(signbit>>17) + float(fracpart)/math.pow(2.0,17)
			
			#if sgn!=0:
			#	val = val -1.0
				
			#val = float(aa[1])/self.memLen.0
			
			dftmem.append(val)

		
		#hw bug in the roach makes last sample jump.
		
		#dftmem[ self.memLen-1]=dftmem[ self.memLen-2]
		return(numpy.array(dftmem))

	
	# execfile('t_brdconfig.py')
	# na=networkAnalyzer(roach)
	
	
	
	
	
	
	#make comb freq based on lut lookupfreq
	def setLutComb(self,cf_Hz, bw_Hz, amp):
	
		resolution = self.getResolution()
	
		ff= arange( cf_Hz - bw_Hz/2.0, cf_Hz + bw_Hz/2.0, resolution ).tolist()
		
		self.setLutFreqs(ff,amp)
		
	
	
	#make sets of combs based on list of freq. freqs are center freq of comb. 
	#set bins, to make freqs in adj bins. set nbins to 2 so 2 bins on either side have signal
	def setLutFreqsBins(self,freqs,nbins,amp):
	
		freqs=self.getLegalFreqs(freqs)
	
		freqs2=[]
		
		fres=self.getFFTResolution()
		
		#make new freqs list. add in orig list, and so many bins offset freq on both sides
		for f in freqs:
		    freqs2.append(f)
	    
		    for b in range(nbins):
		        freqs2.append(f + (1+b)*fres)
			freqs2.append(f - (1+b)*fres)
			
		
		#make sure new list is legal freq
		freqs2=self.getLegalFreqs(freqs2)
		
		
		#remoce any duplicates
		freqs2=list(set(freqs2))
		
		freqs2=sort(freqs2)
		self.setLutFreqs(freqs2,amp)
		
	
	
	
	def setLutChirp(self,cf_Hz, bw_Hz,amp):


	    #freq in radians per sample
	    freq=  (2.0*numpy.pi/ self.dac_clk) * arange( cf_Hz - bw_Hz/2.0, cf_Hz + bw_Hz/2.0, bw_Hz/self.lut_length  )



	    time=arange(self.lut_length)

	    wt=freq * time


	    self.lut_i = amp * numpy.cos(wt)
	    self.lut_q = self.Q_amp_factor * amp * numpy.sin(wt + numpy.pi*self.Q_phase_offs/180.0)



	    self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
	    #self.progRoach()
	    self.progDRAM()

	    self.calcLineFPGADelay()


	
	#applues dekat to cur iqdata
	
	def applyDelay(self):
		self.calcLineFPGADelay()
		
		
		print "apply delay"

		phasep=self.RectToPolar([self.phasesRe,self.phasesIm]);
		
		
		self.dbgappend(('applyDelay,phasep,freqs,carr',phasep,self.frequency_list,self.carrierfreq))

		for k in range(self.getNumSpectra()):
		    rec=self.extractRecord(k);
		    iqp=self.RectToPolar(rec)
		    iqp[1] = iqp[1] + phasep[1]
		    iqdelay=self.PolarToRect(iqp)		    
		    self.replaceRecord(k,iqdelay)
	
	
	
	def removeLineDelay(self):
		
		
		    
		
		self.calcLineDelay()


		phasep=self.RectToPolar([self.phasesRe,self.phasesIm]);
		
		self.dbgappend( ('removeDelayphase',phasep) )
		
		for k in range(self.getNumSpectra()):
		    rec=self.extractRecord(k);
		    iqp=self.RectToPolar(rec)
		    iqp[1] = iqp[1] - phasep[1]
		    iqdelay=self.PolarToRect(iqp)		    
		    self.replaceRecord(k,iqdelay)
		    
		#recalc total delay...    
		self.calcLineFPGADelay()
	
	
	#give actual freqs in Hz, baseband + carrier. give complex spectrino as [i,q]
	def calcXmissnLineDelay(self,iq,freqs):
	
		
		
		if self.isneg_freq:
		    ff=-2*pi*  freqs
		else:
		    ff=2*pi*  freqs
		
		phasesRe= numpy.cos(ff*self.xmission_line_delay)
		phasesIm= numpy.sin(ff*self.xmission_line_delay)
		phasep=self.RectToPolar([phasesRe,phasesIm]);
		
		self.calcSwDly_php=phasep
		
		self.dbgappend( ('calcXmissnLineDelay,fa',self.getObjSpecs()) )

		
		iqp=self.RectToPolar(iq)
		
		iqp[1] =iqp[1] + phasep[1]
		iqp[1] = self.removeTwoPi(iqp[1])
		
		iq=self.PolarToRect(iqp)
		
		
		
		return(iq)
		
		
	

	
	
	
	def getDFT_IQ(self):
	
		global sweep_counter
		
		
		
		if self.is_read_dump_file==1:
		    self.hdfReadIQ()
		    re=self.I_raw[0]
		    im=self.I_raw[1]
		else:
		    re=self.getDFTdata(0)	
		    im=self.getDFTdata(1)

		
		self.Q_raw=[ccopy.deepcopy(re), ccopy.deepcopy(im)]
		self.I_raw=self.Q_raw
		
		
		
		
		self.iqdata=[re,im]
		
		#apply the phase delay die to xmission cable length.
		#this wont be valid for sweeps, where the carrierfreq is change for each fft.
		#in this case we need to removeDelay, then calcXmissnLineDelay()
		if self.is_apply_delay==1:
		    self.applyDelay()
		
		
		
		self.dbgappend(('getDFTIQ,fa',self.getObjSpecs()))
		
		
		self.hdfWrite()
		
		sweep_counter=sweep_counter+1

		
		
		
		return(self.iqdata)
		#return([re,im])


	

	
	
	# execfile('t_brdconfig.py')
	# na=networkAnalyzer(roach)
	
		
	def sendBinFlags(self):
		#clear the rams
	    try:
		self.roach.write('BinData',self.convertToBinary8([0]*4096));
		self.roach.write('BinData',self.convertToBinary8([0]*4096));
	
	
		self.roach.write('BinData',self.convertToBinary8(self.fft_bin_flags));
				#
		# figure out what goes in the binread ram. 
		#    
	
		self.binReadRam=[0]*len(self.fft_bin_list)
		
		#fft_bins_requested bin numbers that are returned in the data in each record. this is final outmem
		#like 2,65
		#fft_bin_list are bins in groups of 4, that are read from FFt to fifo. like 0,1,2,3,64,65,66
		for bl in self.fft_bins_requested:
		    if bl in self.fft_bin_list:
		        indx=self.fft_bin_list.index(bl)
			self.binReadRam[indx]=1
			

		#clear binread out ram.
		
		self.roach.write('BinReadOut',self.convertToBinary8(zeros(4096)));
		#write the fft bin readout flags, this is after fifo.
		self.roach.write('BinReadOut',self.convertToBinary8(self.binReadRam));
	    except:
	        print "No ROACH"

	def progRoach(self):
	    
	    self.calcRegs()	
		
	    if self.is_print==1:
		msg='controlReg %d\n'%(self.controlReg)
		print msg
	    
	    roachlock.acquire()
	    try:
		
		self.roach.write_int('controlReg', self.controlReg)

		#!!self.roach.write_int('dram_controller', 0)
		
		#1 to stop lut playback
		self.roach.write_int('holdcounter', self.holdcounter)
		#1 to erase lut dram
		self.roach.write_int('resetDRAM', self.resetDRAM)
		
		#need to write -1 because of = in the fpga code...
		self.roach.write_int('fftsynctime',self.fftsynctime-1);
	
		
		self.roach.write_int('fftshift',self.roach_fft_shift)

		self.roach.write_int('numffts',self.roach_num_ffts)
		
		#needs to be 1 all times. we readn in FW. SW interface writes it...
		#1 for readout dram
		self.roach.write('RWen', '\x00\x00\x00\x01')
		self.roach.write_int('LUTsize', self.lut_length8)
		
		#self.roach.write('dram_memory', self.lut_binaryIQ)
		
		#self.big_write(self.lut_binaryIQ)
		self.startOutputDac=0
		self.calcRegs();
		
		self.roach.write_int('controlReg', self.controlReg)
		
		self.startOutputDac=1
		self.calcRegs();
		
		self.roach.write_int('controlReg', self.controlReg)
		
		
		
		self.sendBinFlags()
		self.numBinsStored=len(self.fft_bin_list)
		
		self.roach.write_int('numBinsStored', self.numBinsStored)
	

	    except:
	        print "NO ROACH"

	    roachlock.release()
	           
	    	
		
	def setOutDacReg(self,val):	
	
	    roachlock.acquire()
	    try:
		
		self.startOutputDac=val;
		self.roach.write_int('startDacReg', self.startOutputDac);
			
	    except:
	        print "could not write start dac to roach"
		
	    roachlock.release()
	    
	    
	    

	def rewindFFTMem(self):
		self.stopFFTs()
		roachlock.acquire()
		
		
		self.st_fft_mem=1 		
		self.progRoach1()
		
		self.st_fft_mem=0 		
		self.progRoach1()
		#self.roach.write_int('numBinsStored',self.numBinsStored )
		roachlock.release()
	
	
	
	def printRegs(self,isprint, isplot):
		#roachlock.acquire()
		
		
		#create inline class
		class inline: pass
		
		
		regdata=inline()
		
		
		regdata.at= ccopy.deepcopy(at)
		regdata.rf=ccopy.deepcopy(rf)
		
		regdata.LO=ccopy.deepcopy(LO)
		regdata.s=ccopy.deepcopy(s)
		
		#try:
		if 1==1:
		    regs=[ 'controlReg','fftcounter_out','fftshift','fftsynctime','holdcounter',
			    'if_switch','numBinsStored','numffts','stffts_fsm','statusFlags','LUTsize',
			    'MemRecordImag_coefRamAddr','MemRecordReal_coefRamAddr','RWen','binRdOutCnt'
			    ,'bincount_out']

		    for rr in regs:
		    	val=roach.read_int(rr)
			if isprint==1: print '%s  0x%x, %d'%(rr, val,val)
			exec('regdata.%s=%d'%(rr,val))



		    crval=roach.read_int('controlReg')
		    crbits=['mainRst','stFFTMem','fftMemWE','seeaddress','startDac','unused',
		    'startFFTs','adcwavememStart','adcwavememWE','adcwavememSel','unused','unused',
		    'adcforcesync','dacLoopBack','useTestFreq','resetDAC','dumpFIFO']

		    if isprint==1: print '\nControReg Bits\n'
		    bitlist=[]
		    for k in range(len(crbits)):
			mask=1<<k
			if isprint==1: print '    Bit:%d %s  %d'%(k, crbits[k], crval&mask)
			bitlist.append((k,crbits[k],crval&mask))
			
		    regdata.bitlist = bitlist
		    

		    stval=roach.read_int('statusFlags')
		    stbits=['unused','adcwavememDone','adcvalid','run_ffts','fifoOutWr','fftwesync',
		    'fftcoefsync','fftcntdone']

		    if isprint==1: print '\nStatus Flags \n'
		    statbits=[]
		    for k in range(len(stbits)):
			mask=1<<k
			if isprint==1: print '    Bit:%d %s  %d'%(k, stbits[k], stval&mask)
			statbits.append((k, stbits[k], stval&mask))

		    regdata.statbits=statbits
		    
		    
		    if isplot>0:

			#reg name, char len, type, tyoe len
			mems=[('BinData',4096,'B',4096),
		    	      ('BinReadOut',4096,'B',4096),
			      ('MemRecordImag_Shared_BRAM',65536*4,'I',65536),
			      ('MemRecordReal_Shared_BRAM',65536*4,'I',65536)]


			for k in range(len(mems)):
		            if isprint==1: figure(k+1);clf();
			    if isprint==1: print mems[k]
		            a=struct.unpack(mems[k][2]*mems[k][3],roach.read(mems[k][0],mems[k][1]))
		            if isprint==1: plot(a)
		            if isprint==1: title(mems[k][0])
			    
			    exec('regdata.%s=a'%(mems[k][0]))


		else:
		    pass
		#except:
			
			
		
		
		#roachlock.release()
		return(regdata)

	def stopFFTs(self):
		
		roachlock.acquire()		
		self.fft_mem_we=0
		self.start_ffts=1 	
		self.progRoach1()
		roachlock.release()
		#self.setOutDacReg(0)
		

	def trigFFT(self):
		self.stopFFTs()
		self.clearFIFOs();
		self.rewindFFTMem()
		self.trigFFT2()
		
		
	def retrigFFT(self):
		self.stopFFTs()
		self.trigFFT2()
			

	def clearFIFOs(self):
		#self.setOutDacReg(0)
		self.stopFFTs()
		roachlock.acquire()
		self.dump_fifo = 1
		self.progRoach1()


		self.dump_fifo = 0
		self.progRoach1()
		
		#self.roach.write_int('numBinsStored',self.numBinsStored )
		roachlock.release()
	
	def trigFFT2(self):
	    
	    roachlock.acquire()
	    
	    try:
	    
		#make sure whole fifo is read out and them some
		self.roach.write_int('numBinsStored', 1024)
		
		
		
		
		self.fft_mem_we=0
		
		
	
		self.roach.write_int('numBinsStored',self.numBinsStored )
		
		self.start_ffts=1 
			
		self.progRoach1()
		
		self.start_ffts=0
				
		self.progRoach1()
		
		self.fft_mem_we=1
		self.progRoach1()
		#self.setOutDacReg(1)
	    except:
	        print "NO ROACH"
	    
	    roachlock.release()

	   
		


	def calcRegs(self):
		
		
		
		self.controlReg= (self.msm_rst<<0) 
		self.controlReg = self.controlReg + (self.startOutputDac<<4 ) 
		self.controlReg = self.controlReg + (self.st_fft_mem<<1) + (self.fft_mem_we<<2)
		self.controlReg = self.controlReg + (self.adcmem_start<<7) + (self.adcmem_wr<<8)
		self.controlReg = self.controlReg + (self.adcmem_sel<<9) + (self.adcfsync<<12)
		self.controlReg = self.controlReg + (self.adc_nloopback<<13)
		self.controlReg = self.controlReg + (self.seeaddress<<3)
		self.controlReg = self.controlReg + (self.dac_reset_bit<<15)
		
		self.controlReg = self.controlReg + (self.dump_fifo<<16)
		
		self.controlReg = self.controlReg + (self.start_ffts<<6)
		
	
	def hdfWrite(self):
	
	    if (self.hdffile!=None):
	    
	        
	    
		
		#!!print "fftAnalyzerd, write to HDF"
		#make a copy of this object, minux some of the stuff we done need
		#an inline classs
		mydata = self.getObjSpecs()
		
	
	
	
		# for puicking the file... hdf5 bug...
		if False:		
			if len(self.backupobjs)<20:
		
			    self.backupobjs.append(mydata)
			else:
			    pickle.dump(self.backupobjs,
				open('%s%d'%(self.backupfilename,sweep_counter),'wb'))
			    self.backupobjs=[]
			    self.backupobjs.append(mydata)
			#end picking
	
	
	
	
        	grpname = 'FFTSweep_%d'%(sweep_counter)
		#self.iq_index = self.iq_index + 1
		self.hdfWriteObj(self.hdffile,grpname, mydata)
    	
		
	def hdfWriteObj(self,parent, grpname,mydata):
		print '&&&&&&&&&&&&&'	
		print parent
		print grpname
		#print mydata
		#report(mydata)
	
        	#grpname = 'FFTSweep_%d'%(sweep_counter)
		#self.iq_index = self.iq_index + 1
	
    		grp=parent.create_group(grpname)

		grp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
	
   		contents= inspect.getmembers(mydata)
		for c in contents:
		    #print c

		    if inspect.ismethod(c[1])==False:

			#if we hagve list or array, we figure out dimensions. 
			# we can have list of lists, or list of arrays, but not list of dicts
			#we assume it is a list of equal len arrays. 
			if type(c[1])==list or type(c[1])==numpy.ndarray:
			    
			    #!!print "list %s"%(c[0])
			    is_multi_dim = self.isListOfLists(c[1])

			    if is_multi_dim:
				    #!!print '=====ListofLists======='
				    #!!print c[0]
				    myobj=inline()
				    for kk in range(len(c[1])):			
					
					keystr = '_%d'%(kk)	
					#!!print keystr
					exec(  'myobj.%s=c[1][kk]'%(keystr) )
				
				    
				    self.hdfWriteObj(grp, c[0],myobj)
			    else:	
			   
			        #!!print "----WRITE Array----"
			    	
			        dims=[1,len(c[1])]
    	        	   	ds = grp.create_dataset(c[0], dims, dtype='f8', maxshape=dims)
								
				ds[:]=c[1][:]
				#!!print size(ds)
			    
			  

			#for dict, we make a group, then call this function again.
			elif type(c[1])==dict:
			    
			    #!!print '=====dict======='
			    #!!print c[0]
			    myobj=inline()
			    for kk in c[1].keys():			
				if type(kk)==str:
				    keystr = kk
			   	else:
				    keystr = '_%d'%(kk)	
				#!!print keystr
				exec(  'myobj.%s=c[1][kk]'%(keystr) )
				
			    
			    self.hdfWriteObj(grp, c[0],myobj)



			#here we store ints and float scalars, assume no other types besides lists
    			elif (c[0]!= '__doc__' and c[0]!='__module__'):
			   #print 'scalar'
			   dims=[1]
    	        	   ds = grp.create_dataset(c[0], dims, dtype='f8', maxshape=dims)
			   #!!print size(ds)
			   #!!print ds
			   #!!print 'data:'
			   #!!print c
			   #!!print type(c[1])

			   
			   ds[0]=float(c[1])
			   #print ds
		try:
		    self.hdffile.flush()
		except:
		    pass
		

	def isListOfLists(self,lst):
		ans=False
		for x in lst:
		    if type(x)==list or type(x)==numpy.ndarray:
			ans=True

		return(ans)





	def hdfClose(self):
		if self.hdffile!=None:
			self.hdffile.flush()
			self.hdffile.close()
		
	    		pickle.dump(self.backupobjs,open(self.backupfilename,'wb'))

			
		if self.hdffile_r!=None:
			
			self.hdffile_r.close()
			
		self.hdffile=None
		self.hdffile_r=None	   
	
		self.iq_index=0
		self.set_index=0	
    
	def hdfOpenR(self,name,number):
		
		print 'Attempt to open file %s_%05d.hdf'%(name,number)
		self.hdfClose()


		self.hdffile_r = h5py.File('%s_%05d.hdf'%(name,number),'r')


		print self.hdffile_r.keys()

		self.iq_index=0
		self.set_index=0	






	def hdfOpen(self,name,number):
	   
	 
	     #because of a bug in h5py, we have been losing data..
	    self.backupobjs=[]
		
	    self.backupfilename = '%s_%05d.pickle'%(name,number	)	
		
	    self.hdfClose()
	    self.hdffile = h5py.File('%s_%05d.hdf'%(name,number),'a')

	    print self.hdffile
		 
	
		    
	    
	    self.iq_index=0
	    self.set_index=0
	    
		 
			
	def hdfReadIQ(self):

	
    	

            grp = 'FFTSweep_%d'%(self.iq_index)
	    
	    
	    self.iq_index = self.iq_index + 1
	
	    #make a copy of THIW obhect. we cahre not for the values of the
	    #fields, but we want the obhect structuyre. Then we can find
	    #the structure in HDF. We do not search HDF, we search the obhect,
	    #and find value in the HDF and assign.
	    
	    mydata = self.getObjSpecs()
   	    contents= inspect.getmembers(mydata)
	    for c in contents:

		if inspect.ismethod(c[1])==False:

		    #print c[0]
		    
		    if type(c[1])==list or type(c[1])==numpy.ndarray:
		      #print 'list'
		      #print c[0]
		      try:
			dims=[]
			dims.append(len(c[1]))
			dd=c[1]

			if len(dd)>0:
			  #rint type(dd)
 			  while type(dd[0])==list or type(dd[0])==numpy.ndarray:
 			    dims.append(len(dd[0]))
			    if len(dd[0])>0:
				dd=dd[0]
				#print type(dd)
			    else:
				break

			#print dims

			if len(dims)==1:		    	
		            val=zeros(len(self.hdffile_r[grp][c[0]]))
			else:
		            val=range(len(self.hdffile_r[grp][c[0]]))
			    #for vv in val: vv=arange(dims[1])


			exec( 'val[0:]=self.hdffile_r[grp][c[0]][0:]')
			exec(  'mydata.%s=val'%(c[0]) )
			
			
			#print 'listdata'
			#print val
			
			
			#c[1][0:]= parent[grp][c[0]][0:]
		      except:
			pass 




    		    elif (c[0]!= '__doc__' and c[0]!='__module__'):
		       #print 'scalar'
		       dims=[1]

		       try:
			   val =self.hdffile_r[grp][c[0]][0]
    	        	  
			   #print c[0]
			   #print val

			  

			   
			   
			   exec('mydata.%s=val'%(c[0]))
		       except:
			   pass



	    self.hdfspecs=mydata
	    self.setObjSpecs(mydata)
	   
		   		
	    return(mydata)







	def plotIQCircle(self):
	
	    resdata = self.sweepres

	    ts=self.extractTimeSeries(self.frequency_list[0])
	    tsr=self.PolarToRect(ts)
	    tsr_tr=fit.trans_rot3(resdata, tsr)

	    figure(15);clf()
  
	    plot(resdata.trot_xf,resdata.trot_yf,'x')
	    plot(resdata.iqdata[0],resdata.iqdata[1],'x')
	    plot(tsr[0],tsr[1],'x')
	    plot(tsr_tr[0],tsr_tr[1],'x')


	#calc std, mean of mag and phase. supply polar data, noise. 
	
	def calcPulseThreshold(self,iqp):
			
	    
    	    self.magnitude_exp_val = numpy.mean(iqp[0])
    	    self.angle_exp_val = numpy.mean(iqp[1])
   
    	    self.magnitude_std = numpy.std(iqp[0]) 
    	    self.angle_std = numpy.std(iqp[1]) 
    
	
	    self.pulse_threshold = 10.0* (self.magnitude_std + self.angle_std)		    
	
	
	#give noise polar data. find pulses, return single polar vactor with just pulses. return another 
	#vector with trigger signal+pre and post stretch. It is same len as input vectore, and is 1 when
	#we have puilse data. 0 otherwise. give data length before trugger
	#and data len after trig ends in samples. also return num pilses we found. 
	#all of this is ret as a (). (trigger,ipq_pulses,numpulses)
	def extractPulses(self,iqp,pre_length,post_length):	    
	    
	    
	    L=len(iqp[0])
    	    test_val = numpy.abs(iqp[0] - self.magnitude_exp_val + iqp[1] - self.angle_exp_val) 
    	    trigger = numpy.zeros(L)

    	    for k in range(pre_length,L-(1+post_length)):
        	if (test_val[k] + test_val[k+1]) > self.pulse_threshold:
	    	    trigger[(k-pre_length):(k+post_length-1)]=1.0
	    
		
	    


	    #
	    # Count number of pulses we found
	    #

	    n_found_pulses = 0
	  
	    
	    pmag=[]
	    pphs= []

	    for k in range(L-1):
        	if trigger[k+1]-trigger[k]>0.0:
		    n_found_pulses=n_found_pulses+1
		    
		if trigger[k]>0:
		    pmag.append(iqp[0][k])
		    pphs.append(iqp[1][k])


	    iqp_pulses = [numpy.array(pmag) , numpy.array(pphs)]
	    return((trigger,iqp_pulses,n_found_pulses))

    
    
    
	    
	    
	    
	    
	    
	    
