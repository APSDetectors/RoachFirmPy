
class matlabRoach:

	def __init__(self):
		#list of all registers. key is the register. val to key is a list
		#that will be turned into a matlab timeseries.
		# we can set how many samples the val is set into the reg list.		
		#used for write_int		
		self.reglist=dict()
		#ised for write(). list of memories
		self.memlist=dict()

		

		#we set a reg for 10samples at t time.
		self.numclocks=2

		#we count time as we write_int. so all rhe regs will be in correct time 
		#sequence. if we write reg1 and reg2, reg2 should have matlab timeseries
		#where it changes AFTER reg 1.
		#settin current time>0 means that we have all 0's in all regs before anything
		#happens, so nothing for this many clocks in sim.
		#only takes effect on write_int, as that is for writing registers.
		self.current_time = 2


		
	def write_int(self,regname,val):
		#where in time we write data		
		ctime = self.current_time
		#extend cur time to make room for new data
		self.current_time = 	self.current_time + self.numclocks
		if self.reglist.has_key(regname)==False:				
			mydata=[0] * self.current_time
			self.reglist[regname]=mydata
		
		self.extendRegSeq(regname)
		mydata=self.reglist[regname]
		for k in range(self.numclocks):
			mydata[ctime]= val
			ctime = ctime + 1
		
		self.makeEqualLenSeq()

	def write_int2(self,regname,val,whattime):
		self.current_time = whattime		
		self.write_int(regname,val)
		
		

	#
	# sghow last vals in regs
	#
	def lsregs(self):
		for reg in self.reglist.keys():
			print '%s %d'%(reg,self.reglist[reg][self.current_time-1])

	#
	# extend all the registers to be at same curret time.
	#

	def extendRegSeq(self,reg):
		
		rlen=len(self.reglist[reg])
		if rlen<self.current_time:
			dl = self.current_time - rlen
			last=self.reglist[reg][rlen-1]
			self.reglist[reg] = self.reglist[reg] + [last]*dl


	def makeEqualLenSeq(self):
		
		for reg in self.reglist.keys():
			self.extendRegSeq(reg)



	def write(self,regname,valarray,offset=0):
				
		if self.memlist.has_key(regname):
			mydata=self.memlist[regname]
			#print 'matlabRoach.write, find %s'%(regname)
		else:
			mydata=[]
			self.memlist[regname]=mydata
			#print 'matlabRoach.write, make new %s'%(regname)

		
		
		dst=offset;
		
		endlen=offset + len(valarray)

		dlen=len(mydata)
		if endlen>dlen:
			mydata = mydata + ([0]*(endlen-dlen))
			
			#print 'matlabRoach.write extend %s by %d'%(regname,endlen-dlen)

		try:	
		    #print 'matlabRoach.write dst=%d, lenvalarray=%d, lenmydata=%d'%\
		    #		(dst,len(valarray),len(mydata))

		    for k in range(len(valarray)):
			mydata[dst]=valarray[k]
			dst=dst+1

		    self.memlist[regname]=mydata
		    #print 'matlabRoach.write len memlist[regname] %d'%(len(self.memlist[regname]))

		except:
		    print 'EXCEPTION:  matlabroach.write------'
		    print 'len(valarray) %d'%(len(valarray))
		    print 'len(mydata) %d'%(len(mydata))

		    print 'dst %d'%(dst)
		    print 'offset %d'%(offset)
		    print 'dlen %d'%(dlen)
		    print 'endlen %d'%(endlen)
		    print 'endlen-dlen %d'%(endlen-dlen)
		    


	def read_int(self,regname):
		return(0)

		
	def read(self,regname,nbytes):
		data = '0'*nbytes
		md=fromMatlab()
		if regname == 'MemRecordReal_Shared_BRAM':
		    dd=md['magv'].tolist()
	    	    data = struct.pack('>'+'I' * len(dd), *dd)
		    print 'read: reading MemRecordReal_Shared_BRAM'

		if regname == 'MemRecordImag_Shared_BRAM':
		    dd=md['phsv'].tolist()
	    	    data = struct.pack('>'+'I' * len(dd), *dd)
		    print 'read: reading MemRecordImag_Shared_BRAM'

		return(data)


	#send all regusters in the obhject to matlab script. must be called at end in the matlab sim py function
	#simtime makes sure all sim data is at least that long a vector if not longer
	def toMatlab(self,simtime):
		savect=self.current_time
		self.current_time=simtime
		#make all regs arrays len of simtime at least
		self.makeEqualLenSeq()
		self.current_time=savect


		for reg in self.reglist.keys():
			toMatlab(self.reglist[reg],reg)

		
		

        def startNc(self): pass

        def fpgaStatus(self): pass

        def closeFiles(self):pass

        def restart(self):pass

        def shutdown(self):pass

        def help(self):pass

        def listReg(self):pass

        def readAllReg(self):pass

        def sendBof(self,filename):pass

        def infoEth(self):pass

        def stopEth(self,device):pass

        def singleFreqLUT(self,f, iq, sampleRate, size, phase, amplitude):pass

        def convertToBinary128_2(self,data1,channel):
            """ Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

                @param data             Decimal data to be converted  for FPGA.
                """
            binaryData = ''
            for i in range(0, len(data1)):
                if channel==0:
                    x = struct.pack('>HHHHHHHH',
                        data1[i],
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0)

                elif channel==1:
                    x = struct.pack('>HHHHHHHH',
                        0,
                        data1[i],
                        0,
                        0,
                        0,
                        0,
                        0,
                        0)

                elif channel==2:
                    x = struct.pack('>HHHHHHHH',
                        0,
                        0,
                        data1[i],
                        0,
                        0,
                        0,
                        0,
                        0)

                elif channel==3:
                    x = struct.pack('>HHHHHHHH',
                        0,
                        0,
                        0,
                        data1[i],
                        0,
                        0,
                        0,
                        0)


                elif channel==4:
                    x = struct.pack('>HHHHHHHH',
                        0,
                        0,
                        0,
                        0,
                        data1[i],
                        0,
                        0,
                        0)

                elif channel==5:
                    x = struct.pack('>HHHHHHHH',
                        0,
                        0,
                        0,
                        0,
                        0,
                        data1[i],
                        0,
                        0)

                elif channel==6:
                    x = struct.pack('>HHHHHHHH',
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        data1[i],
                        0)

                elif channel==7:
                    x = struct.pack('>HHHHHHHH',
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

            self.write_int(control_reg, 0)

            self.write_int(control_reg, (1<<sync_bit))

            self.write_int(control_reg, 0)


            self.write_int(control_reg, (1<<startdac_bit))


        #bindata is bin string, mult of 128 bits long.
        #dramname is prename...
        def writeDram(self,dramname,bindata):

            control_reg='%s_control'%dramname
            lutsize_reg = '%s_LUTSize'%dramname
            offs_addr_reg = '%s_offsAddr'%dramname
            buffmem = '%s_drambuff128'%dramname

            startdac_bit = 2
            sync_bit =3
            load_addr_bit = 0
            write_bit = 1
            rst_dram_bit = 4


            datalen=len(bindata)
            datalen_word=datalen/16

            print 'nbytes %d lutsizewords %d'%(datalen, datalen_word)

            control = 0

            self.write_int(control_reg, 0)

            self.write_int(control_reg, (1<<sync_bit))
            self.write_int(control_reg, 0)
            self.write_int(control_reg, 0)

            self.write_int(lutsize_reg, datalen_word)

            offaddr = 0
            dataptr = 0

            buffsize_word = 1024
            buffsize = buffsize_word*16

            while dataptr<datalen:
                datawr=bindata[(dataptr):(dataptr+buffsize)]

                self.write_int(offs_addr_reg, offaddr)
                control =  (1<<load_addr_bit)
                self.write_int(control_reg, control)
                control = 0
                self.write_int(control_reg, control)

                self.write(buffmem,datawr)
                print "write %d bytes: %s"%(len(datawr),datawr[:64])
                control =(1<<write_bit)
                self.write_int(control_reg, control)
                control = control + (1<<startdac_bit)
                self.write_int(control_reg, control)
                control = 0
                time.sleep(0.001)
                self.write_int(control_reg, control)

                dataptr= dataptr + buffsize
                offaddr = offaddr + buffsize_word



        def reverseBits(self,data):
            data2=[]
            for d in data:
                d2 = int(bin(d)[:1:-1], 2)
                data2.append(d2)
            return(data2)




        def setupEth(self,device,ip,port,mac):pass





########################################################################
#we conn to a fake roach, which is really matlab codes, so we can use pycodes to 
#control matlab simulation
#######################################################################
def connMatlab():

	print "Opening matlab roach simulation ...\n"
	
	return(roach)
		
