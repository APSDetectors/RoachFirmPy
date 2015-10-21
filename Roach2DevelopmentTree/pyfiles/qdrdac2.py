

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

execfile('Channelizer.py')

execfile('dataExtract.py')

#
#
# FW VERSION SVN 2596
#




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



#has all of above, but add multififo(2),fsm, and out single event fifo
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Oct_12_1715.bof')


#has all of above, but add multififo(2),fsm, and out single event fifo, add out big fifo, 10gb enet, enet fsm
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Oct_13_1409.bof')



#has all of above, but add multififo(4),2fsm, and out single event fifo, add out big fifo, 10gb enet, enet fsm
#has fifo full couhnters
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2015_Oct_21_0952.bof')



#call to read all reg vales on roach print on screen, return as list of tupels
#roach2.readAllReg()


#
# Define stuff
#

#roachscope = roachScope(roach2, 'roachscope')
#roachscope1 = roachScope(roach2, 'roachscope1')

adcscope = roachScope(roach2, 'octoscope')

fftscope = roachScope(roach2, 'octoscope1')

sram = sramLut(roach2,'SRAM_LUT')

qdr0=Qdr(roach2,'qdr0')

qdr1=Qdr(roach2,'qdr1')

if_board=ifBoard(roach2,'if_board')

dac = MKIDDac(roach2, 'MKID_DAC')





#
# Make sure IF is still programmed after new FW load
#


if_board.at.atten_U28=0
if_board.at.atten_U6=0
if_board.at.atten_U7=0



if_board.rf.clk_internal=1
if_board.s.rfouten=1

if_board.rf.baseband_loop=1
if_board.rf.rf_loopback=0

if_board.LO.setFreq(3500e6)
#if_board.LO.setFreq(4500e6)
#if_board.LO.setFreq(2500e6)

if_board.rf.lo_internal = 1
if_board.rf.lo_source = 0


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
# SRAM Generator
#

sram.setLutFreqs(arange(10e6,100e6,10e6),5000)


sram.Q_amp_factor=-1.0

sram.setLutFreqs(arange(10e6,250e6,10e6),0)

"""

sram.setLutFreqs([20e6, 30e6], 1500)

sram.setLutFreqs([10e6], 10000)

sram.setLutFreqs([10e6], 1000)

sram.setLutFreqs([1e6], 32000)

sram.sample_order=[0,1,2,3]

sram.setLutFreqs([100e6], 32000)


sram.setLutFreqs(arange(10e6,100e6,10e6),2000)

"""


#
# DAC
#




dac.setReset()

dac.setSync(1,1)





###################################################################################
# ADC 
#
delays = [0,1,2,3]
roach2.write_int('MKID_ADC_iqtobus_sampleorder',(delays[0]) + (delays[1]<<2) + (delays[2]<<4) + (delays[3]<<6))



###################################################################################
# Octoscope
#

execfile('roachScope.py')

adcscope = roachScope(roach2, 'octoscope')



def scoper():
    ch=0
    adcscope.trigScope(-1,ch)
    adcscope.readScopeOcto()
    adcscope.is_hold=False
    adcscope.interleave([4,5,6,7])
    adcscope.plotScope(signbit = 11,replot=True,pllen=1024);
    Q = adcscope.shorts
    adcscope.interleave([0,1,2,3])
    adcscope.plotScope(signbit = 11,replot=True,pllen=1024);
    I = adcscope.shorts
    Q = numpy.array(Q)
    I = numpy.array(I)
    Q = complex(0,1)*Q
    FF=fft.fft(I[:512]+Q[:512]);
    P = 20*log10( abs(FF) + 1)
    clf();
    plot(P - max(P))
    return(FF)

#clf();semilogy(abs(FF))


scoper()


################################################################
#pos sideband
sram.Q_phase_offs=0.02 * -18.5
sram.Q_amp_factor = -1.0
sram.setLutFreqs(arange(10e6,200e6,10e6), 3000)



####################################################################
#neg sideband

#LO at 3.5G
#sram.Q_phase_offs=0.02 * 18.5
#LO at 4.5G
#sram.Q_phase_offs=0.02 * 10


sram.Q_phase_offs=(pi/180) *0
sram.Q_amp_factor = -1.0
sram.Q_time_delay = 0
sram.setLutFreqs(arange(10e6,200e6,10e6), 2000)

sram.Q_phase_offs=(pi/180) *18
sram.setLutFreqs(arange(10e6,200e6,10e6), 2000)


a=scoper()


#####################################
# cal the 1st tone
#


sram.setLutFreqs([200e6], 20000)


freq =  sram.frequency_list[0]
pbin = 512.0*freq / sram.dac_clk
nbin = 512 - pbin

nph = angle(FF[nbin])
namp = abs(FF[nbin])

pph = angle(FF[pbin])
pamp = abs(FF[pbin])


