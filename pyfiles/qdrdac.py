

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


#disconn from roach
roach2.closeFiles()
"""


#
# Send IF config FW. Needed for initial power up to get clocks working on IF board. needed for using internal 512MHz  Osc.
#


roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/if_board_setup_2015_Aug_13_1230.bof')



if_board=ifBoard(roach2,'if_board')

if_board.rf.clk_internal=1
if_board.s.rfouten=1
if_board.progIfBoard()




#no ADC
#roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_13_1051.bof')

#has dac with fb, and octo roach scope- no fb buffer
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_14_1650.bof')

#has dac with fb, and octo roach scope- fb buffer
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_17_1010.bof')


#has dac with fb, and octo roach scope- no fb buffer, 2x clk at 270
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Aug_17_1102.bof')



#call to read all reg vales on roach print on screen, return as list of tupels
#roach2.readAllReg()


#
# Define stuff
#

roachscope = roachScope(roach2, 'roachscope')
roachscope1 = roachScope(roach2, 'roachscope1')

adcscope = roachScope(roach2, 'octoscope')


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
fsweep.startSweep(1e6,1e6,50e6)




"""

fsweep.setWaitTime(100)
fsweep.startSweep(5e6,1e5,10e6)

fsweep.startSweep(5e6,0.0,5e6)

fsweep.startSweep(1e6,0.0,1e6)

"""

#
# SRAM Generator
#



sram.setLutFreqs(arange(10e6,250e6,1e6),80)

"""

sram.setLutFreqs([20e6, 30e6], 15000)

sram.setLutFreqs([10e6], 32000)


sram.setLutFreqs([1e6], 32000)

sram.sample_order=[0,1,2,3]


"""


#
# DAC
#




dac.setReset()

dac.setSync(1,1)





#
#Select output signal
# 0 = LUT, 1=sweep sine, 2 = modulation of sweep and lut


#for sweep
roach2.write_int('settings_reg',0)

#for  lut
roach2.write_int('settings_reg',1)




#
#ADc scope=NON OCTOSCOPE
#
delays = [3,2,0,1]
roach2.write_int('MKID_ADC_iqtobus_sampleorder',(delays[0]) + (delays[1]<<2) + (delays[2]<<4) + (delays[3]<<6))

ch=0
roachscope1.trigScope(-1,ch);roachscope1.plotScope(signbit = 11);


ch=4
roachscope1.trigScope(-1,ch);roachscope1.plotSpectrum(signbit=11,log='Yes');


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
adcscope.plotScope(signbit = 11,replot=True,pllen=512);





adcscope.interleave([0,1,2,3])
adcscope.plotScope(signbit = 11,replot=True,pllen=512);





adcscope.plotSpectrum(signbit=11,log='Yes',replot=True,pllen=8192);


#
# use scope
#



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

