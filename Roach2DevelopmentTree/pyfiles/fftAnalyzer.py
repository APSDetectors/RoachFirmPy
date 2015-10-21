"""
 execfile('natAnalGui.py')

#works - has gain error between I and Q-0 could be puython scripts
#fwname='fftanalyzerc_2014_Feb_21_0927.bof'


#fwname='fftanalyzerc_2014_Feb_21_1425.bof'

fwname='fftanalyzerc_2014_Apr_10_1156.bof'

roach=connRoach()
startFW(roach,fwname)



setupfa()


 rf.baseband_loop=1
progRFSwitches(roach,rf)

fa.setLutSize(1024*128)



#fa.setLutFreqs([10e6],2000)

fa.setLutFreqs([10e6, 20e6, 30e6, 40e6, 50e6, 60e6, 70e6, 80e6,200e6],2000)
#fa.fftBinFlags(range(400))
#fa.fftBinsFreqs()
fa.fftBinsAll()
fa.progRoach()

fa.trigFFT()


time.sleep(1)

fa.getDFT_IQ();

ts=fa.extractTimeSeries(20e6);clf();plot(ts[1])
ts=fa.extractTimeSeries(10e6);plot(ts[1])
ts=fa.extractTimeSeries(30e6);plot(ts[1])
ts=fa.extractTimeSeries(40e6);plot(ts[1])



 clf();semilogy(fa.extractSpectrum(0)[0])



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




	
########################################################################
#
# uise fftanalyzerc.slx
#
#
#######################################################################

class fftAnalyzer(networkAnalyzer):


	def __init__(self,r):
		global s
		
		networkAnalyzer.__init__(self,r)
		
		#bug in the readback from the fft coef mem. offset buy some number of points
		self.fpga_bug_offset=0
		
		self.dac_clk=s.f
		self.sys_clk=self.dac_clk/4
		
		
		#amplitude of waves we put in lut- as a percentage. 1.0 is full scale
		self.lut_sine_amp=.6
		
		
		#for debug...send address of dram to dac output
		self.seeaddress=0
		
		self.st_fft_mem=0
		self.fft_mem_we=0

		self.fftsynctime=8192
		
		self.holdcounter=0;
		
		self.resetDRAM=0;
	
		
		#
		# can put a phase pulse into the lut
		#give pulse amp, pulse length
		#pulse shaped like sawtooth
		# amp in degrees. length is in samples in the lut
		#
		self.test_pulse_amp=0.0
		self.test_pulse_len=20
		
		
		self.lut_length=8192*8
		self.lut_length2=self.lut_length/2
		self.lut_length4=self.lut_length/4
		self.lut_length8=self.lut_length/8
		

		self.lut_phase_list=[]
		
		#dft memlen
		self.memLen=4096
		self.memLen4=self.memLen/4
		self.memLen8=self.memLen/8

		#waveformme len
		self.memLenW=4096
		
		
		#len of fft on roach
		#!!self.fftLen=2048	
		self.fftLen=512
		#num samples on one tap from 1/4 ADC in roach board.
		self.dftLen=self.fftLen/4
		
	
		self.delay=0;

		
		#phase offset of Q in radians. is is added phase to a sin
		self.Q_phase_offs=0.0
		
		#amp factor to mult by Q amplitude. set to 1.0 . set to 0 for no Q.
		#need -1 for some reason...
		self.Q_amp_factor=-1.0
		
		#we can make Q freq different from I freq w. offset in Hz
		self.Q_freq_offset=0.0
		
		#iqnoise=self.gaussianLUT()
		
		
		#list of bins we wish to return into iqdata. it is list of bins
		#that we actaully readfrom fifo, in final data. a list like 40,129,1022
		#for 2k fft, all bins, this will be range(2048)
		#
		self.fft_bins_requested=[]
		
		#list of bins like 40,41,42,43, 128,129,130,140,1022,1023,1024,1025 for which bins
		# we read out of FFT. is is list of indices of fft_bin_flags that are
		#set to 1, and mult by 4. for all bins, for 2k fft this is same as
		#range(2048). 
		self.fft_bin_list=[]
		
		#list of freqs we wish to generate in setLutFreqs
		self.req_frequency_list=[]
		#list of freqs we ACTUALLY? generate in setLutFreqs
		self.frequency_list=[]
		
		#list of 1's or 0's that we put into RAM on fpga.
		#for 2k fft it is a list of 512 1's and 0's for which coeff we read out
		#into fifos or ram which ever fw we have. intitl coef readout of fft
		#for 2k fft all bins this will be ones(512)
		self.fft_bin_flags=[]
	
	
	
		#which fft bins to get. 1 or zer in each array
	
		self.fftBinFlags(arange(self.fftLen))
			
		
		self.setLutFreqs([1e6],5000);


		#resonatorData object that is IQFreq sweep information. we take noise w/ same settings etc.
		self.sweepres=0
	
		#add noise trace to resontaorData obj if set to one
		#deprecated
		self.is_add_noise_2_res=0
	
	
		self.lut_i=zeros(2048);
		self.lut_q=zeros(2048);
		self.lut_binaryIQ=zeros(2048);
	
	
	
	
	#
	# get settings from resonatrData object and set up attens, rf switches, Lo etc the same way.
	#  We will later add noise traces to this resonator	
	
	
	def setSweepResonator(self,res):
	    self.sweepres = res
	    
	
	#get atteen and rf board settings and lo settinsg and set up if board etc accordingluy
	def setResonatorSettings(self):
	

	    #set attens to same as in the  original sweep
	    at.atten_U6=self.sweepres.atten_U6
	    at.atten_U7=self.sweepres.atten_U7
	    at.atten_U28=self.sweepres.atten_U28

	    progAtten(roach,at)
	   
	    rf.lo_internal=int(self.sweepres.lo_internal)
	    progRFSwitches(roach,rf)

	    fbase= self.sweepres.sweep_fbase
	    fc = self.sweepres.skewcircle_fr
	    
	    self.isneg_freq = self.sweepres.isneg_freq
	    
	    if self.isneg_freq==1:
	    	carr= fbase + fc
	    else:
	    	carr= fc -fbase
	    
            self.setCarrier(carr)
	    
	    
	    
	    self.setLutSize(1024*128)
	    self.setLutFreqs( [fbase], self.sweepres.lut_sine_amp*32768.0)
	    
	    self.fftsynctime=self.dftLen
	    self.roach_fft_shift = self.sweepres.roach_fft_shift
	    self.roach_num_ffts=65536
	    self.stopFFTs()
	    self.fftBinsFreqs()
	    self.progRoach()
	    self.resetDAC()
	    #self.trigFFT()
	    
	    
	    
	    self.dbgappend(('setResonatorSettings,printReg',self.printRegs(0,0) ))
	    self.dbgappend(('setResonatorSettings,fa',self.getObjSpecs()))
	
	#add iq noise data to the resonatorData obj
	#deprecated
	def addNoise2ResData(self):
	
	    if self.sweepres.num_noise_traces==0:
	        self.sweepres.iqnoise=[]
		self.sweepres.fftLen=[]
		self.sweepres.fftsynctime=[]
		self.sweepres.fftdelay=[]
		self.sweepres.binnumber=[]
		self.sweepres.srcfreq=[]
		
		
		 
	    self.sweepres.fftLen.append(self.fftLen)
	    self.sweepres.fftsynctime.append(self.fftsynctime)
	    self.sweepres.fftdelay.append(self.delay)
	    
	    self.sweepres.binnumber.append(self.fft_bins_requested[0])
	    self.sweepres.srcfreq.append(self.frequency_list[0])
		
	    self.sweepres.iqnoise.append(self.iqdata)
	    
	    #self.sweepres.is_noise=1
	    self.sweepres.num_noise_traces = self.sweepres.num_noise_traces+1
	    self.sweepres.is_noise=self.sweepres.num_noise_traces
	
	
	
	
	
	#calc phase increase per fft for some given freq.
	def getPhasePerFFT(self,freq):
		
		
		##freq in rad per sec. how much the phase changes in radians in 1 sec
#		freqrad=2*pi*freq
#		
#		#
#		#time between ffts.
#		#
#		
#		#fpga clk period in sec
#		sys_period=1.0/self.sys_clk
#		
#		#time in sec between successive ffts
#		
#		fftperiod=self.fftsynctime * sys_period;
#		
#		#calc how much the phase change is in fftperiod
#		
#		phase_per_fft = freqrad*fftperiod
#		
#		
#		phase_per_fft =2.0*pi *  ( phase_per_fft/(2.0*pi) - floor(phase_per_fft/(2*pi))  )
#		
	
		#num samples of 1 cycle of freq at fpga freq
		
		f_wavelen=self.sys_clk / freq
		
	
		#number of samples between fft is self.fftsynctime, or 8192
		#number of wavelens bween ffts
		waves_per_fft = self.fftsynctime / f_wavelen
	
		#get the fraction part of the num waves
		waves_per_fft_frac=waves_per_fft - floor(waves_per_fft)
		
		#convert to radians
		phase_per_fft = 2.0*pi*waves_per_fft_frac
	
		return(phase_per_fft)
		
		
		
		
		
	
	#calc phase increase per fft for some given freq.no PI in here
	def getPhasePerFFTNoPi(self,freq):
		
		
		##freq in rad per sec. how much the phase changes in radians in 1 sec
#		freqrad=2*pi*freq
#		
#		#
#		#time between ffts.
#		#
#		
#		#fpga clk period in sec
#		sys_period=1.0/self.sys_clk
#		
#		#time in sec between successive ffts
#		
#		fftperiod=self.fftsynctime * sys_period;
#		
#		#calc how much the phase change is in fftperiod
#		
#		phase_per_fft = freqrad*fftperiod
#		
#		
#		phase_per_fft =2.0*pi *  ( phase_per_fft/(2.0*pi) - floor(phase_per_fft/(2*pi))  )
#		
	
		#num samples of 1 cycle of freq at fpga freq
		
		f_wavelen=self.sys_clk / freq
		
	
		#number of samples between fft is self.fftsynctime, or 8192
		#number of wavelens bween ffts
		waves_per_fft = self.fftsynctime / f_wavelen
	
		#get the fraction part of the num waves
		waves_per_fft_frac=waves_per_fft - floor(waves_per_fft)
		
		#convert to radians
		phase_per_fft = 2.0*waves_per_fft_frac
	
		return(phase_per_fft)
		
			
		
		
	def oneSweep(self,startf,stepf,endf):
	
		pass
		
	def oneSweep2(self,):
		
		pass


	###########################################################################
	#does nothing... for later fw...
	#
	###########################################################################
		
	def zeroPhaseIncs(self):
		pass
		

	###########################################################################
	#does nothing... for later fw...
	#
	###########################################################################
		
	def reprogPhaseIncs(self):
		pass
	

	#set roach so all fft bins are returned
	def fftBinsAll(self):
		
		
		
		self.fftBinFlags(arange(self.fftLen))
		
		
	#if we have set a list of freqs to generate into the LUT, we can set the proper bins to readback from the fft.	
	def fftBinsFreqs(self):
	
		#blist=array(self.frequency_list)
		
		#the 0.0001 is so round wont randomly rand x.5 up or down. it gets rid of
		#0.5's
		#blist=numpy.round(0.0001 + blist/(self.dac_clk / self.fftLen))
		blist = self.getBinsFromFreqs(self.frequency_list)
		
		self.fftBinFlags(blist)
	
	
	#sets flags, one flag per bin when we read out the fft. there are 4 ourputs in fft, so one flag actually does 4 bins.
	#you use this function as such. blist=[56,129,1023,1689] to read out bins 56,129,1023,1689. 
	#under the hood, you end up getting adjecent bins to these as well.
	#	fft_bin_flags is a list sent to roach and in RAM on roach board. it is bin numbers /4, 1's and zeros. If bin 16 is to be readout
	#	fft_bin_flags[4] will have a 1 in it. This will read out bins 16,17,18,19
	#	fft_bin_list is the bins you are reading out. it is a list of numbers looking like this  [16,17,18,19, 128,129,130,131..]
	#	is tis the actual bin numbers we read out. because we have 4 fft outs, we read out in groups of 4 adgance bins.If we read out
	#	whoel fft, then fft_bin_list will be range(2048)
	def fftBinFlags(self,blist):
		
	
		#if self.isneg_freq==1:
		 #   blist = self.fftLen - blist -1
	
		
		self.fft_bins_requested=sort(blist)
		
		self.fft_bin_flags=range(self.fftLen/4)
		
		#this is for backwards compatibility- start and end freq are valid for
		#sweep fw, but not necessaryl for fft fw.
		freqs_=self.getFreqsFromBins(self.fft_bins_requested)
		self.startFreq_Hz=freqs_[0]
		

		
		self.endFreq_Hz = freqs_[len(freqs_)-1]
		#we just calc average incrFreq... it is correct for getting full fft
		#bins, but not for just selecting some bins at wierd freq intervals.    
		self.incrFreq_Hz=(self.endFreq_Hz - self.startFreq_Hz)/len(freqs_)
		
		
		#clear all bin flags. /4 because we have 4 outs on fft block
		#in FW
		for k in range(self.fftLen/4):
			self.fft_bin_flags[k]=0
			

		#we must recalc fftbin list, so clear it.
		self.fft_bin_list=[]
		
		#set flags that need to be set
		for binx in blist:
			
			bin4=int(floor(binx/4))
			
			if self.fft_bin_flags[bin4]==0:
			    self.fft_bin_flags[bin4]=1
			    self.fft_bin_list.append(bin4*4)
			    self.fft_bin_list.append(bin4*4+1)
			    self.fft_bin_list.append(bin4*4+2)
			    self.fft_bin_list.append(bin4*4+3)
	    	
		self.fft_bin_list=sorted(self.fft_bin_list)
	############################################3
	#
	########################################33			
		
	def getBinsFromFreqs(self,freqs):
	
	    bins=[]
	    for f in freqs:
	        bins.append(self.getBinFromFreq(f))	
		
		
		
	    return(bins)
	    
	    
	############################################3
	#
	########################################33			
	    
	def getBinFromFreq(self,freq):
		
		
	    if freq<0:
	        freq=	self.dac_clk - freq
		
		
	    #find which bin in fft this freq cooresponds to
	    whichbin=int(round(0.0001 + freq/(self.dac_clk / self.fftLen)))

	    if self.isneg_freq==1:
	        whichbin = self.fftLen - whichbin
	    
	    return(whichbin)	
		


	    
	############################################3
	#
	########################################33			
	    
	def getBinFromFreqF(self,freq):
		
		
	    if freq<0:
	        freq=	self.dac_clk - freq
		
		
	    #find which bin in fft this freq cooresponds to
	    whichbin=(freq/(self.dac_clk / self.fftLen))

	    if self.isneg_freq==0:
	        whichbin = float(self.fftLen) - whichbin
	    
	    return(whichbin)	
		
	############################################3
	#
	########################################33			

	def getBinsF(self):
	
	    bins=[]
	    for f in self.frequency_list:
	        bins.append(self.getBinFromFreqF(f))	
		
		
		
	    return(bins)


	############################################3
	#
	########################################33			

	def getFreqFromBin(self,bin):
	

	    if self.isneg_freq==1:
	        whichbin = self.fftLen - bin
	    else:
	        whichbin=bin
	    
	    
	    
	    freq=whichbin * (self.dac_clk / self.fftLen)
	    
	    return(freq)
	
	############################################3
	#
	########################################33			


	def getFreqsFromBins(self,bins):
	
	    freqs=[]
	    for b in bins:
	        freqs.append(self.getFreqFromBin(b))
	
	    return(freqs)
	    
	    

	############################################3
	#
	########################################33			
		
	def getRecordLen(self):
	    recordlen=len(self.fft_bin_list)
	    
	    return(recordlen)
	    
	############################################3
	#
	########################################33			
		
	    
	def getNumSpectra(self):
	    recordlen = self.getRecordLen()
	    
	    #famemlen-1 because of bug on last point in the memory.. fw bug
	    #for long spectra do not worry about last point... so dont do -1...
	    #if recordlen<200:
 	    #    nspectra= int(floor((self.memLen-1) / recordlen))
	    #else:
	    
	    nspectra= int(floor((self.memLen) / recordlen))

	    return(nspectra)
	    
	    
	############################################3
	#
	########################################33			
		
	#helper function. sets freqs, bins for readback, and reads back a spectrum in polar coord
	def collectSpectrum(self,freqs,amp):
	
		self.setLutFreqs(freqs,amp)
		self.fftBinsFreqs()
		time.sleep(.5)
		self.trigFFT()
		time.sleep(.5)
		self.getDFT_IQ()
		s=self.extractSpectrum(0);
		
		return(sp)
	############################################3
	#
	########################################33			
		
	#get freq resultion of lut
	def getResolution(self):
		resolution = self.dac_clk/self.lut_length
		return(resolution);


	############################################3
	#
	########################################33			
	#get res of fft bins, Hz per bin	
	def getFFTResolution(self):
		resolution = self.dac_clk/self.fftLen
		return(resolution);
		

	############################################3
	#
	########################################33			
		
	
	#iqdata has raw fft coeff. we have mixed up bins, and several spectra stored.
	# we extract spectra, and put into a 2k array so it looks like a spectruym
	#spec_num is time offset, which spectrum in the iqdata array
	#return POLAR coords
	def extractSpectrum(self,spec_num):
	
		recordlen=getRecordLen()

		
		spectrum_R=zeros(self.fftLen)
		spectrum_I=zeros(self.fftLen)
		
		st=spec_num*recordlen;
		ed=st + recordlen;
		record_R=self.iqdata[0][ st:ed]
		record_I=self.iqdata[1][ st:ed]
		
		for k in range(len(self.fft_bin_list)):
			
			i=self.fft_bin_list[k];
			spectrum_R[i]=record_R[k]
			spectrum_I[i]=record_I[k]
			
		sP=self.RectToPolar([spectrum_R,spectrum_I])
		
		#return([spectrum_R,spectrum_I])
		return(sP)
		
		
	
	
	#extract the bins from one FFT only. return as list of bin numbers, and bin I, Q
	#ret in rectang coords
	def extractRecord(self,spec_num):
	
	
	
		recordlen=self.getRecordLen()
		
		#fpga_bug_offset is a bug in fpga, where we get wrong bins...
		st=spec_num*recordlen + self.fpga_bug_offset;
		ed=st + recordlen+ self.fpga_bug_offset;
		
		try:
		
		    record_R=self.iqdata[0][ st:ed]
		    record_I=self.iqdata[1][ st:ed]

		except:
		    record_R=zeros(recordlen)
		    record_I=zeros(recordlen)
		
		return([record_R, record_I])
		
	
	
	
	def replaceRecord(self,spec_num,data):
	
	
		recordlen=self.getRecordLen()
		
		
		st=spec_num*recordlen;
		ed=st + recordlen;
		self.iqdata[0][ st:ed]=data[0]
		self.iqdata[1][ st:ed]=data[1]
		
		
	
	#extract the bins from one FFT only. return as list of bin numbers, and bin I, Q
	#ret in rectang coords
	def extractRecord2(self,spec_num,iq):
	
	
	
		recordlen=self.getRecordLen()
		
		
		st=spec_num*recordlen;
		ed=st + recordlen;
		record_R=iq[0][ st:ed]
		record_I=iq[1][ st:ed]
		
		
		
		return([record_R, record_I])
		
	
	
	
	def replaceRecord2(self,spec_num,data,iq):
	
	
		recordlen=self.getRecordLen()
		
		
		st=spec_num*recordlen;
		ed=st + recordlen;
		iq[0][ st:ed]=data[0]
		iq[1][ st:ed]=data[1]
		
		
	
	
	#say we readback 20 bins. then we make time series of one of these bins.
	#We supply freq, that is the freq in Hz we soured. If we are actually reading ot that bin,
	#then we retrive all samples of that bin and return in polar coord
	def extractTimeSeries(self,freq):
		nspectra=self.getNumSpectra()
		recordLen=self.getRecordLen()
		#find which bin in fft this freq cooresponds to
		whichbin= self.getBinFromFreq(freq)
		
		
		#look in bin list to make sure it is in there. if so, get the index in the binlist.
		#the index will be offset in the records returned by roach.
		
		aa=where(array(self.fft_bin_list)==whichbin)[0]
		if len(aa)==0:
		    print "Error- that freq not in the binlist"
		    return
		    
		binindex = aa[0]
		
		
		binR=zeros(nspectra)
		binI=zeros(nspectra)
		
		#
		#extract the bin we want and make into a array, R and I.
		#
		
		for spec in range(nspectra):
		    st=spec*recordLen
		    ed=st+recordLen
		    record_R=self.iqdata[0][ st:ed]
		    record_I=self.iqdata[1][ st:ed]
		    
		    binR[spec]=record_R[binindex]
		    binI[spec]=record_I[binindex]
		    
		
		#convert to polar, mag and phase
		bP=self.RectToPolar([binR, binI])
		
		#
		# Calc extected phase inc per fft, and remove it., then we can see only freq changes, phase changes
		#
		phaseperfft=self.getPhasePerFFT(freq)
		
		
		phaseterm = bP[1]
		
		ramp = phaseperfft * arange(len(phaseterm))
		phaseterm=phaseterm-ramp
		#sub 1st point, to offset from 0 phase
		phaseterm = phaseterm-phaseterm[0]
		phaseterm = phaseterm+pi
		
		phaseterm= 2*pi * (  (phaseterm/(2.0*pi) )- floor(phaseterm/(2.0*pi))  )
		phaseterm=phaseterm-pi
		
		bP[1] = phaseterm
		return(bP)	    
		
		
		
		
		
	
	#calls extractSpectrum for each spectrum in the memory.
	def extractSpectra(self,length):
		nspectra= self.getNumSpectra()
		
		spectra_a=[]
		spectra_p=[]
		
		
		if length > nspectra:
		    length = nspectra
		    
		if length<1:
		    length = nspectra
		    
		        
		for k in range(length):
		    spec=self.extractSpectrum(k)
		    s_a=spec[0].tolist()
		    s_p=spec[1].tolist()
		    
		    spectra_a.append(s_a)
		    spectra_p.append(s_p)
		
		    
		return(  [ array(spectra_a) ,array(spectra_p) ])
		    
	
	
	#polots a picture plot time ver freq
	def plotSpectra1(self,length):
	
	    ss=self.extractSpectra(length)
	    figure(1)
	    clf();pcolormesh(ss[0])
	    

	#plot ffts across time. 
	def plotSpectra2(self,length):
	    ss=self.extractSpectra(length)
	    figure(1)
	    clf()
	    subplot(2,1,1)
	    plot(numpy.transpose(ss[0]))
	    
	    subplot(2,1,2)
	    plot(numpy.transpose(ss[1]))
	    
	
	def plotTimes(self,gaina,gainp):
	
	    figure(1)
	    clf()
	    figure(2)
	    clf()
	    
	    figure(3)
	    clf()
	    
	    offset = 0.0
	    
	    
	    for f in self.frequency_list:
	        ts = self.extractTimeSeries(f)
		tsr=self.PolarToRect(ts)
		figure(1)
		plot(tsr[0] -mean(tsr[0]) + gaina*offset)
		figure(2)
		plot(tsr[1] - mean(tsr[1])+ gainp*offset)
		
		figure(3)
		plot(   (180.0/pi)*(ts[1])+ 10*offset)
		offset = offset + 1
		
		
	def plotIvQNoise(self,freq,resdata):
	   
	    ts = self.extractTimeSeries(freq);
	    
	    #ts has its angle set to 0 radians. this is like setting a time delay
	    #so the circle is lined iup on the real axis. Be cause we are concended w/ one
	    #bin, we don't have to rally worry that it is not a curcle in shape, as if we had
	    #many bins. We are looking at ONE bin. adding a time delay is just adding a phase to
	    #one bin. so done worry about time delay.
	    
	    #in ideal case, the circle radius is based on Q. But this is for unity signal going
	    # through the resonator. If we double the signal level sent to resonator, we double
	    # the distx from circle center to origin, and double circle radius. the angle from circle
	    #center to origin remains the same. so we have a ratin of z, the distx from circle center 
	    #to orgin, and r. r/z should be a constant. so we set this to 1.This will remove the effect that
	    # the signal levels from sweeps prob do not match the signal leval from noise. we use 
	    # different FW. 
	    
	    ts_r=self.PolarToRect(ts);

	    
	    #get circle fit data from the 
	    

	    xc=resdata.cir_xc
	    yc=resdata.cir_yc
	    r=resdata.cir_R

	    #Import data
	    x = ts_r[0];
	    y = ts_r[1];

	    #correct data
	    alpha = arctan2(yc,xc);
	    xf = (xc-x)*cos(alpha) + (yc-y)*sin(alpha);
	    yf = -(xc-x)*sin(alpha) + (yc-y)*cos(alpha);

	
	    figure(1)
	    clf()
	    plot(resdata.trot_xf, resdata.trot_yf)

		
	    plot(x,y,'x')
	    	
	
	
	def plotIvQNoise2(self):
	  
	    

	    frindx=min(where(self.sweepres.lorentz_fr<=self.sweepres.freqs)[0])
	    
	    pp=self.RectToPolar([self.sweepres.trot_xf,self.sweepres.trot_yf ])
	  
	    figure(103)
	    
	    clf()
	    polar(pp[1],pp[0])
	    
	    polar(pp[1][frindx],pp[0][frindx],'o')
	    



	    ts = self.extractTimeSeries(self.frequency_list[0]);
	    
	    #angle of ts is 0, set by software. add angle of fres to ts angle.
	    #put at 180 deg off the res for now
	    #
	    #ts[1]=ts[1] + pp[1][frindx] + pi
	    ts[1]=ts[1] +  pi
	    
	    #now cloud is at center-radius, where center on -x axis.
	    #center is this:
	    xc=self.sweepres.cir_xc
	    yc=self.sweepres.cir_yc
	    z=sqrt(xc**2 + yc**2)
	    r=resdata.cir_R
	    
	    ts_r=self.PolarToRect(ts);
	    
	    #translate the data, w/ angle at 180deg. 
	    ts_r[0] = ts_r[0] + z
	    
	    ts2=self.RectToPolar(ts_r)
	    
	    #now add the amgle
	    ts2[1]=ts2[1] + pp[1][frindx]
	    
	    polar(ts2[1],ts2[0],'rx')

	   
	    ts_r=self.PolarToRect(ts);

	    xc=resdata.cir_xc
	    yc=resdata.cir_yc
	    r=resdata.cir_R

	    #Import data
	    x = ts_r[0];
	    y = ts_r[1];

	    #correct data
	    alpha = arctan2(yc,xc);
	    xf = (xc-x)*cos(alpha) + (yc-y)*sin(alpha);
	    yf = -(xc-x)*sin(alpha) + (yc-y)*cos(alpha);

	

	    #get circle fit data from the 


	def setLutSize(self,sz):
		
			
		self.lut_length=sz
		self.lut_length2=self.lut_length/2
		self.lut_length4=self.lut_length/4
		self.lut_length8=self.lut_length/8
			
		self.progRoach();
		#self.startFFT();
	
	def setLutNoise(self):
		iqnoise=array(self.gaussianLUT())
		
		
		self.lut_i=iqnoise[0];
		self.lut_q=iqnoise[1];
		self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
		#self.progRoach()
		self.progDRAM()
	
	
	
	def getLegalFreqs(self,freqs):
		
		
		for k in range(len(freqs)):
		    if freqs[k] < 0:
		        freqs[k] = self.dac_clk-freqs[k]
	
		resolution = self.dac_clk/self.lut_length;
		
		freq_fix=[]
		for freq in freqs:
		    #0.0001 so round does not randomize 0.5...
		    newfreq=resolution * round(0.0001 + freq/resolution)
		    freq_fix.append(newfreq)
		    #if freq!=newfreq:
		    #    print "Error: not enough resolution for req. frequncies"
		    
		return(freq_fix)
		
	


	
	
	def setLutFreqs(self,freqs,amp):
	
	
		

		#amp can be a list of amps w/ len = len(freqs). or a single number. 
		if type(amp)==list:
		    amplist=amp
		    self.lut_sine_amp=max(amp)/32768
		else:
		    self.lut_sine_amp=amp/32768.0
		    amplist=[amp]*len(freqs)
		
		self.req_frequency_list = freqs
		self.frequency_list=self.getLegalFreqs(freqs)
		iq=[zeros(self.lut_length) , zeros(self.lut_length)]
		
		
		self.lut_i=iq[0];
		self.lut_q=iq[1];	
	
		self.lut_phase_list=[]
		
		for k in range(len(self.frequency_list)):

		    freq = self.frequency_list[k]
		    #amp = amps[k]
		    if k==0:
		        phase = 0.0;
		    else:
		        phase = random.uniform(-math.pi, math.pi)
		    
		    self.lut_phase_list.append(phase)
		    self.lut_i=self.lut_i + self.singleFreqLUT(freq, 'I', self.dac_clk,self.dac_clk/self.lut_length , phase, amplist[k])

		    self.lut_q=self.lut_q + self.singleFreqLUT(freq+self.Q_freq_offset, 'Q', self.dac_clk,self.dac_clk/self.lut_length , phase + self.Q_phase_offs, amplist[k]*self.Q_amp_factor)

		
		#fa.lut_i==fa.singleFreqLUT(freq, 'I', fa.dac_clk,fa.dac_clk/fa.lut_length , 0, 50000.0)
	
		
		
		
		self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
		
		#self.progRoach()
		self.progDRAM()

	def setLut(self,datai,dataq):
		
		
		self.setLutSize(len(datai))
		self.lut_i=datai;
		self.lut_q=dataq;
		self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
		self.progDRAM()
		


	def setLutZero(self):
		iq=[zeros(self.lut_length) , zeros(self.lut_length)]
		
		
		self.lut_i=iq[0];
		self.lut_q=iq[1];
		self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
		self.progDRAM()
	
		
	def setLutRamp(self,lenx,ampx):
		iq=arange(self.lut_length)
		
		for k in range(lenx,self.lut_length,lenx):
			iq[k:(self.lut_length)] = iq[k:(self.lut_length)] - iq[k]
		
		
		iq = iq/max(iq)
		iq = iq*ampx
		self.lut_i=iq
		self.lut_q=iq
		self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
		self.progDRAM()
	

		#iq=arange(fa.lut_length)
		
		#for k in range(lenx,fa.lut_length,lenx):
		#	iq[k:(fa.lut_length)] = iq[k:(fa.lut_length)] - iq[k]
	



	def setLutTri(self,freq,ampx):
		
		self.setLutFreq(freq,ampx)
		
		
		iq=zeros(self.lut_length)
		
		for k in range(1,self.lut_length):
			if self.lut_q[k]>=0:
				iq[k] = iq[k-1]+1
			else:
				iq[k] = iq[k-1]-1
			
		
		
		iq = iq - average(iq)
		
		iq = iq/max(iq)
		iq = iq*ampx
		self.lut_i=iq
		self.lut_q=iq
		self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
		self.progDRAM()
	


#fa.setLutFreq(freq,ampx)


#iq=zeros(fa.lut_length)

#for k in range(1,fa.lut_length):
#	if fa.lut_q[k]>0:
#		iq[k] = iq[k-1]+1
#	else:
#		iq[k] = iq[k-1]-1


				
	
	def resetLut(self):
	    try:
		self.roach.write_int('resetDRAM', 1)
		time.sleep(.1)
		self.roach.write_int('resetDRAM', 0)
	    except:
	        print "resetLut No ROACH"
		
	

	def startFFT(self):
	
		
		self.msm_rst=1
		self.progRoach()
		self.msm_rst=0
		self.progRoach()
		
		
		
				
	
	
	
		
	

	def trigFFT(self):
		
		self.fft_mem_we=0
		self.st_fft_mem=1 		
		self.progRoach1()
		
		self.st_fft_mem=0 		
		self.progRoach1()
		
		self.fft_mem_we=1
		self.progRoach1()
		
		

		
		
		

	def getDFTdata(self,output):

		#for debugging so we can see last read from mem
      		global aa;
		
		#I even re, even im, odd re, odd im
		regnames=[
		'MemRecord2_%s'%(ramname),
		'MemRecord3_%s'%(ramname),
		'MemRecord4_%s'%(ramname),
		'MemRecord5_%s'%(ramname),
		'MemRecord1_%s'%(ramname),
		'MemRecord6_%s'%(ramname),
		'MemRecord7_%s'%(ramname),
		'MemRecord8_%s'%(ramname)
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
	
	
	

	
	
	def getDFT_IQ(self):
	
		re=zeros(4*self.memLen);
		im=zeros(4*self.memLen);
		
		
		re[0:4*self.memLen:4]=self.getDFTdata(0)
		re[1:4*self.memLen:4]=self.getDFTdata(2)
		re[2:4*self.memLen:4]=self.getDFTdata(4)
		re[3:4*self.memLen:4]=self.getDFTdata(6)
		

		im[0:4*self.memLen:4]=self.getDFTdata(1)
		im[1:4*self.memLen:4]=self.getDFTdata(3)
		im[2:4*self.memLen:4]=self.getDFTdata(5)
		im[3:4*self.memLen:4]=self.getDFTdata(7)

		
		self.Q_raw=[re, im]
		self.I_raw=[re, im]
		
		self.iqdata=[re,im]
		
		self.hdfWrite()
		
			
		
		
		
		return(self.iqdata)
		#return([re,im])


	

	
		
	def reverseBinary(self,nbits, blist):
	
		rlist=zeros(len(blist))
		
		for k in range(len(rlist)):
			
			val=int(blist[k]);
			rev_val=0
			
			for b in range(nbits):
				bval=1<<b;
				rev_bval=1<<(nbits-b-1)
				if bval&val>0:
					rev_val=rev_val+rev_bval
					
			
			rlist[k]=int(rev_val)						
			
			
			
	
		return(rlist)
	
	
		
	
	
	# execfile('t_brdconfig.py')
	# na=networkAnalyzer(roach)
	
		
	def calcRegs(self):
		
		
		
		self.controlReg= (self.msm_rst<<0) 
		self.controlReg = self.controlReg + (self.startOutputDac<<4 ) 
		self.controlReg = self.controlReg + (self.st_fft_mem<<1) + (self.fft_mem_we<<2)
		self.controlReg = self.controlReg + (self.adcmem_start<<7) + (self.adcmem_wr<<8)
		self.controlReg = self.controlReg + (self.adcmem_sel<<9) + (self.adcfsync<<12)
		self.controlReg = self.controlReg + (self.adc_nloopback<<13)
		self.controlReg = self.controlReg + (self.seeaddress<<3)
		
	def progRoach1(self):
		self.calcRegs()	
		
		if self.is_print==1:
		    msg='controlReg %d\n'%(self.controlReg)
		    print msg
		
		try:
 		    self.roach.write_int('controlReg', self.controlReg)
		except:
		    print "progRoach1  No ROACH"
	
	def progRoach(self):
	    try:
		self.calcRegs()	
		
		if self.is_print==1:
		    msg='controlReg %d\n'%(self.controlReg)
		    print msg
		
		self.roach.write_int('controlReg', self.controlReg)

		#!!self.roach.write_int('dram_controller', 0)
		
		#1 to stop lut playback
		self.roach.write_int('holdcounter', self.holdcounter)
		#1 to erase lut dram
		self.roach.write_int('resetDRAM', self.resetDRAM)
		
		#need to write -1 because of = in the fpga code...
		self.roach.write_int('fftsynctime',self.fftsynctime-1);
	
		
		
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
	    except:
	        print "progRoach No ROACH"
	
		
	def sendBinFlags(self):
	    try:
		self.roach.write('BinData',self.convertToBinary(self.fft_bin_flags));
	    except:
	        print "No ROPACH"


	def progDRAM(self):
		roachlock.acquire()
		
		
		try:
		   
		    self.msm_rst=1
		    self.progRoach1()
		
		
		except:
		    pass
	
		
		self.big_write(self.lut_binaryIQ)
	
	
	        try:
		   
		    self.msm_rst=0
		    self.progRoach1()
		except:
		    pass
		
		
		roachlock.release()

	def convertToBinary128(self,data1, data2):
	    """ Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

        	@param data             Decimal data to be converted  for FPGA.
        	"""
	    binaryData = ''
	    for i in range(0, len(data1)/4):
        	x = struct.pack('>hhhhhhhh', data1[4*i+3], data1[4*i+2], data1[4*i+1], data1[4*i+0],data2[4*i+3], data2[4*i+2], data2[4*i+1], data2[4*i+0])
        	binaryData = binaryData + x

	    return binaryData



	def convertFromBinary128(self,data):
	    data1 = arange(len(data)/4)
	    data2=arange(len(data)/4)
	    
	    for i in range(0, len(data)/16):
                a = struct.unpack('>hhhhhhhh', data[(16*i):(16*i + 16)])
        	for k in range(4):
		    data1[(4*i+k)]=a[3-k]
		    data2[(4*i+k)]=a[4+ 3-k]
		
		

	    return [data1,data2]


	
	def convertToBinary(self,data1):
	    """ Converts  data points to 32-bit binary .

        	@param data             Decimal data to be converted  for FPGA.
        	"""
	    binaryData = ''
	    for i in range(0, len(data1)):
        	x = struct.pack('>I', data1[i])
        	binaryData = binaryData + x

	    return binaryData

	def convertToBinary8(self,data1):
	    """ Converts  data points to 8-bit binary .

        	@param data             Decimal data to be converted  for FPGA.
        	"""
	    binaryData = ''
	    for i in range(0, len(data1)):
        	x = struct.pack('>B', data1[i])
        	binaryData = binaryData + x

	    return binaryData



	def convertFromBinary8(self,binaryData):
	    """ Converts  data points from 8bit bin to floats.

        	@param data             Decimal data to be converted  for FPGA.
        	"""
	    data = []
	    for i in range(0, len(binaryData)):
        	x = struct.unpack('B', binaryData[i])
        	data = data.append(x)

	    return data


	def freqCombLUT(self,fList, sampleRate, resolution, amplitude, phase):
	    """ Returns data points for the DAC look-up table for I and Q.

        	@param fList            List of desired freqs with kHz resolution, e.g., 12.34e6.
        	@param sampleRate       Probably 550e6
        	"""
	    I = [0 for i in range(int(round(sampleRate/resolution)))]
	    Q = [0 for i in range(int(round(sampleRate/resolution)))]

	    for f in fList:
        	phase = random.uniform(-math.pi, math.pi)
        	#phase = 0
        	I = np.add(I, singleFreqLUT(f, 'I', sampleRate, resolution, phase, amplitude))
        	Q = np.add(Q, singleFreqLUT(f, 'Q', sampleRate, resolution, phase, amplitude))

	    return I, Q


	def singleFreqLUT(self,f, iq, sampleRate, resolution, phase, amplitude):
	    """ Returns data points for the DAC look-up table.

        	@param f                List of desired freqs, e.g., 12.34e6 if resolution = 1e4.
        	@param sampleRate       Sample rate of DAC.
        	@param resolution       Example: 1e4 for resolution of 10 kHz.
        	@param phase            Constant phase offset between -pi and pi.
        	"""
		
	    	
	    size = int(round(sampleRate/resolution))
	    #data = []

	    if (size>self.lut_length):
	        print "Error- singleFreqLUT size>lut_length"
	
	    phaserad=numpy.pi * phase / 180.0;
	    phaseterm= phaserad + 2*math.pi*(f/sampleRate)*arange(size)
	    
	    
	    #make test pulse.it is inserted in random part of the waveform.
	    #calc where pulse will be in the wave
	    
	    pulse_st=int(round(rand() * (len(phaseterm)- 2*self.test_pulse_len)))
	    pulse_ed = pulse_st+self.test_pulse_len
	    
	    #now get a piece of the phase term
	    pulsephase = phaseterm[pulse_st:pulse_ed]
	    #now add a new phase term to it, a ramp
	    pulsephase = pulsephase + (pi*self.test_pulse_amp / 180.0 ) * (1.0/len(pulsephase))*arange(len(pulsephase))
	
	    #now put the ramp into the wave		
	    phaseterm[pulse_st:pulse_ed] = pulsephase
	    
       	    if iq == 'I':
                data=numpy.round(amplitude * numpy.cos(phaseterm))
        	    #data.append(int(amplitude*math.sin(2*math.pi*f*t)))
            else:
	    	sign = 1.0;
		if self.isneg_freq: sign=-1.0;
		
      	        data=numpy.round(sign*amplitude * numpy.sin(phaseterm))
		

	    return data  

	def gaussianLUT(self,sampleRate=dac_clk_freq, resolution=6103.5, amplitude=2**12-1, sigma=0.5):

	    size = self.lut_length
	    I = []
	    Q = []
	    for i in range(0, size):
        	t = i/sampleRate
        	x = int(amplitude*random.gauss(0, sigma))
        	I.append(x)
        	Q.append(x)

	    return I, Q


	def big_write(self,data):
	
	    try:	
		chunksize=1024*64
		
		ll=len(data)
		
		if (ll<chunksize):
		    self.roach.write('dram_memory',data)
		    return
		    
		
		assert ll%chunksize==0, "ERROR, lut_length must be multiple of %d"%(chunksize)
		    
		nchunks=ll/chunksize
		
		for k in range(nchunks):
		    
		    st=k*chunksize;
		    ed=(k+1)*chunksize
		    self.roach.write('dram_memory',data[st:ed],offset=st)
	    except:
	        print "big_write No ROACH"	    
		    

	def grabData3(self):
	    self.thread_running=1
	    
   	    for k in range(self.numSweeps):
	    	print "Trigger sweep"
		
		self.trigFFT();
		time.sleep(2)
		
		if self.thread_running==0:
			print "Ending Loop/Thraed"
			sweepCallback()
			return

		
		iq=self.getDFT_IQ();
		
		sweepCallback()
			
		self.sweepcount=self.sweepcount+1
		
		#if self.is_add_noise_2_res==1:
		#    self.addNoise2ResData()


	
