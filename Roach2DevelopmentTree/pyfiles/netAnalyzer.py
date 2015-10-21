'''

execfile('natAnalGui.py')

#fwname ='networkanalyzer_2014_Feb_18_1150.bof'
#fwname = 'networkanalyzer_2014_Apr_21_1006.bof'
fwname = 'networkanalyzer_2014_Jun_25_1330.bof'

roach=connRoach()
startFW(roach,fwname)



setupna()



at.atten_U6=15
progAtten(roach,at)
rf.rf_loopback=0

rf.lo_internal=0
progRFSwitches(roach,rf)

#Fitted Fr 2.560060 GHz

fc= 2.560060e9
carr=2.6e9

na.setCarrier(carr)
#fa.setLutSize(1024*1024)
#fa.setLutSize(1024*128)

fbase=carr-fc


na.startSweep(fbase-1e6,-1,fbase+1e6) 


iq=na.getDFT_IQ();na.plotFreq(iq)





na.startSweep(10e6,-1,10.1e6) 


iq=na.getDFT_IQ();na.plotFreq(iq)




'''



import threading

import scipy	
import scipy.linalg


execfile('fitters.py');




#
# set to 1 when we have fits or power sweep thread running
#

is_thread_running=0

#
#
#
sweep_counter = 0



########################################################################
#
#
#
#
#######################################################################


