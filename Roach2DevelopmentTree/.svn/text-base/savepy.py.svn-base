execfile('/home/oxygen26/TMADDEN/ROACH2/projcts/QT/testDDR/debug.py')
#####################

roach2.wr_toggle = 1
roach2.rd_toggle = 1
roach2.write_int('DRAM_LUT_LUTSize',8 * 2)

roach2.streamDram('DRAM_LUT')

###################################

roach2.dram_test_nbuffers=1
roach2.dbgflags=[]

roach2.wr_toggle = 1;
roach2.rd_toggle = 1;

roach2.dramTestData('DRAM_LUT')

#roach2.wr_toggle = 1
#roach2.rd_toggle = 1
#roach2.write_int('DRAM_LUT_LUTSize',\
#roach2.dram_test_nbuffers*128 * 8 )

roach2.streamDram('DRAM_LUT')

####################

addr = 8 * 0
roach2.write_int('DRAM_LUT_offsAddr',addr)
stdac=2
load=0

ctrl = (1<<load) + (1<<stdac)
roach2.write_int('DRAM_LUT_control',ctrl)
##################


aaa
##############################################
roach2.dram_test_nbuffers=8
roach2.dbgflags=[]

roach2.wr_toggle = 1;
roach2.rd_toggle = 1;

roach2.dramTestData('DRAM_LUT')

roach2.wr_toggle = 1;
roach2.rd_toggle = 1;
roach2.write_int('DRAM_LUT_LUTSize',\
roach2.dram_test_nbuffers*128 * 8 )

roach2.streamDram('DRAM_LUT')


##################################3



roach2.dram_test_nbuffers=2
roach2.dbgflags=[]

roach2.dramTestData('DRAM_LUT')
roach2.streamDram('DRAM_LUT'


#########


roach2.dbgflags=['dbg_kat_callback']
#roach2.dbgflags=[]
roach2.dram_test_nbuffers=2
roach2.when_callback=[1]
roach2.callback_counter = 0

roach2.dramTestData('DRAM_LUT')

#roach2.streamDram('DRAM_LUT')

######


print "START"
#sig3=list('BADCFEHGJILKNMPO')
sig3=list('ABCDEFGHIJKLMNOP')
#sig3=list('PCBEDGFIHKJMLONA')

sig2=[]
for ss in sig3:
    ss=ord(ss)
    sig2.append(ss)

sig2=array(sig2*16)

sig = sig2*256
sig = sig + sig2

data =  roach2.convertToBinary128_2(sig,7)

roach2.wr_toggle = 1
roach2.rd_toggle = 1

roach2.writeDram('DRAM_LUT',data)

roach2.wr_toggle = 1
roach2.rd_toggle = 0

roach2.streamDram('DRAM_LUT')

print "DONE"

bin(28)

roach2.read('DRAM_LUT_drambuff128_0',128*16)[:128]

roach2.read('DRAM_LUT_drambuff128_1',128*16)[:128]





######################################################





'15:9;8:8;7:7;6:6;5:5;4:4;3:3;2:2;1:1;0:0'

'16:16;15:15;14:7;6:6;5:5;4:4;3:3;2:2;1:1;0:0'
'1:1;2:2;3:3;4:4;5:5;13:6;14:14;15:15'
'0:0;1:1;2:2;3:3;4:4;5:5;13:6;14:14;15:15'

sig='qwertyuiopasdfghjklzxcvbnm'*32

roach2.write('capture_rcvdata',sig)

sig='QWERTYUIOPASDFGHJKLZXCVBNM'*32
roach2.write('DRAM_LUT_drambuff128',sig)


#########################################

print "START"
sig3=list('ABCDEFGHIJKLMNOP')
sig2=[]
for ss in sig3:
    ss=ord(ss)
    sig2.append(ss)

sig2=array(sig2*16)

sig = sig2*256
sig = sig + sig2

data =  roach2.convertToBinary128_2(sig,7)
roach2.writeDram('DRAM_LUT',data)

#roach2.streamDram('DRAM_LUT')
print "DONE"



######################################################3




a=roach2.read('DRAM_LUT_drambuff128_1',256)
a







































sig='qwertyuiopasdfghjklzxcvbnm'*32

roach2.write('capture_rcvdata',sig)

sig='QWERTYUIOPASDFGHJKLZXCVBNM'*32
roach2.write('DRAM_LUT_drambuff128',sig)


print "START"

#sig2 = ord('A') +numpy.array( range(26)*64)
sig3=list('Tim Madden is cool')
sig2=[]
for ss in sig3: 
    ss=ord(ss)
    sig2.append(ss)

sig2=array(sig2*32)

sig = sig2*256
sig = sig + sig2

sig=[ord('T')] *32768

sig[:32]

len(sig)


data =  roach2.convertToBinary128_2(sig,7)

data[:64]

datax='ABCDEFGHIJKLMNOP'*(2048)

roach2.writeDram('DRAM_LUT',datax)

roach2.streamDram('DRAM_LUT')

print "DONE"




