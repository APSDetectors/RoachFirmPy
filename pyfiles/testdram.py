import os

execfile('katcpNc.py')

#need these fifos preexistant with mkfifo... 


#need this fifos preexistant with mkfifo
#/local/roachkatcpfifoOut,
#/local/roachkatcpfifoIn
#you can edit the py codes of yuo want differnet fifo names

roach2=katcpNc()
roach2.startNc()




roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbddrb_2015_Apr_21_0939.bof')


roach2.setupEth('xmit0','192.168.1.0',100,'02:02:00:00:00:01')
#roach2.stopEth('xmit0')
roach2.infoEth()


#
# test data- ABCDEFT.... 
#
roach2.dram_test_nbuffers=16


roach2.dramTestData('DRAM_LUT')

roach2.streamDram('DRAM_LUT')


trigScope(0,0)

plotScope(128)

#
# sin on one output of dram
#

i=roach2.singleFreqLUT(1024e4,'I',1024e6,8192,0,20000)

ibin = roach2.convertToBinary128_2(i,7)

roach2.writeDram('DRAM_LUT',ibin)


roach2.streamDram('DRAM_LUT')


trigScope(-1,0);plotScope()



roach2.readAllReg()





#
# sending iq data to dram
#
i=roach2.singleFreqLUT(1e6,'I',512e6,1024*16,0,20000)
q=roach2.singleFreqLUT(1e6,'Q',512e6,1024*16,0,20000)

iqbin=roach2.convertToBinary128(i,q);

roach2.writeDram('DRAM_LUT',iqbin)


roach2.streamDram('DRAM_LUT')


trigScope(-1,0);plotScope()


trigScope(0,7)

plotScope(pllen = 1024, is_usebits = True, bits='15:11')


#
# close conn to roach
#

roach2.closeFiles()