class networkAnalyzer:

	def __init__(self,r):
		
		
		
		
		
		#wire for resettign DAC block in FW
		self.dac_reset_bit=0
		
		#sinusoid amplitude in the DAC, as a percent. 1.0 means DAC is full scale.
		#hardcoded in netanaluzer FW
		self.dac_sine_sweep_amp = 0.6
		
		#device name- a string, saved to hdf dump file...
		self.device_name='NULL'
		
		
		#resonator number- an attribute saved w/ sweepts
		self.resonator_number=-1
		
		
		#power in dbm for anritsu
		self.anritsu_power=-5
		
		#some fw has adjustable gain on the sin output- 
		#some dont
		self.hasIQGainReg=0
		
		#
		#!!self.debugvalue=0
		
		#hdf file to write
		self.hdffile=None
		#hdffile to read
		self.hdffile_r=None
		
		self.roach=r
		
		self.isneg_freq=1
		self.is_print=0;

		self.carrierfreq=3500e6


		self.statusFlags=0
		self.stat_sweepDone=0
	


		#enable signal delta modulator
		self.sd_mod=0
		#reset master state machine
		self.msm_rst=0
		#trigger scan
		self.start_scan=0
		#start dac
		self.startOutputDac=1
		#manual increment of freq
		self.manualSweep=0
		#manual trigger of dft
		self.manDFT=0
		
		
		#set to 1 for adc. set to 0 for loopback.
		self.adc_nloopback=1
		
		#adc mem start, clear addr
		self.adcmem_start=0
		#adc wr mem
		self.adcmem_wr=0
		#adc mem select- 0...7
		self.adcmem_sel=0
		
		#force adc sync hi
		self.adcfsync=1
		
		#start frequency Hz
		self.startFreq_Hz=10e6
		#end freq Hz
		self.endFreq_Hz=50e6
		#freq incr Hz
		self.incrFreq_Hz=0.1e6
		
		#sysclk freq
		self.sys_clk=s.f/4
		#dac clk freq
		self.dac_clk=s.f
		#sintable len
		self.sin_tablen=64
		
		#start freq register
		self.startFreq=0
		self.endFreq=0
		self.freqAddend=0
		self.controlReg=0
		
		
		#for short PFB window- double length hamming window
		#overlap added. 32 or 256 depending on FW.
		#if zero, no windowing.
		#if 1 we get that hamming. need to set dftlen to 32
		self.useOverlapWind=0
		
		self.dftLen=65536
		
	
		self.delay=0;

		#dft memlen
		self.memLen=16384
		self.memLen4=self.memLen/4
		self.memLen8=self.memLen/8

		#waveformme len
		self.memLenW=4096

		self.phasesRe=ones(self.memLen4/2);
		self.phasesIm=zeros(self.memLen4/2);
		


		#for sweeping the power- setting the attenuator on IF
    		#output atten start
		self.attStart=10
	    	self.attEnd=30
	    	self.attIncr=0.5
		#input atten start...
		self.attInStart=25
		
		#for cunting getting iqdata on power sweeps	    	
		self.numSweeps=1
		self.sweepcount=0
		#to plot graph on sweep grab
		self.is_plotsweep=0
		
		#running threeads
	    	self.thread=None
	  	#set to 0 to make functino in thread exit
		self.thread_running=0
		
		#where latest iqdata is stored
		self.iqdata=[ zeros(2048), zeros(2048)]
	
		self.I_raw=[zeros(2048),zeros(2048)]
		self.Q_raw=[zeros(2048),zeros(2048)]
		
	
		#index for reading and writn ghdf files.		
		self.iq_index=0
		self.set_index=0	

		#for returning resonator obj, give in index.
		self.rescnt=0
		
		
		#amplitude cal of DACs 
		self.IOutGain=0.5
		self.QOutGain=0.5
		
		self.IOutGReg=0
		self.QOutGReg=0
		#reg for 1/dftlen window length...
		self.invDftLen=0
		
		
		#this is a list of freqeucies marked by user. 
		#can do power sweep aroumd those freqiencies to do several resonators
		self.markerlistx=[]
		#span of sweep around lists of freqiencues, assumed to be resonators	
		self.markerspan=1e6  #Tom? single resonator span

	def getResonator(self):
		res=resonatorData(self.resonator_number, self.device_name);
		self.rescnt=self.rescnt+1;
		
		stf=self.startFreq_Hz
		edf=self.startFreq_Hz + ((self.memLen4/2)-1)*self.incrFreq_Hz

		
		freqs=self.carrierfreq + self.startFreq_Hz + (numpy.arange(self.memLen4/2) * self.incrFreq_Hz)
		res.setData(self.iqdata, freqs, self.delay,self.carrierfreq)
		
		
		res.isneg_freq=self.isneg_freq
		
		if self.isneg_freq==1:
			res.fliplr()
		
		#tell that we used netanal fw for sweep
		res.sweep_fw_index=0
		
		
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


		#if zero incr freq then it is a noise trace
		if self.incrFreq_Hz<0.1:
		    res.is_noise = 1
		    

			
		
			
			
			
		return(res)


	         
	#take list if mkids and divide into short lists of mkids within bw of 200MHz, then sweep the
	#shorts lists. list of MKID objhects expeced
	def noiseResonators(self,mlist1,numtraces):

		mlist=sorted(mlist1,key=MKID.getFc)
		
		self.thread_running=1
		
		
		lensave = self.dftLen
		self.dftLen=256
		self.progRoach()
		
		for mkid in mlist:	  
		    for resdata in mkid.reslist:
		        try:
			    #if resdata.is_noise==0:
			    if resdata.num_noise_traces<numtraces:
			        self.resonatorNoise(resdata,numtraces)
			    
			    if self.thread_running==0:
			        print "Ending Loop/Thraed"
			        return
			except:
			    print "problem taking noise on resdata MKID Fc=%f"%(mkid.getFc())
			
	   		    traceback.print_exc()
			
		self.dftLen=lensave
		self.progRoach()
			
		    
		
			
	def resonatorNoise(self, resdata,numtraces):
	

		resdata.noise_fw_index=0;
		
		fc=resdata.maxIQvel_freq
		
		if fc<=0:
			fc=resdata.rough_cent_freq
			print "Warning: using rough cent freq for noise"

		#fbase=self.frequency_list[0]
		
		#we take the carrier freq, or LO. WE find diff between LO and fc, and that is then baseband
		
		
		if resdata.isneg_freq==1:
		    fbase= resdata.carrierfreq - fc 
		else:
		    fbase=fc - resdata.carrierfreq
		
		
		
		
		#!!if self.is_resetup_noise==1:
		    #set attens to same as in the  original sweep
		at.atten_U6=resdata.atten_U6
		at.atten_U7=resdata.atten_U7
		at.atten_U28=resdata.atten_U28

		progAtten(roach,at)

		rf.lo_internal=int(resdata.lo_internal)
		progRFSwitches(roach,rf)

		   
	
		
		self.setCarrier(resdata.carrierfreq)

		self.stopSweep()

		


		progAtten(roach,at)
		progRFSwitches(roach,rf)
		time.sleep(1.0)
		for t in range(numtraces):
		   
		    
		    self.oneSweep(fbase,0.0,fbase)
		    
		    
		    time.sleep(0.1)

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


		  

		    resdata.num_noise_traces=resdata.num_noise_traces+1
		    resdata.is_noise = resdata.num_noise_traces
		    resdata.fftLen.append(self.dftLen)
		    resdata.fftsynctime.append(self.dftLen)
		    resdata.fftdelay.append(self.delay)
		    resdata.iqnoise.append(ccopy.deepcopy(self.iqdata))
		    resdata.iqnoise_raw.append( [ccopy.deepcopy(self.I_raw),ccopy.deepcopy(self.Q_raw)] )

		    resdata.binnumber.append(-1)
		    resdata.srcfreq.append(fbase)
		    resdata.noisetrace_len.append(len(self.iqdata[0]))
		    resdata.fftcarrierfreq.append(self.carrierfreq)
		    #!!resdata.carrierfreq=self.carrierfreq
		    
		    self.setSweepResonator(resdata)
		    
    		    sweepCallback()
		    if self.thread_running==0:
				print "Ending Loop/Thraed"
				return












	
	def setSweepResonator(self,res):
	    self.sweepres = res


	
	
	def rfOff(self):
	   
	   

	    atoff=attenSetting()
	    #all in db. it attens by these db's
	    atoff.atten_U28=30.0
	    atoff.atten_U6=30.0
	    atoff.atten_U7=30.0

	    
	    progAtten(self.roach,atoff)
	    
	    
	
	def rfOn(self):
	    global at
	   
	    global rf
	    
	
	    
	    progAtten(self.roach,at)
	    	    
	    
	    progRFSwitches(self.roach,rf)
	    self.progRoach()
			
	def captureADC(self,select):
	
	
		
	
		self.adcmem_wr=0
		self.adcmem_start=1
		self.adcmem_sel=select;
		self.progRoach()
		self.adcmem_start=0
		self.progRoach()
		
		self.adcmem_wr=1
		
		self.progRoach()
		
		time.sleep(.1)
		self.adcmem_wr=0
		self.progRoach()
		
		roachlock.acquire()
		try:
			
			aa=struct.unpack('>'+'I'*self.memLenW,roach.read('adcWaveMem_MemRecord_%s'%(ramname),self.memLenW*4))
		except:
			print "No Roach board"
			aa=range(self.memLenW)
		
		
		roachlock.release()
		
		adcmem=[]
		for i in range(self.memLenW):
		
			sgn=aa[i]&0x800
			frac=float(aa[i]&0x7ff)
			val = frac/2048.0
			if sgn!=0:
				val = val -1.0
				
			#val = float(aa[1])/self.memLenW.0
			
			adcmem.append(val)

		return(numpy.array(adcmem))
		

	#
	# for newer fw w/ 4 adc memorues to get all 4 taps
	# 4 mems w/ 2 selable imputs. iqsel sels which inpuit.
	# for older FW we get i0-3, OR q0-3. 
	#new FW after jun25 2014, we get i0,i1,q0,q1, OR i2,i3,q2,q3. then we can see phase
	
	def trigADCMem(self,iqsel):
		self.adcmem_wr=0
		self.adcmem_start=1
		self.adcmem_sel=iqsel;
		self.progRoach()
		self.adcmem_start=0
		self.progRoach()
		
		self.adcmem_wr=1
		
		self.progRoach()
		
		time.sleep(.1)
		self.adcmem_wr=0
		self.progRoach()
	
	#for jun25 and later:
	#0,0  i0
	#0,1  i1
	#0,2 q0
	#0,3  q1
	#1,0  i2
	#1,1  i3
	#1,2  q2
	#1,3  q3
	def captureADC2(self,iqsel,memsel):
		self.trigADCMem(iqsel);
		return(self.readADC(memsel));
		
		
			
	def readADC(self,memsel):
	
		
		regnames=[
		'adcWaveMem_MemRecord_%s'%(ramname),
		'adcWaveMem1_MemRecord_%s'%(ramname),
		'adcWaveMem2_MemRecord_%s'%(ramname),
		'adcWaveMem3_MemRecord_%s'%(ramname)]
		
		regn=regnames[memsel];
		
		roachlock.acquire()
		
		try:
			aa=struct.unpack('>'+'I'*self.memLenW,roach.read(regn,self.memLenW*4))
		except:
		
			print "No roach"
		
		
		roachlock.acquire()	
				
		adcmem=[]
		for i in range(self.memLenW):
		
			sgn=aa[i]&0x800
			frac=float(aa[i]&0x7ff)
			val = frac/2048.0
			if sgn!=0:
				val = val -1.0
				
			#val = float(aa[1])/self.memLenW.0
			
			adcmem.append(val)

		return(numpy.array(adcmem))
		
	#deprecarted w. Jun25 2014 FW and later.
	def captureADC3(self,iqsel):
		
		self.trigADCMem(iqsel);
		
		s0=self.readADC(0)
		s1=self.readADC(1)
		s2=self.readADC(2)
		s3=self.readADC(3)
		
		lx=s0.size*4
		s0123=zeros(lx)
		
		s0123[range(0,lx,4)]=s0
		s0123[range(1,lx,4)]=s1
		s0123[range(2,lx,4)]=s2
		s0123[range(3,lx,4)]=s3
		return(s0123)
		
		
	
	def setFreq(self,startf):
	
		self.start_scan=0;
		self.msm_rst=1
		self.progRoach()
		self.msm_rst=0
		self.progRoach()
		self.startFreq_Hz=startf
		self.start_scan=0;
		self.progRoach()
				
	
	def setCarrier(self,fc):
		global LO
		global rf
		
		#... if we use external lo...
		if rf.lo_internal==0:
		    print "using anritsu box"
		    #external anritsu box
		    anritsu(fc*1e-9,self.anritsu_power,1)
		    self.carrierfreq=fc
		else:
		    print "using local osc"
		    #internal lo osc
		    LO.setFreq(fc)
		    progLocalOsc(roach,LO,lo_sle)
		    self.carrierfreq=LO.rfout_freq
	
	def startSweep(self,startf,stepf,endf):
	
		
		
		self.start_scan=0;
		self.msm_rst=1
		self.progRoach()
		self.msm_rst=0
		self.progRoach()
		self.startFreq_Hz=int(startf)
		self.endFreq_Hz=int(endf)
		if stepf<0.1:
			self.incrFreq_Hz=(self.endFreq_Hz-self.startFreq_Hz)/self.memLen8
		else:
			self.incrFreq_Hz=stepf
		
	
	
		self.progRoach()
		self.start_scan=1
		self.progRoach()
	
		self.calcPhaseDelay()
		

	def startSweep2(self):
	
		self.startSweep(self.startFreq_Hz,self.incrFreq_Hz,self.endFreq_Hz)

	def oneSweep(self,startf,stepf,endf):
	
		self.startSweep(startf,stepf,endf);
		self.start_scan=0
		self.progRoach()
		
	def oneSweep2(self,):
		self.startSweep(self.startFreq_Hz,self.incrFreq_Hz,self.endFreq_Hz)
		
		
		self.start_scan=0
		self.progRoach()



	def stopSweep(self):
		self.start_scan=0
		self.progRoach()
		self.msm_rst=1
		self.progRoach()
		self.msm_rst=0
		self.progRoach()



	def getDFTdata(self,output,nr_i):

		regnames=[
		'DFTMem1_MemRecord_%s'%(ramname),
		'DFTMem1_MemRecord_%s'%(ramname),
		'DFTMem2_MemRecord_%s'%(ramname),
		'DFTMem2_MemRecord_%s'%(ramname),
		'DFTMem3_MemRecord_%s'%(ramname),
		'DFTMem3_MemRecord_%s'%(ramname),
		'DFTMem4_MemRecord_%s'%(ramname),
		'DFTMem4_MemRecord_%s'%(ramname)]
		
		
		roachlock.acquire()
		
		try:
			aa=struct.unpack('>'+'I'*self.memLen,roach.read(regnames[output],self.memLen*4))
		except:
			aa=range(self.memLen)
			print "No roach board"
			
		
		roachlock.release()
		
		
		dftmem=[]
		odd=output&0x1
		
		for i in range(self.memLen/8):
		
			i8=i*8
			
			fracpart=int(aa[i8 + 4*odd + nr_i])
			intpart=int(aa[i8 + 4*odd + nr_i + 2]&0x7fffffff)
			intpart= intpart - int(aa[i8 + 4*odd + nr_i + 2]&0x80000000)
			
			
			val = float(intpart) + float(fracpart)/math.pow(2.0,32)
			val = val/self.dftLen
			#if sgn!=0:
			#	val = val -1.0
				
			#val = float(aa[1])/self.memLen.0
			
			dftmem.append(val)

		
		#hw bug in the roach makes last sample jump.
		dftmem[ (self.memLen/8)-1]=dftmem[ (self.memLen/8)-2]
		return(numpy.array(dftmem))

	
	# execfile('t_brdconfig.py')
	# na=networkAnalyzer(roach)
	
	
	#return re and Imag
	def getDFT_I(self):
	
		i3r=self.getDFTdata(0,1)
		i0r=self.getDFTdata(2,1)
		i1r=self.getDFTdata(4,1)
		i2r=self.getDFTdata(6,1)
		
		Ir=i0r + i1r + i2r + i3r 
		
		 
		i3i=self.getDFTdata(0,0)
		i0i=self.getDFTdata(2,0)
		i1i=self.getDFTdata(4,0)
		i2i=self.getDFTdata(6,0)
		
		Ii=i0i + i1i + i2i + i3i 
		
		return([Ir, Ii])
	

	#return re and Imag	
	def getDFT_Q(self):
		q3r=self.getDFTdata(1,1)
		q0r=self.getDFTdata(3,1)
		q1r=self.getDFTdata(5,1)
		q2r=self.getDFTdata(7,1)
		
		Qr=q0r + q1r + q2r + q3r 
		
		 
		q3i=self.getDFTdata(1,0)
		q0i=self.getDFTdata(3,0)
		q1i=self.getDFTdata(5,0)
		q2i=self.getDFTdata(7,0)
		
		Qi=q0i + q1i + q2i + q3i 
		
		return([Qr, Qi])
	
	
	

	def removeTwoPi(self,phases):
	    offset=0;
	    for k in range(len(phases)-1):


		    dphs=phases[k+1]-phases[k]
		    if abs(dphs)>3.1416:
			    offset= (-1.0 * sign(dphs) * 2*3.141592653589793)

			    for k2 in range(k,len(phases)-1):
				    phases[k2+1]=phases[k2+1] + offset

	    return(phases)

	
	def getDFT_IQ(self):
		global sweep_counter
		
		Q=self.getDFT_Q()
		I=self.getDFT_I()
		
		
		
		
		#trick fft so we see negative freqeucnes only. 
		#dft in roach use negative phase, or neg sin.
		#we use neg sin in freq generation for negative sideband.
		#we alter calc so we can see correct IQ
		if self.isneg_freq==1:
			re=I[0] + Q[1]
			im=I[1] - Q[0]
			
		else:
			re=I[0] - Q[1]
			im=I[1] + Q[0]
		
			
		
		self.Q_raw=re
		self.I_raw=im	
		#IQ in polar form. [mags, radians]
		iqp=self.RectToPolar([re,im]);
		#polar version of phase delay, should be 1Arg(phases).
		phasep=self.RectToPolar([self.phasesRe,self.phasesIm]);
		
		
		if (self.incrFreq_Hz<0.001):
			iqp[1] = iqp[1] + phasep[1][0]
		else:	
			iqp[1] = iqp[1] + phasep[1]
	
		
		#put fudge factor so full scale sine has coef of 0.5
		#this was measured w/ loopback mode sweep, loopcak w/ fpga loopbacl
		iqp[0] = iqp[0]*0.42334
		
		
		iqdelay=self.PolarToRect(iqp)
		
			
		
		self.iqdata=iqdelay
		
		
		sweep_counter=sweep_counter+1
		
		self.hdfWrite()
		
		
		return(iqdelay)
		#return([re,im])




	#set in sec
	def setDelay(self,d):
		#230e9 is ADC/DAC time delay in ns- we add that to xmission line dly
		self.delay=d+267e-9

		self.calcPhaseDelay()

	
	
	def calcPhaseDelay(self):
	
		#self.carrierfreq
		
		#self.startFreq_Hz=10e6
		#end freq Hz
		#self.endFreq_Hz=50e6
		#freq incr Hz
		#self.incrFreq_Hz=0.1e6

		
		stf=self.startFreq_Hz
		edf=self.startFreq_Hz + ((self.memLen4/2)-1)*self.incrFreq_Hz

		freqs=2*pi* (numpy.linspace(stf,edf,(self.memLen4/2)) - self.carrierfreq)
		

		
		self.phasesRe= numpy.cos(freqs*self.delay)
		self.phasesIm= numpy.sin(freqs*self.delay)

	
	
	def plotDFT_IQp(self):
		freqs=self.startFreq_Hz + (numpy.arange(self.memLen4) * self.incrFreq_Hz)
		
		
		
		
		IQ=self.getDFT_IQ()
		
		IQp=self.RectToPolar(IQ)
		
		figure(1)
		clf()
		subplot(2,1,1)
		plot(freqs,IQp[0])
		subplot(2,1,2)
		plot(freqs,IQp[1])
		
	def polar(self,data):
		figure(2)
		clf()
		iqp=self.RectToPolar(data)
		polar(iqp[1],iqp[0])

	def plotFreq(self,data):
		freqs=self.startFreq_Hz + (numpy.arange(self.memLen/8) * self.incrFreq_Hz)
		
		if self.incrFreq_Hz<0.001:
			freqs=numpy.arange(self.memLen/8);
		
		
		IQ=data
		
		IQp=self.RectToPolar(IQ)
		
		figure(1)
		clf()
		subplot(4,1,1)
		plot(freqs,IQp[0])
		ylabel('Magnitude')
		subplot(4,1,2)
		plot(freqs,self.removeTwoPi(IQp[1]))
		ylabel('Phase')
		subplot(4,1,3)
		plot(freqs,IQ[0])
		ylabel('I')
		subplot(4,1,4)
		plot(freqs,IQ[1])
		ylabel('Q')
		xlabel('Frequency')
		draw()


	def polarDFT_IQ(self):
		freqs=self.startFreq_Hz + (numpy.arange(self.memLen4) * self.incrFreq_Hz)
		
		
		
		
		IQ=self.getDFT_IQ()
		
		IQp=self.RectToPolar(IQ)
		
		figure(2)
		clf()
		polar(IQp[1],IQp[0])
		
				
		 
	def plotDFT_IQr(self):
		freqs=self.startFreq_Hz + (numpy.arange(self.memLen4) * self.incrFreq_Hz)
		
		
		
		
		IQ=self.getDFT_IQ()
		
		
		
		figure(1)
		clf()
		subplot(2,1,1)
		plot(freqs,IQ[0])
		subplot(2,1,2)
		plot(freqs,IQ[1])
		

	
	# execfile('t_brdconfig.py')
	# na=networkAnalyzer(roach)
	
	
	
	#print na.findResPhase(na.iqdata,0,3500e6)
	#print na.findResAmp(na.iqdata,0,3500e6)


		
	def removeTwoPi(self,phases):
		offset=0;
		for k in range(len(phases)-1):


			dphs=phases[k+1]-phases[k]
			if abs(dphs)>3.1416:
				offset= (-1.0 * sign(dphs) * 2*3.141592653589793)

				for k2 in range(k,len(phases)-1):
					phases[k2+1]=phases[k2+1] + offset

		return(phases)

	

	def RectToPolar(self,data):
	
		mags = numpy.sqrt(data[0]*data[0] + data[1]*data[1])
		phase=numpy.arctan2(data[1],data[0])
		return([mags,phase])
		
	def PolarToRect(self,data):
		mags=data[0]
		phase=data[1]
		re=mags*numpy.cos(phase)
		im=mags*numpy.sin(phase)
		return([re,im])
	

	#return re and Imag	
	def plotDFTmagsPh(self,output):
	
	
		freqs=[]
		for k in range(self.memLen4):
			f=self.startFreq_Hz + k*self.incrFreq_Hz
			freqs.append(f)
		
		dftm=self.getDFTmagsPh(output)
		figure(1)
		clf();
		subplot(2,1,1)
		
		plot(freqs,dftm[0])
		subplot(2,1,2)
		plot(freqs,dftm[1])

		
	
	def polarDFTmagsPh(self,output):
		dftm=self.getDFTmagsPh(output)
		figure(2)
		clf();
		polar(dftm[1],dftm[0])

		
	def getDFTmagsPh(self,output):


		re=self.getDFTdata(output,0)
		im=self.getDFTdata(output,1)
		
		magph=self.RectToPolar([re,im])
		
		return(magph)

	
	
	# execfile('t_brdconfig.py')
	# na=networkAnalyzer(roach)
	
		
	def calcRegs(self):
		self.startFreq=int((math.pow(2,30) * self.startFreq_Hz)/(self.sys_clk))
		self.endFreq=int((math.pow(2,30) * self.endFreq_Hz )/self.sys_clk)
		self.freqAddend=int((math.pow(2,30) * self.incrFreq_Hz )/self.sys_clk)
		
		self.controlReg=(self.sd_mod<<3) + (self.msm_rst<<0) + (self.start_scan<<1)
		self.controlReg = self.controlReg + (self.startOutputDac<<4 )+ (self.manDFT<<5) 
		self.controlReg = self.controlReg +(self.manualSweep<<2)
		self.controlReg = self.controlReg + (self.adcmem_start<<7) + (self.adcmem_wr<<8)
		self.controlReg = self.controlReg + (self.adcmem_sel<<9) + (self.adcfsync<<12)
		self.controlReg = self.controlReg + (self.adc_nloopback<<13)
		
		self.controlReg = self.controlReg + (self.useOverlapWind<<14)

		self.controlReg = self.controlReg + (self.dac_reset_bit<<15)
		
	
		
		self.IOutGReg=int(math.pow(2,31)*self.IOutGain)
		self.QOutGReg=int(math.pow(2,31)*self.QOutGain)
		
		
		self.invDftLen=int(pow(2,26) * (64.0 / self.dftLen))
	
	def progRoach(self):
		self.calcRegs()	
		
		if self.is_print==1:
		    msg='controlReg %d\n'%(self.controlReg)
		    print msg
		    msg='startFreq %d\n'%(self.startFreq)
		    print msg
		    msg='endFreq %d\n'%(self.endFreq)
		    print msg
		    msg='freqAddend %d\n'%(self.freqAddend)
		    print msg
		    msg='dftLen %d\n'%(self.dftLen)
		    print msg
		
		roachlock.acquire()
		
		if 1==1:
			self.roach.write_int('controlReg', self.controlReg)
			self.roach.write_int('startFreq', int(self.startFreq))
			self.roach.write_int('endFreq', int(self.endFreq))
			self.roach.write_int('freqAddend', int(self.freqAddend))
			self.roach.write_int('dftLen', self.dftLen)
		#!!
			if self.hasIQGainReg==1:
				self.roach.write_int('GainCal_IGain', self.IOutGReg)
				self.roach.write_int('GainCal_QGain', self.QOutGReg)			
			
			self.roach.write_int('SixFourDivLen32p26', self.invDftLen)
			
		else:
			print "No Roach board"
				
		roachlock.release()
	
	

	def getStatusFlags(self):
		
	    roachlock.acquire()
		
	    try:
		self.statusFlags=self.roach.read_int('statusFlags')
		self.stat_sweepDone=self.statusFlags & 1
	    except:
		print "No Roach board"
		
	    roachlock.release()
		
		

	def resetDAC(self):

	
	    print "Reset Dac"
    	    self.msm_rst=1
	    self.dac_reset_bit=1
	    self.startOutputDac=0
	    self.progRoach()

	    self.dac_reset_bit=0
     	    self.msm_rst=0
	    self.startOutputDac=1
	    self.progRoach()

	    
	def report(self):
	    contents= inspect.getmembers(self)
	    for c in contents:
	     	print c
	

	def report2(self):
	    contents= inspect.getmembers(self)
	    return(contents)
	
	def getTimestamp(self):	
		timestamp = "T".join( str( datetime.datetime.now() ).split() )
		return(timestamp)
	

	def hdfOpen(self,name,number):
		
		
		
		self.hdfClose()
		self.hdffile = h5py.File('%s_%05d.hdf'%(name,number),'w-')

		print self.hdffile
		


		self.hdf_grp_iqdata=self.hdffile.create_group("IQData")

	
		self.hdf_dset_i = self.hdf_grp_iqdata.create_dataset("I", (4096,2,len(self.iqdata[0])), dtype='f8', maxshape=(None, None,None))
		self.hdf_dset_q = self.hdf_grp_iqdata.create_dataset("Q", (4096,2,len(self.iqdata[1])), dtype='f8', maxshape=(None, None,None))

		self.hdf_dset_iq = self.hdf_grp_iqdata.create_dataset("IQ", (4096,2,len(self.iqdata[0])), dtype='f8', maxshape=(None, None,None))
		self.hdf_dset_iq_timestamps = self.hdf_grp_iqdata.create_dataset("Times", (4096,), dtype='S26', maxshape=(None))

		self.hdf_grp_settings=self.hdffile.create_group("Settings")


		
		self.hdf_dset_attU6 = self.hdf_grp_settings.create_dataset("AttenU6", (4096,), dtype='f8', maxshape=(None))
		self.hdf_dset_attU7 = self.hdf_grp_settings.create_dataset("AttenU7", (4096,), dtype='f8', maxshape=(None))
		self.hdf_dset_attU28 = self.hdf_grp_settings.create_dataset("AttenU28", (4096,), dtype='f8', maxshape=(None))
		

		self.hdf_dset_bbloop = self.hdf_grp_settings.create_dataset("bbloop", (4096,), dtype='i1', maxshape=(None))
		self.hdf_dset_rfloop = self.hdf_grp_settings.create_dataset("rfloop", (4096,), dtype='i1', maxshape=(None))
		self.hdf_dset_clkinternal = self.hdf_grp_settings.create_dataset("clkinternal", (4096,), dtype='i1', maxshape=(None))
		self.hdf_dset_lointernal = self.hdf_grp_settings.create_dataset("lointernal", (4096,), dtype='i1', maxshape=(None))
		self.hdf_dset_losource = self.hdf_grp_settings.create_dataset("losource", (4096,), dtype='i1', maxshape=(None))


		self.hdf_dset_SweepStFreq = self.hdf_grp_settings.create_dataset("SweepStFreq", (4096,), dtype='f8', maxshape=(None))
		self.hdf_dset_SweepEdFreq = self.hdf_grp_settings.create_dataset("SweepEdFreq", (4096,), dtype='f8', maxshape=(None))

		self.hdf_dset_SweepIncFreq = self.hdf_grp_settings.create_dataset("SweepIncFreq", (4096,), dtype='f8', maxshape=(None))
		self.hdf_dset_DFTLen = self.hdf_grp_settings.create_dataset("DFTLen", (4096,), dtype='f8', maxshape=(None))
		self.hdf_dset_Delay = self.hdf_grp_settings.create_dataset("Delay", (4096,), dtype='f8', maxshape=(None))
		self.hdf_dset_sdmod = self.hdf_grp_settings.create_dataset("sdmod", (4096,), dtype='f8', maxshape=(None))


		self.hdf_dset_LO = self.hdf_grp_settings.create_dataset("LOFreq", (4096,), dtype='f8', maxshape=(None))

		self.hdf_dset_CLK = self.hdf_grp_settings.create_dataset("ClkFreq", (4096,), dtype='f8', maxshape=(None))
		
		self.hdf_dset_Anritsu = self.hdf_grp_settings.create_dataset("AnritsuPower", (4096,), dtype='f8', maxshape=(None))
		
		
		
		
		
		self.hdf_dset_device_name = self.hdf_grp_settings.create_dataset("DeviceName", (4096,), dtype='S64', maxshape=(None))
		self.hdf_dset_resonator_number = self.hdf_grp_settings.create_dataset("ResonatorNumber", (4096,), dtype='f8', maxshape=(None))
		
		self.hdf_dset_num_sweeps=self.hdf_grp_iqdata.create_dataset("NumSweeps", (1,), dtype='f8', maxshape=(None))


		self.iq_index=0
		self.set_index=0	
			

	def hdfWrite(self):
	
	
		if (self.hdffile!=None):
			print "Writing to file... %d"%(self.iq_index)
			self.hdf_dset_iq[self.iq_index,0]=self.iqdata[0]
			self.hdf_dset_iq[self.iq_index,1]=self.iqdata[1]
			


			self.hdf_dset_i[self.iq_index,0]=self.I_raw[0]
			self.hdf_dset_i[self.iq_index,1]=self.I_raw[1]

			self.hdf_dset_q[self.iq_index,0]=self.Q_raw[0]
			self.hdf_dset_q[self.iq_index,1]=self.Q_raw[1]


			self.hdf_dset_iq_timestamps[self.iq_index]=self.getTimestamp()

			


			self.hdf_dset_attU6[self.iq_index]=at.atten_U6
			self.hdf_dset_attU7[self.iq_index]=at.atten_U7
			self.hdf_dset_attU28[self.iq_index]=at.atten_U28


			self.hdf_dset_bbloop[self.iq_index]=rf.baseband_loop
			self.hdf_dset_rfloop[self.iq_index]=rf.rf_loopback
			self.hdf_dset_clkinternal[self.iq_index]=rf.clk_internal
			self.hdf_dset_lointernal[self.iq_index]=rf.lo_internal
			self.hdf_dset_losource[self.iq_index] = rf.lo_source



			self.hdf_dset_SweepStFreq[self.iq_index] =self.startFreq_Hz
			self.hdf_dset_SweepEdFreq[self.iq_index] =self.endFreq_Hz

			self.hdf_dset_SweepIncFreq[self.iq_index]=self.incrFreq_Hz
			self.hdf_dset_DFTLen[self.iq_index] =self.dftLen
			self.hdf_dset_Delay[self.iq_index]=self.delay
			self.hdf_dset_sdmod[self.iq_index]=self.sd_mod


			self.hdf_dset_LO[self.iq_index]=self.carrierfreq

			
			self.hdf_dset_CLK[self.iq_index]=s.rfout_freq
			
			self.hdf_dset_Anritsu[self.iq_index]=self.anritsu_power
			
	
			self.hdf_dset_device_name[self.iq_index]=self.device_name.encode('utf8')
			
			self.hdf_dset_resonator_number[self.iq_index]=self.resonator_number
			
			self.hdf_dset_num_sweeps[0]=self.iq_index+1
			
			self.iq_index=self.iq_index+1
			
	
		
	def hdfClose(self):
		if self.hdffile!=None:
			self.hdffile.flush()
			self.hdffile.close()
			
			
		if self.hdffile_r!=None:
			
			self.hdffile_r.close()
			
		self.hdffile=None
		self.hdffile_r=None

	def hdfOpenR(self,name,number):
		
		print 'Attempt to open file %s_%05d.hdf'%(name,number)
		self.hdfClose()


		self.hdffile_r = h5py.File('%s_%05d.hdf'%(name,number),'r')


		print self.hdffile_r.keys()

		self.iq_index=0
		self.set_index=0	



		
		
		
			
	def hdfReadIQ(self):
		self.iqdata=[0,0]
		
		print " "
		print "#######################################"
		print " "
		
		
		try:
			self.iqdata[0]=self.hdffile_r['IQData']['IQ'][self.iq_index][0]
			self.iqdata[1]=self.hdffile_r['IQData']['IQ'][self.iq_index][1]
			print self.hdffile_r['IQData']['Times'][self.iq_index]
	
		except:
			print "No IQData"
			
		

		
		try:
			self.I_raw[0]=self.hdffile_r['IQData']['I'][self.iq_index][0]
			self.I_raw[1]=self.hdffile_r['IQData']['I'][self.iq_index][1]
			self.Q_raw[0]=self.hdffile_r['IQData']['Q'][self.iq_index][0]
			self.Q_raw[1]=self.hdffile_r['IQData']['Q'][self.iq_index][1]
	
		except:
			print "No I,Q Raw Data"
			
	
		
		try:
		
			print 'Atten U6: %f'%(self.hdffile_r['Settings']['AttenU6'][self.iq_index])
			print 'Atten U7: %f'%(self.hdffile_r['Settings']['AttenU7'][self.iq_index])
			print 'Atten U28: %f'%(self.hdffile_r['Settings']['AttenU28'][self.iq_index])
		except:
			print "Missing Atten Settings"
			
		try:				
			print 'bbloop: %d'%(self.hdffile_r['Settings']['bbloop'][self.iq_index])
			print 'rfloop: %d'%(self.hdffile_r['Settings']['rfloop'][self.iq_index])
			print 'clkinternal: %d'%(self.hdffile_r['Settings']['clkinternal'][self.iq_index])
			print 'lointernal: %d'%(self.hdffile_r['Settings']['lointernal'][self.iq_index])
			print 'losource: %d'%(self.hdffile_r['Settings']['losource'][self.iq_index])
		except:
			print "Missing IF Settings"
		
		try:	
			print 'SweepStFreq: %f'%(self.hdffile_r['Settings']['SweepStFreq'][self.iq_index])
			print 'SweepEdFreq: %f' %(self.hdffile_r['Settings']['SweepEdFreq'][self.iq_index])
			print 'SweepIncFreq: %f'%(self.hdffile_r['Settings']['SweepIncFreq'][self.iq_index])
			print 'DFTLen: %f'%(self.hdffile_r['Settings']['DFTLen'][self.iq_index])
			print 'Delay: %f'%(self.hdffile_r['Settings']['Delay'][self.iq_index])
			print 'sdmod: %f'%(self.hdffile_r['Settings']['sdmod'][self.iq_index])
			
			self.startFreq_Hz=float(self.hdffile_r['Settings']['SweepStFreq'][self.iq_index])
			self.endFreq_Hz=float(self.hdffile_r['Settings']['SweepEdFreq'][self.iq_index])

			self.incrFreq_Hz=float(self.hdffile_r['Settings']['SweepIncFreq'][self.iq_index])
			self.dftLen=int(self.hdffile_r['Settings']['DFTLen'][self.iq_index])
			self.delay=float(self.hdffile_r['Settings']['Delay'][self.iq_index])
			self.sd_mod=int(self.hdffile_r['Settings']['sdmod'][self.iq_index])

		except:
			print "Missing NetAnal Settings"
			
		try:				
			
			print 'LOFreq: %f'%(self.hdffile_r['Settings']['LOFreq'][self.iq_index])
			print 'ClkFreq: %f'%(self.hdffile_r['Settings']['ClkFreq'][self.iq_index])
			
			self.carrierfreq=self.hdffile_r['Settings']['LOFreq'][self.iq_index]
			clkfreq=self.hdffile_r['Settings']['LOFreq'][self.iq_index]
			self.dac_clk=float(clkfreq/8)
			self.sys_clk=float(clkfreq/32)
			
		except:
			print "Missing Clk Settings"
			
					
		
	
		self.iq_index=self.iq_index+1

