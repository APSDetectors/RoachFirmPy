
"""

execfile("katcpNc.py")


roach2=katcpNc()



roach2.startNc()


roach2.fpgaStatus()


roach2.closeFiles()


roach2.help()


#roach2.sendBof("/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbtest_2015_Mar_30_1419.bof")

roach2.sendBof("/home/oxygen26/TMADDEN/ROACH2/projcts/bestBitFiles/tengbtest_2015_Mar_31_1055.bof")


roach2.listReg()


roach2.In_pipe.readline()


roach2.Out_pipe.write("?status\n")
roach2.Out_pipe.flush()


	
roach2.infoEth()


aa=roach2.read('capture_rcvdata',32)


roach2.stopEth('xmit0')




roach2.stopEth('rcv0')


    
roach2.setupEth('xmit0','192.168.1.0',100,'02:02:00:00:00:01')



roach2.setupEth('rcv0','192.168.1.2',54321,'02:02:00:00:00:02')


data = struct.pack('32B',*[0]*32)

data = struct.pack('32B',*range(32))

regname = 'capture_rcvdata'

data=struct.pack('BBBBBBBBBB',23,11,230,143,54,78,99,127,201,56)

ll=36
roach2.write(regname,struct.pack('%dB'%ll,*range(ll)))

roach2.read(regname,ll)


data2= insertEsc(data)

roach2.Out_pipe.write( '?write %s 0 %s\n'%(regname,data2))
roach2.Out_pipe.flush()
roach2.In_pipe.readline()

roach2.Out_pipe.write( '?read %s 0 %d\n'%(regname,count))
roach2.Out_pipe.flush()
aa=roach2.In_pipe.readline()


regname = 'capture_rcvdata'


aa=testwr2(8192)

aa=testwr(256)


"""

import sys, os, random, math, array, fractions


import time, struct, numpy



def testwr(lx):

    for char in range(256):
        #print '------------'
        data = struct.pack('%dB'%lx,*[char]*lx)
        #print data
        roach2.write(regname,data)
        data2=roach2.read(regname,lx)
        #print data2

        if data2==data:
            print "PASS"
        else:
            print "FAIL"
            print "%s"%data
            print "%s"%data2
            print char
            return((data,data2))



def testwr2(lx):

    data=numpy.arange(lx)
    data = data%256
    data = data.tolist()

    data = struct.pack('%dB'%lx,*data)
    roach2.write(regname,data)
    data2=roach2.read(regname,lx)

    if data==data2: print "PASS"
    else: print "FAIL"

    return((data,data2))



def katCallBack():

    if roach2.callback_counter in roach2.when_callback:

        trigScope(-1,-1)


    else:
        print "CALLBACK- no trigger"

    roach2.callback_counter= roach2.callback_counter+1


#trigin from 0,1,2,3 to trig on those inputs.
#trig in -1 to ignore trig.
#inpt is 0,1,2,3,4,5,6,7
def trigScope(trigin=-1, inpt=0):
    
    if trigin ==-1:
        ig_tr = 1
	trigin = 0
    else:
        ig_tr = 0
	
   
    we_in = 0
    inputsel = inpt + trigin*16  + we_in*64;
    roach2.write_int("roachscope_inputsel",inputsel);

    print "Trigger roachscope"
    #clear trace
    roach2.write('roachscope_snapshot_bram','\0'*4096)
  
    ig_we = 1
  
    ctrl = ig_we*4 + ig_tr*2;

    roach2.write_int('roachscope_snapshot_ctrl',ctrl)


    stat = roach2.read_int('roachscope_snapshot_status')
    print 'stat = %x'%stat

    ctrl+=1;
    roach2.write_int('roachscope_snapshot_ctrl',ctrl)
    time.sleep(0.01)

    stat = roach2.read_int('roachscope_snapshot_status')
    print 'stat = %x'%stat
    print "END Trigger Roachscope"


