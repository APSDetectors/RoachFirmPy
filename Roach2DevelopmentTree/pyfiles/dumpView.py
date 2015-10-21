

###########################################################################################
#
#
#
#aa=3
#
#
###########################################################################################






class dumpView:



    def __init__(self,pname,fnum):	
	global MKID_list
	
	#fa.hdfOpenR('/local/tmadden/data/newdev/newdev_sweeps',222)
	#fa.iq_index=993
	#fa.hdfOpenR('/local/tmadden/data/newdev/newdev_sweeps',210)
	#fa.iq_index=26
	fa.hdfOpenR(pname,fnum)
	fa.iq_index=0
	
	#mkidLoadData('/local/tmadden/data/newdev/resdata14.h5')
	#resdata=MKID_list[0].reslist[0]
	#resdata.info()
	#self.is_circle=True;
	self.is_circle=False;
	
	
	
	self.pulse_data=[]
	fa.I_raw = [zeros(200), zeros(200)]
	
	
	self.numptraces=25
	
	self.specnum=1;
	
	self.dmode='raw'
	
	self.wdata = 'raw'
	
	self.channel_number=0
	self.cirnoise_bbtau=0.0
	self.cirsweep_bbtau=0.0
	
	self.cirnoise_rftau=0.0
	self.cirsweep_rftau=0.0


	self.fpga_bug_offset_=0;
	
	if 1==1:
	    for k in range(500000):
		
		fa.hdfReadIQ()
		
		if self.wdata=='raw':
		   
		    fa.iqdata=fa.I_raw
		
		
		fa.fpga_bug_offset= self.fpga_bug_offset_
		
		if len(fa.frequency_list)<self.channel_number:
		    self.channel_number=0;
		    print "reset channel num 0"
		
		print "N Chans %d"%(len(fa.frequency_list))
		
		print "I_raw vector"
		
		
		if self.dmode=='raw':
		    
		    iqp=fa.RectToPolar(fa.iqdata)
		   
		if self.dmode == 'ts':
		   
		   
		    iqp=fa.extractTimeSeries(fa.frequency_list[self.channel_number])
		    
		

		if self.dmode == 'bs':
		    
		   
		    iq=fa.extractBinSeries(fa.frequency_list[self.channel_number])
		    iqp=fa.RectToPolar(iq)
		    

		if self.dmode == 'spec':
		   
		  
		    iqp=fa.extractSpectrum(self.specnum)
		    
		   
		
			
		
		    
		figure(1)
		clf()
		subplot(2,1,1)
		plot(iqp[0])
		subplot(2,1,2)
		plot(iqp[1])
		draw()
		
		
		if self.is_circle:
		    iq_tr=fit.trans_rot3(resdata, fa.PolarToRect(iqp))
		    iqp_tr=fa.RectToPolar(iq_tr)
		    
		    figure(3)
		    clf()
		    subplot(2,1,1)
		    plot(iqp_tr[0])
		    subplot(2,1,2)
		    plot((180.0/pi)*iqp_tr[1])
		    draw()
		    
		    figure(4);clf()

		    plot(resdata.trot_xf,resdata.trot_yf)
		    
		   
		    plot(iq_tr[0],iq_tr[1],'.')


		
		print fa.iq_index-1
		
		print 'BB Freqs'
		print fa.frequency_list
		print "LO %f "%(fa.carrierfreq)
		print "Actual freqs"
		print (fa.carrierfreq - numpy.array(fa.frequency_list) )
		

		print("hdfView>>"),
		tt=raw_input()
		
		stat=self.execute(tt)
		
##########################################################
#
#
#
###########################################################
	
    def drawGui(self,form):
    	self.creatWidgets(form)
	
	return(self.drawWidgets(form))
	
