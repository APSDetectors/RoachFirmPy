"""

cd ROACH2/projcts/pyfiles

Listen to what comes from riach- the gb card on the linux is 168.1.102. roach sends there
nc -ul 192.168.1.102 50000 | hexdump -v




execfile('katcpNc.py')

execfile('fftAnalyzerR2.py')

execfile('katcpNc.py')


fa = fftAnalyzerR2(roach)

fa = fftAnalyzerR2(roach,is_datacap_=False)


roach=katcpNc()
roach.startNc()

fa.capture.shut()
fa.an.shut()

roach.closeFiles()

fa.chanzer.b_rst = 1
fa.chanzer.progRoach()
fa.chanzer.b_rst = 0
fa.chanzer.progRoach()


##########################################################3

fa.sram.is_mod_freq=True
fa.sram.mod_periods=4.0
fa.sram.setLutSize(65536)

fa.chanzer.setFluxRampDemod(1,1,100,3.0)

fa.setCarrier(5100e6)

freqs = arange(1e6,1e6+128e6,1e6).tolist()
freqs = freqs + arange(271e6,271e6 + 128e6,1e6).tolist()
print len(freqs)
fa.sourceCapture(freqs,2000)
time.sleep(.1)
fa.stopCapture()
print len(freqs)


fa.sourceCapture([10e6],20000)
time.sleep(1)
fa.stopCapture()

iq=fa.getIQ()



dd=fa.dataread

dd.plotEvents2D(fignum=5, chans=-1,data=iq,stevent = 0, nevents=1000)




dftscope = roachScope(roach,'FRD1_DFT_octoscope')

dftscope.trigScope(0,0)
dftscope.readScopeOcto()

#clf()

dftscope.trigScope(-1,0)
dftscope.readScopeOcto()
clf()
dftscope.interleave([7])
plot(10*bitwise_and( dftscope.plotdata, 65280)/256)

#dvld
plot(1000*bitwise_and( dftscope.plotdata, 8)/8)
dftscope.interleave([1])
plot(array(dftscope.plotdata)+12000)
dftscope.interleave([2])
plot(array(dftscope.plotdata)/10)
dftscope.interleave([3])
plot(array(dftscope.plotdata)/10)

dftscope.interleave([4])
plot(array(dftscope.plotdata)/10)

dftscope.interleave([5])
plot(array(dftscope.plotdata)/10)

###
dftscope.trigScope(0,0)
dftscope.readScopeOcto()


clf()
dftscope.interleave([4])
#plot(dftscope.plotdata[:180])

pf = dd.convToFloat(dftscope.plotdata,[1,16,13])
plot(pf[:180])

dftscope.interleave([5])
pf = dd.convToFloat(dftscope.plotdata,[1,16,13])
plot(pf[:180])


#pi = uint16(dftscope.plotdata)
#plot(pi[:180])

###

dftscope.interleave([6])
plot(dftscope.plotdata[:180])

dftscope.trigScope(-1,0)
dftscope.readScopeOcto()
clf()
dftscope.interleave([7])
plot(bitwise_and( dftscope.plotdata, 65280)/256)
#sum en
plot(100*bitwise_and( dftscope.plotdata, 128)/128)
#dvld
plot(100*bitwise_and( dftscope.plotdata, 8)/8)
#rst cnt
plot(100*bitwise_and( dftscope.plotdata, 16)/16)


#dftscope.plotScope(signbit = 15,replot=True,pllen=128)

fa.capture.shut()
fa.capture=None

nc -ul 192.168.1.102 50000 | hexdump -v

clf()

plot(iq[192]['stream_phase'])

plot(iq[192]['stream_mag'])


plot(iq[192]['flux_ramp_phase'])


dd=fa.dataread

dd.plotEvents2D(fignum=5, chans=-1,data=iq,stevent = 0, nevents=1000)

##################################



dbscope = roachScope(roach, 'roachscope')

dbscope.trigScope(trigin=-1, inpt=0)

clf()
dbscope.plotScope(pllen = 2048,
        is_usebits = False, 
        bits = '15:11;10:10;9:9;8:8',
        isprint = False,
        isprintsh=False,
        shskip = 1,
        shoffset=0,
        signbit=-1,        
        replot=False,
        isfit_=True)
       
clf();plot(dbscope.shorts)       
        

roach.write_int('sw_timestamp',1)

roach.write_int('roachscope_snapshot_ctrl',12)

fa = fftAnalyzerR2(
    roach,
    is_powerup=True,
    is_loadFW=True, 
    is_calqdr=True,
    is_anritsu_lo_ = True,
    is_anritsu_clk_=True, 
    is_datacap_=True)
    


fa.ifSetup(rfloop=1, 
        bbloop=0,
        u28=5,
        u6=5,
        u7=5,
        lo_src=0,
        lo_internal=0,
        lofreq = 3500e6,
        lo_on = 1,
        clk_int=-1)


fa.an.setPower(-5)
fa.an.setOnOff(1)
fa.setCarrier(4e9)

fa.adcscopetrig();fa.adcplot(IQ="I")


fa.sweep()

fa.an.setOnOff(0)

fa.sweep(span_Hz = 4000e6, center_Hz =4500e6, pts=5000)

fa.sweep(span_Hz=300e6, center_Hz=5700e6, pts=256)

clf()

plot(fa.freqs_sweep,  fa.iqdata[1])
plot(fa.freqs_sweep,  fa.iqdata[0])


iq=fa.dataread.RectToPolar(fa.iqdata)
clf()
subplot(2,1,1)
plot(fa.freqs_sweep,  iq[0])
subplot(2,1,2)
plot(fa.freqs_sweep,  iq[1])

#nc -ul 192.168.1.102 50000 | tee myfile.bin | hexdump -v


fa.chanzer.flushFifos()
fa.chanzer.clearFull()

fa.capture.dumpPacketFifo()

fa.capture.clearEvents()

roach.write_int('sw_timestamp',12345)

fa.rfft.numFFTs(100)
fa.rfft.trigFFT()

#roach.readAllReg()
roach.read_int('gbdatalen')
roach.read_int('gbeofcount')
roach.read_int('outfifowrB')
roach.read_int('outfifordB')
roach.read_int('evt_len1')
roach.read_int('evtfifordB')
roach.read_int('evtfifowrB')
roach.read_int('numdoneevts1')
roach.read_int('fifowrD')




fa.sourceCapture([10e6],20000)
time.sleep(1)
fa.stopCapture()

fa.getIQ()


clf()
plot(fa.iqdata_raw[192]['stream_mag'])

clf()
for k in fa.iqdata_raw.keys():
    print k
    plot(fa.iqdata_raw[k]['stream_mag'])

fa.iqdata_raw[192]['timestamp']

numpy.bitwise_and(numpy.uint32(fa.iqdata_raw[192]['timestamp']),3)[:2000]


fa.an.freq_time_delay=0.02


figure(1)
clf()




fa.capture.shut()

fa.capture=dataCapture()

fa.sourceCapture([10.1232e6],20000)

fa.an.setPower(-5)
fa.an.setOnOff(1)
fa.setCarrier(5.7474e9 + 10e6)

roach.write_int('sw_timestamp',3)

fa.sourceCapture([10e6],20000)
time.sleep(1)
fa.stopCapture()

iq=fa.getIQ()

clf()
plot(iq[192]['stream_mag'][:20000])

numpy.bitwise_and(numpy.uint32(fa.iqdata_raw[192]['timestamp']),7)[:2000]



sync_rate = fa.chanzer.getSyncRate()
sync_rate
fa.chanzer.setIsSync(1)
seglen = floor(1e6 / sync_rate) - 4
fa.chanzer.setReadFifoSize(seglen)
seglen
fa.chanzer.setReadFifoSize(55)


fa.sourceCapture([10e6],20000,is_zero_phaseinc=True)
time.sleep(.1)
fa.stopCapture()



fa.rfft.trigFFT()

fa.fftscopetrig()

fa.fftplot('Re')

fa.sram.sample_order=[2,3,0,1][::-1]
fa.is_digital_loopback=1


fa.sram.sample_order=[0,1,2,3]
fa.is_digital_loopback=0


iq=fa.getIQ()

clf()
k=192
plot(fa.iqdata_raw[k]['stream_mag'][:4000])

plot(fa.iqdata_raw[192]['stream_mag'])

fa.rfft.trigFFT()

fa.fftscopetrig()

fa.fftplot('M')

fa.fftplot('Re')

fa.adcscopetrig()

fa.adcplot(IQ="IQF")


fa.adcplot(IQ="I")

fa.adcplot(IQ="IQF")

fa.adcdelays=[0,1,2,3]
      


fa.sourceCapture([10e6],30000,numffts = 2000,whichbins='Freqs',is_trig = True)

fa.sourceCapture([10e6],30000,numffts = 1,whichbins='Freqs',is_trig = False)

for kk in range(2000):fa.rfft.trigFFT()

fa.rfft.trigFFT()

fa.if_board.rf.baseband_loop=0
fa.if_board.rf.rf_loopback=1
fa.if_board.at.atten_U6 =5
fa.if_board.at.atten_U6 =5

fa.if_board.progAtten(fa.if_board.at)
fa.if_board.progRFSwitches(fa.if_board.rf)


fa.if_board.at.atten_U6 = fa.if_board.at.atten_U6 + 3
fa.if_board.progAtten(fa.if_board.at)
fa.if_board.progRFSwitches(fa.if_board.rf)
time.sleep(0.1)
fa.rfft.trigFFT()

fa.stopCapture()

################
###############


fc=[5693.11e6,5704.13e6,5711.14e6,5722.29e6,5736e6,5736.76e6,5747.04e6,5752.14e6]
(lo,fbase) = fa.calcCarrierBBFreqs(fc)
fa.setCarrier(lo)
fa.an.setPower(-3)
fa.an.setOnOff(1)

fa.sourceCapture(fbase,10000)
time.sleep(.5)
fa.stopCapture()
time.sleep(0.5)
iq=fa.getIQ()

clf()
semilogy(abs(scipy.signal.welch(iq[192]['stream_mag'])[1]))
#clf();plot(iq[192]['stream_mag']);plot(iq[193]['stream_mag'])

clf()
for kk in range(192,200):plot(iq[kk]['stream_mag'][:10000])

figure(2)
clf()
for kk in range(192,200):semilogy(abs(scipy.signal.welch(iq[kk]['stream_mag'])[1]))

   

trnum=3


hdf.write(iq,'iq5')

trnum = trnum + 1

hdf.write(fa,'fa3')

############
###########


fa.adcscopetrig()

fa.adcplot('I')




a.rfft.trigFFT()


iq=fa.getIQ()

fa.iqdata_raw.keys()

figure(1)
clf()
for k in fa.iqdata_raw.keys():
    print k
    plot(fa.iqdata_raw[k]['stream_phase'])



figure(1)
clf()
for k in fa.iqdata_raw.keys():
    print k
    plot(fa.iqdata_raw[k]['stream_mag'][:5000])



clf()
k=128
plot(fa.iqdata_raw[k]['stream_phase'][:2000])



clf();plot( fa.iqdata_raw[128]['timestamp'])





fa.adcscopetrig()

fa.adcplot('Q')
clf();plot(fa.adcscope.shorts)




execfile('roachScope.py')
ss=roachScope(roach, 'octoscope1')

fa.rfft.stopFFTs()

fa.rfft.trigFFT()

ss.trigScope(0,0)
ss.readScopeOcto()

IC=[0,1,2,3]
QC=[4,5,6,7]
Is=128
ss.interleave(IC,Is)
ss.plotScope(replot=True)
figure(1);clf()
plot(ss.shorts)
I = numpy.array(ss.shorts)
ss.interleave(QC,Is)
ss.plotScope(replot=True)
Q = numpy.array(ss.shorts)
M = numpy.sqrt( I*I + Q*Q)
clf()
plot(M)













#you have to have attens at var,6,6 (6,7,28) for them to work.
#the mixer does wierd things. this cal should be run from time to time.
# it should make a decay exp plot. test with all attens.
#if too muich signal the lesser attens look like mroe attens, and look like the
#atten does not work. 0db atten has less signal than 10db atten. wierd.
#this is caused by mixer prob being overranged, so the signals get messed up
#this mat be overrante of the ADC? who knows... 

fa.attenLoopTest(which = 6,u6=0,u7=3,u28=3,attens = numpy.arange(0.0,32.0,0.5))



Mapping of fft bins to channels

Bins are numbered from 0 to 511, in increasing freq. bin 512 is the sample freq. bin 0 is DC
The bins come out interleaved in 4 ports. Ports are a,b,c,d
Port a has bins 0,4,8, ...
Port b has bins 1,5,9....
port c has bins 2,6,10...
port d has bins 3,7,11...

We number the bins coming from each port with bin4 variable.
bin4 counst from 0 to 127. 
Example, Bin = 5, or 4,6,7, then bin4 is 1 for all those.

When we write each bin to a fifo we have 4 multififlos, one for each port.
Call them fifo a,b,c,d for ports a,b,c,d.
We assing an address, or which fifo in the multififo, (a stack of fifos, and address tells which fifo in the
stack.The write address is numbered from 0 to 63. With 4 of these multififos we get 256 possible address
or nuymber of channels. There are 4 write wires, to set which multififo the address applies to. 

-------------
|   FFT     |                       _________        ___________________            ___________________
|          A|-------MULTIFIFO_A---->|       |       |                   |           |                   |
|           |                       | MUX   |------>|   phase corct,fmt0|--------- >|                   |
|          B|-------MULTIFIFO_B---->|_______|       |___________________|           |                   |
|           |                       _________       _____________________           |   GB Ethernet     |
|          C|-------MULTIFIFO_C---->|       |       |                   |           |                   |
|           |                       | MUX   |------>|   phase corct,fmt1|--------- >|                   |
|          D|-------MULTIFIFO_D---->|_______|       |___________________|           |___________________|
-------------

                    chan 0-63,                       chan0-127, each leg                   in Linux, 
                    4 write wires                                                           numbered 0-255 

The coef selector circuit tells which FFT bins to store. There is a RAM in the coef selector ckt
to tell the write address to multififo, and which multififio to write coef to.

fa.rfft.bin_to_chan
{502: 128}

fa.rfft.showBinFlags()
bin4 125  addr3 0  addr2 0  addr1 0  addr0 0   wr3 0  wr2 4  wr1 0  wr0 0 

bifa.rfft.chan_to_bin4
{128: [125]}

chan is the output channel from 0 to 255.
Multififos A,B readout channels are 0 to 127
Multifisos C,D are channels 128 to 255. 

Write addresses are 0 to 63 for each multififo, whjth a write flag 


bin4 = int(bin/4)
wrN = bin % 4



Given the above bin flags:
bin4 125  addr3 0  addr2 0  addr1 0  addr0 0   wr3 0  wr2 4  wr1 0  wr0 0 

leg0 for wr0 or wr1 high
leg1 for wr2,3 high

leg0 address = addr0 if wr0=high
leg0 address   = 63+addr1 if wr1 = high. 
If both wr0,wr1 high, then we get two leg1 addresses, and are red out seperateklty. That is
they fifos are written at same time, but read out at differnt times.

leg1 address = addr0if wr2=high
leg1 address   = 63+addr3 if wr3 = high. 

linux address = leg0 address 
OR
linux address = leg1 address + 128














"""

