
import scipy.signal


hdfshell_findname=''
hdfshell_findlist = []


hdfshell_searchattr=False
hdfshell_searchpath = ''
hdfshell_getvals=False

#callback for visit in groups.called each time a group/dataset is vidited. for finding.
#creates a list of found things. also looks at attributes.

def hdfshell_find(name):
    global hdfshell_findlist
    global hdfshell_findname
    
   
    sp=resv.getAbsPath(hdfshell_searchpath + '/'+name)
    obj=resv.fp.get(sp)
    if hdfshell_findname!='':
        if hdfshell_findname in name:
	    val = None
	    if hdfshell_getvals:
	        try: val=obj.value
		except: pass

	    hdfshell_findlist.append((name,val))
	    
    else:
        
	
 	val = None
	if hdfshell_getvals:
	    try: val=obj.value
	    except: pass
	
	hdfshell_findlist.append((name,val))
    
    if hdfshell_searchattr:
      
       
	for at in obj.attrs.keys():

	    if hdfshell_findname!='':
        	if hdfshell_findname in at:
		    val = None
	            if hdfshell_getvals:
	        	try: val=obj.attrs[at]
			except: pass
		
		    hdfshell_findlist.append(( name + '/attr/'+at,val))
	    else:
		val = None
	        if hdfshell_getvals:
	            try: val=obj.attrs[at]
		    except: pass
        	hdfshell_findlist.append((name + '/attr/'+at,val))

    return(None)

class hdfShell:


    def __init__(self):
    	self.MKID_list=[]
	
	#self.mkidLoadData(fname)
	
	self.current_mkid=0
	self.current_res=0
	
	self.filenumber=0
	self.filename = ''

	self.fp=None
	self._pwd = None
	self._pwdlist=None
	
	self.history=''
	self.is_clf_refresh = 1
	self.is_pl_noise=0
	
	
######################################################
# load mkids from Device_Mxxxx directory. Several mkids
# and many traces each mkid
######################################################

    def mkidLoadData(self,hobj):
	  
	   


	    self.MKID_list=[]

	 
	    devgrp=None

	    for k in hobj.keys():
		if k[0:6]=='Device':
		    devgrp=k

	    if devgrp==None:
		print "No device data"
		return(-1)

	    device_name=devgrp[7:].encode('utf8')


	    #resview through Resonator_x
	    for k in hobj[devgrp].keys():

		resnum=int(k[10:])


		resgrp=k

		fc =hobj[devgrp][resgrp]['Freq_Cent'][0]

		m=MKID(resnum,device_name,fc)

		try: m.preferred_atten=hobj[devgrp][resgrp]['PrefAtten'][0]
		except:pass

		self.MKID_list.append(m)


		for rd in hobj[devgrp][resgrp].keys():
	    	    if rd[0:7]=='ResData':

	    		grprnum=int(rd[8:])   
			res=resonatorData(resnum,device_name)
			res.readHDF(hobj[devgrp][resgrp],grprnum)

			m.reslist.append(res)
	    
	    
	    
	    return(1);
	    
	
######################################################
#
#like linux find. from shellcmds(find)
######################################################

    def find(self,tt):
    
        
	global hdfshell_findname
	global hdfshell_findlist
	global hdfshell_searchattr
	global hdfshell_searchpath
	
	global hdfshell_getvals
	
    
    	if self._pwd==None: 
	    print "Disk"
	    os.system(tt)
	else:
	    print "HDF File: %s %s"%(self.filename,self._pwd.name)
	    
	    
	    
	    tokens = tt.split()
	    
	  
	    ntok = len(tokens)
	    
	    searchpath = self._pwd.name
	    findname=''
	    searchobj=self._pwd
	    isattr = False
	    isval = False
	    outname = ''
	    
	    if ntok>1:
	        
		
		k=1
		while k<ntok:
		    #find this name
		    if tokens[k]=='-name':
		        findname = tokens[k+1]
			k=k+2
		    #search attributes as well
		    elif tokens[k] == '-attr':
		        isattr=True
			k=k+1
		    #search attributes as well
		    elif tokens[k] == '-ds':
		        isval=True
			k=k+1
		    elif tokens[k]=='-out':
		        outname = tokens[k+1]
			k=k+2		
		    	
		    else:
		        searchpath=tokens[k]
			k=k+1	
		
		
	    searchpath = self.getAbsPath(searchpath)
		
	    searchobj = self.fp.get(searchpath)

	    hdfshell_getvals=isval
	    hdfshell_searchpath=searchpath
	    hdfshell_findlist=[]
	    hdfshell_searchattr = isattr
	    hdfshell_findname=findname
	    searchobj.visit(hdfshell_find)
	    for item in hdfshell_findlist:
	        if isval==False:
		    print item[0]
		else:
		    print '%s	%s'%(item[0],item[1]) 
		    
	    
    	    if outname!='' and isval==True:
	        outdata=[]
	        for item in hdfshell_findlist:
		    outdata.append(item[1][0]) 
		outdata = numpy.array(outdata)
		outname = self.getAbsPath(outname)
	
		self.fp.create_dataset(outname,data=outdata)
		
	
######################################################
#load single resonator object
#
######################################################

    def loadResonator(self,parentgrp,resnum):

	# name will be /sweeps/ResData_0

	res=resonatorData(resnum,'unkown')
	res.readHDF(parentgrp,resnum)
	return(res)



	