#make a sine and cos to add to the wavetable to cancle pbin.
cal_amp = sram.amplist[0] * pamp / namp
cal_ph = pi + (pph - nph) - sram.lut_phase_list[0]


sram.lut_i=sram.lut_i + sram.singleFreqLUT(freq, 'I', sram.dac_clk,sram.lut_length , cal_ph, cal_amp)
sram.lut_q=sram.lut_q + sram.singleFreqLUT(freq, 'Q', sram.dac_clk,sram.lut_length , cal_ph, cal_amp)
sram.lut_binaryIQ=sram.convertToBinary128(sram.lut_i,sram.lut_q)
sram.writeSram(sram.lut_binaryIQ)
sram.streamSram()
        
########################################################################3
#
# FFT stuff
#


execfile('roachFFT.py')


rfft = roachFFT(roach2, 'fftcoefselector')
rfft.setLutSource(sram)



rfft.fftBinsFreqs()


#rfft.fftBinsAll(which='High')



rfft.fftsynctime=128
rfft.progRoach()
rfft.numFFTs(-1)
rfft.trigFFT()


rfft.stopFFTs()

##########################################################################3
#
# Channelizer
#
#


execfile('Channelizer.py')


chanzer = Channelizer(roach2)

chanzer.flushFifos()

chanzer.writeRaw(1)



chanzer.setLastReadChan(127)



chanzer.readFifos(1)



chanzer.checkFull()

chanzer.clearFull()



##########################################################################3
#
#channelizer octoscope



execfile('roachScope.py')

fscope = roachScope(roach2, 'octoscope1')

fscope.clrscope()

fscope.is_hold = False


fscope.trigScope(0,0)

fscope.readScopeOcto()

#chan mags
fscope.interleave([0]);
fscope.plotScope();

#chan phase
fscope.interleave([1]);
fscope.plotScope();


fscope.trigScope(0,0);fscope.readScopeOcto()

#curchan read
fscope.interleave([2]);
fscope.plotScope();


#bits- on FSM fifo
#from 12:0
#from TOP OF LIST is BOTTOM of scope
#storemean
#calcmean
#savepulsestate
#deleteevent
#saveevent
#datapath en
#clearpulse
#fiford1
#fiford0
#muxsela
#fifoempty]
#datavalud
#halffull

fscope.trigScope(0,0)
fscope.readScopeOcto()
fscope.clrscope()


fscope.interleave([3]);
fscope.plotScope(
	bits ='12:12;11:11;10:10;9:9;8:8;7:7;6:6;5:5;4:4;3:3;2:2;1:1;0:0',
	is_usebits = True);



fscope.interleave([3]);
fscope.plotScope();

fscope.is_hold = False


#state
fscope.interleave([4]);
fscope.plotScope(isfit_=False);

fscope.interleave([4]);
fscope.plotScope();

# bits
# 0 save event
# delete event
# ev fifo rd
# out fifo wr
# almost empty a
# almost empty b
# fifo rd b
#fifo rd a
# fsm rst
# ethernet rst
# gb- led up
# led tx
# tx afull
# tx overflow
#tx vld
#tx eof


fscope.trigScope(0,0)
fscope.readScopeOcto()
fscope.clrscope()


fscope.interleave([5]);
fscope.plotScope(
	bits ='15:15;14:14;13:13;12:12;11:11;10:10;9:9;8:8;7:7;6:6;5:5;4:4;3:3;2:2;1:1;0:0',
	is_usebits = True);


#out fifo out data mag
fscope.interleave([6]);
fscope.plotScope();


#out fifo out data phase
fscope.interleave([7]);
fscope.plotScope();


clf()

fscope.is_hold=True







###############################################
# GB Ethernet stuff
#
#
# use port marked 2 on back of linux box on 10gb card. it is eth2.
# sudo ifconfig eth2 192.168.1.102
#
# on roach:
#
#
#  ----------------------------------
#  |                                |
#  |                    ----------  |
#  |                    | port 0 |  |
#  |            slot1   |      1 |  |
#  |                    |      2 |  |
#  |                    |      3 |  |
#  |                    ---------   |
#  |                                |
#  |                    --------    |
#  |                    | port0 |   |
#  |                    |     1 |   |
#  |            slot0   |     2 |   |
#  |                    |     3 |   |
#  |                    ---------   |
#  |                                |
#  |                                |
#  ----------------------------------
#
#   Above is roach with mezzinine cards.
#   We use slot1, port 0 for our 10gb ethernet
#   roach will aitomatically ping and arp req
#   the linux box when we start ethernet
#   
# to dump data
# nc -ul 192.168.1.102 50000 | hexdump -v


ip = (192<<24) + (168 << 16) + (1<<8) + 102

roach2.write_int('txdestip',ip)
port = 50000
roach2.write_int('txdestport',port)

    
roach2.setupEth('xmit0','192.168.1.11',100,'02:02:00:00:00:01')


	
roach2.infoEth()


roach2.stopEth('xmit0')







