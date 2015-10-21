cd /home/oxygen26/TMADDEN/ROACH2/projcts/pyfiles

execfile('natAnalGui.py')

execfile('pyPipeServer.py')


execfile('katcpNc.py')


roach2=katcpNc()



roach2.startNc()


sv=pyPipeServer()


sv.openPipes()





#    cmd="roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbtest_2015_Apr_01_1501.bof')
#roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbtestb_2015_Apr_02_1306.bof')

roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbtestc_2015_Apr_07_1015.bof')



roach2.setupEth('xmit0','192.168.1.0',100,'02:02:00:00:00:01')



# cmd="roach2.setupEth('rcv0','192.168.1.2',54321,'02:02:00:00:00:02')


