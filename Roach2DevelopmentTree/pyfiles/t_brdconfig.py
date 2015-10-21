
print "t_brdconfig.py"


"""
execfile('t_brdconfig.py')
roach=connRoach()
startFW(roach,'ifboard_config_2013_Apr_29_1419.bof')


s= clkGenSetting(3000e6)

progLocalOsc(roach,s,lo_sle)

#You can change any setting in the struct
s.f = 200e6
#update int, divsel, frac, mod based on the req freq.
s.calcNumbers()

#change mux output to gmd
s.MUX = 2
#change muix output to pll N countput output
s.MUX =4 

#turn off rf output
s.rfouten=0

#for rf generator
progLocalOsc(roach,s,lo_sle)

#for clk generator
progLocalOsc(roach,s,clk_sle)

#you can change any setting the ADF4350 chip by changeing a settin gthe s object.
#to see all settings do this following.
s.report()



Setup for ADC board

in unix shell:
ipython -pylab


execfile('t_brdconfig.py')

roach=connRoach()

setupna()

setupfa()



startFW(roach,'fftanalyzer_2013_Aug_28_1452.bof')


startFW(roach,'dramtest_2013_Aug_27_1513.bof')


startFW(roach,'networkanalyzer_2013_Aug_21_1228.bof')
ramname='Shared_BRAM'


na.adc_nloopback=1                                                                           
na.setFreq(30e6);aa=na.captureADC3(0);clf();plot(aa[range(0,200)],'ro');plot(aa[range(0,200)]);


clf();plot(abs(fft(aa)))

na.startSweep(1e7,-1,2e7) 


na.setFreq(1e7);


roachlock.acquire()
clf();aa=na.captureADC(1);plot(aa[1:200])
roachlock.release()


roachlock.acquire();clf();aa=na.captureADC(1);plot(aa[1:200]);roachlock.release()



clf();aa=na.captureADC2(0,0);plot(aa[1:200])



clf();aa=na.captureADC3(0);plot(aa[1:200])


iq=na.getDFT_IQ();na.plotFreq(iq)


fwname='fftanalyzerc_2014_Feb_19_1623.bof'

fwname='fftanalyzerc_2014_Feb_21_0927.bof'
roach=connRoach()
startFW(roach,fwname)
"""



#import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import struct
from numpy import *
import corr, time,fractions, math,inspect,random
import time
import threading
import copy as ccopy
import pickle
import traceback

import scipy.io

#ramname='waveformRam'
ramname='Shared_BRAM'


#mapping of bits in regs
#this is based opnm the FW in theroach board. which bit in the SW register in the FW maps
#to which pin on the gpio on roach, and IF board

anritsu_freqghz_=0
anritsu_power_=0
anritsu_is_on_=0
 


ANRITSUCMD='/home/oxygen26/TMADDEN/ROACH/vx11/vxi11_1.10/anritsuOsc'
ANRITSUIP='192.168.0.68'	


#roach 1 and 2
ROACH_IP= ['192.168.0.67','192.168.0.70']
WHICH_ROACH=0

global na
global fa


def report(obj):
    lst=inspect.getmembers(obj)
    for l in lst: print l


########################################################################
#
#
#######################################################################
	

def dbgstart(isconn,fwindx):
	global roach
	global fa
	global na
	global fit
		

	
	if isconn==1:
	    roach=connRoach()
            time.sleep(2)
        
	
	startFW(roach,fwnames[fwindx])
	
	fit=fitters();
	
	if fwindx==0:
	    setupna()
	    
	    
	if fwindx==1:
	    setupfad2()
	




########################################################################
#
#
#######################################################################


def setupna():

	global dac_clk_freq
	global rf
	global na
	global at
	global s
	global LO
	global roachlock
	
	
	try:
	
		
		
		
		s= clkGenSetting(dac_clk_freq)
		LO= clkGenSetting(3500e6)

		rf=rfSwitchSetting()
		print "EXT CLOCK"
		rf.clk_internal=0
		rf.baseband_loop=0
		rf.rf_loopback=0
		print "EXT LO"
		rf.lo_internal=0
		rf.lo_source=1






		at=attenSetting()
		#all in db. it attens by these db's
		at.atten_U28=0.0
		at.atten_U6=15.0
		at.atten_U7=0.0

		progLocalOsc(roach,s,clk_sle)
		#print "EXTERNAL CLK"
		#anritsu(0.512,6.0,1)
		LO.rfouten=0
	
		progLocalOsc(roach,LO,lo_sle)



		progRFSwitches(roach,rf)




		progAtten(roach,at)

		progRFSwitches(roach,rf)

	except:
		print "No Roach Board available"
		
		
	na=networkAnalyzer(roach)

	na.sd_mod=1

	#na.startSweep(1e7,-1,2e7) 