#######################################################################################
 #get a vector of data from /Settings. A vector is returned, one element
 #for each analuyzer sweep. Though the file always stores vectors of len
 #4096, the returned vector here is only the elements where there is
 #valid data, which could be much shorter...
 #also we can return vectors of data that arre calculated from stored 
 #data in hdf file, like freq span and freq center of sweep.


 #find leng of data in the file. if LO is 0, then no data for that sweep.
 #the jdf file always has vectors of 4096 len as defailt, but that does
 #not mean there is valid data in the whole vector...

	def HDF_getSetting(self,filename,setname):

	
		


		hdffile_r = h5py.File(filename,'r')

		LO=hdffile_r['Settings']['LOFreq'][:]

		
		setlen=len(find(LO)>0);

		stf=hdffile_r['Settings']['SweepStFreq'][:]
		edf=hdffile_r['Settings']['SweepEdFreq'][:]
		incf=hdffile_r['Settings']['SweepIncFreq'][:]





		f_cent=LO - (stf+edf)/2;
		f_span = edf-stf;

		if (setname=='Freq_Span'):

			

			set=f_span[:setlen];   

		elif   (setname=='Freq_Cent'):


			set=f_cent[:setlen];

		else:

			set=hdffile_r['Settings'][setname][:setlen]

		hdffile_r.close()
		
		return(set)

