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



#########3


#get from gui sweep file.


#now plot

ff = '/home/beams0/TMADDEN/ROACH2/datafiles/sep23_2016/reslist.h5'
mkidLoadData(ff)
rffreqs = mkidGetFreqs()

fa.sram.is_mod_freq=True

rsln = fa.sram.getResolution()


fa.sourceCapture(arange(10e6,20e6,1e6),3200)
time.sleep(1)
fa.stopCapture()


fa.setCarrier(10e6+5093e6)
fa.sourceCapture([10e6],32000)
time.sleep(1)
fa.stopCapture()


aa=fa.getIQ()
figure(1)
clf()
subplot(2,1,1)
plot(aa[192]['stream_mag'][1:1000])
subplot(2,1,2)
plot(aa[192]['stream_phase'][1:1000])

fa.adcscope = roachScope(roach, 'octoscope')

fa.adcscopetrig()
fa.adcplot()

fa.adcplot(IQ='IQF')
yscale('log')


hdf.open(fname,'w')
       
pldata = fa.getUsefulData()
fname = '/home/beams0/TMADDEN/ROACH2/datafiles/Feb22_2017/basebandnoise.h5'

hdf.open(fname,'a')   
     
pldata = fa.getUsefulData()
hdf.write(pldata,'rfdata300')

hdf.close()
      



fa.chanzer.setFluxRampDemod(
    is_demod=1,
    is_incl_raw_trans=2, 
    evt_len=100,
    num_cycles=2.0)


fa.chanzer.setFluxRampDemod(
    is_demod=1,
    is_incl_raw_trans=1, 
    evt_len=100,
    num_cycles=2.0)




fa.sweepProgTranslators(rffreqs[:4])

fa.sweepProgTranslators(rffreqs[:4],3)

fa.chanzer.chan_to_translate

fa.chanzer.clearTransTable()

fa.chanzer.setFlxDmodTranTable(192,-0.03,-0.035)
fa.chanzer.setFlxDmodTranTable(193,-0.013,-0.034)
fa.chanzer.setFlxDmodTranTable(194,0.039,0.002)
fa.chanzer.setFlxDmodTranTable(195,0.023,-0.030)

fa.chanzer.progTranslator()

fa.sweep(
  span_Hz=4e6, 
  center_Hz=-1, 
  pts=256,
  amplitude = 0,
  defaultFRD=0,
  if_new_settings = False)
  

measure.getMKIDsFromMultiSweep(sweeplen = 256)

mlmove = ccopy.deepcopy(measure.measspecs.mlist)


mlzeros = ccopy.deepcopy(measure.measspecs.mlist)

mlraw = ccopy.deepcopy(measure.measspecs.mlist)

measure.plotMultiSweeps(mlzeros)

measure.plotMultiSweeps(mlmove)


measure.plotMultiSweeps(mlraw)


measure.plotMultiSweeps(measure.measspecs.mlist_raw1)

measure.plotMultiSweeps(measure.measspecs.mlist_trans)



##########################################################3

fa.sram.is_mod_freq=True
fa.sram.mod_periods=4.0
fa.sram.setLutSize(65536)

fa.chanzer.setFluxRampDemod(1,1,100,3.0)

fa.setCarrier(10e6+5093e6)

fa.sourceCapture(freqs,2000)
freqs = arange(1e6,1e6+128e6,1e6).tolist()
freqs = freqs + arange(271e6,271e6 + 128e6,1e6).tolist()
print len(freqs)
fa.sourceCapture(freqs,2000)
time.sleep(.1)
fa.stopCapture()
print len(freqs)


fa.chanzer.setFluxRampDemod(is_demod=1,is_incl_raw_trans=1, evt_len=100,num_cycles=2.0)


fa.chanzer.setFluxRampDemod(is_demod=1,is_incl_raw_trans=2, evt_len=100,num_cycles=2.0)

fa.sourceCapture([10e6],20000)
time.sleep(.1)
fa.stopCapture()

iq=fa.getIQ()

plot(iq[192]['stream_mag'][:1000])


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




fa.sourceCapture([20e6],20000)
time.sleep(.01)
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

