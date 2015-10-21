

import os

#
# use qdrtest.slx as the firmware
#


execfile('katcpNc.py')
execfile('roachScope.py')
execfile('sramLut.py')
execfile('qdr.py')
execfile('if_board.py')
execfile('mkiddac.py')
execfile('freqSweep.py')


#need this fifos preexistant with mkfifo
#/local/roachkatcpfifoOut,
#/local/roachkatcpfifoIn

#you can edit the py codes of yuo want differnet fifo names





#
# Open connectino to roach board
#


roach2=katcpNc()
roach2.startNc()

"""
#turn off roach
roach2.shutdown()


roach2.restart()


#disconn from roach
roach2.closeFiles()

"""


#
# Send IF config FW. Needed for initial power up to get clocks working on IF board. needed for using internal 512MHz  Osc.
#


roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/if_board_setup_2015_Aug_20_1511.bof')
#if_board_setup_2015_Aug_13_1230


if_board=ifBoard(roach2,'if_board')

if_board.rf.clk_internal=1
if_board.s.rfouten=1

if_board.progIfBoard()




#no ADC
#roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_13_1051.bof')

#has dac with fb, and octo roach scope- no fb buffer
#roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_14_1650.bof')

#has dac with fb, and octo roach scope- fb buffer
#roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_17_1010.bof')


#has adc with fb, and octo roach scope- no fb buffer, 2x clk at 270, has pfb to octoscope
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_20_1631.bof')


#has adc with fb, and octo roach scope- no fb buffer, 2x clk at 270, has pfb to FFT to octoscope
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_24_1648.bof')


#has adc with fb, and octo roach scope- no fb buffer, 2x clk at 270, has pfb to FFT to octoscope, fft coef selector fsm and a  scope
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_25_1640.bof')


#has adc with fb, and octo roach scope- no fb buffer, 2x clk at 270, has pfb to FFT to octoscope, fft coef sel with scope, has rect to polar
#has scope for fft out, has scope for rectto polar oit
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_26_1341.bof')


#testing of black box fft with the version 5 cordoc on one channel.
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Oct_06_1615.bof')



#testing of black box fft with 4 cordic blocks, v5
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Oct_07_1710.bof')


#has black box fft, 4 cordics, and fft coef picker, with 
#its own roach scope
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Oct_08_1446.bof')



#has all of above, but add multififo(2),fsm, and out single event fifo
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Oct_12_1715.bof')


#call to read all reg vales on roach print on screen, return as list of tupels
#roach2.readAllReg()


#
# Define stuff
#

#roachscope = roachScope(roach2, 'roachscope')
#roachscope1 = roachScope(roach2, 'roachscope1')

adcscope = roachScope(roach2, 'octoscope')

fftscope = roachScope(roach2, 'octoscope2')

polscope = roachScope(roach2, 'octoscope1')


sram = sramLut(roach2,'SRAM_LUT')
qdr0=Qdr(roach2,'qdr0')
qdr1=Qdr(roach2,'qdr1')
if_board=ifBoard(roach2,'if_board')

dac = MKIDDac(roach2, 'MKID_DAC')



fsweep = freqSweep(roach2,'QuadIQSweep')



#
# Make sure IF is still programmed after new FW load
#


if_board.rf.clk_internal=1
if_board.s.rfouten=1
if_board.progIfBoard()


#call to read all reg vales on roach print on screen, return as list of tupels
roach2.readAllReg()







#
# calibrate the qdrs
#

qdr0.reset()
qdr0.qdr_cal()
qdr0.qdr_delay_clk_get()
qdr0.qdr_cal_check()

qdr1.reset()
qdr1.qdr_cal()
qdr1.qdr_delay_clk_get()
qdr1.qdr_cal_check()




#
# Freq Sweep generator
#


#ms between freqs, how long to stay on one step
fsweep.setWaitTime(50)
#start freq, step freq, end freq, all in Hz
fsweep.startSweep(10e6,1e6,50e6)