def dbgtestfa2():
    
    for k in range(10*120):
        fa.if_board.progAtten(fa.if_board.at)
        time.sleep(0.1)
        
        
 




import sys, os, random, math, array, fractions


import time, struct, numpy



try:
    ROACH_DIR =  os.environ['ROACH']
except:
    print 'Please set env var ROACH to your roach install dir'
    print 'Using /localc/roach'
    ROACH_DIR='/localc/roach'


execfile('katcpNc.py')
execfile('roachScope.py')
execfile('sramLut.py')
execfile('qdr.py')
execfile('if_board.py')
execfile('mkiddac.py')
execfile('Channelizer.py')
execfile('dataExtract.py')
execfile('hdfSerdes.py')
execfile('roachFFT.py')
execfile('dataCapture.py')
execfile('anritsu.py')
execfile('phaseCorrect.py')
execfile('hdfSerdes.py')

execfile('fluxRampGen.py')

#from katcpNc import *
#from roachScope import *
#from sramLut import *
#from qdr import *
#from if_board import *
#from mkiddac import *
#from Channelizer import *
#from dataExtract import *
#from hdfSerdes import *
#from roachFFT import *
#from dataCapture import *
#from anritsu import *


def saveAnalyzer(filename):

    hdf=hdfSerdes()
    hdf.open(filename,'w')
    hdf.write(fa,'fftAnalyzerR2')
    hdf.close()
        