##########################################################
#
#
#
###########################################################
	
	
	
	
    def creatWidgets(self,form):
 
    #run sweeps and fits and noise. 
            
    	
    	form.button_dump_keys = QPushButton("keys")
	form.connect(form.button_dump_keys, SIGNAL('clicked()'), self.keys)
	    
	  
	form.button_dump_minus = QPushButton("-")
	form.connect(form.button_dump_minus, SIGNAL('clicked()'), self.back)
	 
	form.button_dump_r = QPushButton("r")
	form.connect(form.button_dump_r, SIGNAL('clicked()'), self.raw)  
	    
	form.button_dump_getiq = QPushButton("getiq")
	form.connect(form.button_dump_getiq, SIGNAL('clicked()'), self.getiq)
	
	form.button_dump_getraw = QPushButton("getraw")
	form.connect(form.button_dump_getraw, SIGNAL('clicked()'), self.getraw)
	
	form.button_dump_ts = QPushButton("ts")
	form.connect(form.button_dump_ts, SIGNAL('clicked()'), self.ts)
    
    
    	form.button_dump_bs = QPushButton("bs")
	form.connect(form.button_dump_bs, SIGNAL('clicked()'), self.bs)  
	  
	  
	form.button_dump_nbbtime = QPushButton("nbbtime")
	form.connect(form.button_dump_nbbtime, SIGNAL('clicked()'), self.nbbtime)
	  
	form.button_dump_nrftime = QPushButton("nrftime")
	form.connect(form.button_dump_nrftime, SIGNAL('clicked()'), self.nrftime)
		
		
	form.button_dump_sbbtime = QPushButton("sbbtime")
	form.connect(form.button_dump_sbbtime, SIGNAL('clicked()'), self.sbbtime)	
		
	form.button_dump_srftime = QPushButton("srftime")
	form.connect(form.button_dump_srftime, SIGNAL('clicked()'), self.srftime)	
		
	form.button_dump_nrftime = QPushButton("nrftime")
	form.connect(form.button_dump_nrftime, SIGNAL('clicked()'), self.nrftime)
		
		
	form.button_dump_spec = QPushButton("spec")
	form.connect(form.button_dump_spec, SIGNAL('clicked()'), self.spec) 	
		
		
	form.button_dump_specnum = QPushButton("specnum")
	form.connect(form.button_dump_specnum, SIGNAL('clicked()'), self.specnum)		
		  
		  
	form.button_dump_p = QPushButton("p")
	form.connect(form.button_dump_p, SIGNAL('clicked()'), self.p)
		
	form.button_dump_offs = QPushButton("offs")
	form.connect(form.button_dump_offs, SIGNAL('clicked()'), self.offs)
	
	form.button_dump_python = QPushButton("python")
	form.connect(form.button_dump_python, SIGNAL('clicked()'), self.python)
	
	form.button_dump_field = QPushButton("field")
	form.connect(form.button_dump_field, SIGNAL('clicked()'), self.field)
		
	form.button_dump_pltpls = QPushButton("pltpls")
	form.connect(form.button_dump_pltpls, SIGNAL('clicked()'), self.pltpls)
		
	form.button_dump_th = QPushButton("th")
	form.connect(form.button_dump_th, SIGNAL('clicked()'), self.th)
		  
	form.button_dump_info = QPushButton("info")
	form.connect(form.button_dump_info, SIGNAL('clicked()'), self.info)
	
	form.button_dump_np = QPushButton("np")
	form.connect(form.button_dump_np, SIGNAL('clicked()'), self.np)
		
	form.button_dump_nc = QPushButton("nc")
	form.connect(form.button_dump_nc, SIGNAL('clicked()'), self.nc)
	
	form.button_dump_n = QPushButton("n")
	form.connect(form.button_dump_n, SIGNAL('clicked()'), self.n)
	
	form.button_dump_cirnoise = QPushButton("cirnoise")
	form.connect(form.button_dump_cirnoise, SIGNAL('clicked()'), self.cirnoise)
	
	form.button_dump_cirsweepall = QPushButton("cirsweepall")
	form.connect(form.button_dump_cirsweepall, SIGNAL('clicked()'), self.cirsweepall)
	
	form.button_dump_cirsweep = QPushButton("cirsweep")
	form.connect(form.button_dump_cirsweep, SIGNAL('clicked()'), self.cirsweep)
	
	form.button_dump_lut = QPushButton("lut")
	form.connect(form.button_dump_lut, SIGNAL('clicked()'), self.lut)
	
	form.button_dump_clf = QPushButton("clf")
	form.connect(form.button_dump_clf, SIGNAL('clicked()'), self.clf)