################################################################################33
#hdf file is a list of sweeps doen by net analuyzer. give filename
#and which sweep as an integer from 1 to 4096 (max size of file for now...)
#it returns i,q and freq vector as well as center freq, span and string
#timestamp as to when the sweep was taken.
#call as such
#[i,q,f]=HDF_readIQ('myfile.hdf', 22)
#or for more info
#[i,q,freqs,f_cent,f_span,timestamp]=HDF_readIQ('myfile.hdf', 29)
#the 22 and 29 are just examples for sweep 22 and 29.
#
#(i,q,f,fc,fs,ts)=na.HDF_readIQ(filename,1);
#clf();plot(f,i**2 + q**2)
#
#####################################################################################33		

	#function [i,q,freqs,f_cent,f_span,timestamp]=HDF_readIQ(filename, sweep_index)
	def HDF_readIQ(self,filename, sweep_index):


		
		hdffile_r = h5py.File(filename,'r')

		i=hdffile_r['IQData']['IQ'][sweep_index][0]
		q=hdffile_r['IQData']['IQ'][sweep_index][1]



		i=i[::-1];
		q=q[::-1];
		 

		stf=hdffile_r['Settings']['SweepStFreq'][sweep_index]
		edf=hdffile_r['Settings']['SweepEdFreq'][sweep_index]
		incf=hdffile_r['Settings']['SweepIncFreq'][sweep_index]

		 
		rawfreqs=arange(stf,edf,incf);
		rawfreqs=rawfreqs[::-1]

		LO=hdffile_r['Settings']['LOFreq'][sweep_index]


		freqs=LO - rawfreqs;


		f_cent=LO - (stf+edf)/2;
		f_span = edf-stf;
		timestamp = hdffile_r['IQData']['Times'][self.iq_index]
		
 
		hdffile_r.close()
		
		return( (i,q,freqs,f_cent,f_span,timestamp) )		 
		 