######################################################
#
#
######################################################

    def loadResonator2(self,pathstr):

	# name will be /sweeps/ResData_0

	resdatastr=pathstr.split('/')[-1]
	if resdatastr[0:7]=='ResData':
	        resnum=int(resdatastr[8:])
	else:
	    return(None)
	    
	parentgrp = self.fp.get(pathstr).parent

	res=resonatorData(resnum,'unkown')
	res.readHDF(parentgrp,resnum)
	return(res)

	
######################################################
#load bunch of resonators
#
######################################################

    def loadResonators(self,parentgrp):
        reslist = []
 	for rd in parentgrp.keys():	
 	    if rd[0:7]=='ResData':
	        resnum=int(rd[8:])
		reslist.append(self.loadResonator(parentgrp,resnum))
	
	
	return(reslist)	   
	    
######################################################
# try to load from Device_XXXX dir, of not work, then
# load from local dir- sweeps. looks for ResData_x, and then
#put one resData into on eMKID. make MKID list
######################################################
	    
    def doloadres(self,tt):
    
        stat = self.mkidLoadData(self._pwd)
	
	
        if stat==-1:
	    self.reslist = self.loadResonators(self._pwd)

	    self.MKID_list = []
	    for res in self.reslist:
		m=MKID(res.resonator_num,'NULL',res.rough_cent_freq)
		m.reslist.append(res)
		self.MKID_list.append(m)

	self.current_mkid=0
	self.current_res=0

 	print 'Loadded %d MKIDs'%(len(self.MKID_list))   
    	
######################################################
#
#
######################################################
	
    def resview(self):
    
    	
    	
	stat = True
	while stat:
	
	    print "-----------------------------------------------------------------"
	  
	   
	    
	    
	    
	    try:
	        self.resdata=  self.MKID_list[self.current_mkid].reslist[self.current_res]
 		
		print "MKID# %d TRACE# %d"%(self.current_mkid,self.current_res)
	    	print " %4.1f MHz, %4.1fdB"%(self.MKID_list[self.current_mkid].rough_cent_freq/1e6,self.resdata.atten_U7 )
	        print "---------------------------------------------------------------------"
		self.resdata.plotFreq(isclf=self.is_clf_refresh,isnoise=self.is_pl_noise)
		self.resdata.info()
		

	    except:
	        print "indices out of range"
		
	
	    tt=raw_input("resview>>")
	    self.history=self.history + tt + '\n'
	    stat=self.resviewcmds(tt)
		
	   
	



	
######################################################
#
#
######################################################
	
    def shell(self):
    
    	
    	
	stat = True
	while stat:
	
	
		
	
	    tt=raw_input("hdfsh>>")
	    self.history=self.history + tt + '\n'

	    stat=self.shellcmds(tt)
		
	   


	


######################################################
#
#
######################################################
	
    def resviewcmds(self,tt):
    
    
        stat=True;
	if tt=='hold':self.is_clf_refresh=0
	if tt=='nohold':self.is_clf_refresh=1
	if tt=='plnoise':self.is_pl_noise=1
	if tt=='nonoise':self.is_pl_noise=0
	
	if tt=='-':self.dec();
		
	#if tt=='':self.clf()
	
	if tt=='+':self.inc();
	
	if tt=='fitprefat':self.fitprefat()
	
	if tt=='fitprefatall':self.fitprefatall()
	 
	 
	 
	if tt=='plmkid':self.plmkid()
	 
	if tt=='list':self._list()
	
	if tt=='nmkid':self.clf();self.nmkid()

	

	if tt=='clf':self.clf()
	
	if tt=='q':stat=False
	
	if tt=='fit':self.fit()
	
	if tt=='st':self.start();self.clf()
	
	if tt=='pr':self.plotfit()
	
	if tt=='save':self.save()

	if tt==' ':self.clf();self.inc();
	
	if tt=='iqvel':self.iqvel()
	
	if tt=='prefat':self.prefat()
	
	if tt=='findat':self.findat()
	
	if tt=='findat2':self.findat2()

	if tt=='?':self.man()
	
	if tt=='help':self.man()
	    
	if tt=='man':self.man()
	
	if tt=='flatph': self.flattenPhase()
	
	

	return(stat)  