def loadAnalyzer(filename):
    global fa

    hdf=hdfSerdes()
    hdf.open(filename,'r')
    fa = hdf.read()
    hdf.close()
    


class fluxRampSpecs:

    def __init__(self):
        self.chan_cir_xy = { 192:(0.0,0.0) }
        self.rf_delay = 30e-9
        
        self.flux_bin = 3.0
        self.is_flux_demod = False
    
          
    
    

class fftAnalyzerR2:

    
    def __init__(self,
        roach_=None,
        is_powerup=True,
        is_loadFW=True, 
        is_calqdr=True,
        is_anritsu_lo_ = True,
        is_anritsu_clk_=True, 
        is_datacap_=True):
    
        self.flux_demod_specs = fluxRampSpecs()
     
        self.roach2=roach_
        
        self.tes_bias=0.0
        self.tes_bias_on = 0
        
     
        if self.roach2 != None:
        
            self.powerupFW = ROACH_DIR+'/projcts/bestBitFiles/if_board_setup_2015_Aug_20_1511.bof'

            #this one used for most of data so far-- mar 2016
         
            #this one has new sync ckt, new data format from the gb enet, added 0x5555 and data len header
            #self.mainFW = '/home/oxygen31/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2016_May_23_1513.bof'
            #this is workhorse FW
            #self.mainFW = '/home/oxygen31/TMADDEN/ROACH2/projcts/bestBitFiles/qdrdac_2016_Jul_11_1331.bof'

            #fw for testing flux ramp demod on roach
            self.mainFW = ROACH_DIR+'/projcts/bestBitFiles/qdrdac_2016_Sep_14_0927.bof'




            self.temppath = ROACH_DIR+'/temp/'

            self.is_datacap= is_datacap_
            self.is_anritsu_lo = is_anritsu_lo_

            self.is_anritsu_clk = is_anritsu_clk_

            if is_powerup:
                self.powerUp()

            if is_loadFW:
                self.loadFW()

            self.initObjs()
            self.ifSetup()

            if is_calqdr:
                self.calQDR()

            self.setupEthernet()



            #!!if self.is_anritsu_lo:
            self.an = anritsu(self.is_anritsu_lo)
            self.an.setPower(-5)
            self.an.setOnOff(1)
            self.setCarrier(5757e6)


            self.is_digital_loopback=0




        
    def initObjs(self):
    
        #self.adcscope = roachScope(self.roach2, 'octoscope')

        #self.fftscope = roachScope(self.roach2, 'octoscope1')
        self.sram = sramLut(self.roach2,'SRAM_LUT')
        self.qdr0=Qdr(self.roach2,'qdr0')
        self.qdr1=Qdr(self.roach2,'qdr1')
        self.if_board=ifBoard(self.roach2,'if_board')
        self.dac = MKIDDac(self.roach2, 'MKID_DAC')
        self.rfft = roachFFT(self.roach2, 'fftcoefselector')
        self.rfft.setLutSource(self.sram)
    
        self.chanzer = Channelizer(self.roach2)

        #reset all fsm's on the roach
        self.chanzer.b_rst=1
        self.chanzer.progRoach()
       
        self.chanzer.b_rst=0
        self.chanzer.progRoach()
        
        self.phaser1 = phaseCorrect(self.sram, self.rfft,'PhaseCorrect1',0)
        self.phaser2 = phaseCorrect(self.sram, self.rfft,'PhaseCorrect2',1)
        
        if self.is_datacap:
            self.capture=dataCapture()
            #!!self.capture.capture(True)
        else:
            self.capture = None
        
        self.dataread=dataExtract(self.sram,self.rfft)
    
    
        self.adcscope = roachScope(roach, 'octoscope')
        self.fftscope = roachScope(roach, 'octoscope1')

        
        self.rampgen = fluxRampGenerator(self.roach2,self.chanzer)
        
        #ADC sample order
        #!!self.adcdelays = [0,1,2,3]
    
    
        
    def setCarrier(self,fc_hz,is_on=1):
    
        self.carrierfreq = fc_hz
        
        #!!if self.is_anritsu_lo:
        self.an.setFreq(self.carrierfreq * 1e-9)
         
   
  
        
        
    def powerUp(self):
        
        self.roach2.sendBof(self.powerupFW)
        time.sleep(1)
        self.if_board=ifBoard(self.roach2,'if_board')
        
        if not self.is_anritsu_clk:
            self.if_board.rf.clk_internal=1
            self.if_board.s.rfouten=1
        else:
            self.if_board.rf.clk_internal=0
            self.if_board.s.rfouten=0
        
        
        self.if_board.progIfBoard()


    def loadFW(self):
    
        self.roach2.sendBof(self.mainFW)
        time.sleep(1)
  

        
    def ifSetup(self,
        rfloop=0, 
        bbloop=0,
        u28=0,
        u6=3,
        u7=3,
        lo_src=0,
        lo_internal=-1,
        lofreq = 3500e6,
        lo_on = 1,
        clk_int=-1):

        # Make sure IF is still programmed after new FW load
        #


        self.if_board.at.atten_U28=u28
        self.if_board.at.atten_U6=u6
        self.if_board.at.atten_U7=u7


        if clk_int==-1:
            if self.is_anritsu_clk:clk_int=0
            else: clk_int = 1
            
        self.if_board.rf.clk_internal=clk_int
        self.if_board.s.rfouten = clk_int
        
       
        

        self.if_board.rf.baseband_loop=bbloop
        self.if_board.rf.rf_loopback=rfloop

        self.if_board.LO.setFreq(lofreq)
        #self.if_board.LO.setFreq(4500e6)
        #self.if_board.LO.setFreq(2500e6)

        if lo_internal==-1:
            if self.is_anritsu_lo: 
                lo_internal=0
                lo_src = 1
            else:
                lo_internal=1
                lo_src = 0
            
            
        self.if_board.rf.lo_internal = lo_internal
        self.if_board.rf.lo_source = lo_src


        self.if_board.progIfBoard()



      
        

    def calQDR(self):

        print "Please WAIT- calibrating QDRs"
        #
        # calibrate the qdrs
        #

        self.qdr0.reset()
        self.qdr0.qdr_cal()
        self.qdr0.qdr_delay_clk_get()
        self.qdr0.qdr_cal_check()

        self.qdr1.reset()
        self.qdr1.qdr_cal()
        self.qdr1.qdr_delay_clk_get()
        self.qdr1.qdr_cal_check()


    def stopCapture(self):
        if self.capture != None:
            self.capture.capture(False)

        self.rfft.stopFFTs()

    #given rf freq list, calc carrier freq, bb frqs
    def calcCarrierBBFreqs(self,freqlist_rf_Hz):
    

        farray = numpy.array(freqlist_rf_Hz)
        fmax = numpy.max(farray)
        carrier = 10e6 + fmax
        freq_bb =numpy.sort( +10e6 + fmax- farray )
        freq_bb = freq_bb.tolist()

        return((carrier,freq_bb))    

    def sourceCapture(self,freqlist,amp,numffts = -1,whichbins='Freqs',is_trig = True,is_zero_phaseinc=False):
        
        self.stopCapture()
        
        self.rfft.stopFFTs()

        if self.capture != None:
            self.capture.clearEvents()
            self.capture.capture(True)


        #prog and start lut sines
        self.sram.setLutFreqs(freqlist,amp)
        #startdac
        self.dac.setReset()
        self.dac.setSync(1,1)

        self.roach2.write_int('MKID_ADC_settings',self.is_digital_loopback);
        
        #!!self.roach2.write_int('MKID_ADC_iqtobus_sampleorder',\
        #!!    (self.adcdelays[0]) + (self.adcdelays[1]<<2) + (self.adcdelays[2]<<4) + (self.adcdelays[3]<<6))
      
        if whichbins=='Freqs':
            self.rfft.fftBinsFreqs()
            
        else:
            #"High" "Low", "All"
            self.rfft.fftBinsAll(whichbins)
           
            
      
       
        if self.capture != None:
            self.capture.mapChannels(self.rfft)
            
            #real time flux ramp dempd on C++ code
            self.capture.setTimeDelay(self,self.flux_demod_specs.rf_delay)
            self.capture.setFluxRampBin(self.flux_demod_specs.flux_bin)
            self.capture.setCircleSpecs(self.flux_demod_specs.chan_cir_xy)
            self.capture.setIsFluxRampDemod(self.flux_demod_specs.is_flux_demod)
            
            
            

        
        self.chanzer.flushFifos()
            
        self.chanzer.clearFull()
        self.chanzer.rstFifos()

        self.chanzer.writeRaw(1)
        self.chanzer.setLastReadChan(127)
        self.chanzer.readFifos(1)
        self.chanzer.clearFull()
        
     
        if not is_zero_phaseinc:
            self.phaser1.reprogPhaseIncs() 
            self.phaser2.reprogPhaseIncs()
        else:
            self.phaser1.zeroPhaseIncs() 
            self.phaser2.zeroPhaseIncs()
       
     
        self.rfft.fftsynctime=128
        self.rfft.roach_fft_shift=31
      
      
      
      
        self.rfft.numFFTs(numffts)
        self.rfft.progRoach()
        if is_trig:
            self.rfft.trigFFT()

    def findSweepData(self,chan=192):
        #for k in range(64,300):
        #    if self.iqdata_raw[chan]['stream_mag'][k] >0.001:
        #        return(k)


        k=0
        return(0)



    #calc base band freq list, and LO freq given list of RF freqs
    def calcBBLOFromRFFreqs(self,rffreqs):
  
        frange = max(rffreqs) - min(rffreqs)
        if frange>230e6:
            print "cannot source this freq list- to wide BW"
            return

        LO=max(rffreqs)+10e6
        bbfreqs = LO - rffreqs

        bbfreqs = numpy.sort(bbfreqs)
        return( (LO, bbfreqs) )

    def sweep(self,span_Hz=100e6, center_Hz=3000e6, pts=2048):

        self.stopCapture()


        self.setTESBias(0,0)


        #turn off flux ramp demod
        self.chanzer.setFluxRampDemod(0,1,100,3.0)
        #make sure sync is off... we want all data, not wait for ramp gen sync
        self.rampgen.setIsSync(0)

        self.chanzer.flushFifos()
        self.chanzer.clearFull()
        self.chanzer.rstFifos()
            
        if (self.capture!=None):
            self.capture.dumpPacketFifo()
            self.capture.clearEvents()

        self.sweep_num_freqs=pts;
        #self.sweep_samples_per_freq=floor(65536/self.sweep_num_freqs)

        self.fbase = 10e6
        self.sourceCapture(
            [self.fbase],
            20000,
            numffts = 1,
            whichbins='Freqs',
            is_trig = False)



        self.start_carrier = center_Hz + self.fbase-span_Hz/2.0
        self.end_carrier = center_Hz + self.fbase+span_Hz/2.0
        self.inc_carrier = span_Hz/pts
        self.carrier_freqs = arange(
            self.start_carrier ,
            self.end_carrier,
            self.inc_carrier )

        

        self.an.setOnOff(0)
        
        
        self.roach2.write_int('sw_timestamp',1)
        
        #take off data... we have some fifo problem... some time delay for some rheason...
        #!!for k in range(256):        
        #!!    self.rfft.trigFFT()


        
        self.roach2.write_int('sw_timestamp',2)

        self.an.setOnOff(1)
        
        self.phaser1.zeroPhaseIncs()
        self.phaser2.zeroPhaseIncs()


        for cf in self.carrier_freqs:

            print 'trig fft cf=%f'%cf
            self.setCarrier(cf)

            self.rfft.trigFFT()


        #we have taken 200 points, becaise some FWs may not have fifl readout yet we take
        #rest of points to fill memory, to make sure we have fifos readout. this is not used 
        #data for cal.

        self.roach2.write_int('sw_timestamp',0)

        self.setCarrier(self.fbase + center_Hz)
        time.sleep(.1)
        #!!self.an.setOnOff(0)
          

        self.rfft.numFFTs(65536)
        self.rfft.progRoach()
        self.rfft.trigFFT()

        time.sleep(1)
        self.stopCapture()
        time.sleep(1)   
        
        
        #now mem is fill, we can readout...
        if self.capture!=None:
            self.getIQ();


            stindex = self.findSweepData()
            mags = self.iqdata_raw[192]['stream_mag'][stindex : (stindex+pts)]
            phase = self.iqdata_raw[192]['stream_phase'][stindex : (stindex+pts)]    
            #phase=self.removePhaseJumps(phase)

            self.iqdata = self.dataread.PolarToRect( [mags,phase] )
            self.freqs_sweep = self.carrier_freqs - self.fbase

        self.an.setOnOff(0) 
        self.stopCapture()
        time.sleep(1)   
        
    def getIQ(self):
        dsname = self.temppath + 'TEMP'
        timeout=10
        cnt=0
        self.iqdata_raw={}
        while 192 not in fa.iqdata_raw.keys():
       
       
              self.capture.saveEvents(dsname)
              #!! how to tell the stuff is saved...
              #we should get two commands from the c program. 
              self.capture.getCmd()
              self.capture.getCmd()
              time.sleep(2)
              self.iqdata_raw = self.dataread.readEvents(dsname)
              cnt = cnt+1
       
              #self.dataread
              os.system('rm -rf %s'%(dsname+'_A'))
              os.system('rm -rf %s'%(dsname+'_B'))
 
              if cnt==timeout:
                      print "ERROR cannot get data"
                      break
 
 
        return(self.iqdata_raw)
        


    def removePhaseJumps(self,phase_sig):
        print "removePhaseJumps"
        newphase = [0] * len(phase_sig)

        newphase[0] = phase_sig[0]

        for k in range(1,len(phase_sig)):
            newphase[k] = phase_sig[k]
            dphase = newphase[k] - newphase[k-1]
            while dphase>pi:
                newphase[k] = newphase[k]-2*pi
                dphase = newphase[k] - newphase[k-1]

            while dphase<(-pi):
                newphase[k] = newphase[k]+2*pi
                dphase = newphase[k] - newphase[k-1]

        return(newphase)    




    def setupEthernet(self):
    

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
        self.ip = (192<<24) + (168 << 16) + (1<<8) + 102

        self.roach2.write_int('txdestip',self.ip)
        self.port = 50000
        self.roach2.write_int('txdestport',self.port)
        self.roach2.setupEth('xmit0','192.168.1.11',100,'02:02:00:00:00:01')
        self.roach2.infoEth()







    def attenLoopTest(self,which = 6,u6=0,u7=0,u28=0,attens = numpy.arange(0.0,32.0,0.5)):
        self.if_board.rf.baseband_loop=0
        self.if_board.rf.rf_loopback=1
        self.if_board.at.atten_U6 =u6
        self.if_board.at.atten_U7 =u7
        self.if_board.at.atten_U28 =u28
        self.if_board.progAtten(self.if_board.at)
        self.if_board.progRFSwitches(self.if_board.rf)

        self.sourceCapture([10e6],30000,numffts = 2000,whichbins='Freqs',is_trig = False)



        self.rfft.trigFFT()


        for atten in attens:
            if which ==6:
                self.if_board.at.atten_U6 = atten

            if which ==7:
                self.if_board.at.atten_U7 = atten

            if which ==28:
                self.if_board.at.atten_U28 = atten

            self.if_board.progAtten(self.if_board.at)

            print '----------'
            print atten

            #time.sleep(0.5)
            self.rfft.trigFFT()

        self.rfft.trigFFT()

        self.stopCapture()
        time.sleep(1)

        iq=self.getIQ()

        self.iqdata_raw.keys()

        figure(1)

        for k in self.iqdata_raw.keys():
            print k
            plot(self.iqdata_raw[k]['stream_mag'])


    def fftscopetrig(self,trgx=0):
        self.fftscope.trigScope(trgx,0)
        self.fftscope.readScopeOcto() 
        


    def fftplot(self,V="Re"):
        self.fftscope.is_hold=False
    
        if V=='Re': 
  
            
            self.fftscope.interleave([0,1,2,3],intersize=128)
            clf()
            self.fftscope.plotScope(replot=True);
            figure(1);clf()
            plot(self.fftscope.shorts)

        if V=='Im':
            self.fftscope.concat([4,5,6,7])
            clf()
            self.fftscope.plotScope(replot=True);
            figure(1);clf()
            plot(self.fftscope.shorts)
        
        if V=='M':
                
            self.fftscope.concat([0,1,2,3])
            self.fftscope.plotScope(replot=True);
            Re = numpy.array(self.fftscope.shorts)
            self.fftscope.concat([4,5,6,7])
            self.fftscope.plotScope(replot=True);
            Im = numpy.array(self.fftscope.shorts)
            M = numpy.sqrt(Im*Im + Re*Re)
            figure(1);clf()
            plot(M)
        
    

    def adcscopetrig(self):
    
        self.adcscope.trigScope(-1,0)
        self.adcscope.readScopeOcto()  
    
    def adcplot(self,IQ="I"):
        self.adcscope.is_hold=False
        if IQ=='Q': 
  
            
            self.adcscope.interleave([4,5,6,7])
            self.adcscope.plotScope(signbit = 11,replot=True);

            
        if IQ=='I':
            self.adcscope.interleave([0,1,2,3])
            self.adcscope.plotScope(signbit = 11,replot=True);
        

        if IQ=='IQF':
        
            self.adcscope.is_hold=False
            self.adcscope.interleave([4,5,6,7])
            self.adcscope.plotScope(signbit = 11,replot=True,pllen=1024);
            Q = self.adcscope.shorts
            self.adcscope.interleave([0,1,2,3])
            self.adcscope.plotScope(signbit = 11,replot=True,pllen=1024);
            I = self.adcscope.shorts
            Q = numpy.array(Q[:512])*numpy.hamming(512)
            I = numpy.array(I[:512])*numpy.hamming(512)
            Q = complex(0,1)*Q
            
            FF=fft.fft(I+Q);
            P = 20*log10( abs(FF) + 1)
            clf();
            #plot(P - max(P))
            plot(abs(FF))
    

    def setTESBias(self,is_on,vbias):
    
        if is_on:
            sim.setOutOn(0)
            vsweep = arange(10.0,vbias-0.02,-0.02)
            time.sleep(1.0)
            sim.setVolts(10.0)
            sim.setOutOn(1)

            for v in vsweep:
                sim.setVolts(v)
                print v
                time.sleep(0.01)

            self.tes_bias = vbias       
            self.tes_bias_on = 1
        else:
            self.tes_bias = vbias       
            self.tes_bias_on = 0
            sim.setOutOn(0)
            
            
            
            
            
            



            