def plotScope(pllen = 2048,is_usebits = False, bits = '15:11;10:10;9:9;8:8',isprint = False):
    binstr = roach2.read('roachscope_snapshot_bram',4096)
    shorts = struct.unpack('>2048h',binstr)
    figure(1)
    clf()

    if isprint:
        print binstr
        print len(binstr)
	
    if is_usebits==False:
	plot(shorts[:pllen])

    else:
        bitwidths=bits.split(';')
	stbit = 15
	smax = 0
	graphnum = 0.0
	for k in range(len(bitwidths)):
	    couple = bitwidths[k].split(':')
	    stbit=int(couple[0])
	    edbit=int(couple[1])
	    print '%d %d'%(stbit,edbit)
	    width = 1 + stbit - edbit
	    y=numpy.array([0.0]*pllen)
	    if width>0:
	        mask = (1<<width) - 1
		
		for i in range(pllen):
		    sval = shorts[i]
		   
		    
		    datash = sval>>edbit
		    datash = datash & mask
		    datash = double(datash)
		    
		    factor = double((1<<width));
		    
		    if len(bitwidths)<2:
		        factor = 1.0
			
		    y[i] = (2.0*graphnum) + (datash/factor)
		    
	  	plot(y)
		graphnum = graphnum+1.0
		stbit = stbit - width
    
    