######################################################
#
#
######################################################
	
    def shellman(self,tt):
    
    
      
	print """
	
	pwd - show current working dir. if no hdf open, looks at linux filesystem
	    if hdf open , looks at hdf file
	    
	    
	ls - list dirs in linux, of no file open. else list items in hdf, current dir.
	   ls -ds will list directry, and dataset values
	
	cd - change dir, in linux, or file, if file is open
	   we can cd into a dataset. doing ls will show values in dataset.
	   plot with no artgs will plot the dataset.
	
	open- open hdf file. open qqqq1.h5
	
	close- close hdf file
	
	mv - move file in linux. or move item in hdf file. ise linux syntax like
	    mv /mygropup/mydataset /mynewdataset
	    
	plot- plot 2d. Give pathname to dataset in hdf. can be like 
	      cd /grp/mydaset
	      plot
	      
	      cd ..
	      plot mydatset
	      
	      cd ..
	      plot /grp/mydata
	      
	      for x and y data, give x and y i that order
	      plot /grp/dataset1 /grp2/dataset100
	      
	      plot -ts phase
	      Tjhis will plot by event at proper timestamp- for pulse data
	      
	 mkdir make a dir in lnuyx, or a group in hdf5. can use rel or abs path.
	 
	 py= execute python in a function scope. 
	     py print myglobvar   will print the global var 
	     py myglovbvar=2 will NOT set global.
	     py global myvar; myvar=2, will set global var
	     use class myvars, a global class to store vars for repeated calls to py.
	     py aaa=100
	     py print aaa, will not see aaa.
	     py myvars.aaa = 100
	     py print myvars.aaa  will print 100
	     
	 loadres 
	    cd to a directory like /sweeps, and do ls. you should see dirs like ResData_xxx
	    
	    loadres with no args, will load all the ResData_xxx data into resonator obhects stored in python
	     	at resv.MKID_list[].resdata[]. They are MKID opbhects each a resonatorData obhect, all defined in 
		 fitters.py
		
  	 resview- start the resview progralm, that resviews through all the resonators, type heop after typeing resview
	      you loadres, then type resview
	      this is for examinging all thre resonator sweeps and fits. you can fit, transrot, etc
	      also you can set the preferred attenuation for each mkid. you can plot noise on the circle.
	      
	 clf clear cuyrrent plot
	 
	 transrot 
	    transrot -r /sweeps/ResData_4  -c /Chan_00000
	    this will make new data sets in Chan_00000 that is transrotated data. it expects magnitude and
	    phase data sets to be present. It take sweep data from the resontor, and transrots the raw
	    mag and phase data, making new datasets magniotude_tr, and phase_tr.
	    If the transrot data is already present, it is overwritten. 
	    
	 pltrot -r /sweeps/ResData_4  -c /Chan_00000
	 
	     plot noise on Iq circle. have to call transrot 1st.
	     
	     
	    
	 rm-  if no hdf file open, does rm in linux in nroamal way
	      if file open. there is no easy way to delete data in hdf5. All you can do is rename
	      
	      rm mydata
	      will do this:
	      mkdir /trash
	      mv mydata /trash/mydata_Randomnumber
	      
	      rm will just rename the data and move in hdf5, it does not go away.
	    
	    
	      
	topy /path/dataset varname
	 	this will create global var in python space called varname from taht dataset.
		 also creates myvars.varname
		 
		    
	note myfile.txt
	  	create a text file in the hdf file. it is a note. you start typeing
		then you hit ctrl-D to end. 
		you cannot append to existant note. yuo muyst stat a new one all the time.
		
	cat
	more
		will show what is in a data set.
		
	pliq	will do iq plot, need ONE of the options below
		1)   -c Chan_00000 directory	
			pliq -c Chan_00000	
		2)   -i,-q   need both, i and q datasets
		
		3)    -mag,-ph mag and phase data, need both
		4) -iq for an iqdata in a resonator. 2 vector dataset.
		
		-l for all opeions above do -l 20000 or some number to tell how many poitns tio ploe
		
		
		    
	"""
	
	



######################################################
#
#
######################################################
	
    def shellcmds(self,tt):
    
    
        stat=True;
	if 1==1:
	
	  

	    if tt=='pwd':self.getcwd()

	    if tt[:2]=='ls' :self.ls(tt)

	    if tt[:2]=='cd' : self.cd(tt)

	    if tt[:4]=='open' : self.hdfOpen(tt)

	    if tt=='close' : self.hdfClose()


	    if tt[:5]=='mkdir' : self.mkdir(tt)

	    if tt[:2]=='mv' : self.move(tt)
	    
	    if tt[:2]=='rm' : self.rm(tt)
	    
	    
	    if tt[:4]=='plot' : self.plot(tt)
	    
	    if tt[:2]== 'py' : self.dopython(tt)
	    
	    
	    if tt=='loadres' : self.doloadres(tt)
	    
	    if tt=='resview' : self.resview()
	    
	    if tt[:8]=='transrot' : self.dotransrot(tt)
	    
	    if tt[:6]=='pltrot' : self.doplotiqcircle(tt)
	    
	    if tt[:4]=='pliq' : self.doplotiq(tt)
	    
	    if tt=='clf' : clf()
	    
	    if tt[:4]=='help' : self.shellman(tt)
	    if tt[:3]=='man' : self.shellman(tt)
	    
	    if tt[:4]== 'note' :self.note(tt)
	    
	    if tt[:4]== 'more' : self.ls('ls -ds %s'%(tt.split()[-1]))
	    if tt[:3]== 'cat' : self.ls('ls -ds %s'%(tt.split()[-1]))
	    
	    if tt[:4]=="topy" : self.topy(tt)
	    
	    if tt[:5]=="welch" : self.welch(tt)
	    
	    if tt[:4]=="find" : self.find(tt)
	    
	    
	else:
	    print "Caught exception"

	
	
	if tt=='q':self.hdfClose();stat=False
	return(stat)  
	
	

	
	
##############################################################
#
#
###############################################################

    def welch(self,tt):
    
    

	if len(tt.split())==2:

	    args=tt.split()
	    #get lastarg
	    datapath=self.getAbsPath(args[-1])	    
	        

	    data = self.fp.get(datapath).value[0]
	    fs=1e6;
	    freq,psd = scipy.signal.welch(data,fs)
	    figure(20);
	    loglog(freq,psd)
	    
	else:
	    print "Usage: welch /Chan_00128/phase"
	    
	    		    


	
##############################################################
#
#
###############################################################

    def topy(self,tt):
    
    

	if len(tt.split())==3:

	    args=tt.split()
	    datapath=self.getAbsPath(args[-2])	    
	    varname=args[-1]	    

	    exec('global %s; %s=self.fp.get(datapath).value'%(varname,varname))	
	    exec('myvars.%s=self.fp.get(datapath).value'%(varname))	
	    
	    print "Created Python variable myvars.%s, and global %s"%(varname,varname)	    
	else:
	    print "Usage:\h2py /sweeps/ResData_0 varname"
	    
	    		    
		
	
	
