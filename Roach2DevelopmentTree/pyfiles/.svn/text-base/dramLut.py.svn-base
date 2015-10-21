


class dramLut:

    def __init__(self,rch_,fwn_):
	self.fwname = fwn_

	self.roach = rch_

        self.wr_toggle = 0;
        self.rd_toggle = 0;

    

        self.dram_test_nbuffers=1






    def singleFreqLUT(self,f, iq, sampleRate, size, phase, amplitude):
	""" Returns data points for the DAC look-up table.

	    @param f       List of desired freqs, e.g., 12.34e6 if resolution = 1e4.
	    @param sampleRate       Sample rate of DAC.
	    @param resolution       Example: 1e4 for resolution of 10 kHz.
	    @param phase            Constant phase offset between -pi and pi.
	    """



	#data = []



	phaserad=numpy.pi * phase / 180.0;
	phaseterm= phaserad + 2*math.pi*(f/sampleRate)*numpy.arange(size)


	#make test pulse.it is inserted in random part of the waveform.
	#calc where pulse will be in the wave




	if iq == 'I':
	    data=numpy.round(amplitude * numpy.cos(phaseterm))
	        #data.append(int(amplitude*math.sin(2*math.pi*f*t)))
	else:
	    sign = 1.0;


	    data=numpy.round(sign*amplitude * numpy.sin(phaseterm))


	return data




    def convertToBinary128_2(self,data1,channel):
	""" Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

	    @param data             Decimal data to be converted  for FPGA.
	    """
	binaryData = ''
	for i in range(0, len(data1)):
	    if channel==0:
	        x = struct.pack('>hhhhhhhh',
	            data1[i],
	            0,
	            0,
	            0,
	            0,
	            0,
	            0,
	            0)

	    elif channel==1:
	        x = struct.pack('>hhhhhhhh',
	            0,
	            data1[i],
	            0,
	            0,
	            0,
	            0,
	            0,
	            0)

	    elif channel==2:
	        x = struct.pack('>hhhhhhhh',
	            0,
	            0,
	            data1[i],
	            0,
	            0,
	            0,
	            0,
	            0)

	    elif channel==3:
	        x = struct.pack('>hhhhhhhh',
	            0,
	            0,
	            0,
	            data1[i],
	            0,
	            0,
	            0,
	            0)


	    elif channel==4:
	        x = struct.pack('>hhhhhhhh',
	            0,
	            0,
	            0,
	            0,
	            data1[i],
	            0,
	            0,
	            0)

	    elif channel==5:
	        x = struct.pack('>hhhhhhhh',
	            0,
	            0,
	            0,
	            0,
	            0,
	            data1[i],
	            0,
	            0)

	    elif channel==6:
	        x = struct.pack('>hhhhhhhh',
	            0,
	            0,
	            0,
	            0,
	            0,
	            0,
	            data1[i],
	            0)

	    elif channel==7:
	        x = struct.pack('>hhhhhhhh',
	            0,
	            0,
	            0,
	            0,
	            0,
	            0,
	            0,
	            data1[i])



	    binaryData = binaryData + x

	return binaryData


    def convert128To256(self,datastr128):


	lenbytes = len(datastr128);
	lenword128 = lenbytes / 16;
	lenword256 = lenword128/2;


	stra=''
	strb=''

	cnt_128 = 0

	for cnt_256 in range(lenword256):
	    stra = stra + datastr128[cnt_128:(cnt_128+16)]
	    cnt_128 = cnt_128 + 16
	    strb = strb + datastr128[cnt_128:(cnt_128+16)]
	    cnt_128 = cnt_128 + 16

	return((stra,strb))




    def convertToBinary128(self,data1, data2):
	""" Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

	    @param data             Decimal data to be converted  for FPGA.
	    """
	binaryData = ''
	for i in range(0, len(data1)/4):
	    x = struct.pack('>hhhhhhhh', 
		data1[4*i+3], 
		data1[4*i+2], 
		data1[4*i+1], 
		data1[4*i+0],
		data2[4*i+3], 
		data2[4*i+2], 
		data2[4*i+1], 
		data2[4*i+0])

	    binaryData = binaryData + x

	return binaryData


    def convertFrom128(self,bindata):


	nlongs = len(bindata)/16;

	data0=[]
	data1=[]
	data2=[]
	data3=[]

	data4=[]
	data5=[]
	data6=[]
	data7=[]

	for ptr in range(nlongs):
	    longone = bindata[ (ptr*16):(ptr*16+16) ]
	    shorts = struct.unpack('>hhhhhhhh',longone)	

	    data0.append(shorts[0])
	    data1.append(shorts[1])
	    data2.append(shorts[2])
	    data3.append(shorts[3])

	    data4.append(shorts[4])
	    data5.append(shorts[5])
	    data6.append(shorts[6])
	    data7.append(shorts[7])

	return( (data0, data1, data2, data3, data4, data5, data6, data7 )  )

    def convertToBinary128_3(self,
		data0,data1,data2,data3,
		data4,data5,data6,data7):

	""" Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

	    @param data             Decimal data to be converted  for FPGA.
	    """
	binaryData = ''
	for i in range(0, len(data0)):
	    x = struct.pack('>hhhhhhhh', 
		data0[i], 
		data1[i], 
		data2[i], 
		data3[i],
		data4[i], 
		data5[i], 
		data6[i], 
		data7[i])

	    binaryData = binaryData + x

	return binaryData



    def streamDram(self):
	control_reg='%s_control'%self.fwname
	lutsize_reg = '%s_LUTSize'%self.fwname
	offs_addr_reg = '%s_offsAddr'%self.fwname
	buffmem = '%s_drambuff128'%self.fwname

	startdac_bit = 2
	sync_bit =3
	load_addr_bit = 0
	write_bit = 1
	rst_dram_bit = 4
	ctrl = 0;

	ctrl = (self.rd_toggle<<5) + (self.wr_toggle<<7);
	self.roach.write_int(control_reg, ctrl)

	ctrl = ctrl + (1<<sync_bit);

	self.roach.write_int(control_reg, ctrl)

	ctrl = ctrl - (1<<sync_bit);
	self.roach.write_int(control_reg, ctrl)

	ctrl = ctrl + (1<<startdac_bit);

	self.roach.write_int(control_reg, ctrl)


    def dumpBrams(self,lenx):


	buffmem0 = '%s_drambuff128_0'%self.fwname
	buffmem1 = '%s_drambuff128_1'%self.fwname

	a=self.roach.read(buffmem0,lenx);
	b = self.roach.read(buffmem1,lenx);
	return( (a,b) )


    #bindata is bin string, mult of 128 bits long.

    def writeDram(self,bindata_ab):


	(bindata , bindata_b) = self.convert128To256(bindata_ab)

	control_reg='%s_control'%self.fwname
	lutsize_reg = '%s_LUTSize'%self.fwname
	offs_addr_reg = '%s_offsAddr'%self.fwname
	bramsize_reg = '%s_bramsize'%self.fwname
	buffmem0 = '%s_drambuff128_0'%self.fwname
	buffmem1 = '%s_drambuff128_1'%self.fwname

	startdac_bit = 2
	sync_bit =3

	write_bit = 1
	rst_dram_bit = 4


	datalen=len(bindata)
	datalen_word=datalen/16

	print 'nbytes %d lutsizewords %d'%(datalen, datalen_word)

	#
	#set bram size
	#
	self.roach.write_int(bramsize_reg, 127);

	#
	#set address speeds of bram and dram
	#
	control = (self.rd_toggle<<7) + (self.wr_toggle<<5);

	self.roach.write_int(control_reg, control);

	#
	#pulse sync in bit
	#
	control = control + (1<<sync_bit)
	self.roach.write_int(control_reg, control)

	control = control - (1<<sync_bit)
	self.roach.write_int(control_reg, control);



	offaddr = 0
	dataptr = 0

	#address size iof te buff bram. it is 128 addresses, at 288 bits, or 16 bytes per address
	buffsize_word = 128
	#the dram addr incs by 8 for each 128bit word (or 144 bit word)
	addrinc = buffsize_word*8
	#bufsize in bytes
	buffsize = buffsize_word*16

	#lut size must be datalen_word, or the number of 288 size workds in mem.
	# the 8 is because the dram addr must inc by 8, as lower 3 bits are not used.
	#we add fudge factor because we want the mem to count farther when we are wrting it
	#or else the state machine may overwrite the 1st word... fudge of 16 words
	fudge = 8*16;
	lutsize = 8*datalen_word + fudge
	self.roach.write_int(lutsize_reg, lutsize);
	while dataptr<datalen:
	    #
	    #set control to all bits 0 except the rd and wer toggles.
	    #
	    control = (self.rd_toggle<<7) + (self.wr_toggle<<5);
	    self.roach.write_int(control_reg, control)
	    #
	    #pulse sync in bit
	    #
	    control = control + (1<<sync_bit)
	    self.roach.write_int(control_reg, control)

	    control = control - (1<<sync_bit)
	    self.roach.write_int(control_reg, control);

	    #get 128 * 16 bytes of data for on bram size of data.
	    datawr=bindata[(dataptr):(dataptr+buffsize)]
	    datawr_b=bindata_b[(dataptr):(dataptr+buffsize)]


	    #
	    # write dram start addr for this bloc and load the address
	    #

	    self.roach.write_int(offs_addr_reg, offaddr);



	    #
	    # write data to brams
	    #
	    self.roach.write(buffmem0,datawr);
	    self.roach.write(buffmem1,datawr_b)
	    print "write %d bytes: %s"%(len(datawr),datawr[:64])

	    #
	    #pulse dram/bram in write to dram mode
	    #
	    control =control + (1<<write_bit)
	    self.roach.write_int(control_reg, control);

	    control =control - (1<<write_bit)
	    self.roach.write_int(control_reg, control);



	    #wait for dram to write
	    time.sleep(0.01)



	    #
	    #inc mem ptrs to get next block of data, and next block address in dram
	    #

	    #inc ptr into the raw data to send to next bram size block
	    dataptr= dataptr + buffsize
	    #inc the dram mem
	    offaddr = offaddr + addrinc

	


	#lut size must be datalen_word, or the number of 288 size workds in mem.
	# the 8 is because the dram addr must inc by 8, as lower 3 bits are not used.
	# we sub 8 because instead of 256*8 we want 255*8. ordinal numbers..
	lutsize = 8*datalen_word-8
	self.roach.write_int(lutsize_reg, lutsize);




    def dramTestData(self,chan=7):



	sig3=list('ABCDEFGHIJKLMNOP')

	#convert the chars to ascii values in the list
	sig2=[]
	for ss in sig3:
	    ss=ord(ss)
	    sig2.append(ss)

	#make it longer, 16*len(sig3) will be 256 items, or 128 256 bit workds
	sig2=numpy.array(sig2*16*self.dram_test_nbuffers)

	#make AA,BB,CC etc. into a 16 bit workd
	sig = sig2*256
	sig = sig + sig2

	data =  self.convertToBinary128_2(sig,chan)
	self.writeDram(data)


    def dramTestData2(self):



    	bindata = self.convertToBinary128_3(\
		numpy.arange(128),
		128+numpy.arange(128),
		2*128+numpy.arange(128),
		3*128+numpy.arange(128),
		4*128+numpy.arange(128),
		5*128+numpy.arange(128),
		6*128+numpy.arange(128),
		7*128+numpy.arange(128))

	self.testdata = bindata

	self.writeDram(bindata)



    def reverseBits(self,data):
	data2=[]
	for d in data:
	    d2 = int(bin(d)[:1:-1], 2)
	    data2.append(d2)
	return(data2)

