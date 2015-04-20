date = 'apr16_10:18A'
cd /home/oxygen26/TMADDEN/ROACH2/projcts/pyfiles


execfile('pyPipeServer.py')


execfile('katcpNc.py')


roach2=katcpNc()



roach2.startNc()


sv=pyPipeServer()


sv.openPipes()


# ls -t ./tengbddr/bit_files/*.bof | head -1 | xargs -I%1 cp %1 bestBitFiles/.

# ls -t ./tengbddr/bit_files/*.bof | head -1


roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbddrb_2015_Apr_20_1554.bof')


roach2.setupEth('xmit0','192.168.1.0',100,'02:02:00:00:00:01')



# cmd="roach2.setupEth('rcv0','192.168.1.2',54321,'02:02:00:00:00:02')


