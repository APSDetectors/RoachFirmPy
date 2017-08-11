
"""



Roach linux: 192.168.0.203
Roach box       ...70
Anritsu         ...68
FASPAX      ...41 


use rootsh to run
nm-connection-editor

This will allow set up of net int3erface cards.
eth4 is 164 network
eth5 should be 192.168.0.203, 255.255.255.0, 0.0.0.0 this is 1GB to roach box local net
eth0 is the 10GB enet you use. set to 192.168.1.102 


docs at
https://github.com/ska-sa/katcp_devel/tree/master/tcpborphserver3

see bottom of page for more docs


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

from mpl_toolkits.mplot3d import Axes3D


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

        pass


    else:
        print "CALLBACK- no trigger"

    roach2.callback_counter= roach2.callback_counter+1


    

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
	    os.system('mkfifo /localc/roachkatcpfifoOut')
	    os.system('mkfifo /localc/roachkatcpfifoIn')
	    
	    os.system('sleep 9999999 > /localc/roachkatcpfifoIn &')
	    os.system('sleep 9999999 > /localc/roachkatcpfifoIn &')
	except:
	    pass
	    
    
    	os.system('nc %s %d > /localc/roachkatcpfifoIn < /localc/roachkatcpfifoOut &'%(self.ip,self.port))
	
	
	
	self.In_pipe = open('/localc/roachkatcpfifoIn','r');
	self.Out_pipe = open('/localc/roachkatcpfifoOut','w');
	
	
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


    def readAllReg(self,is_print=True):

        reglist = self.listReg()
        regvals=[]

        for reg in reglist:
           val = self.read_int(reg)
           regvals.append( (reg,val) )
           if is_print: print '%s  = 0x%x'%(reg,val)

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
	
	
    def bit(self,num,val):
    #only for zynq chip, not roach.
        self.Out_pipe.write("?bit %d %d\n"%(num,val));
	self.Out_pipe.flush()
	line=self.In_pipe.readline()
	line=self.In_pipe.readline()
	
	
    def write_int(self,regname, data,offset=0):
    
    	
        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return

    	self.Out_pipe.write("?wordwrite %s %d 0x%x\n"%(regname,offset,data));
	self.Out_pipe.flush()
	line=self.In_pipe.readline()
        #print 'write_int %s %x'%(regname, data)
	#print line
	
	
    def read_int(self,regname,offset=0):
    	
        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return(0)

	self.Out_pipe.write("?wordread %s %d\n"%(regname,offset));
	self.Out_pipe.flush()
	
	line=self.In_pipe.readline()
	
	vals=line.split()[2]
	val=int(vals,16)
        #print 'read_int %s %x'%(regname, val)
	return(val)
	
	


    def write(self,regname,data,offset=0):
        #data is binary string, shoudl line up as ints

        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return

        data2=self.insertEsc(data)
        self.Out_pipe.write( '?write %s %d %s\n'%(regname,offset,data2))


        self.Out_pipe.flush()


        line=self.In_pipe.readline()

        while '!write' not in line:
            print line
            line=self.In_pipe.readline()

        #print line




    def big_write(self,regname,data):
        #data is binary string, shoudl line up as ints

	bsize=1024

	nblocks=len(data)/bsize
	
	
	
	offs = 0
	
	for k in range(nblocks):
	    self.write(regname,data[offs:(offs+bsize)],offs)
	    offs = offs + bsize
	    
	partialb=mod(len(data),bsize)
	if partialb>0:
    	    self.write(regname,data[offs:(offs+partialb)],offs)
	
	

    def read(self,regname,count,offset = 0):


        if regname not in self.reglist:
            print "Unknown register %s"%regname
            return('\n')

        self.Out_pipe.write( '?read %s %d %d\n'%(regname,offset,count))


        self.Out_pipe.flush()



        line=self.In_pipe.readline()

        #print line[:9]
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
	
	
"""
This is tcpborphserver, version 3. A server designed to control
roach2s. It speaks katcp over port 7147. You should be able to
connect to a roach2 and type ?help to see the list of commands. 