################################################################################ 
#list strings you can use in the HDF_getSetting function. these
#strings are all names for data stored in the HDF file, like span,
#start and end freq. some of the settings are actually not in the file
#but calculated from data in the file.
################################################################################3
 
	def HDF_ListSettings(self, filename):
		hdffile_r = h5py.File(filename,'r')

		for k in hdffile_r['Settings'].keys(): print k

		print "Freq_Cent"
		print "Freq_Span"

		hdffile_r.close()


	####################################################################3
	#
	#
	#
	#####################################################################
	
	def HDF_getResonator(self,filename,sweep_index, resnum,chipname):
		res=resonatorData(resnum,chipname);
		
		delay=	self.HDF_getSetting(filename, 'Delay')[sweep_index]	
		lo=	self.HDF_getSetting(filename, 'LOFreq')[sweep_index]	
		(i,q,f,fc,fs,ts)=self.HDF_readIQ(filename,sweep_index);

		res.setData([i,q], f, delay,lo)
		
			
		return(res)	





	def TpowerSweep(self,attInSt,attSt,attEd,sweeps,mkidlist):
	    
	    self.attInStart=attInSt
	    self.attStart=attSt
	    self.attEnd=attEd
	    self.numSweeps=sweeps
	    self.attIncr=1
	
	    self.markerlistx=mkidlist
	
	    print 'attInSt %f, attSt %f, attEd %f,sweeps %f,attIncr %f'%(attInSt,attSt,attEd,sweeps,self.attIncr)
	    self.thread=NetThread(0);
	    self.thread.start()
	
	
		
	def powerSweep(self,attInSt,attSt,attEd,step,sweeps,span,mkidlist):

	    
	    self.attInStart=attInSt
	    self.attStart=attSt
	    self.attEnd=attEd
	    self.numSweeps=sweeps
	    self.res_span = span
	    self.attIncr= step
	
	    self.markerlistx=mkidlist
            print "Starting Power Sweep " 
            self.powerSweep3()



	def powerSweep3(self):
	    self.thread_running=1
	    #markerlist is really MKID objhects

	    if len(self.markerlistx)>0:
    	        for mkid in self.markerlistx:
		
			cf=mkid.rough_cent_freq
			self.resonator_number=mkid.resonator_num
			
			fff=self.calcFreqVals(cf, self.res_span)
			lo=fff[0]
			st=fff[1]
			ed=fff[2]
		
			self.setCarrier(lo)
			self.startSweep(st,-1,ed) 
			
			#read in one sweep... because there is some wierd prob on 1st sweep
			self.oneSweep2()
			time.sleep(.1)
			#wait for 1t sweep to be done
			self.getStatusFlags()
			while(self.stat_sweepDone==0):
			    self.getStatusFlags()
			    time.sleep(.1)
			
			print "Sweeping Resonator %d around %f"%(self.resonator_number, cf)
			
			self.powerSweep2()
	    else:
	    	self.powerSweep2()
	    

	def powerSweep2(self):
	    self.thread_running=1
	    
	    
	    atin=self.attInStart
	    
	    
	    
	    for atx in arange(self.attStart,self.attEnd+1,self.attIncr):
		print 'Atten Out %f, Atten In %f'%(atx,atin)
	
		#at.atten_U6=0;
		at.atten_U7=atx;
		at.atten_U28=atin
		
		progAtten(roach,at);
		progRFSwitches(roach,rf)
		self.resetDAC()
		time.sleep(1)
		
		
		
		for k in range(self.numSweeps):
			print "Sweep %d"%(k)
			self.oneSweep2()
			time.sleep(.1)

			self.getStatusFlags()
			while(self.stat_sweepDone==0):
			    self.getStatusFlags()
			    time.sleep(.1)
			    if self.thread_running==0:
					print "Ending Loop/Thraed"
					return


			iq=self.getDFT_IQ();
			sweepCallback()
			
			res=self.getResonator()
			
			
			#find mkid in mkid list that has this resonator number and add this 
			# res trace data to its trace list.
			for m in MKID_list:
			    if m.resonator_num == self.resonator_number:
			        m.addRes(res)
				
			
			
			if self.is_plotsweep==1:
				self.plotFreq(iq)
			
			time.sleep(1)
			self.sweepcount=self.sweepcount+1
			
			if self.thread_running==0:
				print "Ending Loop/Thraed"
				return
		
		
		atin=atin-self.attIncr	
			
	
	def grabData(self,sweeps):
	    self.numSweeps=sweeps
	    
	    self.grabData3()
		


	def TgrabData(self,sweeps):
	    self.numSweeps=sweeps
	    self.thread=NetThread(1);
	    self.thread.start()
	  
		


	def grabData2(self):
	    self.thread_running=1
	    
   	    for k in range(self.numSweeps):
	    	print "Getting sweep"
		iq=self.getDFT_IQ();
		
		sweepCallback()
		
		if self.is_plotsweep==1:
			self.plotFreq(iq)
			
		self.sweepcount=self.sweepcount+1
		time.sleep(2)
		if self.thread_running==0:
			print "Ending Loop/Thraed"
			return
		
		


	def grabData3(self):
	    self.thread_running=1
	    
	    print "netAnaluzer::grabData3"
	    
   	    for k in range(self.numSweeps):
	    	print "Trigger sweep"
		
		self.oneSweep2();
		time.sleep(0.1)
		
		self.getStatusFlags();
		
		while(self.stat_sweepDone==0):
		    time.sleep(0.1)
		    self.getStatusFlags();
		    if self.thread_running==0:
			print "Ending Loop/Thraed"
			sweepCallback()
			return
		    
		    
		
		iq=self.getDFT_IQ();
		if self.is_plotsweep==1:
			self.plotFreq(iq)
		
		sweepCallback()
			
		self.sweepcount=self.sweepcount+1
		
		if self.thread_running==0:
			print "Ending Loop/Thraed"
			sweepCallback()
			return


	

	def calcFreqVals(self,cf,sf):

		#see if we have to change LO freq.
		#assume 200MHz max BW in the DAC
		lo_freq=self.carrierfreq

		lowf=cf-0.5*sf
		highf=cf+0.5*sf

		print 'lo %f low %f hi %f'%(lo_freq,lowf,highf)

		is_new_lo=False

		if self.isneg_freq==1:
		    #we are using left sideband
		    if lo_freq-lowf >=210e6:
			is_new_lo=True

		    if lo_freq-lowf <=10e6:
			is_new_lo=True

		    if lo_freq-highf >=210e6:
			is_new_lo=True

		    if lo_freq-highf <=10e6:
			is_new_lo=True

		if self.isneg_freq==0:
		    #we are using left sideband
		    if lo_freq-lowf >=-210e6:
			is_new_lo=True

		    if lo_freq-lowf <=-10e6:
			is_new_lo=True

		    if lo_freq-highf >=-210e6:
			is_new_lo=True

		    if lo_freq-highf <=-10e6:
			is_new_lo=True




		if is_new_lo:
    		    lof= 10e6+ sf/2 + cf
		    lof2=lof
		    if rf.lo_internal==1:

			LO2= clkGenSetting(lof)
			lof2=LO2.rfout_freq

		else:
		    lof=lo_freq
		    lof2=lof


		cfadc=(lof2-cf)
		stf=cfadc-sf/2
		edf=cfadc+sf/2


		answer=(lof2,stf,edf)


		return(answer)



		

# the threading or sweeping getting calls this callback
#the function can be redefined in python to dom something more.
#called whenever we get a trace from the roach board getdata() functions
def sweepCallback():
	pass
		



class NetThread (threading.Thread):
    def __init__(self, which_function):
        threading.Thread.__init__(self)
        self.which_function = which_function
        
	
	
    def run(self):
     
        global is_thread_running
	
	print "NetThread::run" 
        is_thread_running=is_thread_running+1
	
    	sweepCallback()
    
    	if self.which_function==0:
		
        	print "Starting Power Sweep " 
        	na.powerSweep3()
		

   
    	if self.which_function==1:
		
        	print "Starting grabData3 " 
        	na.grabData3()
		print "ended grabdata3"
		

 
	
        is_thread_running=is_thread_running-1
	sweepCallback()

	print "Exiting NetThread::run"	


