"""

execfile('freqSweep.py')


fsweep = freqSweep(roach2,'QuadIQSweep')

fsweep.setSampleOrder([1,0,3,2]);fsweep.progRoach()
fsweep.setSampleOrder([2,1,0,3]);fsweep.progRoach()



"""

class freqSweep:


	def __init__(self,rch_,fwn_):
		self.fwname = fwn_

		self.roach = rch_

		#sinusoid amplitude in the DAC, as a percent. 1.0 means DAC is full scale.
		#hardcoded in netanaluzer FW
		self.dac_sine_sweep_amp = 0.6		
		#trigger scan
		self.start_scan=0
		#rst scan
		self.rst_scan=0;
		#if hi we restart scan in hw on scan finish
		self.keep_scanning = 0;

		#start dac
		self.startOutputDac=1
		#manual increment of freq
		self.manualSweep=0


		#wait tiem msec
		self.wait_time_ms=1

		#start frequency Hz
		self.startFreq_Hz=10e6
		#end freq Hz
		self.endFreq_Hz=50e6
		#freq incr Hz
		self.incrFreq_Hz=0.1e6
	
		#sysclk freq
		self.sys_clk=128e6
		#dac clk freq
		self.dac_clk=512e6
		#sintable len
		self.sin_tablen=256
	
		#start freq register
		self.startFreq=0
		self.endFreq=0
		self.freqAddend=0
		self.controlReg=0
		self.waitTime = 0



		#order samples goto DAC. we gen 4 samples at a time
		self.sampleorder = [1,2,3,0]
		
		self.sampleorder_reg = 0
		
		
	#give lost of 4 ints from 0,3. sets samp ord reg on roach 	
	def setSampleOrder(self,so):
	
		self.sampleorder=so
		self.calcRegs()
		
		
			
	def calcRegs(self):

		self.startFreq=int((math.pow(2,30) * self.startFreq_Hz)/(self.sys_clk))

		self.endFreq=int((math.pow(2,30) * self.endFreq_Hz )/self.sys_clk)

		self.freqAddend=int((math.pow(2,30) * self.incrFreq_Hz )/self.sys_clk)

		self.waitTime = int(0.001 * self.wait_time_ms  * self.sys_clk)
		
		self.controlReg= (self.rst_scan<<0) + (self.start_scan<<1)\
			+ (self.keep_scanning<<2)
		
		self.sampleorder_reg = (self.sampleorder[0])  | (self.sampleorder[1]<<2)  | (self.sampleorder[2]<<4) | (self.sampleorder[3]<<6) 
		
		
	
	def progRoach(self):
		self.calcRegs()	
		
		
		
		#roachlock.acquire()
		self.roach.write_int(self.fwname+'_sampleorder', self.sampleorder_reg)
		
		self.roach.write_int(self.fwname+'_control', self.controlReg)
		self.roach.write_int(self.fwname+'_startFreq', int(self.startFreq))
		self.roach.write_int(self.fwname+'_endFreq', int(self.endFreq))
		self.roach.write_int(self.fwname+'_freqAddend', int(self.freqAddend))
		self.roach.write_int(self.fwname+'_waitTime', int(self.waitTime))
		
				
		#roachlock.release()
	
	def setWaitTime(self,ms):
		self.wait_time_ms = ms


	def startSweep(self,startf,stepf,endf):

	
		self.keep_scanning=0;
		self.start_scan=0;
		self.rst_scan=1;
		self.progRoach()
		self.rst_scan=0
		self.progRoach()

		self.startFreq_Hz=int(startf)
		self.endFreq_Hz=int(endf)
		
		self.incrFreq_Hz=stepf
	


		self.progRoach()
		self.keep_scanning=1;
		self.start_scan=1
		self.progRoach()

	

	def startSweep2(self):

		self.startSweep(self.startFreq_Hz,self.incrFreq_Hz,self.endFreq_Hz)

	def oneSweep(self,startf,stepf,endf):

		self.keep_scanning=0;
		self.start_scan=0;
		self.rst_scan=1;
		self.progRoach()
		self.rst_scan=0
		self.progRoach()

		self.startFreq_Hz=int(startf)
		self.endFreq_Hz=int(endf)
		
		self.incrFreq_Hz=stepf
	


		self.progRoach()
		self.keep_scanning=0;
		self.start_scan=1
		self.progRoach()
	
	def oneSweep2(self,):
		self.oneSweep(self.startFreq_Hz,self.incrFreq_Hz,self.endFreq_Hz)
	



	def stopSweep(self):
		self.start_scan=0
		self.keep_scanning=0;
		self.progRoach()
		self.rst_scan=1
		self.progRoach()
		self.rst_scan=0
		self.progRoach()