########################################################################
#
#
#######################################################################
global fa

def setupfa():


	global dac_clk_freq
	global rf
	global na
	global at
	global s
	global LO
	global roachlock
	global fa
	
		
	try:
	
		
		
		
		s= clkGenSetting(dac_clk_freq)
		LO= clkGenSetting(3500e6)

		rf=rfSwitchSetting()
		rf.clk_internal=1
		rf.baseband_loop=0
		rf.rf_loopback=0
		rf.lo_internal=1
		rf.lo_source=1

		at=attenSetting()
		#all in db. it attens by these db's
		at.atten_U28=0.0
		at.atten_U6=15.0
		at.atten_U7=0.0

		progLocalOsc(roach,s,clk_sle)


		LO.rfouten=0
	
		progLocalOsc(roach,LO,lo_sle)



		progRFSwitches(roach,rf)




		progAtten(roach,at)

		progRFSwitches(roach,rf)

	except:
		print "No Roach Board available"
		

	fa=fftAnalyzer(roach)
	fa.setLutFreqs([10e6],10000)

	fa.resetDAC()
	fa.trigFFT()
	fa.getDFT_IQ()
	






########################################################################
#
#
#######################################################################
global fa

def setupfad():


	global dac_clk_freq
	global rf
	global na
	global at
	global s
	global LO
	global roachlock
	global fa
	
		
	try:
	
		
		
		
		s= clkGenSetting(dac_clk_freq)
		LO= clkGenSetting(3500e6)


		rf=rfSwitchSetting()
		print "EXT CLOCK"
		rf.clk_internal=0
		#rf.clk_internal=1
		rf.baseband_loop=0
		rf.rf_loopback=0
		print "EXT LO"
		rf.lo_internal=0
		rf.lo_source=1


		at=attenSetting()
		#all in db. it attens by these db's
		at.atten_U28=0.0
		at.atten_U6=15.0
		at.atten_U7=0.0

		
		LO.rfouten=0
		
		
		progLocalOsc(roach,s,clk_sle)


		
	
		progLocalOsc(roach,LO,lo_sle)



		progRFSwitches(roach,rf)




		progAtten(roach,at)

		progRFSwitches(roach,rf)

	except:
		print "No Roach Board available"
		

	fa=fftAnalyzerd(roach)
	fa.progRoach();
	



def setupfad2():
	global na
	global fa
	
	setupfad()
	na=fa;
	




########################################################################
#
#
#######################################################################
global fa

def setupfai():


	global dac_clk_freq
	global rf
	global na
	global at
	global s
	global LO
	global roachlock
	global fa
	
		
	try:
	
		
		roach.write_int('regs', 0)
		roach.write_int('if_switch', 0)
		
		s= clkGenSetting(dac_clk_freq)
		LO= clkGenSetting(3500e6)


		rf=rfSwitchSetting()
		print "EXT CLOCK"
		rf.clk_internal=0
		#rf.clk_internal=1
		rf.baseband_loop=0
		rf.rf_loopback=0
		print "EXT LO"
		rf.lo_internal=0
		rf.lo_source=1


		at=attenSetting()
		#all in db. it attens by these db's
		at.atten_U28=0.0
		at.atten_U6=15.0
		at.atten_U7=0.0

		
		LO.rfouten=0
		
		
		progLocalOsc(roach,s,clk_sle)


		
	
		progLocalOsc(roach,LO,lo_sle)



		progRFSwitches(roach,rf)




		progAtten(roach,at)

		progRFSwitches(roach,rf)

	except:
		print "No Roach Board available"
		

	fa=fftAnalyzeri(roach)
	fa.progRoach();
	



def setupfai2():
	global na
	global fa
	
	setupfai()
	na=fa;
	


########################################################################
#
#
#######################################################################
global fa