##########################################################
#
#
#
###########################################################
	
		

    def drawWidgets(self,form):
     	tabcols = QHBoxLayout()
    	
	col1== QVBoxLayout()
	col1.addWidget(form.button_dump_keys )
	 
	    
	  
	col1.addWidget(form.button_dump_minus)
	 
	 
	col1.addWidget(form.button_dump_r )
	 
	    
	col1.addWidget(form.button_dump_getiq )
	 
	
	col1.addWidget(form.button_dump_getraw )
	 
	
	col1.addWidget(form.button_dump_ts )
	 
    
 	col2== QVBoxLayout()
    	col2.addWidget(form.button_dump_bs )
	 
	  
	  
	col2.addWidget(form.button_dump_nbbtime )
	 
	  
	col2.addWidget(form.button_dump_nrftime )
	 
		
		
	col2.addWidget(form.button_dump_sbbtime )
	 
		
	col2.addWidget(form.button_dump_srftime )
	 
		
	col2.addWidget(form.button_dump_nrftime )
	 
	
	col3== QVBoxLayout()	
		
	col3.addWidget(form.button_dump_spec )
	 
		
		
	col3.addWidget(form.button_dump_specnum )
	 
		  
		  
	col3.addWidget(form.button_dump_p )
	 
		
	col3.addWidget(form.button_dump_offs )
	 
	
	col3.addWidget(form.button_dump_python )
	 
	
	col3.addWidget(form.button_dump_field )
	 
		
	col4== QVBoxLayout()	
	
	col4.addWidget(form.button_dump_pltpls )
	 
		
	col4.addWidget(form.button_dump_th )
	 
		  
	col4.addWidget(form.button_dump_info )
	 
	
	col4.addWidget(form.button_dump_np )
	 
		
	col4.addWidget(form.button_dump_nc )
	 
	
	col4.addWidget(form.button_dump_n )
	 
	
	col5== QVBoxLayout()	
	
	col5.addWidget(form.button_dump_cirnoise )
	 
	
	col5.addWidget(form.button_dump_cirsweepall )
	 
	
	col5.addWidget(form.button_dump_cirsweep )
	 
	
	col5.addWidget(form.button_dump_lut )
	 
	
	col5.addWidget(form.button_dump_clf )
	 
	tabcols.addLayout(col1)
	tabcols.addLayout(col2)
	tabcols.addLayout(col3)
	tabcols.addLayout(col4)
	tabcols.addLayout(col5)
    	
	return(tabcols)	
		
##########################################################
#
#
#
###########################################################
	


    def execute(self,tt):			
    	stat=True
	
	if tt=='keys':
	    self.keys()
	    
	if tt=='q':
	    stat=self.close()      
	    
	if tt=='-': self.back()
	 
	if tt=='r' :self.raw()  
	    
	if tt=='getiq' :    self.getiq()
	
	if tt=='getraw' : self.getraw()
	
	if tt=='ts': self.ts()
	  
	if tt=='bs': self.bs()  
	  
	  
	if tt=='nbbtime': self.nbbtime()
	  
	if tt=='nrftime': self.nrftime()
		
		
	if tt=='sbbtime': self.sbbtime()	
		
	if tt=='srftime': self.srftime()	
		
	if tt=='nrftime': self.nrftime()
		
		
	if tt=='spec': self.spec() 	
		
		
	if tt=='specnum': self.specnum()		
		  
		  
	if tt=='p': self.p()
		
	if tt=='offs': self.offs()
	if tt=='python': self.python()
	if tt=='field': self.field()
		
	if tt=='pltpls': self.pltpls()
		
	if tt=='th': self.th()
		  
	if tt=='info': self.info()
	if tt=='np': self.np()
		
	if tt=='nc': self.nc()
	if tt=='n': self.n()
	if tt=='cirnoise': self.cirnoise()
	if tt=='cirsweepall': self.cirsweepall()
	
	if tt=='cirsweep': self.cirsweep()
	
	if tt=='lut': self.lut()
	
	if tt=='clf': self.clf()
		
			  
	    
	return(stat)
	
	