##############################################################
#
#
###############################################################


    def note(self,tt):
        
	txtfile=self.getAbsPath(tt.split()[-1])
	
	print 'type ctrl-D to end note'
	notes=''
	
	tt=raw_input()
	try:
	    while(True):
		notes = notes + tt
		notes = notes + '\n'
		tt=raw_input()
	
	except: pass    
	    
	self.fp.create_dataset(txtfile,data=numpy.array(notes))
	print 'created %s'%(txtfile)

##############################################################
#
#
###############################################################

    def dopython(self,tt):
        exec(tt[3:])


##############################################################
#
#
###############################################################

    def dotransrot(self,tt):


	if len(tt.split())>1:


	    args=tt.split()
	    argc=len(args)
	    

	    kk=1
	    while kk<argc:
		if args[kk].find('-')>-1:
		    #- an option
		    if args[kk]=='-r': 
		        respath=args[kk+1]
			kk = kk+2
		    
		    elif args[kk]=='-c':
		        chanpath=args[kk+1]
			kk=kk+2
		    else: kk=kk+1
			

	    if respath[0]!='/': respath =  self._pwd.name + respath
	    if chanpath[0]!='/': chanpath =  self._pwd.name + chanpath
	    res=self.loadResonator2(respath)  

	    magds= self.fp.get(chanpath+'/magnitude')
	    phsds=self.fp.get(chanpath+'/phase')
	    mag=magds.value[0]
	    phs=phsds.value[0]

	    iq=fit.PolarToRect([mag,phs])

	    iqtr=fit.trans_rot3(res,iq)

	    mptr=fit.RectToPolar(iqtr)

	    try:
		magtrds=self.fp.create_dataset(chanpath+'/magnitude_tr',magds.shape)
		phstrds=self.fp.create_dataset(chanpath+'/phase_tr',phsds.shape)
		print "Created %s and %s"%(magtrds.name, phstrds.name)
	    except:
		
		magtrds=self.fp.get(chanpath+'/magnitude_tr')
		phstrds=self.fp.get(chanpath+'/phase_tr')
		print 'will overwrite magnitude_tr and phase_tr'
		
	



	    magtrds[0]=mptr[0]
	    phstrds[0]=mptr[1]

		
		
		
		    
	else:
	    print "Usage:\ntransrot -r /sweeps/ResData_0 -c Chan_00000"
	    
	    		    
		


##############################################################
# five resonatopr path, channel path, should have done transrot first
# plot res circle from trot xf, yf and the magnitude_tr and phasetr from chan
###############################################################

    def doplotiqcircle(self,tt):


	if len(tt.split())>1:


	    args=tt.split()
	    argc=len(args)
	    
	    ll=65536

	    kk=1
	    while kk<argc:
		if args[kk].find('-')>-1:
		    #- an option
		    if args[kk]=='-r': 
		        respath=args[kk+1]
			kk = kk+2
		    
		    elif args[kk]=='-c':
		        chanpath=args[kk+1]
			kk=kk+2
			
		    elif args[kk]=='-l':
		        ll=int(args[kk+1])
			kk=kk+2
		    else:
		        kk=kk+1

	    if respath[0]!='/': respath =  self._pwd.name + respath
	    if chanpath[0]!='/': chanpath =  self._pwd.name + chanpath
	    res=self.loadResonator2(respath)  

	    magds= self.fp.get(chanpath+'/magnitude_tr')
	    phsds=self.fp.get(chanpath+'/phase_tr')
	    mag=magds.value[0]
	    phs=phsds.value[0]

	    iq=fit.PolarToRect([mag,phs])


	    plot(res.trot_xf,res.trot_yf)

	    plot(iq[0][:ll], iq[1][:ll],'r.')

		
		
		
		
		    
	else:
	    print "Usage:\ntransrot -r /sweeps/ResData_0 -c Chan_00000"






############################################################	 

###############################	  ###############################	   
	    		    
    def getAbsPath(self,path):
    
    	if path[0]!='/': path =  self._pwd.name +'/'+ path

        path=path.replace('//','/')
	return(path)




