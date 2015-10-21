import os

execfile('katcpNc.py')
execfile('freqSweep.py')
execfile('roachScope.py')
execfile('dramLut.py')


#need these fifos preexistant with mkfifo... 


#need this fifos preexistant with mkfifo
#/local/roachkatcpfifoOut,
#/local/roachkatcpfifoIn
#you can edit the py codes of yuo want differnet fifo names

roach2=katcpNc()
roach2.startNc()



#No Notch Filter- Workig
roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbddrc_2015_May_05_0835.bof')

#Notch Filter


roach2.setupEth('xmit0','192.168.1.0',100,'02:02:00:00:00:01')
#roach2.stopEth('xmit0')
roach2.infoEth()



roachscope = roachScope(roach2, 'roachscope')
roachscope1 = roachScope(roach2, 'roachscope1')

sweeper = freqSweep(roach2, 'QuadIQSweep')
dram = dramLut(roach2,'DRAM_LUT')


#
# test data- ABCDEFT.... 
#
roach2.dram_test_nbuffers=16


dram.dramTestData(3)

dram.streamDram()


roachscope.trigScope(0,1)
roachscope.plotScope(128)





#
# test data- ramps. 
#


dram.dramTestData2()

dram.streamDram()

ch=0
roachscope.trigScope(0,ch);roachscope.plotScope();ch=ch+1





#
# sin on one output of dram
#

i=dram.singleFreqLUT(1024e4,'I',1024e6,8192,0,20000)

ibin = dram.convertToBinary128_2(i,3)

dram.writeDram(ibin)


dram.streamDram()


roachscope.trigScope(-1,1);roachscope.plotScope()



roach2.readAllReg()





#
# sending iq data to dram
#
i=roach2.singleFreqLUT(1e6,'I',512e6,1024*16,0,20000)
q=roach2.singleFreqLUT(1e6,'Q',512e6,1024*16,0,20000)

iqbin=roach2.convertToBinary128(i,q);

dram.writeDram(iqbin)


dram.streamDram()


roachscope.trigScope(-1,0);roachscope.plotScope()


roachscope.trigScope(0,7)

roachscope.plotScope(pllen = 1024, is_usebits = True, bits='15:11')


#
# IQDATA with sweep
#




i=dram.singleFreqLUT(1e6,'I',512e6,1024*16,0,10000)
q=dram.singleFreqLUT(1e6,'Q',512e6,1024*16,0,10000)


i=i + dram.singleFreqLUT(2e6,'I',512e6,1024*16,0,10000)
q=q + dram.singleFreqLUT(2e6,'Q',512e6,1024*16,0,10000)

i=i + dram.singleFreqLUT(3e6,'I',512e6,1024*16,0,10000)
q=q + dram.singleFreqLUT(3e6,'Q',512e6,1024*16,0,10000)

iqbin=dram.convertToBinary128(i,q);

dram.writeDram(iqbin)


dram.streamDram()



st = 1e6;ed=40e6;step=(ed-st)/4096
sweeper.startSweep(st,step,ed)

st = 0;ed=0;step=0
sweeper.startSweep(st,step,ed)




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