tcpborphserver links in the mainloop of the katcp library which
can and does implement commands which are not directly relevant 
to users who simply wish to interact with the fpga. In addition
tcpborphserver itself may contain commands which are still under
development, and not guaranteed to be retained. 

The following commands are implemented by tcpborphserver3:

  ?listbof

    Lists gateware image files stored on the roach

  ?delbof filename

    Removes a gateware image file 

  ?progdev filename

    Programs a gateware image already stored on the roach in
    the image directory (paths not permitted)

  ?upload port

    Upload and program a local gateware image file to the roach. Send 
    the local image to the tcp port on the roach, as specified. No
    escaping of the image file required as it has its own stream, 
    which should be closed when upload has completed. Still a bit 
    experimental and subject to revision (there was an uploadbof command 
    which was different). 

    Example

      ?upload 3000
      !upload ok 3000

    Then from a local terminal type

      nc -w 2 -q 2 192.168.40.57 3000 < some-image.bof

    Which will give you 

      #fpga loaded
      #fpga ready

  ?fpgastatus

    Checks if the fpga is programmed. Will return fail in case the
    fpga is not programmed. In earlier versions this command was 
    called ?status

  ?listdev [size]
    
    Lists the register names provided by the currently programmed
    gateware image. The optional "size" keyword will include a size
    field in the output

  ?register name position bit-offset length

    Assign a name to an fpga memory location explicitly, instead
    of having it set in the bof (gateware image) file. Experimental

  ?wordwrite register word-offset word

    Writes a 32bit word to the given register at the word-offset. The
    word should be given as a hexadecimal value. Example

    ?wordwrite sys_scratchpad 0 0x74657374

  ?wordread register word-offset [word-count]

    Reads a 32bit word from the given offset in the named register. 
    The word offset is counted in words, not bytes. The value returned
    is given in hexadecimal. Example

    ?wordread sys_scratchpad 0 
    !wordread ok 0x74657374

  ?read register byte-offset count

    Reads data from the given register. Reads start at the specified
    byte-offset and attempt to read count bytes. Data is returned
    in binary form (with escapes as per katcp specification). Not
    all offsets and sizes are supported, as there are alignment 
    alignment constraints. Example

    ?read sys_scratchpad 0 4
    !read ok test

  ?write register byte-offset data

    Write the given binary data to the position byte-offset to the
    named register, subject to alignment constraints

  ?chassis-led led-name state

    Allows you to toggle an LED on the roach chassis. Example

    ?chassis-led red on

    Currently the only useful led name is "red" (there is a "green"
    too, but it gets toggled automatically). chassis-start is not
    needed during normal operation as it should happen automatically

  ?tap-info

    displays some freeform information about running tap instances

  ?tap-stop register-name

    Stop a running tap instance

  ?tap-start tap-device register-name ip-address [port [mac]]

    Start a tap instance with name tap-device, which opens an fpga
    register at register-name to loop traffic to the kernel. The kernel
    interface is given ip-address (netmask fixed to 255.255.255.0). Port
    is a udp port on which gateware collects data

The following commands are part of the katcp library, and with the exception
of log-record and system-info also part of the katcp specification

  ?client-list

    Lists current connections to the server

  ?version-list
    
    Display some version information

  ?sensor-list 

    Display available sensors

  ?sensor-value sensor

    Retrieve a sensor value (rather use sensor-sampling if you 
    wish to see periodic data)

  ?sensor-sampling sensor strategy parameter
   
    Example

    ?sensor-sampling raw.temp.fpga event
  
  ?watchdog

    No-op, used as a ping

  ?log-level
   
    Sets the log level 

    Example to enable lots of debug messages

    ?log-level trace

  ?help

    List available, nonhidden commands

  ?restart
   
    Reboot the roach

  ?halt 

    Turn off the roach

  ?log-record [priority] message

    Write a log message, goes to all client connections 

  ?system-info

    Prints some unstructed information about the system. 
    Mostly useful to debug server internals

"""