def setupfae():


	global dac_clk_freq
	global rf
	global na
	global at
	global s
	global LO
	global roachlock
	global fa
	
		
	try:
	
		
		
		
		s= clkGenSetting(dac_clk_freq)
		LO= clkGenSetting(3500e6)

		rf=rfSwitchSetting()
		rf.clk_internal=1
		rf.baseband_loop=0
		rf.rf_loopback=0
		rf.lo_internal=1
		rf.lo_source=1

		at=attenSetting()
		#all in db. it attens by these db's
		at.atten_U28=0.0
		at.atten_U6=15.0
		at.atten_U7=0.0

		
		LO.rfouten=0
		
		
		progLocalOsc(roach,s,clk_sle)


		
	
		progLocalOsc(roach,LO,lo_sle)



		progRFSwitches(roach,rf)




		progAtten(roach,at)

		progRFSwitches(roach,rf)

	except:
		print "No Roach Board available"
		

	fa=fftAnalyzere(roach)
	fa.setLutFreqs([10e6],10000)

	fa.trigFFT()
	fa.getDFT_IQ()
	



########################################################################
#conn to the roach board via katcp
#
#
#######################################################################
def connRoach():

	print "Opening client ...\n"
	roach = corr.katcp_wrapper.FpgaClient(ROACH_IP[WHICH_ROACH], 7147,timeout=20)
	return(roach)
	
	
	




########################################################################
#pass roach connection ref to katcp
#pass text string lf name of bof file. prog the roach FW
#######################################################################
def startFW(roach,bof):
	roachlock.acquire()

	
	try:
		roach.progdev(bof)
	
	except:
		print "No Roach Board"
	

	roachlock.release()





########################################################################
#
#
#
#
#######################################################################
#

global anritsu_freqghz_
global anritsu_power_
global anritsu_is_on_

def anritsu(freqghz,power,is_on):

    global anritsu_freqghz_
    global anritsu_power_
    global anritsu_is_on_
    
    anritsu_freqghz_=freqghz
    anritsu_power_=power
    anritsu_is_on_=is_on
    
    os.system('%s %s :FREQ:FIX %fGHz'%(ANRITSUCMD,ANRITSUIP,freqghz))
    os.system('%s %s :POW %f'%(ANRITSUCMD,ANRITSUIP,power))
    
    if is_on==1:
        os.system('%s %s :OUTP ON'%(ANRITSUCMD,ANRITSUIP))
    else:
        os.system('%s %s :OUTP OFF'%(ANRITSUCMD,ANRITSUIP))

	
########################################################################
#
#
#
#
#######################################################################
#
#
#def powerSweep(stF,edF, attSt,attEd,sweeps):
#
#	for atx in arange(attSt,attEd,0.5):
#		print atx
#	
#		#at.atten_U6=15;
#		at.atten_U7=atx;
#		progAtten(roach,at);
#		progRFSwitches(roach,rf)
#		
#		na.startSweep(stF,-1,edF)
#		time.sleep(5)
#		
#		
#		for k in range(sweeps):
#			iq=na.getDFT_IQ();
#			na.plotFreq(iq)
#			time.sleep(1)	
#
#
#
#	
#




	
########################################################################
#
#
#
#
#######################################################################

def testSerial(num,pin):
	roach.write_int('if_switch', 1)
	for k in range(num):
		
		roach.write_int('regs',(1<<pin))
		time.sleep(0.1)
		roach.write_int('regs',0)
		time.sleep(0.1)


	
########################################################################
#
#
# give a list or numpy array and write to a file called py2m.m 
#source code in matlab to xfer the data to matlab
#The data in matlab is an arran of name mname_. timeseries called mname
#######################################################################

def toMatlab(data,mname):

	fp=open('py2m.m','a')
	fp.write('\n\n\n')
	fp.write('%s_ = [\n'%(mname))
	for d in data:
	    fp.write('%f\n'%(d))

	
	
	fp.write('];\n\n')

	fp.write('%s=timeseries(%s_);'%(mname,mname))

	fp.flush()
	fp.close()


########################################################################
#
#
#
#
#######################################################################

def fromMatlab():
	hh=scipy.io.loadmat('m2py.mat')
	mydata=dict()
	#make format less idiotic.
	for k in hh.keys():
	    # get real fields
	    if k[0]!='_':
		mydata[k]=hh[k][0]
		
		

	h2=scipy.io.loadmat('simresults.mat')
	mydata['alldata']=h2

	return(mydata)

########################################################################
#
#
#
#
#######################################################################

def testfw2():

	setupfai2()
	rf.baseband_loop=0
	rf.rf_loopback=0
	progRFSwitches(roach,rf)
	fa.setLutSize(65536)
	fa.test_pulse_len=512
	fa.test_pulse_amp = 0

	fa.setLutFreqs([ 10109375.0,   26460937.5,  49468750.0,   61390625.0 ],32168* 0.24795532)
	fa.fftBinsFreqs();

	fa.setCarrier( 2.71923645e+09)

	fa.roach_num_ffts=1e9
	fa.trigFFT()