fa.if_board.progAtten(fa.if_board.at.
fa.if_board.progRFSwitches(fa.if_board.rf)


fa.if_board.at.atten_U6 = fa.if_board.at.atten_U6 + 3
fa.if_board.progAtten(fa.if_board.at.
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






###########
##\
## which FW we use...
######

#!!fwtype = 'qdrdac'
fwtype = 'tesd'



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

execfile("roach_calibration.py")


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
    


    

class fftAnalyzerR2:

    
    def __init__(self,
        roach_=None,
        is_powerup=True,
        is_loadFW=True, 
        is_calqdr=True,
        is_anritsu_lo_ = True,
        is_anritsu_clk_=True, 
        is_datacap_=True):
    
        self.is_running = False
        
        #self.flux_demod_specs = fluxRampSpecs()
     
        self.roach2=roach_
        
        self.max_event_len=255
        self.first_bbfreq=10.0e6
        self.tes_bias=0.0
        self.tes_bias_on = 0

        self.fft_shift=31

        self.freqs_sweep=[]
        self.fbase=[]
        self.bbfreqs = []
        self.LO = 0
        self.iqdata = []
        self.span_Hz =0;
        self.qdr_cal_good=False
        
        self.power_at_resonator =0
        
        self.power_at_ifboard_rfout=0;
        
        self.is_ramp_generator_on=0
        self.ramp_generator_freq = 0
        self.ramp_generator_voltage = 0


        if self.roach2 != None:
        
            self.powerupFW = ROACH_DIR+'/Roach2DevelopmentTree/bestBitFiles/if_board_setup_2015_Aug_20_1511.bof'

            #this one used for most of data so far-- mar 2016
         
            #fw for testing flux ramp demod on roach
            #self.mainFW = ROACH_DIR+'/projcts/bestBitFiles/qdrdac_2016_Nov_18_1100.bof'
            self.mainFW = ROACH_DIR+'/Roach2DevelopmentTree/bestBitFiles/tesd_2017_Feb_14_1518.bof'

            self.temppath = ROACH_DIR+'/temp/'

            self.anritsu_power = -5
            
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
            self.an.setPower(self.anritsu_power)
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
        
        if fwtype == 'tesd':

            self.phaser1 = phaseCorrect(self.sram, self.rfft,'FM_PhaseCorrect3',2,0.0)
            self.phaser2 = phaseCorrect(self.sram, self.rfft,'FM_PhaseCorrect4',3,0.0)
            self.phaser3 = phaseCorrect(self.sram, self.rfft,'FM_PhaseCorrect5',2,64.0)
            self.phaser4 = phaseCorrect(self.sram, self.rfft,'FM_PhaseCorrect6',3,64.0)
        
        elif fwtype == 'qdrdac':
            self.phaser1 = phaseCorrect(self.sram, self.rfft,'PhaseCorrect3',0)
            self.phaser2 = phaseCorrect(self.sram, self.rfft,'PhaseCorrect4',1)
            self.phaser3 = phaseCorrect(self.sram, self.rfft,'PhaseCorrect5',2)
            self.phaser4 = phaseCorrect(self.sram, self.rfft,'PhaseCorrect6',3)

        if self.is_datacap:
            self.capture=dataCapture()
            #!!self.capture.capture(True)
        else:
            self.capture = None
        
        self.dataread=dataExtract(self.sram,self.rfft)
    
    
        #!!self.adcscope = roachScope(roach, 'octoscope')
        #!!self.fftscope = roachScope(roach, 'octoscope1')

        
        self.rampgen = fluxRampGenerator(self.roach2,self.chanzer)
        
        #ADC sample order
        #!!self.adcdelays = [0,1,2,3]
    
    

    def getUsefulData(self):
        dat = self.getUsefulMetaData()
        dat['fa.iqdata_raw'] = self.iqdata_raw
   
        return(dat)


        

    def getUsefulMetaData(self):
   
        dat={
            'fa.rfft.bin_to_chan':self.rfft.bin_to_chan ,
            'fa.rfft.bin_to_legchan':self.rfft.bin_to_legchan ,
            'fa.rfft.bin_to_srcfreq':self.rfft.bin_to_srcfreq ,
            'fa.rfft.bin_to_leg':self.rfft.bin_to_leg ,
            'fa.rfft.chan_to_bin4':self.rfft.chan_to_bin4,  
            'fa.rfft.fft_bin_flags':fa.rfft.fft_bin_flags,         
            'fa.phaser3.phase_inc_array':self.phaser3.phase_inc_array,
            'fa.phaser4.phase_inc_array':self.phaser4.phase_inc_array,
            'fa.if_board':self.if_board,
            'fa.an':self.an,
            'fa.sram.frequency_list':self.sram.frequency_list,
            'fa.iqdata':self.iqdata,
            'fa.sram.amplist':self.sram.amplist,
            'fa.carrierfreq':self.carrierfreq,
            'fa.bbfreqs':self.sram.frequency_list,
            'fa.LO':self.carrierfreq,
            'fa.freqs_sweep':self.freqs_sweep,
            'fa.chanzer.sync_delay':fa.chanzer.sync_delay ,
            'fa.chanzer.settings':fa.chanzer.settings ,
            'fa.chanzer.read_fifo_size':fa.chanzer.read_fifo_size ,
            'fa.chanzer.chan_to_translate':fa.chanzer.chan_to_translate ,
            'fa.chanzer.b_wr_raw_data':fa.chanzer.b_wr_raw_data ,
            'fa.chanzer.b_sync_source':fa.chanzer.b_sync_source ,
            'fa.chanzer.b_savefluxtrans':fa.chanzer.b_savefluxtrans ,
            'fa.chanzer.b_savefluxraw':fa.chanzer.b_savefluxraw ,
            'fa.chanzer.b_is_look_sync':fa.chanzer.b_is_look_sync ,
            'fa.chanzer.b_flux_demod':fa.chanzer.b_flux_demod ,
            'fa.chanzer.b_en_int_rampgen':fa.chanzer.b_en_int_rampgen ,
            'fa.chanzer.b_drop_all_events':fa.chanzer.b_drop_all_events ,
            'fa.chanzer.flux_cos':fa.chanzer.flux_cos ,
            'fa.chanzer.flux_cos_b':fa.chanzer.flux_cos_b ,
            'fa.chanzer.flux_nsin':fa.chanzer.flux_nsin ,
            'fa.chanzer.flux_nsin_b':fa.chanzer.flux_nsin_b,
            'fa.tes_bias':fa.tes_bias ,
            'fa.tes_bias_on':fa.tes_bias_on ,
            'fa.span_Hz':fa.span_Hz ,
            'fa.is_ramp_generator_on':self.is_ramp_generator_on ,
            'fa.ramp_generator_freq':self.ramp_generator_freq ,
            'fa.ramp_generator_voltage':self.ramp_generator_voltage ,
            'fa.mainFW':fa.mainFW ,
            'fa.power_at_resonator':fa.power_at_resonator,
            'fa.power_at_ifboard_rfout':fa.power_at_ifboard_rfout,
            'fa.loadFW':fa.loadFW}
            
        return(dat)

    def setUsefulData(self,dat):
        self.setUsefulMetaData(dat)
        
        self.iqdata_raw = dat['fa.iqdata_raw'] 

    def setUsefulMetaData(self,dat):
   
      
            self.rfft.bin_to_chan  = dat['fa.rfft.bin_to_chan']
            self.rfft.bin_to_legchan  = dat['fa.rfft.bin_to_legchan']
            self.rfft.bin_to_srcfreq  = dat['fa.rfft.bin_to_srcfreq']
            self.rfft.bin_to_leg  = dat['fa.rfft.bin_to_leg']
            self.rfft.chan_to_bin4 = dat['fa.rfft.chan_to_bin4']           
            self.phaser3.phase_inc_array = dat['fa.phaser3.phase_inc_array']
            self.phaser4.phase_inc_array = dat['fa.phaser4.phase_inc_array']
            #self.if_board = dat['fa.if_board']
            #self.an = dat['fa.an']
            self.sram.frequency_list = dat['fa.sram.frequency_list']
            self.iqdata = dat['fa.iqdata']
            self.sram.amplist = dat['fa.sram.amplist']
            self.carrierfreq = dat['fa.carrierfreq']
            self.sram.frequency_list = dat['fa.bbfreqs']
            self.carrierfreq = dat['fa.LO']
            self.freqs_sweep = dat['fa.freqs_sweep']
      



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
        qdrstat0 = self.qdr0.qdr_cal()
        self.qdr0.qdr_delay_clk_get()
        self.qdr0.qdr_cal_check()

        self.qdr1.reset()
        qdrstat1 = self.qdr1.qdr_cal()
        self.qdr1.qdr_delay_clk_get()
        self.qdr1.qdr_cal_check()

        self.qdr_cal_good=True
        if (not qdrstat0) or (not qdrstat1):
            self.qdr_cal_good = False
            
    def stopCapture(self):
        if self.capture != None:
            self.capture.capture(False)
  

        self.rfft.stopFFTs()
       
        if self.capture != None:    
            #time.sleep(2.0)  
            self.capture.setStream2Disk(0,'temp')


    #given rf freq list, calc carrier freq, bb frqs
    def calcCarrierBBFreqs(self,freqlist_rf_Hz):
    

        farray = numpy.array(freqlist_rf_Hz)
        fmax = numpy.max(farray)
        carrier = self.first_bbfreq + fmax
        freq_bb =numpy.sort( self.first_bbfreq + fmax- farray )
        freq_bb = freq_bb.tolist()

        return((carrier,freq_bb))    

    #source and capture tones. if freqlist not lisst of baseband freqs, then reuse freqs. set to -1 for reuse, else list of bb freqs in Hz.amp list or scalar in adu.
    #sources forever or numffts etc. stopCapture to stop
    def sourceCapture(self,
        freqlist,
        amp,
        numffts = -1,
        whichbins='Freqs',
        is_trig = True,
        is_zero_phaseinc=False,
        if_new_settings=True,       
        stream_fname = None):
        
        self.stopCapture()
        
        self.rfft.stopFFTs()

        if self.capture != None:
            self.capture.clearEvents()
            self.capture.capture(True)

        
        #prog and start lut sines
        #if -1 then reuse same freqs from earlier setting
        
        if if_new_settings:
            self.sram.setLutFreqs(freqlist,amp)
            print 'sourceCapture  setLutFreqs'
            
            
        #startdac
        self.dac.setReset()
        self.dac.setSync(1,1)

        self.roach2.write_int('MKID_ADC_settings',self.is_digital_loopback);
        
      
        if if_new_settings:
            print 'sourceCapture fftBinsFreqs or fftBinsAll'
            if whichbins=='Freqs':
                self.rfft.fftBinsFreqs()

            else:
                #"High" "Low", "All"
                self.rfft.fftBinsAll(whichbins)

            
      
       
        if self.capture != None:
            self.capture.mapChannels(self.rfft)
            if stream_fname != None:
                self.capture.setStream2Disk(1,stream_fname)
            else:
                self.capture.setStream2Disk(0,'temp')
            
            
       
    
        self.rfft.fftsynctime=128
        self.rfft.roach_fft_shift=self.fft_shift
                
            
        self.rfft.numFFTs(numffts)
        self.rfft.progRoach()
            

        
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
            self.phaser3.reprogPhaseIncs() 
            self.phaser4.reprogPhaseIncs()
        else:
            self.phaser1.zeroPhaseIncs() 
            self.phaser2.zeroPhaseIncs()
            self.phaser3.zeroPhaseIncs() 
            self.phaser4.zeroPhaseIncs()
       
   
      
      
      
        if is_trig:
            self.rfft.trigFFT()

    def findSweepData(self,chan=192):
        #for k in range(64,300):
        #    if self.iqdata_raw[chan]['stream_mag'][k] >0.001:
        #        return(k)


        k=0
        return(0)


    def calcAmp(self,L):
        amp = 30000.0/L
        return(amp)
        
        
    def captureNoise(self,
        rffreqs=[5100e6],
        timesec=1.0,
        fname = None,
        is_new_settings=True,
        BB=None,
        LO = None, 
        pwr_at_res = None,
        lock = None):

        print 'fftAnaluzerR2.captureNoise'
        self.is_running = True
        
        if LO==None:
            [LO,BB]=self.calcBBLOFromRFFreqs(rffreqs)
        
        if is_new_settings:
            self.setCarrier(LO)
            
        self.an.setOnOff(1)
        
        isn=is_new_settings
        
        num_tones = len(BB);
        if pwr_at_res==None:
            pwr_at_res = tone_power_at_resonator_dbm 
        
        (amp, atu6, atu7, atu28) = calcSineampAttensFromResPower(num_tones, pwr_at_res)
 
        if isn==is_new_settings: 
            self.if_board.at.atten_U6=-atu6
            self.if_board.at.atten_U7=-atu7
            self.if_board.at.atten_U28=-atu28
            self.if_board.progAtten(self.if_board.at)


        self.sourceCapture(
            BB,
            amp,
            whichbins='Freqs',
            if_new_settings=isn,
            stream_fname = fname)

        numsec = 0.0
        
        print 'fftAnaluzerR2.captureNoise- waiting'

        #if we passed a lock, then we release during wait, and reacq after wait
        if lock!=None:
            lock.release()
            
        while numsec<timesec:
        
            time.sleep(1.0)
            numsec = numsec+1.0
            
            if not self.is_running:
                break
        
        print 'fftAnaluzerR2.captureNoise- Stopping'
        
        if lock!=None:
            lock.acquire()
        
        self.stopCapture()
        
        if fname == None:
            self.getIQ()
        else:
        
            self.getIQ(dsname = fname,issave = False)
            os.rename(fname+'_B.h5',fname)
  
        self.an.setOnOff(0)    
       
        if fname!=None:
            print 'saving to %s'%fname
            dat=self.getUsefulMetaData()
            hdf = hdfSerdes()
            hdf.open(fname,'a')
            hdf.write(dat,'metadata')
            
            hdf.close()
            
        

            
             
    #calc base band freq list, and LO freq given list of RF freqs
    def calcBBLOFromRFFreqs(self,rffreqs):
  
        if type(rffreqs)==list:
            rffreqs=numpy.array(rffreqs)
            
        frange = max(rffreqs) - min(rffreqs)
        if frange>230e6:
            print "cannot source this freq list- to wide BW"
            return

        LO=max(rffreqs)+self.first_bbfreq
        bbfreqs = LO - rffreqs

        bbfreqs = numpy.sort(bbfreqs)
        return( (LO, bbfreqs) )

    ########################
    #
    #span_Hz=100e6,  a float
    #center_Hz=3000e6, one freq in hz or a list or array of freqs. these are center freqs
    #nim points to seep pts=2048,
    #raw_trans=1 or 2. raw or translated data raw is preferred
    #center_Hz if -1, then reuse old centerfreqs, and dont recalc.
    ##
    def sweep(self,
        span_Hz=100e6, 
        center_Hz=3000e6, 
        pts=2048,
        pwr_at_res = None,
        defaultFRD=1,
        if_new_settings=True,
        lock=None,
        callback=None):

        self.is_running = True;
        
        self.stopCapture()


        self.setTESBias(0,0)


        #turn off flux ramp demod
        if defaultFRD==1:
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


        
 

       

        if if_new_settings:

            if type(center_Hz)==float or type(center_Hz)==numpy.float64:
                center_Hz = numpy.array([center_Hz])
            
            if type(center_Hz)==list:
                center_Hz = numpy.array(center_Hz)
                
            num_tones = len(center_Hz);
            if pwr_at_res==None:
                pwr_at_res = tone_power_at_resonator_dbm 
            

            (amp, atu6, atu7, atu28) = calcSineampAttensFromResPower(num_tones, pwr_at_res)

            print 'fa.sweep: pr %5.2f, a %5.2f, u6 %5.2f,u7 %5.2f,u28 %5.2f'%(
                pwr_at_res,amp,atu6,atu7,atu28)
            self.if_board.at.atten_U6= -atu6
            self.if_board.at.atten_U7= -atu7
            self.if_board.at.atten_U28= -atu28
            self.if_board.progAtten(self.if_board.at)
            self.if_board.at.report()

            (self.LO, self.bbfreqs) = self.calcBBLOFromRFFreqs(center_Hz)
            self.center_Hz = center_Hz
            self.amplitude = amp
            self.span_Hz = span_Hz
            self.pts = pts
            
            self.fbase = self.bbfreqs
            self.start_carrier = self.LO-self.span_Hz/2.0
            self.end_carrier = self.LO+self.span_Hz/2.0
            self.inc_carrier = self.span_Hz/self.pts
            self.carrier_freqs = arange(
                self.start_carrier ,
                self.end_carrier,
                self.inc_carrier )


            print 'sweep using NEW settings'
            
       
        
        
        
        if_new_settings_ = if_new_settings
        self.sourceCapture(
            self.bbfreqs,
            self.amplitude,
            numffts = 1,
            whichbins='Freqs',
            is_trig = False,
            is_zero_phaseinc=True,
            if_new_settings = if_new_settings_)



        

        self.an.setOnOff(0)
        
        
        self.roach2.write_int('sw_timestamp',1)
        
        #take off data... we have some fifo problem... some time delay for some rheason...


        
        self.roach2.write_int('sw_timestamp',2)

        self.an.setOnOff(1)
        
        self.phaser1.zeroPhaseIncs()
        self.phaser2.zeroPhaseIncs()
        self.phaser3.zeroPhaseIncs()
        self.phaser4.zeroPhaseIncs()


        lcount =0
        
        for cf in self.carrier_freqs:

            #print 'trig fft cf=%f'%cf
            self.setCarrier(cf)

            time.sleep(0.000001)
            self.rfft.trigFFT()

            if not self.is_running: break
            
            
            if callback!=None:
                callback()
                
            #if passed a lock, we rlease, reacquire so other threads can do something if necessary
            #assume we alrady had the lock
            if lock!=None:
                if (lcount%16)==0:
                    lock.release()
                    time.sleep(0.000001)
                    lock.acquire()
                    
            lcount = lcount +1

        #we have taken 200 points, becaise some FWs may not have fifl readout yet we take
        #rest of points to fill memory, to make sure we have fifos readout. this is not used 
        #data for cal.

        self.roach2.write_int('sw_timestamp',0)

        self.setCarrier(self.LO)
        time.sleep(.1)
        

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
            if fwtype=='tesd':
                mags = self.iqdata_raw[192]['stream_mag'][stindex : (stindex+2*pts):2]
                phase = self.iqdata_raw[192]['stream_phase'][stindex : (stindex+2*pts):2]    
            else:
                mags = self.iqdata_raw[192]['stream_mag'][stindex : (stindex+pts)]
                phase = self.iqdata_raw[192]['stream_phase'][stindex : (stindex+pts)]    
            #phase=self.removePhaseJumps(phase)

            self.iqdata = self.dataread.PolarToRect( [mags,phase] )
            self.freqs_sweep = self.carrier_freqs - self.bbfreqs[0]

        self.an.setOnOff(0) 
        self.stopCapture()
        time.sleep(1)   
        self.is_running = False

        
    def getIQ(self,dsname = None,issave = True,is_decimate=False,max_read_size = 1000000):
        
        is_rm_tempfiles = False
        
        if dsname==None:
            dsname = self.temppath + 'TEMP'
            is_rm_tempfiles = True
            
        timeout=10
        cnt=0
        self.iqdata_raw={}

        if issave:
            self.capture.saveEvents(dsname)
        
        while  not os.path.isfile(dsname+'_B.h5'):
          time.sleep(1.0)
          cnt=cnt+1
          print 'waiting for file save to finish'
          if cnt==timeout:
              print "ERROR cannot get data"
              return({})
          
        #we should get two commands from the c program. 
        #self.capture.getCmd()
        #self.capture.getCmd()
        
        hdf=hdfSerdes()
        #if dataset large, and is_decimatge, it gets sample of whole dataset but decimated to reduce sise.
        #max size is set in hdf.maxreadsize. if not decimate, it reads only up to maxreadsize. 
        #default to 1M samples
        hdf.setDecimate(is_decimate)
        hdf.maxreadsize=max_read_size
        
        fn = dsname + '_B.h5'
        hdf.open(fn,'r')
        self.iqdata_raw = hdf.read()
        hdf.close()
       

        #self.dataread
        if is_rm_tempfiles:
            os.system('rm -rf %s'%(dsname+'_A.h5'))
            os.system('rm -rf %s'%(dsname+'_B.h5'))

       

 
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
        
        
        if fwtype == 'tesd':
            self.roach2.setupEth('GBEthernet_xmit0','192.168.1.11',100,'02:02:00:00:00:01')
    
        elif fwtype == 'qdrdac':
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
   
    def setRampGenerator(self, is_on, freq, voltage):
        self.is_ramp_generator_on  = is_on
        self.ramp_generator_freq = freq;
        self.ramp_generator_voltage = voltage;

        agt.setRamp()
        agt.setVolts(self.ramp_generator_voltage)
        agt.setFreq(self.ramp_generator_freq)
        agt.setOutOn(self.is_ramp_generator_on)
 

    def setTESBias(self,is_on,vbias,callback = None):
    
        if sim==None:
            return
            
        if is_on:
            sim.setOutOn(0)
            vsweep = arange(10.0,vbias-0.02,-0.02)
            time.sleep(1.0)
            sim.setVolts(10.0)
            sim.setOutOn(1)

            for v in vsweep:
                self.temp_volts = v
                sim.setVolts(v)
                
                time.sleep(0.01)
                if callback!=None: callback()
                

            self.tes_bias = vbias       
            self.tes_bias_on = 1
        else:
            self.tes_bias = vbias       
            self.tes_bias_on = 0
            sim.setOutOn(0)
            
            
            
            
    #give list of iqcenter data.
    # dict with keys 'rffreq', 'xc', 'yc' mmkidMeasure,getResonatorIQCenters  retyrns this.  
    #this will program the translator in roach w. iq circle centers
    #call sourceCapture with freqs=-1 . also call sweep w/ freqs =-1 for sweep with these sets      
             
    def progTranslatorsFromIQCircles(self,iqcd):
        
        if iqcd != -1:
            self.iqcenterdata = iqcd
        
        
        #rffreqs = []
        #for item in self.iqcenterdata:
        #    rffreqs.append(item['rffreq'])
        
        
     
        for item in self.iqcenterdata:
            #item['bbfreq'] = self.carrierfreq - item['rffreq']
            #item['bin'] = self.rfft.getBinFromFreq(item['bbfreq'])
            #item['LO'] = self.carrierfreq
            #item['chan'] = self.rfft.bin_to_chan[item['bin']]
            
            self.chanzer.setFlxDmodTranTable(chan=item['chan'],xc=item['xc'],yc=item['yc'])

        self.chanzer.progTranslator()
        #return( self.iqcenterdata)
        

    #rffreqs as a list of freqs in hz, actual res freqs in Hz. sweep flags is 3 bits
    #0, test center freq, 1, do sweep for iq center meas, 2 sweep to test iq center
    def sweepProgTranslators(
        self,
        rffreqs, 
        pwr_at_res = None,
        sweepflags = 7,
        lock_=None,
        callback_ = None):
        
        measure.measspecs.rffreqs = rffreqs

        #if sweepflags&1:
        if False:
            self.chanzer.clearTransTable()
            #
            # sweep and do IQ vel to get exact freqs.
            #
            print "Measure exact frequencies of Resonators"

            self.chanzer.setIsSync(0)
            self.chanzer.setFluxRampDemod(
                is_demod=0,
                is_incl_raw_trans=1, 
                evt_len=100,
                num_cycles=2.0)




            self.sweep(
                span_Hz=4e6, 
                center_Hz=rffreqs, 
                pts=256,
                pwr_at_res = pwr_at_res,
                defaultFRD=0,
                lock=lock_,
                callback=callback_)

            #we do IQ calc in htere..
            mlist = measure.getMKIDsFromMultiSweep(sweeplen = 256)
            #reset rffreqs to []
            rffreqsrough=rffreqs
            
            rffreqs = []
            for m in mlist:
                rffreqs.append( m.reslist[0].getFc())

            measure.measspecs.rffreqs = rffreqs
            measure.measspecs.rffreqsrough = rffreqsrough
            
            
            #measure.measspecs.iqdata_msweep_raw0 = ccopy.deepcopy(self.iqdata_raw)
            measure.measspecs.mlist_raw0 = ccopy.deepcopy(measure.measspecs.mlist)
            andata = self.getUsefulData()
            measure.measspecs.andata_0 = ccopy.deepcopy(andata)
            

        #
        # now we have correct freqs, opeimize wave lut table for these freqs. sweep to find IQ curcles
        #
        
        if sweepflags&2:

            print "Sweep to get IQ centers"
            self.chanzer.setIsSync(0)
            self.chanzer.setFluxRampDemod(
                is_demod=0,
                is_incl_raw_trans=1, 
                evt_len=100,
                num_cycles=2.0)

            self.sweep(
                span_Hz=4e6, 
                center_Hz=measure.measspecs.rffreqs, 
                pts=256,
                pwr_at_res = pwr_at_res,
                defaultFRD=0,
                lock=lock_,
                callback=callback_)

            #measure.measspecs.iqdata_msweep_raw1 = ccopy.deepcopy(self.iqdata_raw)


            #get mkid/resonator list from the sweep we just did.
            #stored in measure.measspecs.mlist
            measure.getMKIDsFromMultiSweep(sweeplen = 256)
            measure.measspecs.mlist_raw1 = ccopy.deepcopy(measure.measspecs.mlist)
            andata = self.getUsefulData()
            measure.measspecs.andata_1 = ccopy.deepcopy(andata)




            #extract res data we need such as rffreq, and iq circle centers
            measure.getResonatorIQCenters()

        if sweepflags & 4:
            #
            # Program trnaslators, sweep again to test that we cound IQ cuircles correctly
            #
            print "Test measured IQ centers"

            self.progTranslatorsFromIQCircles(measure.iqcenterdata)

            self.chanzer.setIsSync(0)
            self.chanzer.setFluxRampDemod(
                is_demod=1,
                is_incl_raw_trans=2, 
                evt_len=100,
                num_cycles=2.0)

            self.sweep(
                span_Hz=4e6, 
                center_Hz=-1, 
                pts=256,
                pwr_at_res = pwr_at_res,
                defaultFRD=0,
                if_new_settings = False,
                lock=lock_,
                callback=callback_)

            measure.getMKIDsFromMultiSweep(sweeplen = 256)

            #measure.measspecs.iqdata_msweep_trans = ccopy.deepcopy(self.iqdata_raw)
            measure.measspecs.mlist_trans = ccopy.deepcopy(measure.measspecs.mlist)


            #!!for m in measure.measspecs.mlist_trans: 
            #!! m.reslist[0].setDelay(measure.xmission_line_delay)
            #!! m.reslist[0].applyDelay()

 

            andata = self.getUsefulData()
            measure.measspecs.andata_trans = ccopy.deepcopy(andata)

        self.is_running=False
          
  
  
  
    def plotMultiSweep(self,swlen = 256,is_clf=True):

        if is_clf:
            figure(11)
            clf()
            figure(12)
            clf()
        for k in self.iqdata_raw.keys():
            print k
            figure(11)
            subplot(2,1,1)
            plot(self.iqdata_raw[k]['stream_mag'][:swlen])
            subplot(2,1,2)
            plot(self.iqdata_raw[k]['stream_phase'][:swlen])
            figure(12)
            iq=self.dataread.PolarToRect(
                [self.iqdata_raw[k]['stream_mag'][:swlen], 
                self.iqdata_raw[k]['stream_phase'][:swlen]  ])
            plot(iq[0],iq[1])





    def voltSweep(self,
        vlist=None,
        rffreq=[5100e6],
        numsamples = 2000,
        fnames=None,
        BB=None,
        LO = None,
        amp=None,
        lock = None,
        callback=None,
        issync = 0,
        evtsize2=100,
        syncdelay=0):

        self.is_running=True
        
        if vlist==None:
            vlist = numpy.arange(10.0,0.0,-0.1)

        ev=0
        #base band 10MHz, amp is 30k counts in DACs. take 200 ffts, and only return the 10MHz fft bin. do not trig the ffts yet.

        self.an.setOnOff(1)  
        #get sync from ext ramp gen.
        self.chanzer.setSyncSource(0)
        #trigger on ramp gen pulses
        self.chanzer.setIsSync(issync)
        #meas sync freq, and set up event size (or flux ramp event size) number of samples.
        #self.rampgen.setChannelizerFifoSync()
        self.chanzer.setReadFifoSize(evtsize2)
        
        self.phaser1.zeroPhaseIncs()
        self.phaser2.zeroPhaseIncs()
        self.phaser3.zeroPhaseIncs()
        self.phaser4.zeroPhaseIncs()

        
        self.chanzer.setSyncDelay(syncdelay)
       
    
        time.sleep(0.5)

        sim.setOutOn(1)
        #self.capture.setStream2Disk(1, fnames)

        if BB==None:
            [LO,BB]=self.calcBBLOFromRFFreqs(rffreq)
    
        self.setCarrier(LO)
        if amp==None:
            amp = self.calcAmp(len(rffreq))

       

        self.sourceCapture(
            BB,
            amp,        
            whichbins='Freqs',
            is_trig=False,
            stream_fname = fnames)


        volts = vlist[0]
        sim.setVolts(volts)
        roach.write_int('sw_timestamp',int(1000*volts))
        roach.write_int('sw_timestamp2',int(1000*volts))
        self.rfft.trigFFT()
        #wait for the capture to start
        time.sleep(0.01)

        if lock!=None: lock.release()
        
        for volts in vlist:
            self.temp_volts = volts
            sim.setVolts(volts)
            #embed voltage into roach data stream so we associate the voltage with the data.
            
            if lock!=None: lock.acquire()            
            roach.write_int('sw_timestamp',int(1000*volts))
            roach.write_int('sw_timestamp2',int(1000*volts))
            if lock!=None: lock.release()
            #self.chanzer.flushFifos()
            
            time.sleep(0.3)
            if callback!=None:
                callback()
            
            if not self.is_running:
                break


        if lock!=None: lock.acquire()     
        self.stopCapture()
        ev =self.getIQ(dsname = fnames,issave = False,is_decimate = True,max_read_size = 10000)
        sim.setOutOn(0)
        self.an.setOnOff(0)    

        os.rename(fnames+'_B.h5',fnames)
        
        for ch in ev.keys():        
            #LO = self.carrierfreq - self.rfft.bin_to_srcfreq[ ev[ch]['bin'][0] ]
            ev[ch]['rffreq'] = LO



        if fnames!=None:
           hdf=hdfSerdes()
           hdf.open(fnames,'a')
          
           dat = self.getUsefulMetaData()
           hdf.write(dat,'metadata')
           hdf.close()


        return(ev)


    # pick internal or external suync source- using internal FW ramp gen (we done use it), or the external
    #agilent ramp source. ci is in dex of a gui- OPenLoop is 0, Closed Agilent ramp is 1, closed loop inter ramp is 2

    def setRampSyncSource(self,ci):
        
        #no ramp
        if ci==0:
            self.rampgen.setIsSync(0)
            self.rampgen.setSyncSource(0)
            self.rampgen.setChannelizerFifoSync()
        
        #ext ramp
        elif ci==1:
        #int ramp
            self.rampgen.setIsSync(1)
            self.rampgen.setSyncSource(0)
            self.rampgen.setChannelizerFifoSync()


        else:
            self.rampgen.setIsSync(1)
            self.rampgen.setSyncSource(1)
            self.setRampSpecs()
            ##self.rampgen.setChannelizerFifoSync()
        
  
