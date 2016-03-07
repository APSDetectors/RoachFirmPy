
execfile('katcpNc.py')

execfile('sramLut.py')

execfile('qdr.py')

execfile('if_board.py')

execfile('fccdSimImage.py')



execfile('roachScope.py')




roach2=katcpNc()
roach2.startNc()


#disconn from roach
roach2.closeFiles()


roach2.sendBof('/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/fccdsimulator_2015_Nov_12_1315.bof')


#call to read all reg vales on roach print on screen, return as list of tupels
roach2.readAllReg()



qdr0=Qdr(roach2,'qdr0')

qdr1=Qdr(roach2,'qdr1')

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


##########
#
#

oscope = roachScope(roach2, 'octoscope0')


oscope.trigScope(-1,0)
oscope.readScopeOcto()
oscope.is_hold=False

oscope.interleave([0])
oscope.plotScope(replot=True,pllen=1024);



oscope.interleave([1])
oscope.plotScope(replot=True,pllen=1024);


oscope.interleave([2])
oscope.plotScope(replot=True,pllen=1024);



oscope.interleave([3])
oscope.plotScope(replot=True,pllen=1024);



oscope.interleave([4])
oscope.plotScope(replot=True,pllen=1024);


oscope.interleave([5])
oscope.plotScope(replot=True,pllen=1024);

oscope.interleave([6])
oscope.plotScope(replot=True,pllen=1024);


oscope.interleave([7])
oscope.plotScope(replot=True,pllen=1024);



oscope.trigScope(0,0)
oscope.readScopeOcto()
oscope.is_hold=True
clf()
oscope.interleave([4]);
oscope.plotScope(
	bits ='0:0;1:1;2:2;3:3;4:4;5:5;6:6;7:7',
	is_usebits = True);


oscope.interleave([0])
oscope.plotScope(replot=True);


#

execfile('sramLut.py')

sram = sramLut(roach2,'SRAM_LUT')

#sram.setLutSize(1024*1024)


sram.setLutFreqs([1e6], 1500)



execfile('fccdSimImage.py')

fccdi = fccdSimImage(sram,960,962)


fname = '/localc/fccd/raw_scrambled_rawImm_12001-13000.imm'

aa=fccdi.loadImgImmRaw(fname,100)


fccdi.makePackets()

fccdi.writeSram()

sram.streamSram()


fccdi.estat()

sram.stopSram()

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


roach2.read_int('gbeofcount')



cmd = 'xterm -e /localc/fccd/build-FCCDListener-Desktop-Debug/FCCDListener --cmd_in_pipe_name /localc/fccdcmdpipein --cmd_out_pipe_name /localc/fccdcmdpipeout --outpipe /localc/fccdimgs --CamIP 192.168.1.11 --LocalIP 192.168.1.102 --LocPort 50000 --xsize 960 --ysize 962 --openpipe true --openport true --is_print true &'

os.system(cmd)

