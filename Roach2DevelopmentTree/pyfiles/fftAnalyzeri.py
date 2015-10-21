print "Loading fftAnalyzeri.py"
	
########################################################################
#
# 
#
#######################################################################

class fftAnalyzeri(fftAnalyzerd):


	def __init__(self,r):
		fftAnalyzerd.__init__(self,r)

		#1 to flish the input fifo where fft coef come ine.
		self.flush_input_fifo=0;


		#bit for making ffts run forever.
		self.fft_run_forever = 0
		
		#bit to reset the event counter to 0
		self.reset_event_counter = 0
		
		#32 bit counter- event counter- read from roach
		self.event_counter = 0
		
		#event rate- we read evt cnt in SW twice, 1sec apart. 
		self.events_per_sec = 0
		
		
		#default to multi sweep of resonotors
		self.is_sweep_several=1


		#fir now do not do delay.. bug in appending events, as old events get delay
		#mult times.		
		self.is_apply_delay=0;
		#iqdata is in dict format for this fw
		self.iqdata=dict()

		#1 if we append events on read roach memory\
		self.is_append_events = 0


		#set to 1 to delete all data and not save into roach outfifo and out ram
		self.drop_all_events=0

		#disable pulse detector, and write all data from channe,s
		self.is_write_raw_data=1
		#clear phase accums to 0
		self.clear_phase=0
		
		

		#last channel to read. 0 means it reas only 1 channel. 1 means it reads 0 and 1.
		#up to 255, but we only have 128 fifos.. so up to 127.
		self.last_chan_to_read=0



		#
		# Pulse detecotr threshold. it is a sort of sum of radians/pi plus amplitude.
		# it is a value that is unsigned number of i18_16 type. You can make proper val for thresh
		# as 65536*th, whrer th is between 0 and 1.999... We use val velow for sim
		#we mult 65536 times this value when programming the roach board.
		#!!self.pulse_threshold = 0.0149
		


		#pulse strecter circuit in the pilse detector. number of samples the puse stays
		#high after thresh is triggered, we use 10 samples in sim. 
		self.pulse_stretcher_length = 10
		#num std to set pulse det
		self.pulse_num_std=10
		#map of channel to its noise means, a tuple like this;:\
		# (mag_mu,phs_mu,mag_std,phs_std,thresh)
		self.chan_to_meanth=dict()
		
		#binary numbers to download to the pulse detector rams
		self.pulsedetector_muram=[0]*1024
		self.pulsedetector_thram=[0]*1024
		


		#use a sin gen instead of dram lookuip tabnle for signal generation
		self.use_test_freq=0;
		#freq in Hz of test freq.
		self.test_freq_hz=10.23412323e6;
		#binary version of above...		
		self.test_freq=0
		
		#
		#registers for programming the phase corrector
		#
		
		#phase inc val for some channel. calc from freq offset from fft bin center for taht
		#channel. in radians/pi. must convert to integer unsigned 32, twos complemnt before writing
		#this number here is a floating point number in radians/pi
		#store this number as s float in rad/pi, and convert to 2's comp when programming roach
		self.phase_inc_val = 0

		#address for above phase inc val from 0 to 127 ( or 255), for channel of interest.
		self.phase_inc_addr = 0

		#program mode bit , high if we are programming the RAM storing all phase increments
		self.phase_inc_prog_mode=0
		#write enable bit, to write te RAM in phase accum- it writes phaseincval to addr at
		#phase inc addr. set prog mode high first, then set up inc val and addr. finally pulse
		#write enable 0,1,0 to write the phase incr to correct channel address.
		self.phase_inc_write_en=0

		#map channel to phase of line delay- this is NOT phase correction of freq offset from bin
		self.chan_to_linedel_phase=dict()
		#map src freq or bin center freq to line delay phase
		self.freq_to_linedel_phase = dict()
		#
		#array of phase increments for all fifo chans, in readians/pi
		self.phase_inc_array=[0.0] * 256

		
		#dft memlen
		self.memLen=32768
		self.memLen4=self.memLen/4
		self.memLen8=self.memLen/8


		#min val is dftLen or 128, max is 2048, or len of the BinData ram
		#no reason to have more than 128 becasue we can always get max sample rate of fft,
		# that is store every fft coef, beause we are using thefifos..not readout of all coef
		#is this true? perhapswan to slow the sampl raete in some cases...mult of dftLen is
		#number of ffts to skiop
		self.fftsynctime=self.dftLen


		#map of fifo chan address to fft bin we readout/4
		#given fifo chan, which bin do we readout?
		self.chan_to_bin4=dict()
		
		#giben fft bin, find what fifo chan is getting it.
		self.bin_to_chan=dict()

		self.chan_to_bin=dict()
		#maps of chan to srouce freq and vice versa
		self.chan_to_srcfreq=dict()
		self.srcfreq_to_chan= dict()

		#number of mapped channels. shoudl be 1 to read out one channel
		#last chan to read is this number - 1. so if it is 1, last mapped chan is 0 
		self.num_mapped_addresss = 0



		#
		#we get data in retuyrned memory in packets. we have two rams, for phase and mag
		#phase has the header data.preceeding phse data
		#header is 0x10000 followed by int, chan number . The length of the data is set in 	
		#fifoFSMPh.m, or the firmware. it is 32 words long in the memory.
		self.outmem_headerlen=2;
		#32 ints long
		self.outmem_datalen=32;
		#mem is 32 bits wide.
		self.outmem_width=32;
		#below is sign buts, total buts, num frac buts
		self.outmem_mag_datatype = [0,16,16]
		self.outmem_phs_datatype = [1,16,13]

		self.outmem_ts_masklow = 0x0000ffff<<9
		self.outmem_ts_maskhi = 0xffff0000
		self.outmem_ts_norm= 65536
		self.outmem_fff_mask=0xffff
		self.outmem_chan_mask=0xff
		self.outmem_pulse_mask=0x100

		#last bit of memory to carry over t next mem read
		self.carrydata=[numpy.array([]),numpy.array([])]


		#reset sig for timestamp- it counts at 1MHz, and is 20buts.
		self.timestamp_reset=0

		#given srcfreq, lookup phase delay
		
		self.freq_to_linedel_phase = dict()


		self.roach_fft_shift=255

		self.datamodestrs=['null','src_freqs','whole_fft']
		
		self.data_mode=0
		
		
		#if false we read from roach mem dir from python. and set fft_we_mem to 1.
		#if true we heep fft_we_mem=0, and output mem dever gets written unless pulse server does it on roach box
		#also when getting data, iof false we do roach.read() to get the data.
		#if true, we should ahve pulse server running, and nc server on local linux, so getDFT_iq will not
		#read roach board mem, but will read from a linux pipe.
		self.is_use_pulse_server=False
		#!!self.pulsefile=-1
		
		
		#!!self.read_pipe_nelememts=65536
		
		#wjhen sweeping w/ the ffts, how many samples at each freq
		self.sweep_samples_per_freq=64




	
		self.lut_length=65536*2
		self.lut_length2=self.lut_length/2
		self.lut_length4=self.lut_length/4	
		self.lut_length8=self.lut_length/8

	##########################################################################
	#
	#
	#
	##########################################################################

	def getObjSpecs(self):
	
		specs = fftAnalyzerd.getObjSpecs(self)




		#1 if we append events on read roach memory\
		specs.is_append_events  = self.is_append_events 


		#set to 1 to delete all data and not save into roach outfifo and out ram
		specs.drop_all_events = self.drop_all_events

		#disable pulse detector, and write all data from channe,s
		specs.is_write_raw_data = self.is_write_raw_data
		#clear phase accums to 0
		specs.clear_phase = self.clear_phase
		
		

		#last channel to read. 0 means it reas only 1 channel. 1 means it reads 0 and 1.
		#up to 255, but we only have 128 fifos.. so up to 127.
		specs.last_chan_to_read = self.last_chan_to_read





		#pulse strecter circuit in the pilse detector. number of samples the puse stays
		#high after thresh is triggered, we use 10 samples in sim. 
		specs.pulse_stretcher_length  = self.pulse_stretcher_length 
		#num std to set pulse det
		specs.pulse_num_std = self.pulse_num_std
		#map of channel to its noise means, a tuple like this;:\
		# (mag_mu,phs_mu,mag_std,phs_std,thresh)
		specs.chan_to_meanth = self.chan_to_meanth
		
		#binary numbers to download to the pulse detector rams
		specs.pulsedetector_muram = self.pulsedetector_muram
		specs.pulsedetector_thram = self.pulsedetector_thram
		


		#use a sin gen instead of dram lookuip tabnle for signal generation
		specs.use_test_freq = self.use_test_freq
		#freq in Hz of test freq.
		specs.test_freq_hz = self.test_freq_hz
		#binary version of above...		
		specs.test_freq = self.test_freq
		
		#
		#registers for programming the phase corrector
		#
		
		#phase inc val for some channel. calc from freq offset from fft bin center for taht
		#channel. in radians/pi. must convert to integer unsigned 32, twos complemnt before writing
		#this number here is a floating point number in radians/pi
		#store this number as s float in rad/pi, and convert to 2's comp when programming roach
		specs.phase_inc_val  = self.phase_inc_val 

		#address for above phase inc val from 0 to 127 ( or 255), for channel of interest.
		specs.phase_inc_addr  = self.phase_inc_addr 

		#program mode bit , high if we are programming the RAM storing all phase increments
		specs.phase_inc_prog_mode = self.phase_inc_prog_mode
		#write enable bit, to write te RAM in phase accum- it writes phaseincval to addr at
		#phase inc addr. set prog mode high first, then set up inc val and addr. finally pulse
		#write enable 0,1,0 to write the phase incr to correct channel address.
		specs.phase_inc_write_en = self.phase_inc_write_en

		#map channel to phase of line delay- this is NOT phase correction of freq offset from bin
		specs.chan_to_linedel_phase = self.chan_to_linedel_phase
		#map src freq or bin center freq to line delay phase
		specs.freq_to_linedel_phase  = self.freq_to_linedel_phase 
		#
		#array of phase increments for all fifo chans, in readians/pi
		specs.phase_inc_array = self.phase_inc_array

	


		#map of fifo chan address to fft bin we readout/4
		#given fifo chan, which bin do we readout?
		specs.chan_to_bin4 = self.chan_to_bin4
		
		#giben fft bin, find what fifo chan is getting it.
		specs.bin_to_chan = self.bin_to_chan

		specs.chan_to_bin = self.chan_to_bin
		#maps of chan to srouce freq and vice versa
		specs.chan_to_srcfreq = self.chan_to_srcfreq
		specs.srcfreq_to_chan = self.srcfreq_to_chan

		#number of mapped channels. shoudl be 1 to read out one channel
		#last chan to read is this number - 1. so if it is 1, last mapped chan is 0 
		specs.num_mapped_addresss  = self.num_mapped_addresss 



		#
		#we get data in retuyrned memory in packets. we have two rams, for phase and mag
		#phase has the header data.preceeding phse data
		#header is 0x10000 followed by int, chan number . The length of the data is set in 	
		#fifoFSMPh.m, or the firmware. it is 32 words long in the memory.
		specs.outmem_headerlen = self.outmem_headerlen
		#32 ints long
		specs.outmem_datalen = self.outmem_datalen
		#mem is 32 bits wide.
		specs.outmem_width = self.outmem_width
		#below is sign buts, total buts, num frac buts
		specs.outmem_mag_datatype  = self.outmem_mag_datatype 
		specs.outmem_phs_datatype  = self.outmem_phs_datatype 

		specs.outmem_ts_masklow  = self.outmem_ts_masklow 
		specs.outmem_ts_maskhi  = self.outmem_ts_maskhi 
		specs.outmem_ts_norm = self.outmem_ts_norm
		specs.outmem_fff_mask = self.outmem_fff_mask
		specs.outmem_chan_mask = self.outmem_chan_mask
		specs.outmem_pulse_mask = self.outmem_pulse_mask

		#last bit of memory to carry over t next mem read
		specs.carrydata = self.carrydata


		#reset sig for timestamp- it counts at 1MHz, and is 20buts.
		specs.timestamp_reset = self.timestamp_reset

		#given srcfreq, lookup phase delay
		
		specs.freq_to_linedel_phase  = self.freq_to_linedel_phase 


		
		specs.data_mode = self.data_mode
		
		
		#if false we read from roach mem dir from python. and set fft_we_mem to 1.
		#if true we heep fft_we_mem=0, and output mem dever gets written unless pulse server does it on roach box
		#also when getting data, iof false we do roach.read() to get the data.
		#if true, we should ahve pulse server running, and nc server on local linux, so getDFT_iq will not
		#read roach board mem, but will read from a linux pipe.
		specs.is_use_pulse_server = self.is_use_pulse_server
		#!!self.pulsefile=-1
		
		
		#!!self.read_pipe_nelememts=65536
		
		#wjhen sweeping w/ the ffts, how many samples at each freq
		specs.sweep_samples_per_freq = self.sweep_samples_per_freq

		return(specs)



	##########################################################################
	#
	#
	#
	##########################################################################
	
	def setUsePulseServer(self,is_use):
	
		self.fft_mem_we=0
		self.progRoach1()
		
		if is_use:
		    self.is_use_pulse_server=True
		    #!!self.openPulsePipe('/local/tmadden/testdata.bin')
		
		else:
		    self.is_use_pulse_server=False
		    #!!self.closePulsePipe()



	###########################################################################
	#
	#data type is (18,15) where we have 18 bits data, 15 fraction bits
	#converts vector of binary twos comp to floats.
	###########################################################################

	def convToFloat(self,data, datatype):

		nfrac=2
		nbits=1
		sbit=0
		
		#pow(2,(datatype[output][1]+1), 
		#if we have 16 fraction bits, this is
		#pow(2,16)-1 = 0x10000 - 1 = 0xffff
		if datatype[nfrac]>0:
		    fracmask = int(pow(2,datatype[nfrac])-1)
		    fracnorm=float(pow(2.0,datatype[nfrac]))
		else:
		    fracmask = 0
		    fracnorm=1.0
		    
		#mask for int part not including sign bit.
		#datatype[output][0] - datatype[output][1] - 1 is 18-15-1=2, where we have 2 bits
		#fir int part not counting sign bit.
		numintbits =   datatype[nbits] - (datatype[sbit] + datatype[nfrac])
		#for 2 int buits, we take 3<<numfracbits, 3<<15	
		#this is int portion mask not incl the 	
		if numintbits>0:	
		    intmask=(pow(2,numintbits)-1) << datatype[nfrac]
		else:
		    intmask=0

		#sign mask is numbuts-1
		if datatype[sbit]>0:
		    signmask = int(pow(2,(datatype[nbits]-1)))
		    signval = -1.0 * float(signmask)/fracnorm
		else:
		    signmask=0
		    signval=0.0

		#print 'fracmask %x fracnorm  %f numintbits  %d intmask  %x signmask  %x signval  %f '%\
		#	(fracmask,fracnorm,numintbits,intmask,signmask,signval)
		
		newdata = []
		for d in data:

			fracpart=int(d) &  fracmask
			frac =  float(fracpart)/fracnorm
			
			intpart = int(d) & intmask;
			intval = float(intpart) / fracnorm

			#if we have 18 bit data, sign but is but 17.
			#signbit will be 1 or 0, below becayse of > sign
			signbit=float((int(d) & signmask)>0);
			signval_ = signbit*signval
			

			val = signval_ + intval + frac

			#print ' fracpart  %d   frac %f intpart  %d  intval %f signbit  %d signval_  %f  val %f'%\
			#	(fracpart,frac,intpart,intval,signbit,signval_,val)

			newdata.append(val)
			
		return(array(newdata))
	########################################################################
	#
	# 3dplot- plots events in iqdata, time vs freq vs amp or phase.
	# gibue zlim to limit the z axis as a tuyple (bottomlim,toplim)
	# ampphase=1 to plot phase instead of amp. 0 for amps
	############################################################################

	def plotChan3D(self,fignum=1,zlim=-1,nspec=-1,ampphase=0):
		fig = figure(fignum)
		clf()
		ax = fig.gca(projection='3d')
		
		zranges=[]
		for chan in self.iqdata.keys():	
		  try:
		    if nspec==-1:
			nspec=len(self.iqdata[chan]['stream'][ampphase])	    
		    
		    
		    
		    z=self.iqdata[chan]['stream'][ampphase][:nspec]
		   
		    
		    zranges.append(median(z))
		    y=arange(len(z))
		   
		    x = numpy.array( [ self.iqdata[chan]['bin']  ]*len(z) )
		    ax.plot(x, y, z,label='zz')
		  except:
		    print "bad chan?"
		#ax.legend()

		rng=median(array(zranges))

		if zlim==-1: ax.set_zlim(bottom=rng/2, top=rng*2)
		else:ax.set_zlim(bottom=zlim[0], top=zlim[1])
		
		#plt.show()


		return(ax)


	########################################################################
	#
	#2d plot of iqdata. chans is list of channels, or -1. data is an iqdata struct
	#or -1
	#
	############################################################################

	def plotEvents2D(self,fignum=5, chans=-1,data=-1):
	
		if data ==-1: data = self.iqdata
		
		if chans==-1: chans=data.keys()

		figure(fignum)
		clf()
		pcolors = ['b','g','r','c','m','y','k']
		ccount = 0
		for c in chans:
		    i=0		
		    for ts_ in data[c]['timestamp']:
		      try:
			#!!ts = e[3]
			evx=self.getEventFromStream(c,index=-1,ts=ts_,events=data)
			amp=evx['mag']
			phs=evx['phs']
			timevec=range(ts_,ts_+32)
			subplot(2,1,1)
			plot(timevec,amp,pcolors[ccount])
			subplot(2,1,2)
			plot(timevec,phs,pcolors[ccount])
		      except:
			print 'Exception in fftAnalyzeri.plotEvents2D'
		    ccount=(ccount+1)%(len(pcolors))

		  
		


	########################################################################
	#
	#
	#
	############################################################################

	def plotTimestamps(self,fignum=4, chans=-1,data = -1):
		figure(fignum)
		clf()

		if data ==-1: data = self.iqdata
		
		if chans==-1: chans=data.keys()

	

		for c in chans:
		    ll=[]		
		    for ts in data[c]['timestamp']:
			
			ll.append(ts)

		    plot(ll)

					

	########################################################################
	#
	#
	#
	############################################################################

	def plotTimestampsD(self,fignum=6, chans=-1,data = -1):
		figure(fignum)
		clf()

		if data ==-1: data = self.iqdata
		
		if chans==-1: chans=data.keys()

	

		for c in chans:
		    ll=[]		
		    for ts in data[c]['timestamp']:
			
			ll.append(ts)

		    plot(numpy.diff(ll))

				
	########################################################################
	#
	#
	#
	############################################################################

	def waterfall(self,fignum=3,numspec=20,skip=0):
  		figure(fignum);clf()
		yy=arange(self.fftLen)
		yoffs=0
		xoffs=0
		xinc=max(self.extractSpectrum(0)[0])/20.0
		poffs = 0.0
		for k in range(0,numspec,skip):
		  try:  
		    sp=self.extractSpectrum(k)
		    subplot(2,1,1)
		    
		    subplot(2,1,1)
		    plot(yy+yoffs, xoffs+sp[0])
		    subplot(2,1,2)
		    plot(yy+yoffs,poffs+sp[1])

		    yoffs=yoffs + self.fftLen/50
		    xoffs=xoffs + xinc
		    poffs = poffs + pi/20
 		  except:
		    break



	########################################################################
	#
	#
	#list settings of the py code, and FW
	############################################################################


	def lssets(self):
		
	    for c in self.chan_to_bin:
		try: 
		    print "chan: %d bin: %d  srcfreq %fMHz  bin4 %d  "%\
			(c,self.chan_to_bin[c][0],self.chan_to_srcfreq[c]/1e6 , 
			self.chan_to_bin4[c][0])

		except:
		    print "chan: %d bin: %d  bin4 %d   "%\
			(c,self.chan_to_bin[c][0],  
			self.chan_to_bin4[c][0])


	    print "Source Frequencies"
	    print fa.frequency_list

	    print "LO %fMHz"%(self.carrierfreq/1e6)

	    

		


	########################################################################
	#
	#list events retrieved, stored in iqdata
	#
	############################################################################


	def lsevents(self,ev=0,isplot=0):

		if ev==0:ev=self.iqdata

		print "Channels:"
		print ev.keys()

		if isplot>1:
		  
		    
		    self.waterfall(fignum=11,numspec=20,skip=32)


		for chan in ev.keys():
		    print "\n\n-------------------------"
		    print "channel %d"%(chan)
		    ph=0.0
		    if ev[chan].has_key('phase'):ph=ev[chan]['phase']

		    sf=0
		    if self.chan_to_srcfreq.has_key(chan): sf=self.chan_to_srcfreq[chan]
		    
		    try:	
		      print 'bin   %d  \nphase  %d  \nnumevents  %d  \nstreamlen  %d \nbinfreq %f \nsrcfreq %f\n'%\
			(ev[chan]['bin'][0],
			ph,
			len(ev[chan]['timestamp']),
			len(ev[0]['stream'][0]),
			fa.getFreqFromBin(ev[chan]['bin'][0]),
			sf)

		    except:
		      
		      print 'bin   %d  \nphase  %d  \nnumevents  %d  \nstreamlen  %d \nbinfreq %f \nsrcfreq %f\n'%\
			(ev[chan]['bin'],
			ph,
			len(ev[chan]['timestamp']),
			len(ev[chan]['stream'][0]),
			fa.getFreqFromBin(ev[chan]['bin']),
			sf)

		    
		    if isplot>0: 
			figure(1000+chan)
			for index in range(len(ev[chan]['timestamp'])):
			    evx=self.getEventFromStream(chan,index)
			
			    print "    timestamp %d  ispulse %d"%(
			    	evx['timestamp'],evx['is_pulse'])
				
			   	
			    subplot(2,1,1);plot(evx['mag'])
			    subplot(2,1,2);plot(evx['phs'])

		    if isplot>1:
			figure(12)
		        subplot(2,1,1)
		        plot(ev[chan]['stream'][0])
		
		        subplot(2,1,2)
		        plot(ev[chan]['stream'][1])

		print '\nsearches %d'%(self.searches)
		print 'carryovers %d'%(self.carryovers)
		print 'eventcount %d'%(self.eventcount)

	###########################################################################
	#
	#	carry data is when we get 1/2 event at end of fpga mem, and
	#	we must store in SW, before we grab more data from foga.	
	#	then we stich the event back together this happens when	
	#	a pulse or waveform is half sent to fpga output ram
	###########################################################################

	def clearCarry(self):

		self.carrydata=[numpy.array([]),numpy.array([])]


	def clearEvents(self):
		self.iqdata=dict()