class katcpNc:

    def __init__(self,ipaddr='192.168.0.70',prt=7147):
    
    
	
    	self.ip=ipaddr
	self.port = prt
	
	
	self.Out_pipe=0
	self.In_pipe=0
	
        self.reglist = []

        self.wr_toggle = 0;
        self.rd_toggle = 0;

        # 'dbg_dramwr_wait'
        # "dbg_kat_callback'
        self.dbgflags=[]

        self.dram_test_nbuffers=1

        self.when_callback=range(10000)
        self.callback_counter = 0

    def removeEsc(self,instr):
        outstr = instr
        outstr=outstr.replace('\\\\','\\')
        outstr=outstr.replace('\\0','\0')
        outstr=outstr.replace('\_',' ')
        outstr=outstr.replace('\\t','\t')
        outstr=outstr.replace('\\n','\n')
        outstr=outstr.replace('\\r','\r')
        outstr=outstr.replace('\\#','#')
        outstr=outstr.replace('\\e','\x1b')


        return(outstr)


    def insertEsc(self,instr):
        outstr = instr
        outstr=outstr.replace('\\','\\\\')
        outstr=outstr.replace('\0','\\0')
        outstr=outstr.replace(' ','\_')
        outstr=outstr.replace('\n','\\n')
        outstr=outstr.replace('\r','\\r')
        outstr=outstr.replace('#','\\#')
        outstr=outstr.replace('\t','\\t')
        outstr=outstr.replace('\x1b','\\e')
        return(outstr)



	
    def startNc(self):
    
    	try:
	    os.system('mkfifo /local/roachkatcpfifoOut')
	    os.system('mkfifo /local/roachkatcpfifoIn')
	    
	    os.system('sleep 9999999 > /local/roachkatcpfifoIn &')
	    os.system('sleep 9999999 > /local/roachkatcpfifoIn &')
	except:
	    pass
	    
    
    	os.system('nc %s %d > /local/roachkatcpfifoIn < /local/roachkatcpfifoOut &'%(self.ip,self.port))
	
	
	
	self.In_pipe = open('/local/roachkatcpfifoIn','r');
	self.Out_pipe = open('/local/roachkatcpfifoOut','w');
	
	
	print self.In_pipe.readline()
	print self.In_pipe.readline()
	
	
    def fpgaStatus(self):
    
    
        self.Out_pipe.write("?status\n")
	self.Out_pipe.flush()
	
	line1=self.In_pipe.readline()
	line2=self.In_pipe.readline()
	line3=self.In_pipe.readline()
	
	
	
	if "fail" in line3:
	    return(False)

	
	if "pass" in line3:
	    return(False)
	    
	print "Problem with Roach"
	
	print line1
	print line2
	print line3
	    
	    
 	return(False)
	
	
	
    def closeFiles(self):
        
	self.In_pipe.close()
	self.In_pipe=0
	self.Out_pipe.close()
	self.Out_pipe=0
	
	os.system('pkill -f "sleep 9999999" ')
	
	os.system('pkill -f "nc 192.168.0" ')
	
	


    def restart(self):



        self.Out_pipe.write("?restart\n")
        self.Out_pipe.flush()

        line=self.In_pipe.readline()

        while "!" not in line:
            print line
            line=self.In_pipe.readline()

        print line




    def shutdown(self):



        self.Out_pipe.write("?halt\n")
        self.Out_pipe.flush()

        line=self.In_pipe.readline()

        while "!" not in line:
            print line
            line=self.In_pipe.readline()

        print line





	
	
    def help(self):
    
     
	
        self.Out_pipe.write("?help\n")
	self.Out_pipe.flush()
	
	line=self.In_pipe.readline()
	
	while "!help" not in line:
	    print line
	    line=self.In_pipe.readline()
	    
	print line
	
	
	
	
	
    def listReg(self):
    
	
	self.Out_pipe.write("?listdev\n");
	self.Out_pipe.flush()
	
        reglist=[]

	line=self.In_pipe.readline()
	
	while "!listdev" not in line:
	    print line
            if '#listdev' in line:
                reglist.append(line[9:-1])
            line=self.In_pipe.readline()
	    
	print line
	
        self.reglist = reglist
        return(reglist)


    def readAllReg(self):

        reglist = self.listReg()
        regvals=[]

        for reg in reglist:
           val = self.read_int(reg)
           regvals.append( (reg,val) )
           print '%s  = 0x%x'%(reg,val)

        return(regvals)


    def sendBof(self,filename):
    
    
    	self.Out_pipe.write("?upload 3000\n");
	self.Out_pipe.flush()
	
	line=self.In_pipe.readline()
	print line
	line=self.In_pipe.readline()
	print line

	if "!upload ok" not in line:
	    print "Problem w/ upload"
	    return(False);
	    
	os.system('nc -w 2 %s 3000 < %s '%(self.ip, filename))    
	
	print self.In_pipe.readline()
	print self.In_pipe.readline()

	
        self.listReg()
	
    def write_int(self,regname, data):
    
    	
        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return

    	self.Out_pipe.write("?wordwrite %s 0 0x%x\n"%(regname,data));
	self.Out_pipe.flush()
	line=self.In_pipe.readline()
        print 'write_int %s %x'%(regname, data)
	print line
	
	
    def read_int(self,regname):
    	
        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return(0)

	self.Out_pipe.write("?wordread %s 0\n"%(regname));
	self.Out_pipe.flush()
	
	line=self.In_pipe.readline()
	
	vals=line.split()[2]
	val=int(vals,16)
        print 'read_int %s %x'%(regname, val)
	return(val)
	
	


    def write(self,regname,data):
        #data is binary string, shoudl line up as ints

        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return

        data2=self.insertEsc(data)
        self.Out_pipe.write( '?write %s 0 %s\n'%(regname,data2))


        self.Out_pipe.flush()


        line=self.In_pipe.readline()

        while '!write' not in line:
            print line
            line=self.In_pipe.readline()

        print line



    def read(self,regname,count):


        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return('\n')

        self.Out_pipe.write( '?read %s 0 %d\n'%(regname,count))


        self.Out_pipe.flush()



        line=self.In_pipe.readline()

        print line[:9]
        data = self.removeEsc(line)[9:-1]

        return(data)

	
    def infoEth(self):
    
    	self.Out_pipe.write( '?tap-info\n')
	
		
	self.Out_pipe.flush()
	

	line=self.In_pipe.readline()
	
	while "!" not in line:
	    print line
	    line=self.In_pipe.readline()
	    
	print line
    	
	
    def stopEth(self,device):
    
    	self.Out_pipe.write('?tap-stop %s\n'%(device + '_dev'))

	self.Out_pipe.flush()
	

	line=self.In_pipe.readline()
	
	while "!" not in line:
	    print line
	    line=self.In_pipe.readline()
	    
	print line
	

    def singleFreqLUT(self,f, iq, sampleRate, size, phase, amplitude):
        """ Returns data points for the DAC look-up table.

            @param f                List of desired freqs, e.g., 12.34e6 if resolution = 1e4.
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
            x = struct.pack('>hhhhhhhh', data1[4*i+3], data1[4*i+2], data1[4*i+1], data1[4*i+0],data2[4*i+3], data2[4*i+2], data2[4*i+1], data2[4*i+0])
            binaryData = binaryData + x

        return binaryData


    def streamDram(self,dramname):
        control_reg='%s_control'%dramname
        lutsize_reg = '%s_LUTSize'%dramname
        offs_addr_reg = '%s_offsAddr'%dramname
        buffmem = '%s_drambuff128'%dramname

        startdac_bit = 2
        sync_bit =3
        load_addr_bit = 0
        write_bit = 1
        rst_dram_bit = 4
        ctrl = 0;

        ctrl = (self.rd_toggle<<5) + (self.wr_toggle<<7);
        self.write_int(control_reg, ctrl)

        ctrl = ctrl + (1<<sync_bit);

        self.write_int(control_reg, ctrl)

        ctrl = ctrl - (1<<sync_bit);
        self.write_int(control_reg, ctrl)

        ctrl = ctrl + (1<<startdac_bit);

        self.write_int(control_reg, ctrl)


    #bindata is bin string, mult of 128 bits long.
    #dramname is prename...
    def writeDram_v0(self,dramname,bindata_ab):


        (bindata , bindata_b) = self.convert128To256(bindata_ab)

        control_reg='%s_control'%dramname
        lutsize_reg = '%s_LUTSize'%dramname
        offs_addr_reg = '%s_offsAddr'%dramname
        buffmem0 = '%s_drambuff128_0'%dramname
        buffmem1 = '%s_drambuff128_1'%dramname

        startdac_bit = 2
        sync_bit =3
        load_addr_bit = 0
        write_bit = 1
        rst_dram_bit = 4


        datalen=len(bindata)
        datalen_word=datalen/16

        print 'nbytes %d lutsizewords %d'%(datalen, datalen_word)
        #
        #set address speeds of bram and dram
        #
        control = (self.rd_toggle<<5) + (self.wr_toggle<<7);

        self.write_int(control_reg, control);

        #
        #pulse sync in bit
        #
        control = control + (1<<sync_bit)
        self.write_int(control_reg, control)

        control = control - (1<<sync_bit)
        self.write_int(control_reg, control);



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
        self.write_int(lutsize_reg, lutsize);
        while dataptr<datalen:
            #
            #set control to all bits 0 except the rd and wer toggles.
            #
            control = (self.rd_toggle<<7) + (self.wr_toggle<<5);
            self.write_int(control_reg, control)
            #
            #pulse sync in bit
            #
            control = control + (1<<sync_bit)
            self.write_int(control_reg, control)

            control = control - (1<<sync_bit)
            self.write_int(control_reg, control);

            #get 128 * 16 bytes of data for on bram size of data.
            datawr=bindata[(dataptr):(dataptr+buffsize)]
            datawr_b=bindata_b[(dataptr):(dataptr+buffsize)]


            #
            # write dram start addr for this bloc and load the address
            #

            self.write_int(offs_addr_reg, offaddr);

            control =  control  + (1<<load_addr_bit)
            self.write_int(control_reg, control);

            control = control  - (1<<load_addr_bit)
            self.write_int(control_reg, control);


            #
            # write data to brams
            #
            self.write(buffmem0,datawr);
            self.write(buffmem1,datawr_b)
            print "write %d bytes: %s"%(len(datawr),datawr[:64])

            #
            #put dram/bram in write to dram mode
            #
            control =control + (1<<write_bit)
            self.write_int(control_reg, control);


            #
            # start dac which will do the block write to dram
            #
            control = control + (1<<startdac_bit)
            self.write_int(control_reg, control);

            #wait for dram to write
            time.sleep(0.01)

            #
            # turn off start dac to stop sm.turn off write mode
            #
            control = control - ( (1<<startdac_bit)  +  (1<<write_bit)  )
            self.write_int(control_reg, control);

            #
            #inc mem ptrs to get next block of data, and next block address in dram
            #

            #inc ptr into the raw data to send to next bram size block
            dataptr= dataptr + buffsize
            #inc the dram mem
            offaddr = offaddr + addrinc

            if 'dbg_kat_callback' in self.dbgflags:
                print 'calling katCallBack'
                katCallBack()


        #lut size must be datalen_word, or the number of 288 size workds in mem.
        # the 8 is because the dram addr must inc by 8, as lower 3 bits are not used.
        # we sub 8 because instead of 256*8 we want 255*8. ordinal numbers..
        lutsize = 8*datalen_word-8
        self.write_int(lutsize_reg, lutsize);



    #bindata is bin string, mult of 128 bits long.
    #dramname is prename...
    def writeDram(self,dramname,bindata_ab):


        (bindata , bindata_b) = self.convert128To256(bindata_ab)

        control_reg='%s_control'%dramname
        lutsize_reg = '%s_LUTSize'%dramname
        offs_addr_reg = '%s_offsAddr'%dramname
        bramsize_reg = '%s_bramsize'%dramname
        buffmem0 = '%s_drambuff128_0'%dramname
        buffmem1 = '%s_drambuff128_1'%dramname

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
        self.write_int(bramsize_reg, 127);

        #
        #set address speeds of bram and dram
        #
        control = (self.rd_toggle<<7) + (self.wr_toggle<<5);

        self.write_int(control_reg, control);

        #
        #pulse sync in bit
        #
        control = control + (1<<sync_bit)
        self.write_int(control_reg, control)

        control = control - (1<<sync_bit)
        self.write_int(control_reg, control);



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
        self.write_int(lutsize_reg, lutsize);
        while dataptr<datalen:
            #
            #set control to all bits 0 except the rd and wer toggles.
            #
            control = (self.rd_toggle<<7) + (self.wr_toggle<<5);
            self.write_int(control_reg, control)
            #
            #pulse sync in bit
            #
            control = control + (1<<sync_bit)
            self.write_int(control_reg, control)

            control = control - (1<<sync_bit)
            self.write_int(control_reg, control);

            #get 128 * 16 bytes of data for on bram size of data.
            datawr=bindata[(dataptr):(dataptr+buffsize)]
            datawr_b=bindata_b[(dataptr):(dataptr+buffsize)]


            #
            # write dram start addr for this bloc and load the address
            #

            self.write_int(offs_addr_reg, offaddr);



            #
            # write data to brams
            #
            self.write(buffmem0,datawr);
            self.write(buffmem1,datawr_b)
            print "write %d bytes: %s"%(len(datawr),datawr[:64])

            #
            #pulse dram/bram in write to dram mode
            #
            control =control + (1<<write_bit)
            self.write_int(control_reg, control);

            control =control - (1<<write_bit)
            self.write_int(control_reg, control);



            #wait for dram to write
            time.sleep(0.01)



            #
            #inc mem ptrs to get next block of data, and next block address in dram
            #

            #inc ptr into the raw data to send to next bram size block
            dataptr= dataptr + buffsize
            #inc the dram mem
            offaddr = offaddr + addrinc

            if 'dbg_kat_callback' in self.dbgflags:
                print 'calling katCallBack'
                katCallBack()


        #lut size must be datalen_word, or the number of 288 size workds in mem.
        # the 8 is because the dram addr must inc by 8, as lower 3 bits are not used.
        # we sub 8 because instead of 256*8 we want 255*8. ordinal numbers..
        lutsize = 8*datalen_word-8
        self.write_int(lutsize_reg, lutsize);




    def dramTestData(self,dramname):



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

        data =  self.convertToBinary128_2(sig,7)
        self.writeDram(dramname,data)



    def reverseBits(self,data):
        data2=[]
        for d in data:
            d2 = int(bin(d)[:1:-1], 2)
            data2.append(d2)
        return(data2)
	
    def setupEth(self,device,ip,port,mac):
    
    
    	iptok=ip.split('.')
    	ipint = (int(iptok[0],10)<<24 ) + (int(iptok[1],10)<<16 ) + (int(iptok[2],10)<<8 ) + (int(iptok[3],10)) 
    	
	mactok=mac.split(':')
	
	macint = (int(mactok[0],16)<<40 ) 
	macint = macint + (int(mactok[1],16)<<32 ) 
	macint = macint + (int(mactok[2],16)<<24 ) 
	macint = macint + (int(mactok[3],16)<<16 ) 
	macint = macint + (int(mactok[4],16)<<8 ) 
	macint = macint + (int(mactok[5],16)) 
    
    	strg = '?tap-start %s %s %s %d %s\n'\
		%(device+'_dev',\
		device,\
		ip,\
		port,\
		mac)
    
        print strg
    	self.Out_pipe.write( strg);	
	
		
	self.Out_pipe.flush()
	

	line=self.In_pipe.readline()
	
	while "!" not in line:
	    print line
	    line=self.In_pipe.readline()
	    
	print line
	
	