##########################################################
#
#
#
###########################################################
	
	 
	
    def keys(self):	
	 print fa.hdffile_r.keys()
	 fa.iq_index = fa.iq_index-1; 
		

##########################################################
#
#
#
###########################################################
	

    def close(self):
        fa.hdfClose(); 
	return(False)
	

##########################################################
#
#
###################################################

    def back(self):
    	
	fa.iq_index = fa.iq_index-2; 

##########################################################
#
#
###################################################

    def raw(self):		
	
	self.dmode = 'raw'
	fa.iq_index = fa.iq_index-1; 
		    
##########################################################
#
#
###################################################

    def getiq(self):

		
	self.wdata = 'getiq'
	fa.iq_index = fa.iq_index-1; 

##########################################################
#
#
###################################################

    def getraw(self):
	self.wdata = 'raw'
	fa.iq_index = fa.iq_index-1; 


##########################################################
#
#
###################################################

    def ts(self):


		
		    self.dmode='ts'
		    fa.iq_index = fa.iq_index-1; 
		 
##########################################################
#
#
###################################################

    def bs(self):		 
		 
		    
		
		    self.dmode='bs'
		    fa.iq_index = fa.iq_index-1; 
##########################################################
#
#
###################################################

    def spec(self):		
		
		
		    self.dmode='spec'
		    fa.iq_index = fa.iq_index-1; 
		
		
##########################################################
#
#
###################################################

    def nbbtime(self):
    		
		
		    print "for baseband freq, enter time delay in ns, for noise trace"
		    print "this will change phase of noise in cirnoise"
		    tt=raw_input()
		    self.cirnoise_bbtau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 
		
	
##########################################################
#
#
###################################################

    def nrftime(self):		
		
		    print "for rf freq, enter time delay in ns, for noise trace"
		    print "this will change phase of noise in cirnoise"
		    tt=raw_input()
		    self.cirnoise_rftau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 
		

##########################################################
#
#
###################################################

    def sbbtime(self):		
		
		    print "for baseband freq, enter time delay in ns, for sweep trace"
		    print "this will change phase of pplot in cirsweep"
		    tt=raw_input()
		    self.cirsweep_bbtau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 

	
				

##########################################################
#
#
###################################################

    def srftime(self):		
		
		    print "for rf freq, enter time delay in ns, for sweep trace"
		    print "this will change phase of pplot in cirsweep"
		    tt=raw_input()
		    self.cirsweep_rftau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 

	
			
		
##########################################################
#
#
###################################################

    def specnum(self):		
	
		    print "enter integer for spec number"
		   
		    tt=raw_input()
		    self.specnum=int(tt)
		    fa.iq_index = fa.iq_index-1; 
	
		
##########################################################
#
#
###################################################

    def clf(self):		
		
		
		    figure(10)
		    clf()
		    figure(11)
		    clf()
		    fa.iq_index = fa.iq_index-1; 
		    
		
##########################################################
#
#
###################################################

    def lut(self):		
		
		
		    figure(13)
		    
		    
		    subplot(2,1,1)
		    plot(fa.lut_i)
		    subplot(2,1,2)
		    plot(fa.lut_q)
		    draw()
		    fa.iq_index = fa.iq_index-1; 
		    
		    
		#we plot sweep on circle...
		
		    