#
#	fa.clearFIFOs()
#	fa.fft_run_forever=1;fa.progRoach1()
#	
#	
#	fa.recordEvents(0)
#	fa.trigFFT()
#	time.sleep(1)
#	
#	fa.recordEvents(1)
#	time.sleep(0.001)
#	fa.recordEvents(0)
#	fa.getDFT_IQ()
#	
#	fa.rewindFFTMem();fa.rewindFFTMem();fa.rewindFFTMem();
#	
#	#fa.printRegs()
#	
#	
#	fa.calcPulseDetMeans()
#	
#	fa.printMeanTh()
#
#
#
#	fa.recordEvents(1)
#	time.sleep(0.001)
#	fa.recordEvents(0)
#	fa.getDFT_IQ()
#	
#	fa.rewindFFTMem();fa.rewindFFTMem();fa.rewindFFTMem();
#	
#	#fa.printRegs()
#	
#	
#	fa.calcPulseDetMeans()
#	
#	fa.printMeanTh()
#	
#	
#	
#	fa.progPulseDetector(fa.pulse_num_std,1,10)
#	
#	
#	
	
	
	
	
	
	
	
def testfw(level=4):
	if level>=3:
		setupfai2()
		rf.baseband_loop=0
		rf.rf_loopback=0
		progRFSwitches(roach,rf)
	if level>=2:
	
		#fa.setLutFreqs(arange(10.0e6,210e6,10.2e6),1000);
		#fa.setLutFreqs([10.21e6],10000);
		fa.setLutSize(65536)
		fa.test_pulse_len=512
		fa.test_pulse_amp = 0
		
		#fa.setLutFreqs([10.183923e6,50.384901e6,80e6],10000);
		#fa.setLutFreqs([12.1231e6,40.2341e6,160.1237483e6],10000);
		#fa.setLutFreqs([12.1231e6],10000);
		#fa.setLutFreqs(arange(10e6,200e6,20e6),1000)
		fa.setLutFreqs([ 10109375.0,   26460937.5,  49468750.0,   61390625.0 ],32168* 0.24795532)
		fa.fftBinsFreqs();
		
		fa.setCarrier( 2.71923645e+09)
		#fa.fftBinsAll()

	if level>=1:
		
		#for testing pulse detector
		#fa.numFFTs(8192)
		#fa.recordEvents(0)
		#fa.calcMeans(1)
		#time.sleep(0.1)
		#fa.trigFFT();
		#time.sleep(0.1)
		#fa.calcMeans(0)
			
			
		#fa.setPulseDetector(0.1,1,0)
		#fa.recordEvents(1)
		#fa.trigFFT();
		
		
		#fa.phase_inc_array=[0.0] * 256
		
		#for testing single ffts and phase etc.
		#fa.roach_num_ffts=1
		#fa.progRoach()
		#fa.trigFFT()
		
		#fa.printRegs()
		#for k in range(400):fa.retrigFFT()


		#for 10 sec of data
		#fa.clearFIFOs()
		#fa.setUsePulseServer(1)
		
		
		#fa.setPulseDetector(10,1)
		
		#fa.measurePulseDetectorMeanThresh()
		
		fa.roach_num_ffts=1e9
		fa.trigFFT()
		time.sleep(1)
		#fa.sweepAndStream('zzzz2.h5',10,0)
		
	
	if fa.getDataAvailable():
		a=fa.getDFT_IQ();
		fa.plotChan3D(zlim=[-3,+3],ampphase=1);
		#fa.plotChan3D(fignum=2,zlim=[0,0.02]);
		fa.plotChan3D(fignum=2);
		fa.waterfall(numspec=256,skip=8)
		fa.lsevents()
		fa.plotTimestamps()
		fa.plotEvents2D()
		fa.plotTimestampsD()
		fa.rewindFFTMem()
		
		
		specs=fa.getObjSpecs()
		try: os.system('rm maddog.h5')
		except: pass
		
		fp = h5py.File('maddog.h5','a')
		fa.hdfWriteObj(fp,'settings', specs)
		fp.close()

		
		
		
		
	else:
		print "No Data available from Roach"




