import os

#
# use qdrtest.slx as the firmware
#


execfile('katcpNc.py')
execfile('freqSweep.py')
execfile('roachScope.py')
execfile('sramLut.py')


#need these fifos preexistant with mkfifo... 


#need this fifos preexistant with mkfifo
#/local/roachkatcpfifoOut,
#/local/roachkatcpfifoIn
#you can edit the py codes of yuo want differnet fifo names

roach2=katcpNc()
roach2.startNc()

roach2.closeFiles()


#200MHz
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrtest_2015_May_08_1547.bof')

#100MHz
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrtest_2015_May_08_1411.bof')

#128MHz
#roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrtest_2015_May_13_1424.bof')

roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrtest_2015_May_13_1458.bof')

#128MHz, w. FIR filter
#
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/qdrtest_2015_May_15_0753.bof')


#
# qdr test
#

execfile('qdr.py')

qdr0=Qdr(roach2,'qdr0')

qdr0.reset()

qdr0.qdr_cal()

qdr0.qdr_delay_clk_get()

qdr0.qdr_cal_check()


qdr1=Qdr(roach2,'qdr1')

qdr1.reset()

qdr1.qdr_cal()

qdr1.qdr_delay_clk_get()

qdr1.qdr_cal_check()


#
# Define stuff
#
execfile('freqSweep.py')
execfile('roachScope.py')
execfile('sramLut.py')

roachscope = roachScope(roach2, 'roachscope')
roachscope1 = roachScope(roach2, 'roachscope1')

sweeper = freqSweep(roach2, 'QuadIQSweep')

sram = sramLut(roach2,'SRAM_LUT')




#
# look at bits
#

ch=1
bitsx = '0:0;1:1;2:2;3:3;4:4;5:5;6:6;7:7;11:8'
roachscope1.trigScope(-1,ch);roachscope1.plotScope(isprint=True,is_usebits = True,bits=bitsx);


#
# look at qdr mem w/ scope
#

shskip_=4
shoffset_=0
pllen_=128
mn='qdr1_memory'
roachscope.plotScope(memname = mn,shskip=shskip_,shoffset=shoffset_,isprintsh=True)

#
# look at signals
#

ch=0
roachscope.trigScope(-1,ch);roachscope.plotScope(isprintsh=True);




#
# test data- ABCDEFT.... 
#
roach2.sram_test_nbuffers=16


sram.sramTestData(7)

sram.streamSram()


roachscope.trigScope(0,1)
roachscope.plotScope(128)
#qdrtest_2015_May_08_0941.bof


#
# manual writes
#
sram.stopSram()

roach2.write('qdr0_memory','abcdefgh'*256)
roach2.read('qdr0_memory',8*256)




roach2.write('qdr1_memory','IJKLMNOP'*256)
roach2.read('qdr1_memory',8*256)


roach2.write('qdr1_memory','IJKLMNOP'*256)

roach2.write('qdr0_memory','\x00'*16*256)
roach2.write('qdr1_memory','\x00'*16*256)


roach2.write_int('SRAM_LUT_LUTSize',roach2.write('qdr0_memory','\x00'*16*256)
roach2.write('qdr1_memory','\x00'*16*256)
256)

sram.which_write='cpu'

sram.which_write='bram'

sram.writeSram('ABCDEFGHijklmnop'*1024)

sram.streamSram()


ch=3
roachscope.trigScope(0,ch);roachscope.plotScope(isprint=True)




roach2.read('qdr0_memory',128*8)

roach2.read('qdr1_memory',2048,2048*3)

#
# test data- ramps. 
#

sram.sramTestData2(rlen=128)

sram.streamSram()

roach2.readAllReg()

ch=0
roachscope.trigScope(-1,ch);roachscope.plotScope(pllen=256);ch=ch+1



#
# sin on one output of sram
#

i=sram.singleFreqLUT(1024e4,'I',1024e6,8192,0,20000)

ibin = sram.convertToBinary128_2(i,7)

sram.writeSram(ibin)


sram.streamSram()


roachscope.trigScope(-1,1);roachscope.plotScope()



roach2.readAllReg()





#
# sending iq data to sram
#
i=roach2.singleFreqLUT(1e6,'I',512e6,1024*16,0,20000)
q=roach2.singleFreqLUT(1e6,'Q',512e6,1024*16,0,20000)

iqbin=roach2.convertToBinary128(i,q);


sram.writeSram(iqbin)

sram.streamSram()



ch=0
roachscope.trigScope(0,ch);roachscope.plotScope(isprint=False);ch=ch+1


sram.streamSram()

ch=0
roachscope.trigScope(-1,ch);roachscope.plotScope()


roachscope.trigScope(0,7)

roachscope.plotScope(pllen = 1024, is_usebits = True, bits='15:11')


#
# IQDATA with sweep
#




i=sram.singleFreqLUT(1e6,'I',512e6,1024*16,0,10000)
q=sram.singleFreqLUT(1e6,'Q',512e6,1024*16,0,10000)


i=i + sram.singleFreqLUT(2e6,'I',512e6,1024*16,0,10000)
q=q + sram.singleFreqLUT(2e6,'Q',512e6,1024*16,0,10000)

i=i + sram.singleFreqLUT(3e6,'I',512e6,1024*16,0,10000)
q=q + sram.singleFreqLUT(3e6,'Q',512e6,1024*16,0,10000)

iqbin=sram.convertToBinary128(i,q);

sram.writeSram(iqbin)


sram.streamSram()


st = 1e1;ed=20e6;step=(ed-st)/8192
sweeper.startSweep(st,step,ed)

st = 0;ed=0;step=0
sweeper.startSweep(st,step,ed)



ch=0
roachscope.trigScope(0,ch);roachscope.plotSpectrum();ch=ch+1

ch=0
roachscope1.trigScope(0,ch);roachscope1.plotSpectrum();ch=ch+1

ch=2
for k in range(50):roachscope1.trigScope(0,ch);roachscope1.plotSpectrum();draw()

for k in range(50):roachscope1.trigScope(0,ch);roachscope1.plotScope();draw()




ch=0
roachscope.trigScope(0,ch);roachscope.plotScope();ch=ch+1

ch=0
roachscope1.trigScope(0,ch);roachscope1.plotScope();ch=ch+1


roachscope.trigScope(-1,5);roachscope.plotScope()


roachscope.trigScope(0,7)
roachscope.plotScope()


roachscope.plotScope(pllen = 1024, is_usebits = True, bits='15:11')

roachscope.plotScope(is_usebits = True, bits='15:15;14:14;13:13;12:12;11:11;10:10;9:9;8:8')











#
# close conn to roach
#

roach2.closeFiles()