##############################################################
# five resonatopr path, channel path, should have done transrot first
# plot res circle from trot xf, yf and the magnitude_tr and phasetr from chan
###############################################################

    def doplotiq(self,tt):


	if len(tt.split())>1:

	    iqpath=None
	    phasepath= None
	    magpath = None
	    chanpath=None
	    ipath = None
	    qpath= None
	    cs='r.'
	    
	    args=tt.split()
	    argc=len(args)
	    
	    ll=50

	    kk=1
	    while kk<argc:
		if args[kk].find('-')>-1:
		    #- an option
		    if args[kk]=='-iq': 
		        iqpath=args[kk+1]
			kk = kk+2
		    
		    elif args[kk]=='-ph':
		        phasepath=args[kk+1]
			kk=kk+2
			
		    elif args[kk]=='-mag':
		        magpath=args[kk+1]
			kk=kk+2
		 
		    elif args[kk]=='-c':
		        chanpath=args[kk+1]
			kk=kk+2
		    elif args[kk]=='-i':
		        ipath=args[kk+1]
			kk=kk+2
		    elif args[kk]=='-q':
		        qpath=args[kk+1]
			kk=kk+2
	    	    elif args[kk]=='-l':
		        ll=int(args[kk+1])
			kk=kk+2
		    elif args[kk]=='-cs':
		        cs=args[kk+1]
			kk=kk+2
		    else:
		        kk=kk+1




	    if iqpath!=None:
	    	iqpath=self.getAbsPath(iqpath)
		iq=self.fp.get(iqpath)
		plot(iq[0][:ll],iq[1],cs)
		
		
	    
	    elif phasepath!=None:
	    	phasepath=self.getAbsPath(phasepath)
	    	magpath=self.getAbsPath(magpath)
		
		phs=self.fp.get(phasepath).value[0]
		mag=self.fp.get(magpath).value[0]
		
		iq=fit.PolarToRect([mag,phs])
		
		plot(iq[0][:ll],iq[1][:ll],cs)
		
	    elif ipath!=None:
	    
	    	  
	    	ipath=self.getAbsPath(ipath)
	    	qpath=self.getAbsPath(qpath)
		
		i=self.fp.get(ipath)
		q=self.fp.get(qpath)
		
		
		
		plot(i[:ll],q[:ll],cs)
	    elif chanpath!=None:
	    
	       	  
	    	chanpath=self.getAbsPath(chanpath)




		magds= self.fp.get(chanpath+'/magnitude')
		phsds=self.fp.get(chanpath+'/phase')
		mag=magds.value[0]
		phs=phsds.value[0]

		iq=fit.PolarToRect([mag,phs])


		
		plot(iq[0][:ll], iq[1][:ll],cs)

		
		
		
		
		    
	else:
	    self.shellcmds('man')
	    
	    		    
		



##############################################################
#
#
###############################################################

    def move(self,tt):
        src=tt.split()[1]
        dst=tt.split()[2]
     	
	if self._pwd==None: 
	    print "Disk"
	    os.system(tt)
	    return()
	
	if src[0]!='/': src =  self._pwd.name + src   
	if dst[0]!='/': dst =  self._pwd.name + dst   
	
	lastdst=dst.split('/')[-1]
	lastsrc=src.split('/')[-1]
	if lastdst=='.' : dst=dst.replace('.',lastsrc)
	
	
	print "move %s to %s"%(src,dst)
	
	self._pwd.move(src,dst)

	

##############################################################
#
#
###############################################################

    def rm(self,tt):
        src=tt.split()[1]
    
     	
	if self._pwd==None: 
	    print "Disk"
	    os.system(tt)
	    return()
	
	
	self.mkdir('mkdir /trash')
	
	dst=src + '_%d'%(int(rand()*1e9))
	dst=dst.split('/')[-1]
	
	self.move('mv %s /trash/%s'%(src,dst))

##############################################################
#
#
###############################################################

    def mkdir(self,tt):
        k=tt.split()[1]
     	
	if self._pwd==None: 
	    print "Disk"
	    os.system(tt)
	    return()
	    
	    

	if type(self._pwd)==h5py.h5g.GroupID or \
	    type(self._pwd)==h5py._hl.files.File or \
	    type(self._pwd)==h5py._hl.group.Group:
	    
	    print "attempt to create group %s"%(k)
	    try: self._pwd.create_group(k)
	    except: print "cannot mkdir %s, already there?"%(k)

##############################################################
#
#
###############################################################
    def cd(self,tt):
        k=tt.split()[1]
    
    	if self._pwd==None: 
	    print "Disk"
	    os.chdir(k)
	    return()
	    
	    
        k=tt.split()[1]
	
	if k=='..':
	    if len(self._pwdlist)>-1:
	        self._pwdlist.pop(-1)
		self._pwd=self._pwdlist[-1]
	else:
	
 	    self._pwd=self._pwd[k]
	    self._pwdlist.append(self._pwd)
	
	
	print "HDF File: %s %s"%(self.filename,self._pwd.name)


##############################################################
#
#
###############################################################

    def ls(self,tt):
	if self._pwd==None: 
	    print "Disk"
	    os.system(tt)
	else:
	    print "HDF File: %s %s"%(self.filename,self._pwd.name)
	    
	    
	    
	    tokens = tt.split()
	    arg=None
	    is_ds=False
	    is_arg=False
	    if len(tokens)>1:
	        
		if tokens[-1].find('-')==-1:
		    is_arg=True
		    arg=tokens[-1]
		    
		is_ds='-ds' in tokens
	    
	    
	    
	    
	    if type(self._pwd)==h5py.h5g.GroupID or \
	        type(self._pwd)==h5py._hl.files.File or \
		type(self._pwd)==h5py._hl.group.Group:
	        
		
		if is_arg:
		    k = arg
		    print "%s \t\t\t %s"%(k, type(self._pwd[k]))
		    for atx in self._pwd[k].attrs.keys():
			        print "\t %s \t %s"%(atx,self._pwd[k].attrs[atx])
		    
		    try:
		       
			for kk in self._pwd[k].keys():
	        	    print "%s \t\t\t %s"%(kk, type(self._pwd[k][kk]))
			    for atx in self._pwd[k].attrs.keys():
			        print "\t %s \t %s"%(atx,self._pwd[k].attrs[atx])
			    
		    except:
			print self._pwd[k].value
	    		print "dataset----"
	        	print self._pwd[k].name
			print self._pwd[k].shape
			for atx in self._pwd[k].attrs.keys():
			     print "\t %s \t %s"%(atx,self._pwd[k].attrs[atx])
		
		
		
		else:
		
		    for k in self._pwd.keys():
		        if is_ds and type(self._pwd[k])==h5py._hl.dataset.Dataset:
	        	    print "%s \t DS \t %s \t %s"%(k,self._pwd[k].shape,self._pwd[k].value )
			    
			    for atx in self._pwd[k].attrs.keys():
			        print "\t %s \t %s"%(atx,self._pwd[k].attrs[atx])
			    
			    
			else:
			    print "%s \t\t\t %s"%(k, type(self._pwd[k]))
			    for atx in self._pwd[k].attrs.keys():
			        print "\t %s \t %s"%(atx,self._pwd[k].attrs[atx])
	    else:
	        print self._pwd.value
	    	print "dataset----"
	        print self._pwd.name
		print self._pwd.shape
		for atx in self._pwd[k].attrs.keys():
			 print "\t %s \t %s"%(atx,self._pwd[k].attrs[atx])
	