"""

fsweep.setWaitTime(100)
fsweep.startSweep(5e6,1e5,10e6)

fsweep.startSweep(5e6,0.0,5e6)

fsweep.startSweep(10e6,0.0,10e6)

fsweep.startSweep(1e6,0.0,1e6)

fsweep.startSweep(10e6,0.0,12e6)

"""

#
# SRAM Generator
#

sram.setLutFreqs(arange(10e6,100e6,10e6),2000)


sram.Q_amp_factor=-1.0

sram.setLutFreqs(arange(10e6,250e6,10e6),800)

"""

sram.setLutFreqs([20e6, 30e6], 1500)

sram.setLutFreqs([10e6], 32000)

sram.setLutFreqs([10e6], 1000)

sram.setLutFreqs([1e6], 32000)

sram.sample_order=[0,1,2,3]


sram.setLutFreqs(arange(10e6,100e6,10e6),2000)

"""


#
# DAC
#




dac.setReset()

dac.setSync(1,1)





#
#Select output signal
# 0 = LUT, 1=sweep sine, 2 = modulation of sweep and lut


#for lut
roach2.write_int('settings_reg',0)

#for  sweep
roach2.write_int('settings_reg',1)



#startfft
roach2.write_int('settings_reg',1)


#
#ADc scope=NON OCTOSCOPE
#
#delays = [3,2,0,1]

#roach2.write_int('MKID_ADC_iqtobus_sampleorder',(delays[0]) + (delays[1]<<2) + (delays[2]<<4) + (delays[3]<<6))

#ch=0
#roachscope1.trigScope(-1,ch);roachscope1.plotScope(signbit = 11);


#ch=4
#roachscope1.trigScope(-1,ch);roachscope1.plotSpectrum(signbit=11,log='Yes');


#
# Octoscope
#
delays = [0,1,2,3]
roach2.write_int('MKID_ADC_iqtobus_sampleorder',(delays[0]) + (delays[1]<<2) + (delays[2]<<4) + (delays[3]<<6))



execfile('roachScope.py')

adcscope = roachScope(roach2, 'octoscope')


ch=0
adcscope.trigScope(-1,ch)
adcscope.readScopeOcto()
#adcscope.multiplotdata[1]




adcscope.interleave([4,5,6,7])
adcscope.plotScope(signbit = 11,replot=True,pllen=1024);

Q = adcscope.shorts


adcscope.is_hold = True

ch=0
adcscope.trigScope(-1,ch)
adcscope.readScopeOcto()
#adcscope.multiplotdata[1]


adcscope.interleave([0,1,2,3])
adcscope.plotScope(signbit = 11,replot=True,pllen=1024);
I = adcscope.shorts




adcscope.plotSpectrum(signbit=11,log='Yes',replot=True,pllen=8192);


Q = numpy.array(Q)
I = numpy.array(I)
Q = complex(0,1)*Q
FF=fft.fft(I[:512]+Q[:512]);
clf();plot(abs(FF))
clf();semilogy(abs(FF))



#################################################################
# polar out scope
#


polscope = roachScope(roach2, 'octoscope1')



#################################################################
# FFT out scope
#


fftscope = roachScope(roach2, 'octoscope2')






ch=0
fftscope.trigScope(0,0)

fftscope.readScopeOcto()
#adcscope.multiplotdata[1]

fftscope.interleave([0]);
fftscope.plotScope(replot=True);

clf()

#fftscope.interleave([0,1,2,3])
fftscope.is_hold=True


fftscope.interleave([0]);
fftscope.plotScope(replot=True);

fftscope.interleave([1]);
fftscope.plotScope(replot=True);

fftscope.interleave([2]);
fftscope.plotScope(replot=True);

fftscope.interleave([3]);
fftscope.plotScope(replot=True);


fftscope.interleave([4]);
fftscope.plotScope(replot=True);

fftscope.interleave([5]);
fftscope.plotScope(replot=True);

fftscope.interleave([6]);
fftscope.plotScope(replot=True);

fftscope.interleave([7]);
fftscope.plotScope(replot=True);

#Q = numpy.array(fftscope.shorts)


clf()

#fftscope.interleave([0,1,2,3])
fftscope.is_hold=False