##########################################################
#
#
###################################################

    def cirsweep(self):		
		#we plot sweep on circle...
		
		
		    ll=50
	
		   
		 
		    
		    
		      
		    fa.firmware_delay = self.cirsweep_bbtau
		    fa.xmission_line_delay=self.cirsweep_rftau;
		    fa.applyDelay()
		    
		    fa.removeLineDelay()
		    
		    
		    #iqp=fa.extractTimeSeries(fa.frequency_list[3-resnum])
		    fbase=fa.frequency_list[len(fa.frequency_list)-(self.channel_number+1)]
		    iq=fa.extractBinSeries(fbase)
		    

		    iq[0]=iq[0][:ll]
		    iq[1]=iq[1][:ll]
		    iqp=fa.RectToPolar(iq)
		    
		    iqp=fa.calcLineSweepDelay(iqp,fbase)

		    iq=fa.PolarToRect(iqp)
		    
		    print "sweep fbase %f"%(fbase)
		    carrfs=arange(fa.start_carrier,fa.end_carrier, fa.inc_carrier)
		    freqs=carrfs - fbase
		    print "sweep center freq %f"%(freqs[ll/2])

		    figure(10)
		    #clf()
		    subplot(2,1,1)
		    plot(freqs,iqp[0][:ll])
		    subplot(2,1,2)
		    plot(freqs,iqp[1][:ll])
		    draw()

		    figure(11)
		    #clf()
		    plot(iq[0],iq[1])
		    draw()
		    fa.iq_index = fa.iq_index-1; 
		
		#for all channels in trace plot the circle sweep raw data




##########################################################
#
#
###################################################

    def cirsweepall(self):		
		
		
		    figure(10)
		    clf()
		    
		    figure(11)
		    clf()
		    ll=50
	
		   
		    
		    for self.channel_number in range(len(fa.frequency_list)):
			#iqp=fa.extractTimeSeries(fa.frequency_list[3-resnum])
			iq=fa.extractBinSeries(fa.frequency_list[len(fa.frequency_list)-(self.channel_number+1)])
			

			iq[0]=iq[0][:ll]
			iq[1]=iq[1][:ll]
			iqp=fa.RectToPolar(iq)

			fbase=fa.frequency_list[len(fa.frequency_list)-(self.channel_number+1)]
			print "sweep fbase %f"%(fbase)
			carrfs=arange(fa.start_carrier,fa.end_carrier, fa.inc_carrier)
			freqs=carrfs - fbase
			print "sweep center freq %f"%(freqs[ll/2])

			figure(10)

			subplot(2,1,1)
			plot(freqs,iqp[0][:ll])
			subplot(2,1,2)
			plot(freqs,iqp[1][:ll])
			draw()

			figure(11)

			plot(iq[0],iq[1])
			draw()
		    
		    
		    fa.iq_index = fa.iq_index-1; 
		



		

##########################################################
#
#
###################################################

    def cirnoise(self):		
		
		    fa.iq_index = fa.iq_index-1; 
		    
		    fbase=fa.frequency_list[len(fa.frequency_list)-(self.channel_number+1)]
		    print "noise fbase %f"%(fbase)
		    iqn=fa.iqdata
		    
		    print "channel number %d"%(self.channel_number)
		    
		   
		    
		    
		    fa.firmware_delay = self.cirnoise_bbtau
		    fa.xmission_line_delay=self.cirnoise_rftau;
		    fa.applyDelay()
		    
		    iqnp=fa.extractTimeSeries(fbase)
		    

		    
		   
		    
		    
		    
		    iqn=fa.PolarToRect(iqnp)
		    freqn=fa.carrierfreq-fbase
		    print "noise freq %f"%(freqn)
	
	
		    print "Delay BBtime %f ns"%(self.cirnoise_bbtau)
		    
		    
		
		 
		        
		    iqn=fa.PolarToRect(iqnp)
		    figure(10)
		    subplot(2,1,1)
		    plot(array([freqn]*len(iqnp[0])),iqnp[0],'.')
		    subplot(2,1,2)
		    plot(array([freqn]*len(iqnp[1])),iqnp[1],'.')

		    figure(11)
		    plot(iqn[0],iqn[1],'.')
		



##########################################################
#
#
###################################################

    def n(self):		
		
		
		
		    tt=raw_input()
		    fa.iq_index=int(tt)
		


