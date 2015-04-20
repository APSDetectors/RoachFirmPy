import os

execfile('katcpNc.py')

#need these fifos preexistant with mkfifo... 


#need this fifos preexistant with mkfifo
#/local/roachkatcpfifoOut,
#/local/roachkatcpfifoIn
#you can edit the py codes of yuo want differnet fifo names

roach2=katcpNc()
roach2.startNc()




roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbddrb_2015_Apr_20_1554.bof')


roach2.setupEth('xmit0','192.168.1.0',100,'02:02:00:00:00:01')



roach2.dram_test_nbuffers=16


roach2.dramTestData('DRAM_LUT')

roach2.streamDram('DRAM_LUT')


trigScope(0,0)

plotScope(128)