##############################################################
#
#
###############################################################

    def getcwd(self):
	if self._pwd==None: 
	    print "Disk"
	    os.system('pwd')
	else:
	    print "HDF File: %s %s"%(self.filename,self._pwd.name)
	    
	

##############################################################
#
#
###############################################################

    def hdfClose(self):
      try:
     	
	t=time.asctime().replace(' ','_')
	
	hname=	'/history/history_%s.txt'%(t)    
	self.fp.create_dataset(hname,data=numpy.array(self.history))
	print 'created %s'%(hname)
      
        self.fp.flush()
        self.fp.close()
	self.fp=None
	self._pwd = None
	self._pwdlist=None
      except:
      	pass

##############################################################
#
#
###############################################################

    def hdfOpen(self,tt):
    	    self.fp=h5py.File(tt.split()[1],'r+');
	    self._pwd =self.fp
	  

	    self._pwdlist = [self._pwd]
	    self.filename = tt.split()[1]    
    

##############################################################
#
#
###############################################################



##############################################################
#
# plots a dataset. can plot x v y given 2 ds. can plot by timestamp
# with -ts. can plot length of points with -l N
#must deal w/ the fact some DS are acautlly in DS[0] and no in DS.
#has top figure it out. cannot plot 2d DS, like iqdata. need somebetter
#method of finding it... just makes 2 plots
###############################################################


    def plot(self,tt):
	
	dsy=self._pwd
	ydata = None
	xdata = None
	is_ts = False
	is_len= False
	
	ll = 4096
	
	colorspec = 'b'
	
	if len(tt.split())>1:


	    args=tt.split()
	    argc=len(args)
	    

	    kk=1
	    while kk<argc:
		if args[kk].find('-')>-1:
		    #- an option
		    if args[kk]=='-l': 
		        ll=int(args[kk+1])
			kk = kk+2
			is_len = True

		    if args[kk]=='-cs': 
		        colorspec=args[kk+1]
			kk = kk+2
			


		    if args[kk]=='-ts': 
		        is_ts = True
			kk = kk+1

		elif kk==argc-2:
		    #2nd last arg no -
		    xdata=args[kk]
		    kk=kk+1
		elif kk==argc-1:
		    #last arg no -
		    ydata=args[kk]
		    kk=kk+1


	    if ydata!=None:
	        if ydata[0]!='/': ydata =  self._pwd.name + '/' + ydata   
	    
	    if xdata!=None:
	        if xdata[0]!='/': xdata =  self._pwd.name + '/' + xdata   
		
	    
	    try:
	        tdata= self._pwd.name + '/' + 'timestamps'   
		dts = self.fp.get(tdata)
	    except:
	        is_ts = False
		

	    if ydata!=None : dsy=self.fp.get(ydata)
	    if xdata!=None : dsx=self.fp.get(xdata)
	
	print colorspec 
	
	if xdata==None:  
            print "plot 2d %s "%(ydata)
	    
	    
	    if is_ts==False:

		if len(dsy.shape)==1: plot(dsy.value[:ll],colorspec)
		if len(dsy.shape)==2: 
	            fnum = 1
	    	    for ss in range(dsy.shape[0]):
		 	    figure(fnum);fnum=fnum+1			
	    		    plot(dsy.value[ss][:ll],colorspec)
	    #if plotting events by timestamp, ll is num events
	    else:
	    
	    	if is_len==False: ll=10
		
		
		if len(dsy.shape)==1: 
		    mydata=dsy.value[:(32+(ll*32))]
		if len(dsy.shape)==2: 
		    mydata = dsy.value[0][:(32+(ll*32))]
		
		myts=dts[0][:ll]
		
		k=0;
		for ts in myts:
		   
		   plot( arange(ts,(ts+32)),  mydata[k:(k+32)],colorspec)
		   k=k+32
		
		

	else:
	    print "plot 2d %s %s "%(xdata, ydata)
	    
	    if len(dsy.shape)==1 and len(dsx.shape)==1: 
	        plot(dsx.value[:ll], dsy.value[:ll],colorspec)
	    
	    if len(dsy.shape)==2 and len(dsx.shape)==1: 
	    	fnum=1
	    	for yy in range(dsy.shape[0]):
			figure(fnum);fnum=fnum+1			
	    		plot(dsx.value[:ll], dsy.value[yy][:ll],colorspec)
	    
	    
	    if len(dsy.shape)==2 and len(dsx.shape)==2: 
	        fnum = 1
	    	for yy in range(dsy.shape[0]):
		   for xx in range(dsx.shape[0]):	
		   	figure(fnum);fnum=fnum+1		
	    		plot(dsx.value[xx][:ll], dsy.value[yy][:ll],colorspec)
	