########################################################################
#
#
#
#
#######################################################################
def matlabSim():
	global roach

	global dac_clk_freq
	global rf
	global na
	global at
	global s
	global LO
	global roachlock
	global fa
	

	os.system('rm py2m.m')

	roach=matlabRoach()
	

	roach.write_int('regs', 0)
	roach.write_int('if_switch', 0)
	s= clkGenSetting(dac_clk_freq)
	LO= clkGenSetting(3500e6)
	rf=rfSwitchSetting()	
	at=attenSetting()
	fa=fftAnalyzeri(roach)



	#loopback the test freq so we have sigal into ffts
	#disable Lut for sim	
	fa.use_test_freq=1
	#loopback- so disable dac/adc for sim
	fa.adc_nloopback=0
	#need to use opposite sudeband for sim, dont know why...
	fa.Q_amp_factor=1.0

	fa.setLutSize(2048)
	ff=[2.25e6,10.5e6,40.75e6,100.0e6,180.25e6]
	fa.setLutFreqs(ff,2000)
	#fa.fftBinsAll()
	fa.fftBinsFreqs()
	fa.fftsynctime=128
	#fa.fftBinsAll()
	fa.progRoach()
	fa.trigFFT()

	roach.current_time = 14000
	
	
	fa.clearFIFOs()

	roach.toMatlab(100)
	#puts raw array to matlab... for BinData sim? can we use workspace var in the sim?
	toMatlab(fa.fft_bin_flags,'fft_bin_flags')

	fa.setLutSize(32768*4)
	
	fa.setLutFreqs(ff,2000)

	luti=fa.toTwoComp(fa.lut_i/32768.0,16,15)
	lutq=fa.toTwoComp(fa.lut_q/32768.0,16,15)

	toMatlab(luti[0::4],'lut_i0')
	toMatlab(luti[1::4],'lut_i1')
	toMatlab(luti[2::4],'lut_i2')
	toMatlab(luti[3::4],'lut_i3')
	
	toMatlab(lutq[0::4],'lut_q0')
	toMatlab(lutq[1::4],'lut_q1')
	toMatlab(lutq[2::4],'lut_q2')
	toMatlab(lutq[3::4],'lut_q3')
	
	toMatlab(fa.pulsedetector_thram,'threshmem');
	toMatlab(fa.pulsedetector_muram,'magphmeanmem');
	
	
	
	roach.lsregs()

	#read in sumulation data from matlab
	try:	
	    md=fromMatlab()
	    fa.iqdata=fa.extractEvents(md['magv'],md['phsv'])
	except:
	    print 'run simulation in matlab'
		

########################################################################
#
# on roach box
#make a named pipe. do this ONCE
# mkfifo /root/mypipe

# on roach linux box start nc server
#nc -l 7777
# on roach box, connect my pipe to netcat, to send data to roach linux box
#nc 192.168.0.202 7777 < mypipe
# also on roach box, make sure mypipe never closes,
# while true; do sleep 999999999; done > mypipe &
#
# now do this any number of times:
#unix_cmd> /root/mypipe
#the output goes to the other computer!
#cd /proc/526/hw/ioreg
#cat MemRecordReal_Shared_BRAM >/root/mypipe
#binary data is then transferred over the network to the roach limnux box.
#For a buffer use mbuffer, buffer, or dd. dd is most common.
#arecord | dd ibs=16000 iflag=fullblock oflag=dsync | aplay


#ssh root@192.168.0.67 ps -aux | grep bof > /tmp/pslist.txt

#get pid
#ssh root@192.168.0.67 ps -aux | grep bof | awk '{print $2}'

# on linux:
# on xterm1
# mkfifo mypipe
#  nc -l 7777 > mypipe
#
#on roach
#mkfifo mypipe
#  nc 192.168.0.202 7777 <mypipe &
# sleep 9999999 > mypipe &
# slee will prevent eof from hamming and shutting nc
#./pulsereader 1729 >mypipe
# we can ctrl C the pulsereader and restart. nc will keep running. 
#
#on linux
#xterm2
# to monitor
#  ./bin2list < mypipe
# can ht ctrl C and all uis fine. server keeps running. 
# to save to fkle
#./bin2hdf5 aa.h5 <mypipe
# can hit ctrl C to save h5 files correctly
# cat mypipe > myfile.bin
# will save binary fikle

#goto 2 pipes fuill data and monitor data
# mkfifo fullpipe
# mkfifo monpipe
# nc -l 7777 | tee monpipe >fullpipe
#


#######################################################################

	
########################################################################
#
#
#
#
#######################################################################

execfile('roachMatlab.py')

execfile('netAnalyzer.py')

execfile('fftAnalyzer.py')

execfile('fftAnalyzerd.py')
execfile('fftAnalyzere.py')

execfile('fftAnalyzeri.py')


execfile('resView.py')
#execfile('t_brdconfig.py')
