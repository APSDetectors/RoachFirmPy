pywindow=
"""

#sig=roach2.singleFreqLUT(1e6,'I',400e6,4096,0.0,20000)
#data = roach2.convertToBinary128(sig,sig)

print "START"

sig2 = ord('a') +numpy.array( range(32)*64)
sig = sig2*256
sig = sig + sig2


sig[:32]

len(sig)

data =  roach2.convertToBinary128_2(sig,7)
len(data)

data[:64]

roach2.writeDram('DRAM_LUT',data)

roach2.streamDram('DRAM_LUT')

print "DONE"


"""


rebof=
"""
/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbddr_2015_Apr_08_1150.bof
"""