#
#	###########################################################################
#	#
#	#take int data from two memories, mag and phase, and make floating ppoint 
#	#guve int data from both memorues, raw int 32 but words.
#	###########################################################################
#	def extractEvents(self,mag,phs,append=0):
#		
#		
#		if append==0: events=dict()
#		else: events=self.iqdata
#
#
#		searches=0
#		carryover=0
#		evtcnt=0
#		nbad_events=0
#
#		endsearch = len(phs) - (self.outmem_headerlen + self.outmem_datalen)
#		#rtry in case we go out of bounds...k+1 etc...
#		if 1==1:
#		  k = 0
#		  while k<endsearch:
#		    #print k
#		    if phs[k]&self.outmem_fff_mask == 0xffff:
#	      	      try:
#			
#		 	chan=phs[k+1]&self.outmem_chan_mask
#			timestamp = int(phs[k]&self.outmem_ts_masklow) >>16
#			timestamp = timestamp + (int(mag[k]&self.outmem_ts_maskhi) <<2)
#			is_pulse = phs[k+1]&self.outmem_pulse_mask
#			dp=phs[(k+2):(k+2+self.outmem_datalen)]
#			dm=mag[(k+2):(k+2+self.outmem_datalen)]
#			dataph=self.convToFloat(dp,self.outmem_phs_datatype)
#			dataph=dataph*pi
#			datamag=self.convToFloat(dm,self.outmem_mag_datatype)
#
#			if events.has_key(chan)==False:
#			    #!print 'chan %d'%(chan)
#			    events[chan]=dict()
#			    events[chan]['stream']=[array([]), array([])]
#			    events[chan]['events']=[]
#			    events[chan]['bin']=self.chan_to_bin[chan][0]
#			
#			events[chan]['events'].append([datamag, dataph,is_pulse,timestamp])
#			stm=events[chan]['stream'][0]
#			stp=events[chan]['stream'][1]
#			events[chan]['stream'][0] = numpy.append(stm,datamag )
#			events[chan]['stream'][1] = numpy.append(stp,dataph )
#			#!print 'chan   %d  k  %d  is_pulse  %d  timestamp  %x    '%\
#			#!	(chan,k,is_pulse,timestamp)
#			nextk=k+self.outmem_headerlen + self.outmem_datalen			
#			
#		
#			k = nextk
#			evtcnt=evtcnt+1
#		      except:
#			#print "bad event"
#			nbad_events=nbad_events+1
#		    else:
#		      k=k+1
#		      searches=searches+1	    
#		    #print k
#
#		else:
#		  pass
#
#		print k
#		print 'badevents = %d'%(nbad_events)
#		self.carrydata=[mag[k:]  , phs[k:]]
#		self.searches = searches
#		self.carryovers=carryover
#		self.eventcount = evtcnt
#		return(events)
#
#
#
#
#
#	###########################################################################
#	#
#	#take int data from two memories, mag and phase, and make floating ppoint 
#	#guve int data from both memorues, raw int 32 but words.
#	###########################################################################
#	def extractEvents2(self,magphs,append=0):
#		
#		
#		if append==0: events=dict()
#		else: events=self.iqdata
#
#
#		searches=0
#		carryover=0
#		evtcnt=0
#		nbad_events=0
#
#		endsearch = len(magphs) - (self.outmem_headerlen + self.outmem_datalen)
#		#rtry in case we go out of bounds...k+1 etc...
#		if 1==1:
#		  k = 0
#		  while k<endsearch:
#		    #print 'while %d magphs 0x%x'%(k,magphs[k])
#		    if magphs[k]&self.outmem_fff_mask == 0xaaaa:
#	      	      try:
#			
#		 	chan=magphs[k+1]&self.outmem_chan_mask
#			timestamp = int(magphs[k]&self.outmem_ts_maskhi) 
#			timestamp = timestamp + (int(magphs[k+1]&self.outmem_ts_masklow) >>9)
#			is_pulse = magphs[k+1]&self.outmem_pulse_mask
#			dp=(magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff
#			dm=((magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff0000)>>16
#			dataph=self.convToFloat(dp,self.outmem_phs_datatype)
#			dataph=dataph*pi
#			datamag=self.convToFloat(dm,self.outmem_mag_datatype)
#
#			if events.has_key(chan)==False:
#			    print 'chan %d'%(chan)
#			    events[chan]=dict()
#			    events[chan]['stream']=[array([]), array([])]
#			    events[chan]['events']=[]
#			    events[chan]['bin']=self.chan_to_bin[chan][0]
#			
#			events[chan]['events'].append([datamag, dataph,is_pulse,timestamp])
#			stm=events[chan]['stream'][0]
#			stp=events[chan]['stream'][1]
#			events[chan]['stream'][0] = numpy.append(stm,datamag )
#			events[chan]['stream'][1] = numpy.append(stp,dataph )
#			
#			#print 'chan   %d  k  %d  is_pulse  %d  timestamp  %x    '%\
#			#	(chan,k,is_pulse,timestamp)
#			
#			nextk=k+self.outmem_headerlen + self.outmem_datalen			
#			
#		
#			k = nextk
#			evtcnt=evtcnt+1
#		      except:
#			#print "bad event"
#			nbad_events=nbad_events+1
#			k=k+32
#			
#		    else:
#		      k=k+1
#		      searches=searches+1	    
#		    #print k
#
#		else:
#		  pass
#
#		print k
#		print 'badevents = %d'%(nbad_events)
#		self.carrydata=[magphs[k:]]
#		self.searches = searches
#		self.carryovers=carryover
#		self.eventcount = evtcnt
#		return(events)
#
#
#
#

	###########################################################################
	#
	#take int data from two memories, mag and phase, and make floating ppoint 
	#guve int data from both memorues, raw int 32 but words.
	###########################################################################
	def extractEvents(self,magphs,append=0):
		
		
		if append==0: events=dict()
		else: events=self.iqdata


		searches=0
		carryover=0
		evtcnt=0
		nbad_events=0

		endsearch = len(magphs) - (self.outmem_headerlen + self.outmem_datalen)
		#rtry in case we go out of bounds...k+1 etc...
		if 1==1:
		  k = 0
		  while k<endsearch:
		    #print 'while %d magphs 0x%x'%(k,magphs[k])
		    if magphs[k]&self.outmem_fff_mask == 0xaaaa:
	      	      try:
			
		 	chan=magphs[k+1]&self.outmem_chan_mask
			timestamp = int(magphs[k]&self.outmem_ts_maskhi) 
			timestamp = timestamp + (int(magphs[k+1]&self.outmem_ts_masklow) >>9)
			is_pulse = magphs[k+1]&self.outmem_pulse_mask
			dp=(magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff
			dm=((magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff0000)>>16
			dataph=self.convToFloat(dp,self.outmem_phs_datatype)
			dataph=dataph*pi
			datamag=self.convToFloat(dm,self.outmem_mag_datatype)

			if events.has_key(chan)==False:
			    print 'chan %d'%(chan)
			    events[chan]=dict()
			    events[chan]['stream']=[array([]), array([])]
			    
			    events[chan]['timestamp']=[]
			    events[chan]['is_pulse']=[]
			    events[chan]['bin']=self.chan_to_bin[chan][0]
			
			events[chan]['timestamp'].append(timestamp)
			events[chan]['is_pulse'].append(is_pulse)
			stm=events[chan]['stream'][0]
			stp=events[chan]['stream'][1]
			events[chan]['stream'][0] = numpy.append(stm,datamag )
			events[chan]['stream'][1] = numpy.append(stp,dataph )
			
			#print 'chan   %d  k  %d  is_pulse  %d  timestamp  %x    '%\
			#	(chan,k,is_pulse,timestamp)
			
			nextk=k+self.outmem_headerlen + self.outmem_datalen			
			
		
			k = nextk
			evtcnt=evtcnt+1
		      except:
			#print "bad event"
			nbad_events=nbad_events+1
			k=k+32
			
		    else:
		      k=k+1
		      searches=searches+1	    
		    #print k

		else:
		  pass

		print k
		print 'badevents = %d'%(nbad_events)
		self.carrydata=[magphs[k:]]
		self.searches = searches
		self.carryovers=carryover
		self.eventcount = evtcnt
		return(events)




	###########################################################################
	# give chan, event dict which default to iqdata.
	#give ts or index into timestamps. return mag and phs at that ts
	#
	###########################################################################
	
	def getEventFromStream(self,chan=0,index=-1,ts=-1,events=-1):
	
	    if events==-1: events=self.iqdata
	    
	    if ts>-1:
	        #find the timestamp and get index
	        index = 0
		
		while (
		   events[chan]['timestamp'][index]!=ts  and 
		   index<len(events[chan]['timestamp'])):
		   
		    index=index+1
	    
	    #case if index and ts being -1
            if index==-1: index==0
	    #case of not found ts
	    if index == len(events[chan]['timestamp']):index=0
	    
	
	    ts=events[chan]['timestamp'][index]
	    st_=index*32
	    ed_=st_+32
	    mag=events[chan]['stream'][0][st_:ed_]
	    phs=events[chan]['stream'][1][st_:ed_]	
	    is_pulse=events[chan]['is_pulse'][index]
	    
	    answer={ 'mag':mag,
	    		'phs':phs,
			'timestamp':ts,
			'is_pulse':is_pulse}
	    return(answer)
	    



	###########################################################################
	#
	#given the channels we arereading out, map the channel to source freq.
	###########################################################################
	def mapChanToSrcFreq(self):
		self.chan_to_srcfreq=dict()
		self.srcfreq_to_chan= dict()
		for freq in self.frequency_list:
		    bin = self.getBinFromFreq(freq)
		    chan = self.bin_to_chan[bin]
		    self.chan_to_srcfreq[chan]=freq
		    self.srcfreq_to_chan[freq]=chan

	
		


	###########################################################################
	#
	#read 9output mem of fpga. this does not rewind mem. so if we do two gets,	
	# we get same data twice, we must reqind memory, or set mem counter to 0
	#to allow stored fifo data to stream into foga output mem. if we do 	
	#..
	#mem structuyre is a large outptu fifo of 32K, fillowed by output RAM
	#of 32k that we readout from roach board. when mem is empty, fifo dumps to it
	#if mem fills up, fifo holds dasta. if we read out the ram, we get its data,
	#but fifo will not automatically dump new data after read. we must rewind ram
	#by sett8ign address counter of ram to 0, calling rewindMem in puthon. search
	#for def rewind... I forgot function name. If we call getDFT_IQ over and over
	#from older FW, we always get fresh data. If we do in new FW, this one, we 
	#get same data over and over. We must rewind to let fifo dump.
	###########################################################################


	def getDFTdata(self):

		#for debugging so we can see last read from mem
      		global aa;
		
		#I even re, even im, odd re, odd im
		regnames=['MemRecordPolar_%s'%(ramname)]

		nwords = roach.read_int('MemRecordPolar_coefRamAddr')
		#phase is type i_18_15, mag is i_18_16, where it is 18 bits total, signed, dec pointis RIGHT
		#of bit 15 or 16. or 15 or 16 bits of fraction. i18_0 would be point RIGHT of bit 0, no frac.
		
		#above we have mag and phase data type as ele 0 and 1.


		if nwords==0: return(numpy.array([]))


		data = roach.read(regnames[0],4*nwords)
		
		aa=struct.unpack('>'+'I'*(len(data)/4),data)
		
		outdata =  numpy.int_(numpy.concatenate( (self.carrydata[0], numpy.array(aa))))
		

		return(outdata)


	###########################################################################
	#
	#read out IQ data, from output rams. do not reqind mem afterward.
	#to get fresh data we must first rewind mem rewindFFTMem(), to trigger
	#output fifo to dump to out mem in foga.
	###########################################################################


	
	
	def getDFT_IQ(self):
	
		global sweep_counter
		
		
		
		if self.is_read_dump_file==1:
		    self.hdfReadIQ()
		    re=self.I_raw[0]
		    im=self.I_raw[1]
		else:
		  reim=self.getDFTdata()
		  #if self.is_use_pulse_server==False:			
		 #   reim=self.getDFTdata()	
		  #else:
		   # reim=self.readPulsePipe()

		
		#self.rewindFFTMem()
		self.Q_raw=[ccopy.deepcopy(reim)]
		self.I_raw=self.Q_raw
		
		
		
		
		self.iqdata=self.extractEvents(reim,self.is_append_events)
		
		#apply the phase delay die to xmission cable length.
		#this wont be valid for sweeps, where the carrierfreq is change for each fft.
		#in this case we need to removeDelay, then calcXmissnLineDelay()
		if self.is_apply_delay==1:
		    self.applyDelay(1.0)
		
		
		
		#self.dbgappend(('getDFTIQ,fa',self.getObjSpecs()))
		
		
		self.hdfWrite()
		
		sweep_counter=sweep_counter+1

		
		
		
		return(self.iqdata)
		#return([re,im])

	###########################################################################
	#
	#
	###########################################################################
	#
#	def openPulsePipe(self,nn):
#	
#		self.pulsefile=open(nn,'rb')	
#		
#	def closePulsePipe(self):
#	
#		if self.pulsefile!= -1:
#		    self.pulsefile.close()
#		
#		self.pulsefile=-1
		
			
	###########################################################################
	#
	#
#	###########################################################################
#	def readPulsePipe(self):
#		
#		
#		#rehead=self.pulsefile.read(8)
#		
#		reim=self.pulsefile.read(self.read_pipe_nelememts*4)
#		
#		re=numpy.array(struct.unpack('>'+'I'*self.read_pipe_nelememts,reim))
#		return(re)
#		
#		
#



	###########################################################################
	#
	#convert float data to fixed point twos comp. nbits like 18 for 18 bits.
	#dpoint is number of fraction bits.
	###########################################################################

	def toTwoComp(self,data,nbits,dpoint):


		bdata=[0] * len(data)

		for k in range(len(data)):
		    bdata[k]=floor(abs(data[k]) *(1<<dpoint))
		    if data[k]<0:
			bdata[k]=pow(2,nbits) - bdata[k]
		
		    bdata[k] = int(bdata[k])
		   
		
		
		return(bdata)

		
	###########################################################################
	#
	#
	###########################################################################
	def fftBinsFreqs(self):
	
		
		blist = self.getBinsFromFreqs(self.frequency_list)
		
		self.fftBinFlags(blist)
		self.mapChanToSrcFreq()
		self.calcPhaseIncs()
		self.progRoach()

		self.data_mode = 1  

	###########################################################################
	#
	#
	###########################################################################
		
	def zeroPhaseIncs(self):
		

		self.phase_inc_array=[0.0] * 256
	
	
	###########################################################################
		
	def reprogPhaseIncs(self):
	
		self.calcPhaseIncs()
		self.progRoach()

	
		

	###########################################################################
	#
	#
	###########################################################################
		
	def calcPhaseIncs(self):
		#bins for each freq
		blist = self.getBinsFromFreqs(self.frequency_list)

		#bin center freqs
		bin_cf = self.getFreqsFromBins(blist)

		self.phase_inc_array=[0.0] * 256
	
		for k in range(len(blist)):
		    bin = blist[k]
		    binf=bin_cf[k];
		    f=self.frequency_list[k]
		    dphase = self.getPhasePerFFTNoPi(f)
		    chan = self.bin_to_chan[bin]
		    
		   
		    print "bin  %d  chan  %d freq  %fMHz  dphase %f*pi"%\
			(bin, chan, f/1e6,dphase)
		    #we now put the negative intot he phase acc, to cancle the phase change
		    self.phase_inc_array[chan]= dphase

	###########################################################################
	#
	#
	###########################################################################

	def extractSpectrum(self,spec_num):	
    	    

	    spectrum_P=zeros(self.fftLen)
	    spectrum_M=zeros(self.fftLen)

	    #iqdata is no longer 2 arrauys, but a dict.
	    #
	    if 1==1:
	      for chan in self.iqdata.keys():
		binx=self.chan_to_bin[chan][0]
		spectrum_P[binx]=self.iqdata[chan]['stream'][1][spec_num]
		spectrum_M[binx]=self.iqdata[chan]['stream'][0][spec_num]
	    else:
	      print "fftAnalzeri.extractSpectrum--bad spec_num"

	    #put in freq order. We have carrier or DC at bin fftLen/2. bins 0-fftLen/2 are
	    #right of DC. bins fftLen/2 are reverszed order (they are negative freqs), and put on left of DC.
	    left=spectrum_P[(self.fftLen/2):]
	    right=spectrum_P[:(self.fftLen/2)]
	    spectrum_P=numpy.concatenate((left,right))
	    

	    left=spectrum_M[(self.fftLen/2):]
	    right=spectrum_M[:(self.fftLen/2)]
	    spectrum_M=numpy.concatenate((left,right))

	    
	    return([spectrum_M,spectrum_P])
	    




	###########################################################################
	#
	# a record is ONE FFT, where bins are interleaved, in series. 
	#if we have 10 bins returnes, in old FW, then rec is 10 long.
	#in new Fw we have channelizer, where one chan is ONE fft bin.
	#so rec len is 1
	###########################################################################

	def getRecordLen(self):
		print "fftanalyzeri.getRecordLen- No records in the FW"

	###########################################################################
	#
	#
	###########################################################################
			
		
	    
	def getNumSpectra(self):
	    
	    
	    #famemlen-1 because of bug on last point in the memory.. fw bug
	    #for long spectra do not worry about last point... so dont do -1...
	    #if recordlen<200:
 	    #    nspectra= int(floor((self.memLen-1) / recordlen))
	    #else:
	    
	    try:
	        bin=self.iqdata.keys()[0]
	        nspectra=len(self.iqdata[bin]['stream'][0])
	    except: nspectra = 0
	    

	    return(nspectra)

	###########################################################################
	#
	#
	###########################################################################
			
		
		
	    
	def getNumSpectra2(self,chan):
	    
	    
	    #famemlen-1 because of bug on last point in the memory.. fw bug
	    #for long spectra do not worry about last point... so dont do -1...
	    #if recordlen<200:
 	    #    nspectra= int(floor((self.memLen-1) / recordlen))
	    #else:
	    
	    
	    nspectra=len(self.iqdata[chan]['stream'][0])
	    

	    return(nspectra)
	



#say we readback 20 bins. then we make time series of one of these bins.
	#We supply freq, that is the freq in Hz we soured. If we are actually reading ot that bin,
	#then we retrive all samples of that bin and return in polar coord
	def extractTimeSeries(self,freq):

	    binIQ=self.extractBinSeries(freq)

	    #convert to polar, mag and phase
	    bP=self.RectToPolar(binIQ)

	    
	    #bP[0]= bP[0] - bP[0][0]
	    
	    return(bP)	    


	###########################################################################
	#
	#
	###########################################################################
    
	
	def extractBinSeries(self,freq):

	    freq=self.getLegalFreqs([freq])[0]
	    #recordlen=self.getRecordLen()

	    
	    
 	    nspectra= self.getNumSpectra()
		
	    #find which bin in fft this freq cooresponds to
	    whichbin=self.getBinFromFreq(freq)
	    print whichbin
	    
	

	    aa=where(array(self.fft_bins_requested)==whichbin)[0]
	    if len(aa)==0:
		print "fftanayzeri.extractBinSeriesError- that freq not in  fft_bins_requested"
		return

	   
	    chan=self.bin_to_chan[whichbin]
	    print chan

  	    if self.iqdata.has_key(chan)==False:
		print 'fftanayzeri.extractBinSeries- ERROR - no data for that channel'
		return

	 

	    sP=self.iqdata[chan]['stream']
	    sR=self.PolarToRect(sP)

	    #
	    #extract the bin we want and make into a array, R and I.
	    #

	

	    return(sR)




	###########################################################################
	#
	#
	###########################################################################

		#set roach so all fft bins are returned
	def fftBinsAll(self):
	    self.fftBinFlags(range(256,512,1))
	    self.mapChanToSrcFreq()	
	    self.progRoach()

  	    self.data_mode = 2


	###########################################################################
	#
	#order of fft bins out of the fft block. counting from 0 to 511. output 0 gives 0,4,8,...
	#output 1 gives 1,5,9... output 2 gives 2,6,10..., output 3 gives 3,7,11 ...
	#
	#self.fft_bin_flags is calculated. it is array of len fftLen/4, or 128
	# we have 4 toutput of fft block, so bits 0 to 3 are flags for readout of each fft output.
	# buts 4 to 10 are channel number from 0 to 127. actauuly we onluy use 0 to 63, as we only 
	#have that may fifos per block. we have 2 blocks of 64 cgabels, so 
	#self.fft_bin_list, list of bins we are readng out, from 0 to 511. 
	#if we try to assign more then 128 bins to channels, then we will restart at chan 0.
	#so if we have blist of 256 bins, for 1/2 of FFT coef, (max possible for this fw) then
	#chan 0 get bin0 and bin 128, chan1 get bin1, bin129. these will be interleaved. so do not use
	#pulse finder mode. also need to have space in ffts, so set fftsynctime to 128*5 or so.
	#need SW to de-interleave the stuff
	###########################################################################



	def fftBinFlags(self,blist):
		
	
		#if self.isneg_freq==1:
		 #   blist = self.fftLen - blist -1
	
		
		self.fft_bins_requested=sort(blist)
		
		self.fft_bin_flags=[0] * 1024
		
		#this is for backwards compatibility- start and end freq are valid for
		#sweep fw, but not necessaryl for fft fw.
		freqs_=self.getFreqsFromBins(self.fft_bins_requested)
		self.startFreq_Hz=freqs_[0]
		

		
		self.endFreq_Hz = freqs_[len(freqs_)-1]
		#we just calc average incrFreq... it is correct for getting full fft
		#bins, but not for just selecting some bins at wierd freq intervals.    
		self.incrFreq_Hz=(self.endFreq_Hz - self.startFreq_Hz)/len(freqs_)
		
		
		
			

		#we must recalc fftbin list, so clear it.
		self.fft_bin_list=[]

		#here we assign fifo channels to each read out bin. start w/ 0
		#tghis is a bit complex:
		# we have four 64 chan fifosm, so the fifo chan in each fifo wants 6 bit address.
		#but we have 256 channels total w/ 4 fifos.
		# Another problem is that we cannot arbitraruoly assign fft bins to channels
		#for pos freq, 
		#
		#chans 0-63 is fifo0, 64-127 is fifo1, 128-191 is fifo2, 192-255 is fifo4
		#this is address in a fifo, 0 to 63 for foer the 4 fifos
		fifo_address=[0,0,0,0]	
		mapped_address=[0,0,0,0]
		#max fifo chan
		max_mapped_chan = 0;

		self.chan_to_bin4=dict()
			
		self.bin_to_chan=dict()
		self.chan_to_bin=dict()
		self.num_mapped_addresss=len(blist)
		#set flags that need to be set
		#binx in range(512), bin4 in range(128)
		#for binx 0,1,2,3,4,5,6, bin4 will be 0 0 0 0,1,1,1,1
		for binx in blist:
			
			self.fft_bin_list.append(binx)

			#we get 128 bins spit out of each fft output for 512 fft.
			#bin4 couns from 0 to 127 telling when our bin will spit out	
			bin4=(binx)>>2
			#this is which output of fft blobk the bin will com out.
			which_out = (binx%4)
			
			
			#we readout 4 coef at once in 4 fft outs.
			#0 gives 0,4,8
			#1 is 1,5,9
			#2 is 2,6,10
			#3 is 3,7,11

			#binx is the actual bin we want to readout.

			
			#keep track of already-set flags.
			fftwesync0=self.fft_bin_flags[bin4] &1
			fftwesync1=self.fft_bin_flags[bin4] &2
			fftwesync2=self.fft_bin_flags[bin4] &4
			fftwesync3=self.fft_bin_flags[bin4] &8
 
				
			mapped_address[0]=(self.fft_bin_flags[bin4]&0x000003f0)>>4
			mapped_address[1]=(self.fft_bin_flags[bin4]&0x0000fc00)>>10 
			mapped_address[2]=(self.fft_bin_flags[bin4]&0x003f0000)>>16 
			mapped_address[3]=(self.fft_bin_flags[bin4]&0x0fc00000)>>22
			

			#we houdl be setting fftwezunc 0,1,2,3 but becauswe we cannot
			#read both halves of coef in FW we just use 0 and 1
			#see commented lines below...
			if which_out==0: fftwesync0=1;
			elif which_out==1: fftwesync1=2;
			elif which_out==2: fftwesync2=4;
			else: fftwesync3=8;
			
			
			mapped_address[which_out]=fifo_address[which_out]
			fifo_address[which_out] = (fifo_address[which_out] + 1)%64
			
	
		
			mapped_channel=mapped_address[which_out] + (which_out<<6)
			
			
			self.bin_to_chan[binx]=mapped_channel
			if self.chan_to_bin.has_key(mapped_channel)==False:
				self.chan_to_bin[mapped_channel]=[]
				self.chan_to_bin4[mapped_channel]=[]


			self.chan_to_bin4[mapped_channel].append(bin4)
			self.chan_to_bin[mapped_channel].append(binx)
			

			if max_mapped_chan<mapped_channel: 
			    max_mapped_chan=mapped_channel


			#!!else:
			    #this happens when we have low fifo to a bin4, and hi fifo to same bin4.
			    #then we can reuse channels if 
			#!!    mapped_address= self.bin4_to_addr[bin4]
			    
			   
	
		    	#set flags for which fft outputs to read out to save to fifos.
			#current FW only pays atten to fftwesync0 and 1, so we cannot readout
			#bins 256 to 511 as of now.
			self.fft_bin_flags[bin4]=fftwesync0 +  fftwesync1 +fftwesync2 +fftwesync3;
				    

			
			self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[0]<<4)
			self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[1]<<10)
			self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[2]<<16)
			self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[3]<<22)

			
			
			
	    	
		self.fft_bin_list=sorted(self.fft_bin_list)
		
		
		self.last_chan_to_read=max_mapped_chan	

	###########################################################################
	#
	#
	###########################################################################
	
	def showBinFlags(self):
		for bin4 in range(self.dftLen):
		    if self.fft_bin_flags[bin4]>0:
			print "bin4 %d  addr3 %d  addr2 %d  addr1 %d  addr0 %d   wr3 %d  wr2 %d  wr1 %d  wr0 %d "%\
				(bin4, 
				(self.fft_bin_flags[bin4]&0x0fc00000)>>22, 
				(self.fft_bin_flags[bin4]&0x003f0000)>>16, 
				(self.fft_bin_flags[bin4]&0x0000fc00)>>10, 
				(self.fft_bin_flags[bin4]&0x000003f0)>>4, 
				self.fft_bin_flags[bin4]&8,
				self.fft_bin_flags[bin4]&4,
				self.fft_bin_flags[bin4]&2,
				self.fft_bin_flags[bin4]&1)	
	

	###########################################################################
	# called by progRoach
	#
	###########################################################################



	def progPhaseCorrect(self):
	
	    L=len(self.phase_inc_array)	
	    nchans = self.num_mapped_addresss
    	    bin_inc = self.toTwoComp(self.phase_inc_array,32,30)


	    self.roach.write_int('PhaseCorrect1_phaseIncProgWe', 2)
    	    for k in range(L):
			
		self.roach.write_int('PhaseCorrect1_phaseIncAddr', k)
    		self.roach.write_int('PhaseCorrect1_phaseIncVal', bin_inc[k])
	    	
	    	self.roach.write_int('PhaseCorrect1_phaseIncProgWe', 3)
	    	self.roach.write_int('PhaseCorrect1_phaseIncProgWe', 2)
		

  

   
            self.roach.write_int('PhaseCorrect1_phaseIncProgWe', 0)

	
	###########################################################################
	#
	#
	###########################################################################

	###########################################################################
	#
	#
	###########################################################################

	def setPulseDetector(self,plen,is_wr_raw):
		
		self.pulse_stretcher_length=plen
		self.is_write_raw_data=is_wr_raw

		roachlock.acquire()
		
		self.progRoach1()
		roachlock.release()




	###########################################################################
	#
	#
	###########################################################################

	def progPulseDetectorRAM(self):
	
		#PulseDetector_meanmagph32
		#PulseDetector_thresh32_1
		
	
		self.roach.write('PulseDetector_thresh32_1',
			self.convertToBinary(self.pulsedetector_thram));
		self.roach.write('PulseDetector_meanmagph32',
	
			self.convertToBinary(self.pulsedetector_muram));
	
	

			

	###########################################################################
	#
	#
	###########################################################################





	
	def calcPulseDetMeans(self):
		self.chan_to_meanth=dict()
		
		self.pulsedetector_muram=[0]*1024
		self.pulsedetector_thram=[0]*1024
		
		for chan in self.iqdata.keys():
		    mag=self.iqdata[chan]['stream'][0]
		    phs=self.iqdata[chan]['stream'][1]
		    
		    phs=self.removeTwoPi(phs)
		    
		    mag_mu=median(mag)
		    phs_mu=median(phs)/pi
		    
		    mag_std=std(mag)
		    phs_std=std(phs)/pi
		    
		    thresh= self.pulse_num_std*2*(mag_std + phs_std)
		    
		    mag_mub=self.toTwoComp([mag_mu],16,14)[0]
		    phs_mub=self.toTwoComp([phs_mu],16,13)[0]
		    thresh_b = self.toTwoComp([thresh],18,16)[0]
		    
		    self.pulsedetector_muram[chan] = mag_mub + (phs_mub*(1<<16))
		    self.pulsedetector_thram[chan]=thresh_b
		    
		    self.chan_to_meanth[chan] = [mag_mu,phs_mu,mag_std,phs_std,thresh]
		    
	
	
	def reCalcPulseDetMeans(self):
		
		self.pulsedetector_muram=[0]*1024
		self.pulsedetector_thram=[0]*1024
		
		for chan in self.chan_to_meanth.keys():
		   
		    mag_mu=self.chan_to_meanth[chan][0]
		    phs_mu=self.chan_to_meanth[chan][1]
		    
		    mag_std=self.chan_to_meanth[chan][2]
		    phs_std=self.chan_to_meanth[chan][3]
		    
		    
		    thresh= self.pulse_num_std*2*(mag_std + phs_std)
		    
		    mag_mub=self.toTwoComp([mag_mu],16,14)[0]
		    phs_mub=self.toTwoComp([phs_mu],16,13)[0]
		    thresh_b = self.toTwoComp([thresh],18,16)[0]
		    
		    self.pulsedetector_muram[chan] = mag_mub + (phs_mub*(1<<16))
		    self.pulsedetector_thram[chan]=thresh_b
		    self.chan_to_meanth[chan] = [mag_mu,phs_mu,mag_std,phs_std,thresh]
		   

	###########################################################################
	#
	#
	###########################################################################

	
	def measurePulseDetectorMeanThresh(self,is_prog=1):


		#clear output fifos and stop ffts
		self.clearFIFOs()
		#turn off pulse det, and collect raw nose data
		self.setPulseDetector(10,1);		


		#!!self.numFFTs(65536);
		self.numFFTs(54651);
		self.trigFFT()


		time.sleep(1.0)
		print 'getting mkid data'
		self.getDFT_IQ()

		self.calcPulseDetMeans()

		
		if is_prog:
		    self.progPulseDetector(self.pulse_num_std,1,10)
		
		
		self.printMeanTh()

	###########################################################################
	#
	#
	###########################################################################

	def printMeanTh(self):
		for ch in self.chan_to_meanth.keys():
		    print 'chan %d ampmean %6.5f phmean %6.5f thresh %6.5f'%\
		    	(ch,
			self.chan_to_meanth[ch][0],
			pi*self.chan_to_meanth[ch][1],
			self.chan_to_meanth[ch][4])
		
	

	###########################################################################
	#
	#
	###########################################################################


	def progPulseDetector(self,numthresh,is_use_pulse_det, pulselen):
		self.pulse_num_std=numthresh		
		self.reCalcPulseDetMeans()
		   
		roachlock.acquire()
		self.progPulseDetectorRAM()
		roachlock.release()
		self.setPulseDetector(pulselen,1-is_use_pulse_det);
			

	###########################################################################
	#
	#
	###########################################################################

	
	
	
	def getEventRate(self,waittimesec=0.5):
	
	    roachlock.acquire()
	   
	    cnt=roach.read_int('savedEventCounter')
	    fftcnt=roach.read_int('fftcounter_out')
	    
	    
	    time.sleep(waittimesec)
	    self.event_counter=roach.read_int('savedEventCounter')
	    
	    fftcnt2=roach.read_int('fftcounter_out')


	    self.events_per_sec= (self.event_counter - cnt)/waittimesec
	    ffts_sec=(fftcnt2-fftcnt)/waittimesec
	    
		
	    
	    roachlock.release()	
	    
	    
	    print 'ffts persec %f events persec %f'%(ffts_sec, self.events_per_sec)
	    
	    return(self.events_per_sec)	

	###########################################################################
	#
	#
	###########################################################################




	def calcRegs(self):
		
		self.test_freq=int((math.pow(2,30) * self.test_freq_hz)/(self.sys_clk))
		
		self.controlReg= (self.msm_rst<<0) 
		self.controlReg = self.controlReg + (self.startOutputDac<<4 ) 
		self.controlReg = self.controlReg + (self.st_fft_mem<<1) + (self.fft_mem_we<<2)
		self.controlReg = self.controlReg + (self.adcmem_start<<7) + (self.adcmem_wr<<8)
		self.controlReg = self.controlReg + (self.adcmem_sel<<9) + (self.adcfsync<<12)
		self.controlReg = self.controlReg + (self.adc_nloopback<<13)
		self.controlReg = self.controlReg + (self.seeaddress<<3)
		self.controlReg = self.controlReg + (self.dac_reset_bit<<15)

		self.controlReg = self.controlReg + (self.use_test_freq<<14)

		self.controlReg = self.controlReg + (self.dump_fifo<<16)
		
		self.controlReg = self.controlReg + (self.start_ffts<<6)

		self.controlReg = self.controlReg + (self.is_write_raw_data<<5)
		self.controlReg = self.controlReg + (self.clear_phase<<17)
		

		self.controlReg = self.controlReg + (self.isneg_freq<<19)
		self.controlReg = self.controlReg + (self.timestamp_reset<<20)
		self.controlReg = self.controlReg + (self.drop_all_events<<21)
		
		self.controlReg = self.controlReg + (self.fft_run_forever<<25)
		self.controlReg = self.controlReg + (self.reset_event_counter<<24)
		
		self.controlReg = self.controlReg + (self.flush_input_fifo<<26)
		
		
		

	



	###########################################################################
	#
	#
	###########################################################################


		
	def sendBinFlags(self):
		#clear the rams
	    try:
		#self.roach.write('BinData',self.convertToBinary16([0]*2048));
		
	
	
		self.roach.write('BinData',self.convertToBinary(self.fft_bin_flags));
		

		
	    except:
	        print "sendBinFlagsNo ROACH"

	###########################################################################
	#
	#
	###########################################################################



	def stopFFTs(self):
		
		roachlock.acquire()		
		self.fft_mem_we=0
		self.start_ffts=1 	
		self.progRoach1()
		roachlock.release()
		#self.setOutDacReg(0)
		

	###########################################################################
	#
	#
	###########################################################################


	def trigFFT(self):
		self.stopFFTs()
		self.clearFIFOs();
		#self.rewindFFTMem()
		
		self.clearCarry()
		self.clearEvents()
		self.trigFFT2()

	###########################################################################
	#
	#
	###########################################################################

	def enableReadChanFifos(self,is_enable):
		roachlock.acquire()
					
		self.dump_fifo = is_enable
		self.progRoach1()
		
		roachlock.release()



	###########################################################################
	# flush input fifos- should be done after ffts are stopped. 
	#
	###########################################################################

	
	def flushInputFifos(self):
	
		self.enableReadChanFifos(0)
	
		self.flush_input_fifo = 1;
		roachlock.acquire()
		self.progRoach1()
		time.sleep(0.001)
		self.flush_input_fifo = 0;
		self.progRoach1()
		roachlock.release()


	###########################################################################
	#
	#
	###########################################################################

	def getDataAvailable(self):
	
		#!!if fa.is_use_pulse_server: return(True)
		
		
		aa=self.printRegs(isprint=0)
		
		return(aa.MemRecordPolar_coefRamAddr>0)

	###########################################################################
	#
	#
	###########################################################################

	def enableWriteFFTMem(self,is_enable):
		roachlock.acquire()
		self.fft_mem_we=is_enable
	
		
		self.progRoach1()
		
	
		roachlock.release()


	###########################################################################
	#
	#
	###########################################################################

				
		
	def retrigFFT(self):
		self.stopFFTs()
		self.trigFFT2()



	###########################################################################
	# reset out mem addr to 0, so new write is done. leave mem in write mode
	# or non write mode whichever is already set
	###########################################################################

	def rewindFFTMem(self):
		#self.stopFFTs()
		roachlock.acquire()
		
		savewe=self.fft_mem_we
		self.fft_mem_we=0
		self.progRoach1()
		self.st_fft_mem=1 		
		self.progRoach1()
		
		self.st_fft_mem=0 		
		self.progRoach1()
		self.fft_mem_we=savewe
		self.progRoach1()
		#self.roach.write_int('numBinsStored',self.numBinsStored )
		roachlock.release()
	



	###########################################################################
	#
	#
	###########################################################################

	def recordEvents(self,is_rec=1):
	
		self.drop_all_events=1
		if is_rec ==1: self.drop_all_events=0
		roachlock.acquire()

		self.progRoach1()
		roachlock.release()

	
		
			

	###########################################################################
	# stop ffts, force readout of channel fifos into output fifo.
	# force dump of outfifo to out mem, rewind out mem. rewind ouyt mem, and turn 
	#off writing to out mem
	###########################################################################


	def clearFIFOs(self):
		
		#stop ffts so no data into chan fifos
		self.stopFFTs()
		
		#throw away what is in onput fifos. 
		self.flushInputFifos()
		
		
		rec_events=1 - self.drop_all_events
		self.recordEvents(0)

		self.enableWriteFFTMem(1)

		self.rewindFFTMem()

		#readout chan fifos
		#should be emopty so comment out...
		#leave here for older FW w/out fifo flush
		self.enableReadChanFifos(1)
		self.enableReadChanFifos(0)
	

		self.rewindFFTMem()
		self.rewindFFTMem()
		self.enableWriteFFTMem(0)
		
		self.recordEvents(rec_events)

	###########################################################################
	#
	#
	###########################################################################
	def resetPhaseAccum(self,is_rst=-1):

		roachlock.acquire()

		if is_rst==-1:
			self.clear_phase=1
			self.progRoach1()
			#time.sleep(0.1)

			self.clear_phase=0
			self.progRoach1()
			
		else:
			self.clear_phase=is_rst
			self.progRoach1()
			

		roachlock.release()
		

	###########################################################################
	#
	#
	###########################################################################

	def numFFTs(self,n):
		self.roach_num_ffts=n
		roachlock.acquire()
		self.roach.write_int('numffts',self.roach_num_ffts)
		roachlock.release()
	###########################################################################
	#
	# enable writing to fft mem, pulse start fft 1, 0. 
	###########################################################################

	

	def trigFFT2(self):
	    
	
	    roachlock.acquire()
	    
	    try:
	

		self.clear_phase=1
		self.progRoach1()


		self.clear_phase=0
		self.progRoach1()

		time.sleep(0.001)
		
		if self.is_use_pulse_server==False:
			self.fft_mem_we=1
		else:
		 	self.fft_mem_we=0
	
		self.start_ffts=1 
		self.dump_fifo	=1
		self.progRoach1()
		
		self.start_ffts=0
				
		self.progRoach1()
		
	    except:
	        print "trigFFT2 NO ROACH"
	    
	    roachlock.release()

	
	###########################################################################
	#
	#
	###########################################################################
	

	def resetDAC(self):

	    roachlock.acquire()
	    print "Reset Dac"
    	    self.msm_rst=1
	    self.dac_reset_bit=1
	    self.startOutputDac=0
	    self.progRoach1()

	    self.dac_reset_bit=0
     	    self.msm_rst=0
	    self.startOutputDac=1
	    self.progRoach1()
	    roachlock.release()



	###########################################################################
	#
	#
	###########################################################################

	def progRoach(self):
	    
	    self.calcRegs()	
		
	    if self.is_print==1:
		msg='controlReg %d\n'%(self.controlReg)
		print msg
	    
	    roachlock.acquire()
	    if 1==1:
		
		self.roach.write_int('controlReg', self.controlReg)

		#self.roach.write_int('testFreq', int(self.test_freq))

		self.roach.write_int('lastChanToRead', self.last_chan_to_read)

		

		self.roach.write_int('PulseDetector_pulselength', self.pulse_stretcher_length)

		self.progPulseDetectorRAM()

		#!!self.roach.write_int('dram_controller', 0)
		
		#1 to stop lut playback
		self.roach.write_int('holdcounter', self.holdcounter)
		#1 to erase lut dram
		self.roach.write_int('resetDRAM', self.resetDRAM)
		
		#need to write -1 because of = in the fpga code...
		self.roach.write_int('fftsynctime',self.fftsynctime-1);
	
		
		self.roach.write_int('fftshift',self.roach_fft_shift)

		self.roach.write_int('numffts',self.roach_num_ffts)
		
		#needs to be 1 all times. we readn in FW. SW interface writes it...
		#1 for readout dram
		self.roach.write_int('RWen', 1)
		self.roach.write_int('LUTsize', self.lut_length8)
		
		#self.roach.write('dram_memory', self.lut_binaryIQ)
		
		#self.big_write(self.lut_binaryIQ)
		self.startOutputDac=0
		self.calcRegs();
		
		self.roach.write_int('controlReg', self.controlReg)
		
		self.startOutputDac=1
		self.calcRegs();
		
		self.roach.write_int('controlReg', self.controlReg)
		
		
		
		self.sendBinFlags()
		
		self.progPhaseCorrect()
		
	

	    else:
	        print "progRoach NO ROACH"

	    roachlock.release()
	           

	###########################################################################
	#
	#
	###########################################################################

	def printRegs(self,isprint=1, isplot=0):
		#roachlock.acquire()
		
		
		#create inline class
		class inline: pass
		
		
		regdata=inline()
		
		
		regdata.at= ccopy.deepcopy(at)
		regdata.rf=ccopy.deepcopy(rf)
		
		regdata.LO=ccopy.deepcopy(LO)
		regdata.s=ccopy.deepcopy(s)
		
		#try:
		if 1==1:
		    regs=[ 'controlReg','fftcounter_out','fftshift','fftsynctime','holdcounter',
			    'if_switch','numffts','stffts_fsm','statusFlags','LUTsize',
			    'MemRecordPolar_coefRamAddr','RWen',
			    'bincount_out','timestamp_out','lastChanToRead','PulseDetector_pulselength',
			    'readoutControl','readoutStat','fifoOverFlowCnt','savedEventCounter']

		    for rr in regs:
		    	val=roach.read_int(rr)
			if isprint==1: print '%s  0x%x, %d'%(rr, val,val)
			exec('regdata.%s=%d'%(rr,val))



		    crval=roach.read_int('controlReg')
		    crbits=['mainRst','stFFTMem','fftMemWE','seeaddress','startDac','is_write_raw_data',
		    'startFFTs','adcwavememStart','adcwavememWE','adcwavememSel','unused','unused',
		    'adcforcesync','dacLoopBack','useTestFreq','resetDAC','dumpFIFO','clearPhase','unused',
			'is_neg_freq','timestamp_reset','drop_all_events','bitToDS0','bitToDS1',
			'reset_event_counter', 'fft_run_forever','flush_input_fifo']
	





		    if isprint==1: print '\nControReg Bits\n'
		    bitlist=[]
		    for k in range(len(crbits)):
			mask=1<<k
			if isprint==1: print '    Bit:%d %s  %d'%(k, crbits[k], crval&mask)
			bitlist.append((k,crbits[k],crval&mask))
			
		    regdata.bitlist = bitlist
		    

		    stval=roach.read_int('statusFlags')
		    stbits=['outMemDone','adcwavememDone','adcvalid','run_ffts','fifo_data_full','fifo_data_avail',
		    'is_pulse','fftcntdone','bitFromDS3','bitFromDS2','bitFromDS1','bitFromDS0']

		    if isprint==1: print '\nStatus Flags \n'
		    statbits=[]
		    for k in range(len(stbits)):
			mask=1<<k
			if isprint==1: print '    Bit:%d %s  %d'%(k, stbits[k], stval&mask)
			statbits.append((k, stbits[k], stval&mask))

		    regdata.statbits=statbits
		    
		    
		    if isplot>0:

			#reg name, char len, type, tyoe len
			mems=[('BinData',2048*2,'H',2048),	    	      
			      ('MemRecordPolar_Shared_BRAM',32768*4,'I',32768) ]


			for k in range(len(mems)):
		            if isprint==1: figure(k+1);clf();
			    if isprint==1: print mems[k]
		            a=struct.unpack('>' + mems[k][2]*mems[k][3],roach.read(mems[k][0],mems[k][1]))
		            if isprint==1: plot(a)
		            if isprint==1: title(mems[k][0])
			    
			    exec('regdata.%s=a'%(mems[k][0]))


		else:
		    pass
		#except:
			
			
		
		
		#roachlock.release()
		return(regdata)

	def convertToBinary16(self,data1):
	    """ Converts  data points to 16-bit binary .

        	@param data             Decimal data to be converted  for FPGA.
        	"""
	    binaryData = ''
	    for i in range(0, len(data1)):
        	x = struct.pack('>H', data1[i])
        	binaryData = binaryData + x

	    return binaryData

	    	





	def calcLineFPGADelay(self):
	
		
		
		#we di bit want bin center freq. we want the sourced freqs...
		# we have higher freq resolution in the lut than we do in the fft.
		#sourced freqs, and hence phase delay, are based on actual sourced freq.
		#sourced freqs are not in bin centers
		
		
		#get center freq of bins
		flist1 = self.getFreqsFromBins(self.fft_bins_requested)
		
		#get freqs we source...
		flist2 = self.frequency_list
		
		#if we are asking for all bins, then let flist be the ffr bins.
		if len(flist1)>len(flist2):
		    flist = flist1
		else:
		    #if we are getting just freqs of interest, then we use the sourced frequencuies
		    flist = flist2
		
		
		flist = numpy.array(flist)

		if self.isneg_freq:
		    #freqs=-2*pi*  (self.carrierfreq - flist)
		    freqs=2*pi*  (self.carrierfreq - flist)
		else:
		    freqs=2*pi*  (self.carrierfreq + flist) 
	

		self.phasesRe=numpy.cos(freqs*self.xmission_line_delay + flist*self.firmware_delay)
		self.phasesIm = numpy.sin(freqs*self.xmission_line_delay + flist*self.firmware_delay)
		
		self.freq_to_linedel_phase = dict()
		for k in range(len(flist)):
		    f=flist[k]
		    p=[self.phasesRe[k], self.phasesIm[k]]
		    self.freq_to_linedel_phase[f] = p
			

	def calcLineDelay(self):
	
		
		
		#we di bit want bin center freq. we want the sourced freqs...
		# we have higher freq resolution in the lut than we do in the fft.
		#sourced freqs, and hence phase delay, are based on actual sourced freq.
		#sourced freqs are not in bin centers
		
		if self.data_mode == 2:
		    #get center freq of bins
		    flist = self.getFreqsFromBins(self.fft_bins_requested)
		
		else:
		    #get freqs we source...
		    flist = self.frequency_list
		
		binlist = self.getBinsFromFreqs(flist)
		
		flist = numpy.array(flist)

		if self.isneg_freq:
		    #freqs=-2*pi*  (self.carrierfreq - flist)
		    freqs=2*pi*  (self.carrierfreq - flist)
		else:
		    freqs=2*pi*  (self.carrierfreq + flist) 
		
		
		
		
		self.phasesRe=   numpy.cos(freqs*self.xmission_line_delay)
		self.phasesIm=   numpy.sin(freqs*self.xmission_line_delay)


		self.freq_to_linedel_phase = dict()
		for k in range(len(flist)):
		    f=flist[k]
		    bin=binlist[k]
		    chan = self.bin_to_chan[bin]
		    p=[self.phasesRe[k], self.phasesIm[k]]
		    self.freq_to_linedel_phase[f] = p
		    self.chan_to_linedel_phase[chan]=p
			

	def calcLineSweepDelay(self,iqp,bbfreq):
	
			
		#we di bit want bin center freq. we want the sourced freqs...
		# we have higher freq resolution in the lut than we do in the fft.
		#sourced freqs, and hence phase delay, are based on actual sourced freq.
		#sourced freqs are not in bin centers
		
		
		carr=arange(self.start_carrier,self.end_carrier,self.inc_carrier)
		if self.isneg_freq==1:
			freqs=carr - bbfreq
		else:
			freqs=carr + bbfreq
		
		ft=freqs*self.xmission_line_delay;
		ft = ft - floor(ft);
		
		iqp[1] = iqp[1] + 2*pi*ft;
	
		


		return(iqp)
	



	
	#applues dekat to cur iqdata

	
	
	def applyDelay(self,sign):
		self.calcLineDelay()
		
		
		print "apply delay"

		phasep=self.RectToPolar([self.phasesRe,self.phasesIm]);
		
		
		
		for chan in self.iqdata.keys():
		    if self.chan_to_linedel_phase.has_key(chan):
			
		    
		    	phase=self.chan_to_linedel_phase[chan]
		    	phaseP=self.RectToPolar(phase)[1]
			
			if self.iqdata[chan].has_key('phase'):
		    	    self.iqdata[chan]['phase']= self.iqdata[chan]['phase'] + sign* phaseP
			else:
			    self.iqdata[chan]['phase']=  sign* phaseP
		    	#add phase to each event:
		    	#!!for event in self.iqdata[chan]['events']:
			#!!	event[1] = event[1] + phaseP
		   
		    
		    	self.iqdata[chan]['stream'][1] = self.iqdata[chan]['stream'][1] + sign*phaseP
		    
		
	
	
	def removeLineDelay(self):
		
		
		self.applyDelay(-1.0) 
		
	def erfplot(self):

		figure(1)
		L=1024
		A=2.0
		c=1.5
		ph= 4*(2*pi)* arange(L)/L; 	
		aa=A*cos(ph);
		clf()
		plot(aa)
		clip=c * scipy.special.erf(aa/c);
		plot(clip)

		figure(2)
		plot(abs(fft.fft(aa))[:L/2])
		plot(abs(fft.fft(clip))[:L/2])


		

	def testsin(self,L,N,A,clipfactor):
	
	    aa=zeros(L)
	    for k in range(N):
		ph= floor(rand()*(L/2))*(2*pi)* arange(L)/L; 
		ph = ph + rand()*2*pi
		aa=aa + A*cos(ph);

	    

	    figure(1);
	    clf();
	    plot(aa[:128]);
	    print "maxabs %f "%(numpy.max(abs(aa)))
	    figure(2);
	    clf()
	    plot(abs(fft.fft(aa))[:L/2])

	    figure(1);
	    aasc=aa*(A/numpy.max(abs(aa)))
	    plot(aasc[:128])

	    figure(2);
	    clf()
	    F=abs(fft.fft(aa))/L
	    F=F*F
	    
	    plot(F[:L/2])
	    yscale('log')
	    ylim((1e-6,1.0))


	    figure(3);
	    clf()
	    Fsc=abs(fft.fft(aasc))/L
	    Fsc=Fsc*Fsc
	   
	    plot(Fsc[:L/2])
	    yscale('log')
	    ylim((1e-6,1.0))



	    #now clip amplitudes:
	    clip=A * scipy.special.erf(aa/(clipfactor*A));

	    figure(4);
	    clf()
	    plot(clip[:128]);


	    print "max %f min %f"%(numpy.max(aa),numpy.min(aa))
	    figure(5);
	    clf()
	    Fcl=abs(fft.fft(clip))/L
	    Fcl=Fcl*Fcl
	    plot(Fcl[:L/2])
	    yscale('log')
	    ylim((1e-6,1.0))





	###########################################################################
	#
	#
	###########################################################################


	def grabData3(self):
	    self.thread_running=1
	     
	    
	    self.progRoach()
	    self.clearFIFOs()
 	    self.numFFTs(65536)
   	    for k in range(self.numSweeps):
	    	print "Trigger sweep"
		
		self.trigFFT();
		time.sleep(.5)
		
		if self.thread_running==0:
			print "Ending Loop/Thraed"
			sweepCallback()
			return

		
		iq=self.getDFT_IQ();

		self.rewindFFTMem()

		sweepCallback()
		time.sleep(.5)
			
		self.sweepcount=self.sweepcount+1
		
		#if self.is_add_noise_2_res==1:
		#    self.addNoise2ResData()




	




	###########################################################################
	# more or less debugging cmds- 
	#
	###########################################################################

	def openStreamHdf(self,fname,_sw=False,_sec=-1):
	
	   
	    self.fft_mem_we=0
	    self.progRoach1()
		
		
	    self.is_use_pulse_server=True
	    self.createHdfStreamFile(fname,savesweeps=_sw)
	    os.system('./startpulse hdf %s %d'%(fname,_sec))






	
	def closeStream(self):
	    self.is_use_pulse_server=False
	    os.system(' pkill -INT  nc')
	    os.system(' pkill -INT  -f startrpulse')

	

	###########################################################################
	#
	#
	###########################################################################

	def captureStream(self,fname,sec,_savesw=False):
	    self.clearFIFOs()
	    self.numFFTs(sec*1e6)
	    
	    self.openStreamHdf(fname,_sw=_savesw,_sec=sec)
	    
	    self.trigFFT()
	    
	    time.sleep(sec+5)
	    
	    self.closeStream()
	    
	    
	

	
	
	###########################################################################
	# 
	###########################################################################


	def createHdfStreamFile(self,name,savesweeps=False):
	

	    chans=fa.chan_to_bin.keys()
	    chanlist=''
	    for k in range(len(chans)):

		chanlist = chanlist + '%d'%(chans[k])
		if k<(len(chans)-1):
	            chanlist = chanlist + ','

	    os.system('bin2hdf5 -chans %s %s < /dev/null'%(chanlist, name))

	    fp = h5py.File(name,'a')
	  
	    #cycle thry each  channel, should have groups for each
	    
	    for ch in chans:
	        fp['Chan_%05d'%(ch)]['magnitude'].attrs.create('bin',self.chan_to_bin[ch])
	        fp['Chan_%05d'%(ch)]['magnitude'].attrs.create('srcfreq',self.chan_to_srcfreq[ch])
	        fp['Chan_%05d'%(ch)]['magnitude'].attrs.create('lo',self.carrierfreq)
		#!! need to cheak is_neg)freq0 we always use neg, but need to chaek... 
	        fp['Chan_%05d'%(ch)]['magnitude'].attrs.create('rffreq',self.carrierfreq-self.chan_to_srcfreq[ch])
		fp['Chan_%05d'%(ch)]['magnitude'].attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
		


	        fp['Chan_%05d'%(ch)]['phase'].attrs.create('bin',self.chan_to_bin[ch])
	        fp['Chan_%05d'%(ch)]['phase'].attrs.create('srcfreq',self.chan_to_srcfreq[ch])
	        fp['Chan_%05d'%(ch)]['phase'].attrs.create('lo',self.carrierfreq)
	        fp['Chan_%05d'%(ch)]['phase'].attrs.create('rffreq',self.carrierfreq-self.chan_to_srcfreq[ch])
		fp['Chan_%05d'%(ch)]['phase'].attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))		   
															   	   
	    #if no settings, we except, and add settings dir
	    try:
	        fp['settings'].keys()	
	    except:	    		
	        mysettings = self.getObjSpecs()
	        self.hdfWriteObj(fp,'settings', mysettings)
	
	
	    if savesweeps:
		#if no settings, we except, and add settings dir
		try:
	            fp['sweeps'].keys()	
		except:
		    i=0;
	            swp=fp.create_group('sweeps')
		    swp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
		    
		    for m in self.fft_mkid_list:
	    		m.reslist[0].writeHDF(swp,i);
			i=i+1	
	              

	
	    
			
	    fp.close()
	    
	


	###########################################################################
	# sweep and take data. you must set carrier freq correctly, and set up
	# all channels, src freqs etc. 
	###########################################################################

	
	def sweepAndStream(self,fname,sec,is_pulsedet):
		

		span=1e6
		pts=50
		cnt=0
		
			

		self.fft_mkid_list=[]
		for ch in self.chan_to_srcfreq.keys():
		    ff=   self.carrierfreq - self.chan_to_srcfreq[ch]	    
		    self.fft_mkid_list.append(MKID(cnt, self.device_name,ff))
		    cnt=cnt+1


		#self.is_sweep_several=1    
		self.sweepResonators(self.fft_mkid_list,span,pts)


		#self.is_sweep_several=0    

		try:
		    for m in self.fft_mkid_list: #loops through list of resonators
			fit.resonator=m.reslist[0]
			fit.reslist=m.reslist
			fit.fit_circle2(); #fit a circle to data
			fit.trans_rot2(); #move coordinate system to center of circle
			fit.IQvelocityCalc()
		except:
		    print "prob w/ fit"
	
		#self.calcPhaseIncs()
		#self.progRoach()

		#use the 1st mkid to find correct carrier... no recalc yet a bit bad...
		#assume neg sideband...
		carr=self.fft_mkid_list[0].reslist[0].maxIQvel_freq + self.fft_mkid_list[0].reslist[0].sweep_fbase

		self.setCarrier(carr)
		
		
			
		#if pulse det enabnled, get mean signal for channels
		if is_pulsedet==1:
		    self.setPulseDetector(self.pulse_stretcher_length,0);
		    self.measurePulseDetectorMeanThresh()

		    print "Capturing jonly pulses, measured signal means"
			
		else:
		    self.setPulseDetector(self.pulse_stretcher_length,1);
		    print "calturing all data. noise and pulses"
			
		
		self.captureStream(fname,sec,_savesw=True)
		self.setUsePulseServer(0)

		
	#set up the frequencies and bins for fftanal for this list of mkids. 
	#make copies of mkids	
	def fftAnalSetupFromMlist(self,mlist):
	
		self.clearFIFOs();
	
		self.fft_mkid_list=[]
		fc_s=[]
		cnt = 0
		for mkid in mlist:
		    #get rough ctne freq, or fitted freq, if available
   		    fc=mkid.getFc2()
		    fc_s.append(fc)
		    

		fc_s=numpy.sort(fc_s)

		frange=max(fc_s) - min(fc_s)
		if (frange>200e6):
		    print "resonators too far apart, cannot sweep all of them"
		    return


		# we have wierd number so we don't have nice number of sines. We always then have some freq error based
		#based on wave tablelen. could use 10MJz, bit too nice.
		carr=max(fc_s)+10109375

		freqs=carr-fc_s
		freqs = freqs[::-1]

		print "carrier freq %d"%(carr)
		print "Base Freqs"
		print freqs
		print "Res Freqs "
		print fc_s

		self.setLutFreqs(freqs,32500.0/len(freqs))
		self.fftBinsFreqs()
		self.progRoach()		
		progAtten(roach,at)
		progRFSwitches(roach,rf)
		















	
	def sweepAndStream2(self,fname,sec,is_pulsedet, mlist):
		
		
		
		
			
			
		span=1e6
		pts=50
		cnt=0
		
			
		self.fft_mkid_list=[]
		for m in mlist:
		    
		    
		    ff=m.getFc2()
		    
		
		    
		    
		    self.fft_mkid_list.append(MKID(cnt, self.device_name,ff))
		    cnt=cnt+1
		

		#self.is_sweep_several=1    
		self.sweepResonators(self.fft_mkid_list,span,pts)


		

		for m in self.fft_mkid_list: #loops through list of resonators
		    fit.resonator=m.reslist[0]
		    fit.reslist=m.reslist
		    fit.fit_circle2(); #fit a circle to data
		    fit.trans_rot2(); #move coordinate system to center of circle
		    fit.IQvelocityCalc()

		#self.reprogPhaseIncs()
		
		#use the 1st mkid to find correct carrier... no recalc yet a bit bad...
		#assume neg sideband...
		carr=self.fft_mkid_list[0].reslist[0].maxIQvel_freq + self.fft_mkid_list[0].reslist[0].sweep_fbase

		self.setCarrier(carr)
	
		
			
		#if pulse det enabnled, get mean signal for channels
		if is_pulsedet==1:
		    self.setPulseDetector(self.pulse_stretcher_length,0);
		    self.measurePulseDetectorMeanThresh()

		    print "Capturing jonly pulses, measured signal means"
			
		else:
		    self.setPulseDetector(self.pulse_stretcher_length,1);
		    print "calturing all data. noise and pulses"
			
		
		
		self.captureStream(fname,sec,_savesw=True)
		self.setUsePulseServer(0)
	   