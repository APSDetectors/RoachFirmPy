
class roachScope:

	def __init__(self,rch_,fwn_):
		self.fwname = fwn_

		self.roach = rch_
		self.plotdata=0
		self.spect_mag=0
		self.is_hold=False

		self.is_octo=False


	#trigin from 0,1,2,3 to trig on those inputs.
	#trig in -1 to ignore trig.
	#inpt is 0,1,2,3,4,5,6,7
	def trigScope(self,trigin=-1, inpt=0):
	    
	    if trigin ==-1:
		ig_tr = 1
		trigin = 0
	    else:
		ig_tr = 0
	
	   
	    we_in = 0
	    inputsel = inpt + trigin*16  + we_in*64;
	    self.roach.write_int(self.fwname + "_inputsel",inputsel);

	    print "Trigger roachscope"
	    #clear trace
	    self.roach.write(self.fwname + '_snapshot_bram','\0'*4096)
	  
	    ig_we = 1
	  
	    ctrl = ig_we*4 + ig_tr*2;

	    self.roach.write_int(self.fwname + '_snapshot_ctrl',ctrl)


	    stat = self.roach.read_int(self.fwname + '_snapshot_status')
	    print 'stat = %x'%stat

	    ctrl+=1;
	    self.roach.write_int(self.fwname + '_snapshot_ctrl',ctrl)
	    time.sleep(0.01)

	    stat = self.roach.read_int(self.fwname + '_snapshot_status')
	    print 'stat = %x'%stat
	    print "END Trigger Roachscope"



	def readScope(self):
		binstr = self.roach.read(self.fwname + '_snapshot_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		self.plotdata = ccopy.deepcopy(shorts)

		self.is_octo=False


	def readScopeOcto(self):
		
		
		binstr = self.roach.read(self.fwname + '_snapshot_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		
		self.multiplotdata = [shorts]

		binstr = self.roach.read(self.fwname + '_snapshot1_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))

		self.multiplotdata.append(shorts)
		
		binstr = self.roach.read(self.fwname + '_snapshot2_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		self.multiplotdata.append(shorts)


		binstr = self.roach.read(self.fwname + '_snapshot3_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		self.multiplotdata.append(shorts)

		binstr = self.roach.read(self.fwname + '_snapshot4_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		self.multiplotdata.append(shorts)

		binstr = self.roach.read(self.fwname + '_snapshot5_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		self.multiplotdata.append(shorts)

		binstr = self.roach.read(self.fwname + '_snapshot6_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		self.multiplotdata.append(shorts)

		binstr = self.roach.read(self.fwname + '_snapshot7_bram',4096)
		shorts = list(struct.unpack('>2048h',binstr))
		self.multiplotdata.append(shorts)

		self.plotdata = ccopy.deepcopy(self.multiplotdata[0])
		
		self.is_octo=True;


	def interleave(self,chans):
	
	    self.plotdata = [0] * (len(chans) * len(self.multiplotdata[0]))
	    
	    nc = len(chans) 
	    
	    for k in range(nc):
	        self.plotdata[k::nc] =  self.multiplotdata[chans[k]]
	        

	def plotSpectrum(self,pllen = 2048,signbit = -1,replot=False,log='No'):

	    if replot==False:
		self.readScope()
		shorts = ccopy.deepcopy(self.plotdata)	       
	    else:
	        shorts = ccopy.deepcopy(self.plotdata)	       
	    	    
	    if signbit!=-1:
	    	for kk in range(len(shorts)):
		    sgn = shorts[kk] & (1<<signbit)
		    if sgn!=0:
		        shorts[kk] = shorts[kk] - (1 << (signbit+1))

	    
	    
	    figure(1)

	    if self.is_hold==False: clf()

	    w=numpy.hamming(pllen)
	    self.spect_mag =numpy.abs(numpy.fft.fft(w*shorts[:pllen]))
	    if log=='No':
	        plot(self.spect_mag)
	    else:
	    	semilogy(self.spect_mag)


	def plotScope(self,pllen = 2048,
		is_usebits = False, 
		bits = '15:11;10:10;9:9;8:8',
		isprint = False,
		isprintsh=False,
		shskip = 1,
		shoffset=0,
		signbit=-1,		
		replot=False):


	    if replot==False:
		self.readScope()
		shorts = ccopy.deepcopy(self.plotdata)
	    else:
	        shorts = ccopy.deepcopy(self.plotdata)	       
	    
	    
	    shorts = shorts[shoffset::shskip]	    
	    if signbit!=-1:
	    	for kk in range(len(shorts)):
		    sgn = shorts[kk] & (1<<signbit)
		    if sgn!=0:
		        shorts[kk] = shorts[kk] - (1 << (signbit+1))

		
	    
	    figure(1)



	    if self.is_hold==False: clf()

	    if isprint:
		print binstr
		print len(binstr)
	
	    if isprintsh:
		print shorts
		print len(shorts)


	    if is_usebits==False:
		plot(shorts[:pllen],drawstyle = 'steps')

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
			    
		  	plot(y,drawstyle='steps')
			graphnum = graphnum+1.0
			stbit = stbit - width
	    
	    

