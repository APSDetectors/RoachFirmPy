"""


execfile('natAnalGui.py')

#works - has gain error between I and Q-0 could be puython scripts

#fwname='fftanalyzerd_2014_Apr_10_1607.bof'
#fwname = 'fftanalyzerd_2014_Apr_11_1143.bof'

fwname ='fftanalyzerd_2014_Apr_23_1437.bof'

roach=connRoach()
startFW(roach,fwname)



setupfad()


 rf.baseband_loop=1
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




	
########################################################################
#
# uise fftanalyzerc.slx
#
#
#######################################################################

class fftAnalyzere(fftAnalyzer):


	def __init__(self,r):
		fftAnalyzer.__init__(self,r)
		
		self.Q_amp_factor=-1.0
		self.isneg_freq=1

		#want 256, but some bug... 300 is fastest we can do... 
		self.fftsynctime=300
		

		#dft memlen
		self.memLen=65536
		self.memLen2=self.memLen/2
		self.memLen4=self.memLen/4
		self.memLen8=self.memLen/8


		
		#len of fft on roach
		self.fftLen=256	
		#num samples on one tap from 1/4 ADC in roach board.
		self.dftLen=self.fftLen/4
		
	
		#number of bins read out of all 4 outoputs of fft compboned. 
		self.numBinsStored=0
		
		#list of bins we actially stpre in readout ram after fifos, this is 1 and 0 array. 
		self.binReadRam=zeros(10)
				

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
	    phaseterm=phaseterm-ramp
	    #sub 1st point, to offset from 0 phase
	    phaseterm = phaseterm-numpy.median(phaseterm)
	    #make phase around pi, so we dont wrap to 6.28 when removing multipiples of 2pi	    
	    phaseterm = phaseterm+pi
	
		#take out multiples of 2pi
	    phaseterm= 2*pi * (  (phaseterm/(2.0*pi) )- floor(phaseterm/(2.0*pi))  )
	    #now make around 0 radians
	    phaseterm=phaseterm-pi

	    


	    bP[1] = phaseterm
	    
	    #bP[0]= bP[0] - bP[0][0]
	    
	    return(bP)	    


	#set in sec
	def setDelay(self,d):
		#230e9 is ADC/DAC time delay in ns- we add that to xmission line dly
		self.delay=d+230e-9

		self.resetDelay()



	
	def resetDelay(self):
	
		flist = self.getFreqsFromBins(self.fft_bins_requested)

		if self.isneg_freq:
		    freqs=2*pi*numpy.array(flist)  - self.carrierfreq
		else:
		    freqs=-2*pi*numpy.array(flist)  - self.carrierfreq
		
		
		self.phasesRe= numpy.cos(freqs*self.delay)
		self.phasesIm= numpy.sin(freqs*self.delay)



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
	    recordlen=self.getRecordLen()

	    
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

	    for spec in range(1,nspectra):
		st=spec*recordlen
		ed=st+recordlen
		record_R=self.iqdata[0][ st:ed]
		record_I=self.iqdata[1][ st:ed]
		binR[spec]=record_R[binindex]
		binI[spec]=record_I[binindex]


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
		
	
	def getDFTdata(self,output):

		#for debugging so we can see last read from mem
      		global aa;
		
		#I even re, even im, odd re, odd im
		regnames=[
		'MemRecordReal1_%s'%(ramname),
		'MemRecordImag1_%s'%(ramname),
		'MemRecordReal_%s'%(ramname),
		'MemRecordImag_%s'%(ramname),
		]
		
		aa=struct.unpack('>'+'I'*self.memLen2,roach.read(regnames[output],4*self.memLen2))
		
#aa=struct.unpack('>'+'I'*fa.memLen,roach.read(regnames[output],4*(fa.dftLen/4)))
		
		dftmem=[]
		odd=output&0x1
		
		for i in range(self.memLen2):
		
			
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

	    self.resetDelay()


	
	
	def getDFT_IQ(self):
	
		
		
		#get re and im from both ffts.
		# re0,im0 happens before re1,im1. the times are pingponged.
		re0=self.getDFTdata(0)
		im0=self.getDFTdata(1)
		re1=self.getDFTdata(2)
		im1=self.getDFTdata(3)

		re = zeros(self.memLen)
		im = zeros(self.memLen)
		
		
		#for now put all re0,im0 1st then a block of re1mim1. it has to be reorderd to ping pong
		re[:self.memLen2]=re0
		re[self.memLen2:]=re1
		
		im[:self.memLen2]=im0
		im[self.memLen2:]=im1
		
		self.iqdata=[zeros(self.memLen), zeros(self.memLen)]
		
		
		iqtemp=[re,im]
		
		#reorder to a fft ping pong. count 1/2 spectra
		numsp2=	self.getNumSpectra()/2	
		for k in range(numsp2):
		
		    #get ping and pong record from iqtemp
		    rec0=self.extractRecord2(k,iqtemp);
		    rec1=self.extractRecord2(k+numsp2,iqtemp);
		    
		    #put into iqdata, in new order.	    
		    self.replaceRecord(2*k,rec0)
		    self.replaceRecord(2*k + 1,rec1)
		    
		    
		
		#self.Q_raw=[re, im]
		#self.I_raw=[re, im]
		
		
		
		
		self.resetDelay()
		
		
		phasep=self.RectToPolar([self.phasesRe,self.phasesIm]);
		
		for k in range(self.getNumSpectra()):
		    rec=self.extractRecord(k);
		    iqp=self.RectToPolar(rec)
		    iqp[1] = iqp[1] + phasep[1]
		    iqdelay=self.PolarToRect(iqp)		    
		    self.replaceRecord(k,iqdelay)
		
		self.hdfWrite()
		
			
		
		
		
		return(self.iqdata)
		#return([re,im])


	

	
	
	# execfile('t_brdconfig.py')
	# na=networkAnalyzer(roach)
	
		
	def sendBinFlags(self):
		#clear the rams
		self.roach.write('BinData',self.convertToBinary8([0]*4096));
		self.roach.write('BinReadOut',self.convertToBinary8([0]*4096));
	
	
		self.roach.write('BinData',self.convertToBinary8(self.fft_bin_flags));
				#
		# figure out what goes in the binread ram. 
		#    
	
		self.binReadRam=[0]*len(self.fft_bin_list)
		
		for bl in self.fft_bins_requested:
		    if bl in self.fft_bin_list:
		        indx=self.fft_bin_list.index(bl)
			self.binReadRam[indx]=1
			

		self.roach.write('BinReadOut',self.convertToBinary8(self.binReadRam));


	
	def progRoach(self):
		fftAnalyzer.progRoach(self)
		
		self.numBinsStored=len(self.fft_bin_list)
		
		self.roach.write_int('numBinsStored', self.numBinsStored)




	def calcRegs(self):
		
		
		
		self.controlReg= (self.msm_rst<<0) 
		self.controlReg = self.controlReg + (self.startOutputDac<<4 ) 
		self.controlReg = self.controlReg + (self.st_fft_mem<<1) + (self.fft_mem_we<<2)
		self.controlReg = self.controlReg + (self.adcmem_start<<7) + (self.adcmem_wr<<8)
		self.controlReg = self.controlReg + (self.adcmem_sel<<9) + (self.adcfsync<<12)
		self.controlReg = self.controlReg + (self.adc_nloopback<<13)
		self.controlReg = self.controlReg + (self.seeaddress<<3)
		self.controlReg = self.controlReg + (self.dac_reset_bit<<15)
		

	