##############################################################
#
#
###############################################################


    def fitprefat(self):
        self.findat3()
	self.fit()



##############################################################
#
#
###############################################################


    def fitprefatall(self):
        ms=self.current_mkid
	mr=self.current_res
	
	
	
	for k in range(len(self.MKID_list)):
	    self.current_mkid=k
	    self.fitprefat()
	    
	self.current_mkid=ms
	self.current_res=mr    

##############################################################
#
#
###############################################################

    def plmkid(self):
    	
	
	
	ss=self.current_res
	mkid=self.MKID_list[self.current_mkid]
	self.clf();
	for res in mkid.reslist:
	   res.plotFreq(isclf=0,isnoise=0)
	   
	self.current_res=ss
	
##############################################################
#
#
###############################################################

    def _list(self):
    
        print "============================================================"
	print "Num MKIDs %d"%(len(self.MKID_list))
	
	k=0;
	for m in self.MKID_list:
	    print "Index %d,  %4.1f MHz, PrefAtten %4.1fdB %d Traces"%(k, m.rough_cent_freq/1e6, m.preferred_atten,len(m.reslist))
	    k=k+1
	
        print "============================================================"
	
##############################################################
#
#
###############################################################

    def man(self):
    
	hh="""
	'hold' 'nohold' turn off/on clf on plot
	
	'-': prev trace, clear plot, , then draw
		
	 '': clear plot, ;  redraw 
	 
	 'nmkid': next mkid, trace 0, clf, draw
	 
	 'fitprefat': fit trace for this mkid, that is at pref. atten
	 
	 'fitprefatall' : fit the trace at pref atten for all mkids
	 
	 'plmkid': plot all traces this mkid
	 
	 'list': list mkids, n traces

	 'clf': clear plot, redraw
	 
	 "+": next trace draw, no clear
	
	 'q':quit
	
	 'fit': fit this trace, 
	
	 'st':1st mkid, 1st trace; clear plot, 
	
	 'pr': plot fit curves,  this trace, 
	
	 'save': save()

	 ' ':  clf, next trace, draw 
	
	 'iqvel ': calc iqvel's this mkid, ()
	
	 'prefat': set preferred atten for mkid, 
	
	 'findat': find trace this mkid by atten U7,
	 
	 'findat2': find by total atten (U6,U7,lutamp) 
	 
	 'flatph:  flatten phase so it is proper timedelay'
	 
	 'iqvel'   make iqvel for this mkid, all traces
	 
	"""
	
	print hh
	

##############################################################
#
#
###############################################################


    def prefat(self):
        mkid=self.MKID_list[self.current_mkid]
	
	print "enter pref attenin db (+number), mkid %f Hz"%(mkid.rough_cent_freq)
	pf=float(raw_input())
	#find res w/ atten of 7.
	
	for resdata in mkid.reslist:
	    if resdata.atten_U7==pf:
	    	
		att = -20.0*log10(resdata.lut_sine_amp)
		att=att+resdata.atten_U7
		att=att+resdata.atten_U6
		mkid.preferred_atten=att
		print "U6 %fdB,  U7 %fdB, lut %fdB, total %fdB"%(resdata.atten_U6,resdata.atten_U7,-20.0*log10(resdata.lut_sine_amp),att)
	        






##############################################################
#
#
###############################################################

    def findat(self):
        mkid=self.MKID_list[self.current_mkid]
	
	print "enter  attenin db (+number), mkid %f Hz"%(mkid.rough_cent_freq)
	pf=float(raw_input())
	#find res w/ atten of 7.
	
	for k in range(len(mkid.reslist)):
	    
	    resdata=mkid.reslist[k]
	    if resdata.atten_U7==pf:
	    	print "Found"
		self.current_res=k






##############################################################
#
#
###############################################################

    def findat2(self):
        mkid=self.MKID_list[self.current_mkid]
	
	print "enter  attenin db (+number), mkid %f Hz"%(mkid.rough_cent_freq)
	pf=float(raw_input())
	#find res w/ atten 
	
	for k in range(len(mkid.reslist)):
	    
	    resdata=mkid.reslist[k]
	    totalatten= resdata.atten_U7+ resdata.atten_U6 - 20.0*log10(resdata.lut_sine_amp)
	    
	    if abs(totalatten-pf)<1.0:
	    	print "Found"
		self.current_res=k




##############################################################
#
#
###############################################################

    def findat3(self):
        mkid=self.MKID_list[self.current_mkid]
	
	
	pf=mkid.preferred_atten
	#find res w/ atten 
	
	for k in range(len(mkid.reslist)):
	    
	    resdata=mkid.reslist[k]
	    totalatten= resdata.atten_U7+ resdata.atten_U6 - 20.0*log10(resdata.lut_sine_amp)
	    
	    if abs(totalatten-pf)<1.0:
	    	print "Found"
		self.current_res=k



######################################################
# calc iqvel for all traces in mkid, plot maxiqvel vs trace num
#
######################################################

    def iqvel(self):
    
        mkid=self.MKID_list[self.current_mkid]
	
	fit.clearResList()
	fit.addResList(mkid.reslist)
	
	fit.IQvelocityCalc()
	
	
	figure(10)
	clf()
	figure(11)
	clf()
	vlist=[]
	alist = []
	rlist=[]
	
	for k in range(len(mkid.reslist)):
	    
	    vlist.append(mkid.reslist[k].maxIQvel)
	    alist.append(mkid.reslist[k].atten_U7)
	    rlist.append(mkid.reslist[k].maxIQvel_ratio)
	
	figure(10)
	plot(alist, vlist,'x')
	#plot(alist, vlist)

	figure(11)
	plot(alist, rlist,'x')
	
	
	