fftscope.interleave([0,1,2,3]);
fftscope.plotScope(signbit = 15,replot=True);


clf()
P = I*I + Q*Q
plot(P[:1024])





ch=0
fftscope.trigScope(-1,ch)
fftscope.readScopeOcto()
#adcscope.multiplotdata[1]



fftscope.interleave([4,5,6,7])
fftscope.plotScope(replot=True,pllen=1024);
I = adcscope.shorts


ch=0
fftscope.interleave([ch]);fftscope.plotScope(replot=True);ch=ch+1




fftscope.plotSpectrum(signbit=11,log='Yes',replot=True,pllen=8192);


Q = numpy.array(Q)
I = numpy.array(I)
Q = complex(0,1)*Q
FF=fft.fft(I+Q);
clf();plot(abs(FF))
clf();semilogy(abs(FF))



########################################################################3
#
# FFT stuff
#


execfile('roachFFT.py')


rfft = roachFFT(roach2, 'fftcoefselector')



 
rfft.setLutSource(sram)

rfft.fftBinsFreqs()

rfft.fftBinsAll(which='High')




rfft.info()

rfft.showBinFlags()

 
rfft.regs()


rfft.fftsynctime=128

rfft.progRoach()



rfft.numFFTs(-1)

rfft.trigFFT()

rfft.stopFFTs()






execfile('roachScope.py')

fscope = roachScope(roach2, 'octoscope1')


fscope.trigScope(0,0)

fscope.readScopeOcto()

fscope.interleave([1]);
fscope.plotScope(replot=True);

fscope.interleave([0,1,2,3]);
fscope.plotScope(replot=True);


fscope.interleave([0]);
fscope.plotScope(replot=True);

fscope.interleave([1]);
fscope.plotScope(replot=True);

fscope.interleave([2]);
fscope.plotScope(replot=True);

fscope.interleave([3]);
fscope.plotScope(replot=True);


fscope.interleave([7]);
fscope.plotScope(replot=True);


clf()

fscope.interleave([5]);
fscope.plotScope(
	bits ='11:6;5:0',
	is_usebits = True,replot=True);


fscope.interleave([3]);
fscope.plotScope(
	bits ='5:0',
	is_usebits = True,replot=True);




fscope.interleave([5]);
fscope.plotScope(
	bits ='5:0',
	is_usebits = True,replot=True);


fscope.interleave([4]);
fscope.plotScope(
	bits ='11:6',
	is_usebits = True,replot=True);




clf()


fscope.interleave([2]);
fscope.plotScope(
	bits ='12:12;11:11;10:10;9:9;3:3;2:2;1:1;0:0',
	is_usebits = True,replot=True);


fscope.interleave([2]);
fscope.plotScope(
	bits ='12:12;11:11;10:10;9:9',
	is_usebits = True,replot=True);


fscope.interleave([2]);
fscope.plotScope(
	bits ='3:3;2:2;1:1;0:0',
	is_usebits = True,replot=True);



fscope.is_hold=True


fscope.interleave([2]);
fscope.plotScope(
	bits ='0:0;1:1;2:2;3:3;4:4;5:5;6:6;7:7;8:8;9:9',
	is_usebits = True,replot=True);


fscope.trigScope(0,0)

fscope.readScopeOcto()

fscope.interleave([2]);
fscope.plotScope(
	bits ='6:6;5:5',
	is_usebits = True,replot=True);



clf()



fscope.trigScope(0,1)
fscope.plotScope()

fscope.trigScope(0,2)
fscope.plotScope()

fscope.trigScope(0,3)
fscope.plotScope()

fscope.trigScope(0,4)
fscope.plotScope()



"""

ch=0
roachscope.trigScope(-1,ch);roachscope.plotSpectrum();



ch=0
roachscope.trigScope(-1,ch);roachscope.plotScope();ch=ch+1

roachscope.trigScope(-1,ch);roachscope.plotScope();ch=0

"""



#
# close roach
#

"""
#turn off roach
roach2.shutdown()


#disconn from roach
roach2.closeFiles()



"""