##########################################################
#
#
###################################################

    def nc(self):		
		
		 
		 
		 
		    print 'enter which channel'
		    tt=raw_input()
		    self.channel_number=int(tt)
		    fa.iq_index = fa.iq_index-1; 
		    fbase = fa.frequency_list[len(fa.frequency_list)-(self.channel_number+1)]
		    print "fbase %f, freq %f"%(fbase,fa.carrierfreq-fbase)
		


##########################################################
#
#
###################################################

    def np(self):		
		
		
		    print 'enter num traces for pulse find'
		    tt=raw_input()
		    self.numptraces=int(tt)
		    fa.iq_index = fa.iq_index-1; 
		    


##########################################################
#
#
###################################################

    def info(self):		
		
		
		    fa.info(0)
		    fa.iq_index = fa.iq_index-1;
		


##########################################################
#
#
###################################################

    def th(self):		
		
		
		
		  
		    print "calc pulse threshold"
		    fa.calcPulseThreshold( [ iqp[0][10:(len(iqp[0])-10)],iqp[1][10:(len(iqp[1])-10)]])
		    fa.iq_index = fa.iq_index-1; 
		    


##########################################################
#
#
###################################################

    def pltpls(self):		
		
		
		
		
		    fa.iq_index = fa.iq_index-1; 
		    figure(2)
		    clf()
		    figure(5)
		    clf()
		    
		    figure(6);clf()

		    plot(resdata.trot_xf,resdata.trot_yf)
		    
		    for px in range(len(self.pulse_data)):
		       
		        figure(2)
			subplot(2,1,1)
			plot(self.pulse_data[px][0])
			
			subplot(2,1,2)
			plot((180.0/pi)*self.pulse_data[px][1])
			draw()
			
			
			
			if self.is_circle:
			    iq_tr=fit.trans_rot3(resdata, fa.PolarToRect(self.pulse_data[px]))
			    iqp_tr=fa.RectToPolar(iq_tr)

			    figure(5)
			    subplot(2,1,1)
			    plot(iqp_tr[0])
			    subplot(2,1,2)
			    plot((180.0/pi)*iqp_tr[1])
			    draw()

			    figure(6)


			    plot(iq_tr[0],iq_tr[1],'.')
			    figure(1)
			


##########################################################
#
#
###################################################

    def field(self):		
		
		
		
		    print "type name of field in class fftAnalyzerd"
		    tt=raw_input()
		    exec "print fa.%s"%(tt)
		    fa.iq_index = fa.iq_index-1; 
		    




##########################################################
#
#
###################################################

    def python(self):		
	
		
		
		
		    print "type a python command"
		    tt=raw_input()
		    exec tt
		    fa.iq_index = fa.iq_index-1; 



##########################################################
#
#
###################################################

    def offs(self):		
	  	
		
		
		    print "type fpga_bug_offset"
		    tt=raw_input()
		    self.fpga_bug_offset_=int(tt);
		    fa.iq_index = fa.iq_index-1; 
		    


##########################################################
#
#
###################################################

    def p(self):		
		
		    
		    print "finding pulses,%d sweeps"%(self.numptraces)
		    fa.iq_index = fa.iq_index-1;
		    for px in range(self.numptraces):
			fa.hdfReadIQ() 

			fa.iqdata=fa.I_raw

			if self.dmode=='raw':
			    iqp=fa.RectToPolar(fa.iqdata)

			if self.dmode == 'ts':
			    iqp=fa.extractTimeSeries(fa.frequency_list[channel_num])
			  
			if self.dmode == 'bs':
			    iqp=fa.extractBinSeries(fa.frequency_list[channel_num])
			  


			 
			result=fa.extractPulses(iqp,10,30)
			nplses=result[2]
			pdata=result[1]
			trigger=5*result[0]*fa.magnitude_std + fa.magnitude_exp_val
			print 'Found %d pulses'%(nplses)
			if nplses>0:
		            self.pulse_data.append(pdata)

			    figure(2)
			    clf()
			    subplot(2,1,1)
			    plot(iqp[0])
			    plot(trigger)
			    subplot(2,1,2)
			    plot(iqp[1])
			    draw()

		    