######################################################
#
#
######################################################

    def plotfit(self):
    
        resdata=  self.MKID_list[self.current_mkid].reslist[self.current_res]
	fit.clearResList()
	fit.addRes(resdata)
	fit.plotResonators()



######################################################
#
#
######################################################

    def start(self):
    	
	self.current_mkid=0
	self.current_res=0



######################################################
#
#
######################################################

    def save(self):
     
        fn2=self.filename + "_" + "%i"%(int(9999*rand()))
	
	
	os.rename(self.filename, fn2)
	
	mkidSaveData(self.filename)

######################################################
#
#
######################################################

    def fit(self):
        resdata=  self.MKID_list[self.current_mkid].reslist[self.current_res]
	resdata.is_ran_fits=0
	fit.clearResList()
	fit.addRes(resdata)
	fit.fitResonators()

######################################################
#
#
######################################################


    def flattenPhase(self):
        print "flatten phase"
        resdata=  self.MKID_list[self.current_mkid].reslist[self.current_res]
	#resdata.is_ran_fits=0
	fit.clearResList()
	fit.addRes(resdata)
	fit.setResIndex(0)
	fit.addLineToPhase()




######################################################
#
#
######################################################

    def inc(self):
        if self.current_res< len(self.MKID_list[self.current_mkid].reslist)-1:
	    self.current_res=self.current_res+1
	else:
	    self.current_res=0
	    self.current_mkid = self.current_mkid +1
	    
	    
   
######################################################
#
#
######################################################

    def nmkid(self):
        
	self.current_res=0
	self.current_mkid = self.current_mkid +1

 
######################################################
#
#
######################################################

    def dec(self):
      if self.current_res>0:
	    self.current_res=self.current_res-1
      else:
	    self.current_mkid = self.current_mkid -1
	    self.current_res=len(self.MKID_list[self.current_mkid].reslist)-1

	
######################################################
#
#
######################################################

    def clf(self):
        figure(1);clf()
	figure(2);clf()
	figure(3);clf()
	figure(4);clf()
	figure(8);clf()
	
######################################################
#
#
######################################################


    def plotFreq(self):

	global lastres	
	resdata=  self.MKID_list[self.current_mkid].reslist[self.current_res]

	lastres=resdata
	IQ=resdata.iqdata
	freqs=resdata.freqs

	IQp=resdata.RectToPolar(IQ)

	figure(1)
	#clf()
	subplot(4,1,1)
	plot(freqs,IQp[0])
	ylabel('Magnitude')
	subplot(4,1,2)
	plot(freqs,resdata.removeTwoPi(IQp[1]))
	ylabel('Phase')
	subplot(4,1,3)
	plot(freqs,IQ[0])
	ylabel('I')
	subplot(4,1,4)
	plot(freqs,IQ[1])
	ylabel('Q')
	draw()
	
	figure(2)
	#clf()
	plot(IQ[0],IQ[1],'x')
	
	plot(0,0,'rx')
	
	
	
	
	try:
	    figure(8)
	    #clf()
	    lf=len(resdata.freqs)-1
	    plot(resdata.freqs[1:lf],resdata.maxIQVel_z)
	    
	    plot(resdata.freqs[1:lf],resdata.maxIQVel_gz)
	except:
	    print "Incomplte IQ velocity"
	
	
	
	try:
	
	

	    ntr = int(resdata.num_noise_traces)

	    figure(3)
	    #clf()
	    subplot(ntr,1,1)
	    figure(4)
	    #clf()
	    subplot(ntr,1,1)
	
	    for k in range(ntr):
		figure(1);subplot(4,1,1)
		fv=resdata.fftcarrierfreq[k] - resdata.srcfreq[k]
		iqn=resdata.iqnoise[k]
		
		
		
		fv=numpy.array([fv] * len(iqn[0]))
		iqnp=resdata.RectToPolar(iqn)
		plot(fv,iqnp[0],'.')
		subplot(4,1,2)
		plot(fv,iqnp[1],'.')
		subplot(4,1,3)
		plot(fv,iqn[0],'.')
		subplot(4,1,4)
		plot(fv,iqn[1],'.')


		figure(2)
		plot(iqn[0],iqn[1],'.')
		
		
		figure(3)
		ax=subplot(ntr,1,k+1)
		plot(iqnp[0])
		
		stdmag=std(iqnp[0])
		md=median(iqnp[0])
		ax.set_ylim((md-3*stdmag,md+3*stdmag))
		
		figure(4)
		ax=subplot(ntr,1,k+1)
		plot(iqnp[1])
		stdph=std(iqnp[1])
		md=median(iqnp[1])
		ax.set_ylim((md -3*stdph,md+stdph))
		print k
		
	except:
	    print "incomplete noise data" 







######################################################
#
#
######################################################
class mvars_(object):pass
	
myvars=mvars_()

	
resv=None				
def hdfshell(fn=None):
    global fit
    global resv
    
    
    try: fit
    except: fit = fitters()
    
    if resv==None:
        resv = hdfShell()
    
    if fn!=None: 
        resv.shellcmds('open %s'%(fn))
	resv.shellcmds('ls')
    
    
    resv.shell()
