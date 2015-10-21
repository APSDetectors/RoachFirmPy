

import multiprocessing


###########################################################################################
#
#
#
#
#
#
###########################################################################################


def findAllResonators(leftfreqM, rightfreqM,rthresh,isplot,datafilename,datafilenum, resfilename):
	global na
	global form
	
	
	

	form.stopSweep()
	
	time.sleep(3)
	
	if isplot==1:
		na.is_plotsweep=1
		
	
	span_fM=120.0
	
	fit.reslist=[]
	
	na.hdfOpen(datafilename,datafilenum)
	
	
	for cent_f in arange(leftfreqM,rightfreqM,0.75*span_fM):
	
		fff=na.calcFreqVals(cent_f*1e6, span_fM*1e6)
		
		lo=fff[0]
		st=fff[1]
		ed=fff[2]
		
		na.setCarrier(lo)
		na.startSweep(st,-1,ed) 

		
		#take one sweep and read roach back.
		na.grabData(1)
		
		if isplot==2:
			form.updatePlot()
		
		
		

		res=na.getResonator()
		
		rr=fit.extractResonators(res,rthresh)
		
		figure(4)
		draw()
		
		print rr
		if (rr!=None):
			fit.addResList(rr) 






	fit.plotResonators()
	draw()
	
	
	
	#now we have rough idea where resonators are in the reslist.
	#extract center frequencies from the resonator objects and then
	#sweep  each one w/ narrow span of 2MHz
	
	span_fM=2.0;
	
	#we copy ptr to reslist, these are iq's of all resonators extracted from
	#wide sweep. We must make new set of iq res obhects with low-span sweeps so 
	#we can fit
	rawreslist=fit.reslist
	fit.clearResList()
	
	
	for rawres in rawreslist:
		
		cent_f=rawres.rough_cent_freq
		fff=na.calcFreqVals(cent_f, span_fM*1e6)
		lo=fff[0]
		st=fff[1]
		ed=fff[2]
		
		na.setCarrier(lo)
		na.startSweep(st,-1,ed) 

		
		#take one sweep and read roach back.
		na.grabData(1)
		
		if isplot==2:
			form.updatePlot()

		res=na.getResonator()

		fit.addRes(res)
		
		
	
	#save to hdf file
	fit.saveResonators(resfilename)
	
	na.is_plotsweep=0

	
		
		

###########################################################################################
#
#
#
#
#
#
###########################################################################################


def hdf_findResonators(filename,search_att, search_span):

	AttenU7=na.HDF_getSetting(filename,'AttenU7');
	span=na.HDF_getSetting(filename,'Freq_Span');
	fc=na.HDF_getSetting(filename,'Freq_Cent');



	ind_att=find(AttenU7==search_att)

	ind_sp=find(span==search_span)

	#indices in the file w/ atten =10 and span =2MHz
	ind = list(set(ind_att).intersection(set(ind_sp)))

	print "Center freqs GHz"
	print fc[ind]/1e9

	fit.clearResList()

	rnum=0

	for ii in ind:
		res=na.HDF_getResonator(filename,ii, rnum)
		fit.addRes(res)
		rnum=rnum+1

	fit.plotResonators()
	draw()

	#fit.fitResonators()
	#fit.saveResonators('myres')

###########################################################################################
#
#
#
#
#
#
###########################################################################################

fit_hosts=['local', 'xraydetector28.aps.anl.gov' , '164.54.85.124']
#fit_hosts=['xraydetector28.aps.anl.gov' , '164.54.85.124']

#
#def fitMultiProcessor():
#
#
#	#path to temp files to store res data and fits. must be on ldap so other systems can get there
#	path='/home/oxygen26/TMADDEN/hdf_files'
#	
#	#
#	#remove all files from path
#	#
#	
#	flist = os.listdir(path)
#	
#	for f in flist:
#	    ff='%s/%s'%(path,f)
#	    os.remove(ff)
#	
#	
#	#
#	# save one mkid per hdf file in temp dir
#	#
#	
#	fnum=0
#	for mkid in MKID_list:
#	    
#	    fname='%s/resfile%02d.hdf'%(path,fnum)
#	    
#	    mkidSaveDataOne(fname, mkid)
#	    fnum=fnum+1
#	    
#	    
#	    
#	    
#	#
#	# Now er call fitting for each hdf file all at once. we have one theread here that fires up a thread for
#	# each mkid. on remote hosts we ssh and call runFits script. local host we call fitOneResonatorFile. 
#	# each mkid has its own thread on local host, and it wither does fits or waits for ssh to return. I have
#	#    local certificate in my .ssh so we can ssh withtout a password.
#	#
#	#ssh xraydetector21 ROACH/projcts/runFits 2
#	
#	#make threadpool. fnum is now number of mkids
#	#one thread per mkid.
#	pool=QThreadPool()
#    	pool.setMaxThreadCount(fnum)
#	
#	nhosts = len(fit_hosts)
#	
#	
#	
#	#!! set max to 3 so we do not debug forever
#	fnum=11
#	for fitnum in range(fnum):
#	    host=fit_hosts[fitnum%nhosts]
#	    runnable=QFitOneMKID(fitnum,host)
#	    status=pool.tryStart(runnable)
#		    
#	    if status==False:
#	        print "could not start mkid %d on host %s"%(fitnum,host)
#	
#	
#	while pool.waitForDone(5000)==False:
#		print "\n\n---Still Running fits---\n\n"
#			
#


###########################################################################################
#
#
#
#
#
#
###########################################################################################
#
#
#def fitOneResonatorFile(fnum):
#
#	global MKID_list
#	fit=fitters()
#	
#	path='/home/oxygen26/TMADDEN/hdf_files'
#	
#	
#	
#	    
#	fname='%s/resfile%02d.hdf'%(path,fnum)
#	    
#	  
#	mkidLoadData(fname)
#	
#	
#	print "Now to fit resonator traces"
#	
#	mkid=MKID_list[0]
#
#	fit.reslist=mkid.reslist
#	fit.fitResonators()
#	
#	fnameout='%s/resfileOUT%02d.hdf'%(path,fnum)
#	mkidSaveData(fnameout)
#	
#	

###########################################################################################
#
#
#
#
#
#
###########################################################################################


#class QFitOneMKID (QRunnable):
#    def __init__(self, n,h):
#        QRunnable.__init__(self)
#        self.fnum=n
#	self.host = h
#        
#	
#	
#    def run(self):
#    
#    	print "###############thread %d, host %s################"%(self.fnum,self.host)
#    	if self.host=='local':
#	    os.system('xterm -e /home/oxygen26/TMADDEN/ROACH/projcts/runFits %d'%(self.fnum)) 
#	    time.sleep(1)
#	else:
#	    os.system('ssh -Y %s xterm -e ROACH/projcts/runFits %d'%(self.host,self.fnum)) 
#	    time.sleep(15)
#	
	
	

 

###########################################################################################
#
#
#
#
#
#
###########################################################################################

global poolx

def fitMP():

    global MKID_list
    global poolx
    
    MKID_list4=MKID_list[0:4]
    
    nproc = len(MKID_list4)
    p= multiprocessing.Pool(nproc)
    poolx=p
	
    results=range(nproc);
    k=0;
    for mkid in MKID_list4:
        results[k]= p.apply_async(fitOneResonatorMP, [mkid])
	k=k+1
	

    return(results)
    	


###########################################################################################
#
#
#
#
#
#
###########################################################################################

from multiprocessing.managers import BaseManager
import Queue
from multiprocessing import Process

global queue1
global queue2
global is_started_mp_queue


try:
    is_started_mp_queue
except:
    is_started_mp_queue=0

#
#  used by our gui. it is the queue that sits on network for multiproc fitting
#


def queueMP():

    global queue1
    global queue2
    global MKID_list
    global poolx

    queue1 = Queue.Queue()
    queue2 = Queue.Queue()
    class QueueManager(BaseManager): pass
    QueueManager.register('get_queue1', callable=lambda:queue1)
    QueueManager.register('get_queue2', callable=lambda:queue2)
    
    m = QueueManager(address=('', 50000), authkey='abracadabra')

   
    

    s = m.get_server()
    s.serve_forever()

#
#  start up a queue that is hosted on the network, called by gui
#

def startQMP():
    global is_started_mp_queue
    
    if (is_started_mp_queue==0):
        
        pc=Process(target=queueMP);
        pc.start()
        is_started_mp_queue=1
	print 'Started Queue'





global is_started_mp_fitter

try:
    is_started_mp_fitter
except:
    is_started_mp_fitter=0


#
#  called by gui. starts a process that does fits. it grabs data from queue on servername.
# call w/ '' if qieie is local server

def startFitServeMP(servername):
    global is_started_mp_fitter
   
    
    if is_started_mp_fitter==0:
        pc=Process(target=dole2proc,args=(servername,));
        pc.start()
	is_started_mp_fitter=1
	print 'Started fit server'
	


#
# runs on fitter process above. used by gui
#

def dole2proc(servername):
    global poolx
    
 

    print "Starting dole2proc"
    print servername
    
    nproc = multiprocessing.cpu_count()
    p= multiprocessing.Pool(nproc)
    poolx=p
	
	
    class QueueManager(BaseManager): pass


    QueueManager.register('get_queue1')
    QueueManager.register('get_queue2')
    m = QueueManager(address=(servername,50000), authkey='abracadabra')
    m.connect()


    q1 = m.get_queue1()
    q2 = m.get_queue2()


    print poolx
    print q1
    print q2
    	
    while 1==1:
    	print "waiting for mkid"
    	mkidtuple = q1.get()
	
	#we expect a tuple of form (int, int, resonatorData object)
	#if 1st int is <0, then we expect reonatorDataObject to be a string.
	#the string is a message of some kind say to kill process pool
	
	if (mkidtuple[0]<0):
	    if mkidtuple[2]=="restart":
	        poolx.terminate()
		poolx.close()
		print "Killed fittings"
		poolx= multiprocessing.Pool(nproc)
    		print "Restart process pool"
	
	else:
	    print "Got mkid"
	    print mkidtuple

            result =  poolx.apply_async(fitOneResonatorMP, (mkidtuple,servername))
	
	
    print "Ending  dole2proc"


###########################################################################################
#
#
#
#
#
#
###########################################################################################

#
# debugging...
#

def fitOneResonatorMP(mkidtuple,servername):

    print "Inside fitres function"
    print servername
    print mkidtuple
    
    mkidnum=mkidtuple[0]
    tracenum=mkidtuple[1]
    restrace=mkidtuple[2]
    
    
    class QueueManager(BaseManager): pass


    QueueManager.register('get_queue1')
    QueueManager.register('get_queue2')
    m = QueueManager(address=(servername,50000), authkey='abracadabra')
    m.connect()


    
    q2 = m.get_queue2()
	
    fit=fitters()
	
    fit.fit_plots=0
	
	
    fit.fit_prints=1
	
	
	
	

    fit.reslist=[restrace]
    fit.fitResonators()
	
    	
    q2.put(mkidtuple)
	
	
	

###########################################################################################
#
#
#
#
#
#
###########################################################################################



global fit_put_q_count
fit_put_q_count=0


global fit_get_q_count
fit_get_q_count=0

def putMkidFitQueue(mlist):
    global fit_put_q_count

    from multiprocessing.managers import BaseManager
    class QueueManager(BaseManager): pass


    QueueManager.register('get_queue1')
    QueueManager.register('get_queue2')
    m = QueueManager(address=('',50000), authkey='abracadabra')
    m.connect()


    q1 = m.get_queue1()
    q2=m.get_queue2()

    for mkid in mlist:
        for res in mkid.reslist:
    
    	    print "Sending MKID %d, Trace %d"%(mkid.resonator_num,res.trace_id)
	    #make tuple w/ res trace object. also send resonator num for mkid and res, so we know which mkid and trace it is.
    	    mkid_tuple=(mkid.resonator_num,res.trace_id,res)
	    q1.put(mkid_tuple);
	    fit_put_q_count=fit_put_q_count+1


###########################################################################################
#
#
# get fitted res from ret queue, for multi proc fitting, updates MKID_list
# ret 0, did not get res. fits still running
# ret 1, got a resonaotr, fits may still be running
# ret 2, didnot get res, fits are done
###########################################################################################


def getMkidFitQueue():
    global MKID_list
    global fit_put_q_count
    global fit_get_q_count
    
    class QueueManager(BaseManager): pass


    QueueManager.register('get_queue1')
    QueueManager.register('get_queue2')
    m = QueueManager(address=('',50000), authkey='abracadabra')
    m.connect()


    q1 = m.get_queue1()
    q2=m.get_queue2()

    try:
        mkid_tuple=q2.get(False)
	print mkid_tuple
	
	for mkid in MKID_list:
	    if mkid.resonator_num == mkid_tuple[0]:
	      for k in range(len(mkid.reslist)):
	        
		if mkid.reslist[k].trace_id==mkid_tuple[1]:
		    mkid.reslist[k] = mkid_tuple[2]
		    print "Updated MKID %d, Trace %d"%(mkid.resonator_num, mkid.reslist[k].trace_id)
		    fit_get_q_count=fit_get_q_count+1
	
	
	return(1)
	
    except:
        if fit_get_q_count==fit_put_q_count:
	    pass
	    #print "In Q count == Out Q Count, fits are done"
	    return(2)
	else:
	    return(0)

###########################################################################################
#
#
#
#
#
#
###########################################################################################

def stopFitsMP():
    

    from multiprocessing.managers import BaseManager
    class QueueManager(BaseManager): pass


    QueueManager.register('get_queue1')
    QueueManager.register('get_queue2')
    m = QueueManager(address=('',50000), authkey='abracadabra')
    m.connect()


    q1 = m.get_queue1()
    q2=m.get_queue2()
    mkid_tuple=(-1,-1,"restart")
   
    q1.put(mkid_tuple);
    


##########################################################################################
#
#
#
#
#
#
###########################################################################################



'''
#to kill all oythons in unix prompt
pkill -f python

#################
#server ron on other comptuers

import os
os.chdir('ROACH/projcts')
execfile('fitters.py')
execfile('controlScripts.py')


startFitServeMP('164.54.85.124')

startFitServeMP('')


#########################
#client run on roach

import os
os.chdir('ROACH/projcts')
execfile('natAnalGui.py')

filename2='/local/hdfFiles/M153_Set5_Chip1_test2.hdf'
mkidLoadData(filename2)


startQMP()

mlist=[MKID_list[0]]

putMkidFitQueue(mlist)




##################################



from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass


QueueManager.register('get_queue1')
QueueManager.register('get_queue2')
m = QueueManager(address=('',50000), authkey='abracadabra')
m.connect()


q1 = m.get_queue1()
q2=m.get_queue2()


a1=(0,0,MKID_list[0].reslist[0])
a2=(0,1,MKID_list[0].reslist[1])
a3=(0,2,MKID_list[0].reslist[2])
a4=(0,3,MKID_list[0].reslist[3])



q1.put(a1)
q1.put(a2)
q1.put(a3)
q1.put(a4)


q2.empty()

aa=q2.get()
aa

MKID_list[aa[0]].reslist[aa[1]]=aa[2]

'''


###########################################################################################
#
#
#
#
#
#
###########################################################################################



def aveFaSpectra():
    global fa
    
    recordlen=len(fa.fft_bins_requested)
    
    nspectra= int(floor( fa.memLen / recordlen))

    amp=fa.extractSpectrum(0)[0]
    
    
    for k in range(1,nspectra):
    	amp = amp + fa.extractSpectrum(k)[0]
    
    return(amp);
    


###########################################################################################
#
#
#
'''
filename='/local/tmadden/data/juldev_fftswfits.hdf'
mkidLoadData(filename)
mkidDump()
resdata=MKID_list[1].reslist[0]

resdata.atten_U6=5
resdata.atten_U7=0

fc=resdata.skewcircle_fr
noiseResonator(1,fc,0,15)
fa.plotIvQNoise(fc-fa.carrierfreq,resdata)
'''
#
#
#
###########################################################################################
global fbase
fbase=0

def noiseResonator(is_loadfw,resdata,isloop,seperation):
	global roach
	global fa
	global at
	global rf

	global fbase
	global sweepres
	
	sweepres=resdata

	if (is_loadfw>0):
  	   

	    #roach=connRoach()
	    time.sleep(1)
	    startFW(roach,fwnames[1])
	    time.sleep(5)

	    setupfad()

	
	
	
	
	fc=resdata.skewcircle_fr
	
	#set attens to same as in the  original sweep
	at.atten_U6=resdata.atten_U6
	at.atten_U7=resdata.atten_U7
	at.atten_U28=resdata.atten_U28
	
	progAtten(roach,at)
	rf.rf_loopback=isloop


	#rf.baseband_loop=1
	
	rf.lo_internal=int(resdata.lo_internal)
	progRFSwitches(roach,rf)

	


	

	

	#if resdata.isneg_freq==1:
	#    fbase=carr-fc

	#else:		    
	#    fbase=fc-carr
	    
  	fbase=resdata.sweep_fbase
	    

	
	if resdata.isneg_freq==1:
	    carr= fc + fbase
	else:
	    carr=fc-fbase
	    
	    
	
	fa.setCarrier(carr)
	
	
	
	print 'fc=%f  carr=%f  fbase=%f  '%(fc,carr,fbase)
	
	print 'Soured freq %f '%(fa.getLegalFreqs([fc])[0])
	
	#fa.setLutSize(1024*1024)
	#fa.test_pulse_amp=60.0
	#fa.test_pulse_len=20000
	
	fa.stopFFTs()
	
	
	
	#fa.setLutFreqsBins([fbase],4,1000)
	
	fa.setLutFreqs([ fbase ],resdata.lut_sine_amp*32768)
	
	fa.fftBinsFreqs()
	

	fa.fftsynctime=512

	fa.roach_num_ffts=65536
	
	fa.roach_fft_shift=resdata.roach_fft_shift
	

	fa.progRoach()

	fa.resetDAC()
	
	fa.trigFFT()
	time.sleep(.5)
	
	noisePlots(resdata, seperation);
	
	iq=fa.captureADC_IQ(0)

        print (180.0/pi)*(angle(fft.fft(iq[1])[896])-angle(fft.fft(iq[0])[896]))





ntime = 1.0

def noisePlots(resdata, seperation):
	
	fa.trigFFT()
	time.sleep(ntime)

	fa.getDFT_IQ();
	
	noisePlots2(resdata, seperation)
	
	

def noisePlots2(resdata, seperation):
	
	
	#sp=fa.extractRecord(1)
	#figure(303);clf();plot(sp[0],sp[1])
	#figure(305);clf();
	#subplot(2,1,1);plot(fa.extractSpectrum(0)[0]);
	#subplot(2,1,2);plot(fa.extractSpectrum(0)[1])
	try:

	    fa.plotTimes(seperation*.001,seperation*.001)
	    #figure(302);clf();semilogy(fa.extractSpectrum(10)[0])
	    fbase=resdata.sweep_fbase
	    
	    ts=fa.extractTimeSeries(fa.getLegalFreqs([fbase])[0])
	    tsr=fa.PolarToRect(ts)
	    figure(301);clf();plot(tsr[0],tsr[1],'x')
	    plot(0,0,'ro')

	    figure(302);clf()
	    plot(tsr[0])
	    plot(tsr[1])
	    
	    figure(101);clf()
	    plot(resdata.trot_xf,resdata.trot_yf,'bx')
	
	    plot(resdata.iqdata[0],resdata.iqdata[1],'gx')
	    
	    
	    
	    

	    #tsr[0] = tsr[0] - mean(tsr[0]) + sweepres.cir_R

	    
	    
	    plot(tsr[0],tsr[1],'rx')
	    
	    
	    tsr_tr=fit.trans_rot3(resdata, tsr)
	    plot(tsr_tr[0],tsr_tr[1],'rx')
	    
	    
	except:
	    print "exception..."    


def plotRes(resdata):
  
	    figure(101);clf()
	    plot(resdata.trot_xf,resdata.trot_yf,'gx')
	
	    plot(resdata.iqdata[0],resdata.iqdata[1],'bx')
	    
	    plot(0,0,'rx')
	    tsr=resdata.iqnoise[0]
	    
	    

	    #tsr[0] = tsr[0] - mean(tsr[0]) + sweepres.cir_R

	    
	    
	    plot(tsr[0],tsr[1],'b.')
	    
	    
	    tsr_tr=fit.trans_rot3(resdata, tsr)
	    plot(tsr_tr[0],tsr_tr[1],'g.')
	    

###########################################################################################
#
#
#
# take mkid list, 1st trace each mkid. extract fitted freq, and add to lut
# set fft bins to return
#
###########################################################################################


def mkid2freqs():
    global fa
    global at
    
    
    maxf=0
    
    flist = []
    
    for mkid in MKID_list:
        res=mkid.reslist[0]
	
	if res.skewcircle_fr> maxf:
	    maxf=res.skewcircle_fr
	    
	if  res.skewcircle_fr>0.0:   
	    flist.append(res.skewcircle_fr)
	else:
	    print "Bad Res fit "
	    
    carr=maxf+10e6
    
    print "Setting carrier to %f MHz"%(carr/1e6)
    fa.setCarrier(carr)
    
    flist=flist[::-1]
    
    flist=array(flist)
    
    print "Freqiencies"
    print flist
    
    fbase=carr - flist
    
    print "BaseBand"
    print fbase
    
    print "Actual freqs to source"
    print fa.getLegalFreqs(fbase.tolist())
    
    ampx=1000.0
    fa.setLutFreqs(fbase.tolist(),ampx)
    
    #rel atten of sweep and lut source
    atten= round(20.0 * log10((32768.0*res.dac_sine_sweep_amp)/ampx))
    
    #now alter atten of attenuator to compensate
    
    at.atten_U6=res.atten_U6
    at.atten_U7=res.atten_U7
    at.atten_U28 = res.atten_U28
    
    if at.atten_U6 > atten:
        at.atten_U6 = at.atten_U6 - atten
	atten=0
    else:
        atten = atten -at.atten_U6
	at.atten_U6 = 0

    
    if atten>0:
	if at.atten_U7 > atten:
            at.atten_U7 = at.atten_U7 - atten
	    atten=0
	else:
            atten = atten -at.atten_U7
	    at.atten_U7 = 0
	    
	    
	    
    print "Difference between readout atten and sweep %d dB"%(atten)	    
	    
    progAtten(roach,at)
    
    fa.fftBinsFreqs()
    fa.progRoach()
    
    fa.resetDAC()
    
        
	    
	    

    	
	
    
    
    
    
    	 




###########################################################################################
#
#
#
#
#
#
###########################################################################################

def sweepResonator(is_loadfw,resdata,isloop,isnoise):
	global roach
	global fa
	global at
	global rf
	global fbase
	global fbw
	global na
	global sweepres
	
	#execfile('natAnalGui.py')

	if is_loadfw==1:
	    fwname ='networkanalyzer_2014_Apr_21_1006.bof'

	    #roach=connRoach()
	    time.sleep(1)
	    startFW(roach,fwname)
	    #time.sleep(5)


	    setupna()
	   
	     
	    #figure(304);clf()
	    
	    #figure(100);clf()
	    #figure(101);clf()

	fc=resdata.skewcircle_fr
	carr=resdata.carrierfreq
	
	if isnoise==0:
	    #set attens to same as in the  original sweep
	    at.atten_U6=resdata.atten_U6
	    at.atten_U7=resdata.atten_U7
	    at.atten_U28=resdata.atten_U28

	    progAtten(roach,at)
	    rf.rf_loopback=0
	    rf.baseband_loop=0
	    na.adc_nloopback=1
	    na.isneg_freq=1
	    
	    if isloop>0:
	        rf.rf_loopback=isloop

	    if isloop>1:
	        rf.baseband_loop=1

	    if isloop>2:
	    	#bugsomehwere, where the loopback is opposite freq then dac
		na.adc_nloopback=0
		na.isneg_freq=0
		
		
		
	    rf.lo_internal=int(resdata.lo_internal)
	    progRFSwitches(roach,rf)

	    na.setCarrier(carr)
	    na.progRoach()
	    na.resetDAC()
	    

	#fa.setLutSize(1024*1024)
	#fa.setLutSize(1024*128)
	if resdata.isneg_freq==1:
	    fbase=carr-fc
	else:		    
	    fbase=fc-carr
	    

	fbw=(resdata.endFreq_Hz - resdata.startFreq_Hz)/2.0
	
	
	if isnoise==1:
	    fbw=0.0
	    
	    
	print 'fc=%f  carr=%f  fbase=%f  fbw=%f'%(fc,carr,fbase,fbw)

	na.resetDAC()
	
	na.startSweep(fbase-fbw,-1,fbase+fbw) 
	
	if is_loadfw==1:
		#40 for loopback, 70 through mikd
		na.setDelay(70e-9)
		
	#na.startSweep(10e6,-1,240e6) 
	
	
	time.sleep(.1)

	getNoise(isnoise)



def getNoise(isnoise):

	global sweepres
	
	na.oneSweep2()
	time.sleep(5)

	iq=na.getDFT_IQ();na.plotFreq(iq)
	
	figure(304);plot(na.RectToPolar(na.iqdata)[0])
	draw()
    
 	
	if isnoise>0:
	    figure(100);plot(na.iqdata[0],na.iqdata[1],'rx')

	else:
	    figure(100);plot(na.iqdata[0],na.iqdata[1],'x')
	    plot(0,0,'ro')
	
	
	draw()
	
	fit = fitters()    
	newres=na.getResonator()
	fit.setResonator(newres)
	
	if isnoise<=0:    
	    fit.fit_circle2()
	    sweepres=newres
	    
	else:
	    newres.cir_R=sweepres.cir_R
	    newres.cir_xc=sweepres.cir_xc
	    newres.cir_yc=sweepres.cir_yc
	
	
	fit.trans_rot2()
	
	

	if isnoise>0:
	    figure(101);plot(newres.trot_xf,newres.trot_yf,'rx')

	else:
	    figure(101);plot(newres.trot_xf,newres.trot_yf,'x')
	    plot(0,0,'ro')

	
	draw()
	



def fitRes():
	fit=fitters()
	fit.clearResList();
	fit.addRes(na.getResonator())
	fit.fitResonators()
	resdata2 = fit.resonator
	return(resdata2)



###########################################################################################
#
#
#
#
#
#
###########################################################################################

'''
	

# the threading or sweeping getting calls this callback
#the function can be redefined in python to dom something more.
#called whenever we get a trace from the roach board getdata() functions

def sweepCallback(): doCallback()
'''
def doCallback():
	na.plotFreq(na.iqdata)
	figure(304);plot(na.RectToPolar(na.iqdata)[0])
	figure(100);plot(na.iqdata[0],na.iqdata[1],'x')
	plot(0,0,'ro')	
	fit = fitters()    
	newres=na.getResonator()
	fit.setResonator(newres)
	fit.fit_circle2()
	sweepres=newres
	fit.trans_rot2()
	figure(101);plot(newres.trot_xf,newres.trot_yf,'x')
	plot(0,0,'ro')







###########################################################################################
#
#
#
'''


filename='/local/tmadden/data/resJul2014_3.hdf'
mkidLoadData(filename)
mkidDump()
resdata=MKID_list[1].reslist[0]
reslist=[ MKID_list[1].reslist[0], MKID_list[3].reslist[0] ]

'''

#
#
#
###########################################################################################

ftime = 0.1

def fftSweep(setup, reslist,span,pts):

	if setup==1:
	    noiseResonator(1,reslist[0],0,0.1)	
	
	fa.stopFFTs()
	
	fa.zeroCoefMem()
	fa.clearFIFOs();
	fa.rewindFFTMem()
	fa.fftBinsFreqs()
	
	fa.roach_num_ffts=1
	fa.progRoach()

	
	###
	
	fc_s=[]
	for resdata in reslist:
	
   	    fc=resdata.skewcircle_fr
	   
	    fc_s.append(fc)
	    
	
	fc_s=numpy.sort(fc_s)
	
	frange=max(fc_s) - min(fc_s)
	if (frange>200e6):
	    print "resonators too far apart, cannot sweep all of them"
	    return
	    
	    
	carr=max(fc_s)+10e6
	
	freqs=carr-fc_s
	freqs = freqs[::-1]

	print "carrier freq %d"%(carr)
	print "Base Freqs"
	print freqs
	print "Res Freqs "
	print fc_s
	
	
	###
	
	
	fa.setLutFreqs(freqs,32500.0/len(freqs))
	
	fa.fftBinsFreqs()

	fa.progRoach()
	
	for cf in arange(
		carr-span/2.0 ,
		carr+span/2.0,
		span/pts ):
		
	    fa.setCarrier(cf)
	    print carr
	    #progAtten(roach,at)
	    #progRFSwitches(roach,rf)
	    #fa.resetDAC()
	    fa.retrigFFT()
	    time.sleep(ftime)

	fa.getDFT_IQ();
	
	print "carrier freq %d"%(carr)
	print "Base Freqs"
	print freqs
	print "Res Freqs "
	print fc_s
	
	
	return(0)
	






###########################################################################################
#
#
#
#
#
#
#
###########################################################################################




def fftCollectTone(outfreq,fbase):

	fa.stopFFTs()
	
	fa.zeroCoefMem()
	fa.clearFIFOs();
	fa.rewindFFTMem()
	
	
	
	fa.roach_fft_shift=255
	fa.roach_num_ffts=65536
	fa.fftsynctime=128
	
	fa.progRoach()


	
	
	
	carr=outfreq+fbase
	
	

	print "carrier freq %d"%(carr)
	
	
	
	###
	
	
	fa.setLutFreqs([fbase],32000)
	
	fa.fftBinsFreqs()

	fa.progRoach()
	
	
		
	fa.setCarrier(carr)
	time.sleep(1.0)
	fa.trigFFT()
	time.sleep(1.0)
	fa.getDFT_IQ();
	



###########################################################################################
#
#
#
#
#
#
#
###########################################################################################


###########################################################################################
#
#
#
#
#
#
#
###########################################################################################


###########################################################################################
#
#
#
#
#
#
#
###########################################################################################








###########################################################################################
#
#
#    def sweepCallback():pass
#
# for debugging
#
###########################################################################################

def dbgit4():
	pass
	


def dbgit3():

	
	
	

	###


	figure(1)
	clf()
	draw()
	figure(2)
	clf()
	draw()
	


	na.stopFFTs()
	na.setLutFreqs([1e6],32000)

	na.fftBinsFreqs()

	na.adc_nloopback=0

	na.progRoach()

	na.trigFFT()

	
	for trial in range(100):

	    

	    time.sleep(rand())
	    iq=na.captureADC_IQ(0)
	    iqp=na.RectToPolar(iq)

	    f=na.frequency_list[0]
	    #f=f*4.0

	    ll=len(iq[0])

	    dphase=2.0*pi*(f/na.sys_clk)
	    ramp = dphase * arange(ll)
	    iqp[1] = iqp[1] + ramp
	    iqp[1]= numpy.unwrap(iqp[1])

	    iqp[1]= abs(iqp[1] - iqp[1][0])
	    
	    
	    print max(iqp[1])
	    
	   
	    
	    if max(iqp[1])>0.002:
		figure(1)
		subplot(2,1,1)
		plot(iq[0])

		subplot(2,1,1)
		plot(iq[1])

		subplot(2,1,1)
		plot(iqp[0])


		subplot(2,1,2)
		plot(iqp[1])

    		draw()


		



	    iq=[na.lut_i, na.lut_q]
	    iqp=na.RectToPolar(iq)

	    f=na.frequency_list[0]
	    #f=f*4

	    ll=len(iq[0])

	    #phase per sample
	    dphase=2.0*pi*(f/na.dac_clk)
	    ramp = dphase * arange(ll)
	    iqp[1] = iqp[1] - ramp
	    iqp[1]= numpy.unwrap(iqp[1])
	    iqp[1]= abs(iqp[1] - iqp[1][0])
	    
	    print max(iqp[1])
	    
	   
	    
	    if max(iqp[1])>0.0002:

		figure(2)
		subplot(2,1,1)
		plot(iq[0])

		subplot(2,1,1)
		plot(iq[1])

		subplot(2,1,1)
		plot(iqp[0])


		subplot(2,1,2)
		plot(iqp[1])

		draw()




def dbgit(dd):

	global MKID_list
	MKID_list = []
	MKID_list.append(MKID(1,'',2555e6))
	
	
	num=50
	na.roach_fft_shift=511
	na.setDelay(dd)
	def sweepCallback():pass

	na.is_resetup_noise=0

	na.sweepResonators(MKID_list,3e6,num)

	fit.clearResList()
	resdata=MKID_list[0].reslist[0]
	resdata.plotFreq()
	resdata.info()
	
	
	

	re=na.getDFTdata(0)
	im=na.getDFTdata(1)

	#not work on res- bad 1st pt
	iq=na.extractBinSeries(na.frequency_list[0])
	#iq=[re,im]
	
	
	iq[0] = iq[0][:num]
	iq[1] = iq[1][:num]
	iqp=na.RectToPolar(iq)
	figure(5)
	
	clf()
	subplot(2,1,1)
	plot(iq[0])
	plot(iq[1])
	plot(iqp[0])
	subplot(2,1,2)
	plot(iqp[1])
	
	
	
	
	fit.addRes(resdata)
	#fit.fitResonators()


	na.noiseResonators(MKID_list,5)
	resdata.plotFreq()
	
	re=na.getDFTdata(0)
	im=na.getDFTdata(1)
	#1st and last points bad...strop them off
	
	ll=len(re)
	
	re=re[1:(ll-2)]
	im=im[1:(ll-2)]
	
	#works!
	#iq=[re,im]
	
	
	#bad 1st pt, phase off from the res.
	iq=na.extractBinSeries(na.frequency_list[0])
	#iq=na.iqdata
	
	iqp=na.RectToPolar(iq)
	
	
	
	freqs=array([num/2]*len(iqp[1]))
	figure(5)
	subplot(2,1,2)
	plot(freqs,iqp[1],'.')
	
	#plot(freqs,iqp[1]-pi/2.0,'.')


	

	subplot(2,1,1)
	plot(freqs,iqp[0],'.')
	
	
	figure(6)
	clf()
	subplot(2,1,1)
	plot(iq[0])
	plot(iq[1])
	plot(iqp[0])
	subplot(2,1,2)
	plot(iqp[1])
	

	#plot(iqp[1]-pi/2.0,'x')
	





def dbgit6():

	global MKID_list
	MKID_list = []
	MKID_list.append(MKID(1,'',3771e6))
	
	
	num=50
	na.roach_fft_shift=511
	na.setDelay(30e-9)
	def sweepCallback():pass

	na.is_resetup_noise=0

	na.sweepResonators(MKID_list,3e6,num)

	fit.clearResList()
	resdata=MKID_list[0].reslist[0]
	resdata.plotFreq()
	resdata.info()
	
	
	
	
	
	
	fit.addRes(resdata)
	fit.fitResonators()


	na.noiseResonators(MKID_list,5)
	resdata.plotFreq()
	
	
	

	#plot(iqp[1]-pi/2.0,'x')
	




def dbgit2():
	
	MKID_list = []
	MKID_list.append(MKID(1,'',2555e6))

	mkid=MKID_list[0]
	
	na.stopFFTs()

	na.zeroCoefMem()
	na.clearFIFOs();
	na.rewindFFTMem()
	na.fftBinsFreqs()

	na.roach_num_ffts=1
	na.fftsynctime=512

	na.progRoach()

	fc=mkid.rough_cent_freq
	carr=fc+10e6
	
	
	fbase=10e6
	
	freqs=[fbase]
	

	###


	na.setLutFreqs(freqs,32500.0/len(freqs))

	na.fftBinsFreqs()

	
	na.progRoach()
	na.setCarrier(carr)

	if 1==0:
	    for k in range(50):
		na.startOutputDac=0;na.progRoach1()
		na.startOutputDac=1;na.progRoach1()
		na.retrigFFT()
		time.sleep(0.1)

	  
	  
	na.printRegs(1,0)
	  
	na.roach_num_ffts=65536
	na.fftsynctime=512

	na.progRoach()

	time.sleep(1)
	na.retrigFFT()
	time.sleep(2)

	na.getDFT_IQ();

	figure(5)
	
	iq=na.iqdata
	iqp=na.RectToPolar(iq)
	#clf()
	subplot(2,1,1)
	plot(iqp[0])
	subplot(2,1,2)
	plot(iqp[1])
	na.printRegs(1,0)
	


#   mkidSaveData('dbg.hdf')
#   na.dbgsave('dbgaaa.bin')
#  for k in range(200,230):print '%d %s'%(k,na.debugobjs[k][0])


def dbgit5(a,b):
    
    for k in range(a,a+b):
        print '%d %s'%(k,na.debugobjs[k][0])


	
def dbgit4():

   
    #na.dbgload('/local/tmadden/data/M129_c1_102_dbg.bin')

    # raw data for sweeps
  #
#423 sweepResonators2,fa
#424 sweepResonators2,printRegs
#624 carrier,anritsupwr
#625 applyDelay,phasep,freqs,carr
#626 getDFTIQ,fa
#627 removeDelayphase
#628 calcSweepDelay,fa
#629 calcSweepDelay,fa
#630 calcSweepDelay,fa
#631 calcSweepDelay,fa
#632 sweepResonators2,fa
#633 sweepResonators2,printRegs
#634 carrier,anritsupwr
#833 carrier,anritsupwr
#834 applyDelay,phasep,freqs,carr
#835 getDFTIQ,fa
#836 removeDelayphase
#837 calcSweepDelay,fa
#838 calcSweepDelay,fa
#839 calcSweepDelay,fa
#840 calcSweepDelay,fa
#
#1057 resonatorNoise,fa
#1058 resonatorNoise,printRegs
#1059 applyDelay,phasep,freqs,carr
#1060 getDFTIQ,fa
#1061 applyDelay,phasep,freqs,carr
#1062 getDFTIQ,fa
#1063 applyDelay,phasep,freqs,carr
#1064 getDFTIQ,fa
#1065 applyDelay,phasep,freqs,carr
#1066 getDFTIQ,fa
#1067 applyDelay,phasep,freqs,carr
#1068 getDFTIQ,fa
#1069 resonatorNoise,fa
#1070 resonatorNoise,printRegs
#1071 applyDelay,phasep,freqs,carr
#1072 getDFTIQ,fa
#1073 applyDelay,phasep,freqs,carr
#1074 getDFTIQ,fa
#1075 applyDelay,phasep,freqs,carr
#1076 getDFTIQ,fa
#1077 applyDelay,phasep,freqs,carr
#1078 getDFTIQ,fa
#1079 applyDelay,phasep,freqs,carr
#1080 getDFTIQ,fa
   
#--------------------------------------------------------
#
#Res 22  fc 3771.7MHz
#MKID_list[14]
#
    
    filename='/local/tmadden/data/M129_c1_102.hdf'

    #mkidLoadData(filename)
    resdata=MKID_list[14].reslist[0]
    
    plotRes(resdata)
    resdata.plotFreq()
    
    swdata0=na.debugobjs[632]
    swhw=na.debugobjs[633]
    carrsw= na.debugobjs[634+100]
    resdata=MKID_list[14].reslist[0]

    swdata1=na.debugobjs[835]


    ndata=na.debugobjs[1060]
    nhw=na.debugobjs[1058]
    
    
    resfreqs=carrsw[1] - swdata0[1].frequency_list 
    
    print 'sweep freqs'
    print resfreqs
    
    noisefreq=ndata[1].carrierfreq - ndata[1].frequency_list 
    
    print 'noise freqs'
    print noisefreq
    
    
    
    print "sweep atten"
    
    report(swhw[1].at)
    
    print 'noise atten'
    
    report(nhw[1].at)
    
    
    #set to sweep raw data
    swdata1[1].iqdata = swdata1[1].I_raw
    
    
    
    
    
    na.setObjSpecs(swdata1[1])

    nres=len(na.frequency_list)
    
    bins=na.extractBinSeries(na.frequency_list[1])
    bins[0] = bins[0][:200]
    bins[1] = bins[1][:200]

    binsp=na.RectToPolar(bins)
    figure(10)
    clf()
    subplot(2,1,1)
    plot(binsp[0])
    plot(bins[0])
    plot(bins[1])
    subplot(2,1,2)
    plot(binsp[1])
    

    ndata[1].iqdata = ndata[1].I_raw
    na.setObjSpecs(ndata[1])

    
    
    bins=na.extractBinSeries(na.frequency_list[0])
    bins[0] = bins[0][1:65000]
    bins[1] = bins[1][1:65000]

    binsp=na.RectToPolar(bins)
    
    ff=array([94]*len(bins[0]))
    
    subplot(2,1,1)
    plot(ff,binsp[0],'.')
    plot(ff,bins[0],'o')
    plot(ff,bins[1],'x')
    
    subplot(2,1,2)
    plot(ff,binsp[1],'.')
    
    
    resdata.info()

###########################################################################################
#
#
#
#
#
#
###########################################################################################




def calcFFTTimeDelay(d1,d2):


  fa.firmware_delay=0.0
  most_dc=0.0;
  most_dc_delay=0.0;
  
  plotcnt=0;
  
  for delay in arange(d1,d2,-1e-9):
    plotcnt=plotcnt+1;
    
    fa.iqdata=ccopy.deepcopy(fa.I_raw)
    
    #fa.setDelay(0)
    fa.xmission_line_delay=0;
    fa.firmware_delay=delay
    fa.applyDelay()
    
    #amp phases
    a_p=fa.extractSpectrum(0)
    
    
    if plotcnt%10==0:
        figure(1);clf();subplot(2,1,1);
	plot(a_p[0]);subplot(2,1,2);plot(a_p[1])
	draw()
    
    
    #get phases where amp >0
    #where uses arrays not lists
    indx=where(a_p[0] >1e-6)[0]
    
    
    phases=[]
    for i in indx:
        phases.append(a_p[1][i])
	
    phases=array(phases)
    PF=abs(fft.fft(phases))
    lf=len(PF)
    
    
      
    if plotcnt%10==0:
        figure(2);clf();
	plot(PF)
	draw()
	print 'dcpcnt %5.5f delay %5.5f mostdly %5.5f'%(dc_percent,delay,most_dc_delay)
	print delay
    
  
    
    
    dc_percent=PF[0]/sum(PF[0:(lf/2)])
    if dc_percent>most_dc:
        most_dc=dc_percent;
	most_dc_delay=delay
	
   
  return(most_dc_delay)
   # 
#    
#    figure(1)
#    clf()
#    plot(phases)
#    draw()
#    
#    figure(2)
#    clf()
#    plot(abs(fft.fft(phases)))
#    draw()
#    
#    
#    
    
    



###########################################################################################
#
#
#
#aa=3
#
#
###########################################################################################

def hdfView(pname,fnum):
	
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
	#is_circle=True;
	is_circle=False;
	
	
	
	pulse_data=[]
	fa.I_raw = [zeros(200), zeros(200)]
	
	
	numptraces=25
	
	specnum=1;
	
	dmode='raw'
	
	wdata = 'raw'
	
	channel_number=0
	cirnoise_bbtau=0.0
	cirsweep_bbtau=0.0
	
	cirnoise_rftau=0.0
	cirsweep_rftau=0.0


	fpga_bug_offset_=0;
	
	if 1==1:
	    for k in range(5000):
		
		fa.hdfReadIQ()
		
		if wdata=='raw':
		   
		    fa.iqdata=fa.I_raw
		
		
		fa.fpga_bug_offset= fpga_bug_offset_
		
		if len(fa.frequency_list)<channel_number:
		    channel_number=0;
		    print "reset channel num 0"
		
		print "N Chans %d"%(len(fa.frequency_list))
		
		print "I_raw vector"
		
		
		if dmode=='raw':
		    
		    iqp=fa.RectToPolar(fa.iqdata)
		   
		if dmode == 'ts':
		   
		   
		    iqp=fa.extractTimeSeries(fa.frequency_list[channel_number])
		    
		

		if dmode == 'bs':
		    
		   
		    iq=fa.extractBinSeries(fa.frequency_list[channel_number])
		    iqp=fa.RectToPolar(iq)
		    

		if dmode == 'spec':
		   
		  
		    iqp=fa.extractSpectrum(specnum)
		    
		   
		
			
		
		    
		figure(1)
		clf()
		subplot(2,1,1)
		plot(iqp[0])
		subplot(2,1,2)
		plot(iqp[1])
		draw()
		
		
		if is_circle:
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
		
		if tt=='keys':
		    print fa.hdffile_r.keys()
		    fa.iq_index = fa.iq_index-1; 
		
		if tt=='q': fa.hdfClose(); return(pulse_data)
		if tt=='-': fa.iq_index = fa.iq_index-2; 
		
		if tt=='r' : 
		    dmode = 'raw'
		    fa.iq_index = fa.iq_index-1; 
		    


		if tt=='getiq' : 
		    wdata = 'getiq'
		    fa.iq_index = fa.iq_index-1; 

		if tt=='getraw' : 
		    wdata = 'raw'
		    fa.iq_index = fa.iq_index-1; 


		if tt=='ts' :
		    dmode='ts'
		    fa.iq_index = fa.iq_index-1; 
		    
		if tt=='bs' : 
		    dmode='bs'
		    fa.iq_index = fa.iq_index-1; 
		
		
		if tt=='spec' : 
		    dmode='spec'
		    fa.iq_index = fa.iq_index-1; 
		
		
		
		if tt=="nbbtime":
		    print "for baseband freq, enter time delay in ns, for noise trace"
		    print "this will change phase of noise in cirnoise"
		    tt=raw_input()
		    cirnoise_bbtau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 
		
	
		
		if tt=="nrftime":
		    print "for rf freq, enter time delay in ns, for noise trace"
		    print "this will change phase of noise in cirnoise"
		    tt=raw_input()
		    cirnoise_rftau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 
		

		if tt=="sbbtime":
		    print "for baseband freq, enter time delay in ns, for sweep trace"
		    print "this will change phase of pplot in cirsweep"
		    tt=raw_input()
		    cirsweep_bbtau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 

	
				

		if tt=="srftime":
		    print "for rf freq, enter time delay in ns, for sweep trace"
		    print "this will change phase of pplot in cirsweep"
		    tt=raw_input()
		    cirsweep_rftau=float(tt)*1e-9
		    fa.iq_index = fa.iq_index-1; 

	
			
		
		if tt=="specnum":
		    print "enter integer for spec number"
		   
		    tt=raw_input()
		    specnum=int(tt)
		    fa.iq_index = fa.iq_index-1; 
	
		
		if tt=='clf':
		
		    figure(10)
		    clf()
		    figure(11)
		    clf()
		    fa.iq_index = fa.iq_index-1; 
		    
		
		if tt=='lut':
		
		    figure(13)
		    
		    
		    subplot(2,1,1)
		    plot(fa.lut_i)
		    subplot(2,1,2)
		    plot(fa.lut_q)
		    draw()
		    fa.iq_index = fa.iq_index-1; 
		    
		    
		#we plot sweep on circle...
		
		    
		#we plot sweep on circle...
		if tt=='cirsweep':
		
		    ll=50
	
		   
		 
		    
		    
		      
		    fa.firmware_delay = cirsweep_bbtau
		    fa.xmission_line_delay=cirsweep_rftau;
		    fa.applyDelay()
		    
		    fa.removeLineDelay()
		    
		    
		    #iqp=fa.extractTimeSeries(fa.frequency_list[3-resnum])
		    fbase=fa.frequency_list[len(fa.frequency_list)-(channel_number+1)]
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
		if tt=='cirsweepall':
		
		    figure(10)
		    clf()
		    
		    figure(11)
		    clf()
		    ll=50
	
		   
		    
		    for channel_number in range(len(fa.frequency_list)):
			#iqp=fa.extractTimeSeries(fa.frequency_list[3-resnum])
			iq=fa.extractBinSeries(fa.frequency_list[len(fa.frequency_list)-(channel_number+1)])
			

			iq[0]=iq[0][:ll]
			iq[1]=iq[1][:ll]
			iqp=fa.RectToPolar(iq)

			fbase=fa.frequency_list[len(fa.frequency_list)-(channel_number+1)]
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
		



		

		if tt=='cirnoise':
		    fa.iq_index = fa.iq_index-1; 
		    
		    fbase=fa.frequency_list[len(fa.frequency_list)-(channel_number+1)]
		    print "noise fbase %f"%(fbase)
		    iqn=fa.iqdata
		    
		    print "channel number %d"%(channel_number)
		    
		   
		    
		    
		    fa.firmware_delay = cirnoise_bbtau
		    fa.xmission_line_delay=cirnoise_rftau;
		    fa.applyDelay()
		    
		    iqnp=fa.extractTimeSeries(fbase)
		    

		    
		   
		    
		    
		    
		    iqn=fa.PolarToRect(iqnp)
		    freqn=fa.carrierfreq-fbase
		    print "noise freq %f"%(freqn)
	
	
		    print "Delay BBtime %f ns"%(cirnoise_bbtau)
		    
		    
		
		 
		        
		    iqn=fa.PolarToRect(iqnp)
		    figure(10)
		    subplot(2,1,1)
		    plot(array([freqn]*len(iqnp[0])),iqnp[0],'.')
		    subplot(2,1,2)
		    plot(array([freqn]*len(iqnp[1])),iqnp[1],'.')

		    figure(11)
		    plot(iqn[0],iqn[1],'.')
		
		if tt=='n':
		    tt=raw_input()
		    fa.iq_index=int(tt)
		
		if tt=='nc':
		    print 'enter which channel'
		    tt=raw_input()
		    channel_number=int(tt)
		    fa.iq_index = fa.iq_index-1; 
		    fbase = fa.frequency_list[len(fa.frequency_list)-(channel_number+1)]
		    print "fbase %f, freq %f"%(fbase,fa.carrierfreq-fbase)
		
		if tt=='np':
		    print 'enter num traces for pulse find'
		    tt=raw_input()
		    numptraces=int(tt)
		    fa.iq_index = fa.iq_index-1; 
		    
		if tt=='info':
		    fa.info(0)
		    fa.iq_index = fa.iq_index-1;
		    
		if tt=="th":
		    print "calc pulse threshold"
		    fa.calcPulseThreshold( [ iqp[0][10:(len(iqp[0])-10)],iqp[1][10:(len(iqp[1])-10)]])
		    fa.iq_index = fa.iq_index-1; 
		    
		if tt=="pltpls":
		    fa.iq_index = fa.iq_index-1; 
		    figure(2)
		    clf()
		    figure(5)
		    clf()
		    
		    figure(6);clf()

		    plot(resdata.trot_xf,resdata.trot_yf)
		    
		    for px in range(len(pulse_data)):
		       
		        figure(2)
			subplot(2,1,1)
			plot(pulse_data[px][0])
			
			subplot(2,1,2)
			plot((180.0/pi)*pulse_data[px][1])
			draw()
			
			
			
			if is_circle:
			    iq_tr=fit.trans_rot3(resdata, fa.PolarToRect(pulse_data[px]))
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
			
		if tt=="field":
		    print "type name of field in class fftAnalyzerd"
		    tt=raw_input()
		    exec "print fa.%s"%(tt)
		    fa.iq_index = fa.iq_index-1; 
		    


		if tt=="python":
		    print "type a python command"
		    tt=raw_input()
		    exec tt
		    fa.iq_index = fa.iq_index-1; 

	  	if tt=="offs":
		    print "type fpga_bug_offset"
		    tt=raw_input()
		    fpga_bug_offset_=int(tt);
		    fa.iq_index = fa.iq_index-1; 
		    
		if tt=='p':
		    
		    print "finding pulses,%d sweeps"%(numptraces)
		    fa.iq_index = fa.iq_index-1;
		    for px in range(numptraces):
			fa.hdfReadIQ() 

			fa.iqdata=fa.I_raw

			if dmode=='raw':
			    iqp=fa.RectToPolar(fa.iqdata)

			if dmode == 'ts':
			    iqp=fa.extractTimeSeries(fa.frequency_list[channel_num])
			  
			if dmode == 'bs':
			    iqp=fa.extractBinSeries(fa.frequency_list[channel_num])
			  


			 
			result=fa.extractPulses(iqp,10,30)
			nplses=result[2]
			pdata=result[1]
			trigger=5*result[0]*fa.magnitude_std + fa.magnitude_exp_val
			print 'Found %d pulses'%(nplses)
			if nplses>0:
		            pulse_data.append(pdata)

			    figure(2)
			    clf()
			    subplot(2,1,1)
			    plot(iqp[0])
			    plot(trigger)
			    subplot(2,1,2)
			    plot(iqp[1])
			    draw()

		    
		   
	
	

###########################################################################################
#
#
#
#aa=3
#
#
###########################################################################################	
	
def dbgfits():
	
	
	#######################
	
	fa.hdfOpenR('/local/tmadden/data/newdev/newdev_sweeps',210)
	
	fa.iq_index=1
	
	
	spec=fa.hdfReadIQ()
	
	ll=200
	
	
	
	
	#iq=[ fa.I_raw[0][:ll], fa.I_raw[1][:ll]  ]
	#iqp=fa.RectToPolar(iq)
	
	iqsave = fa.iqdata
	fa.iqdata=fa.I_raw
	#iqp=fa.extractTimeSeries(fa.frequency_list[3-resnum])
	iq=fa.extractBinSeries(fa.frequency_list[3-resnum])
	fa.iqdata=iqsave

	iq[0]=iq[0][:ll]
	iq[1]=iq[1][:ll]
	iqp=fa.RectToPolar(iq)

	#there should be NO delay to worry about due to adcs, baseband
	#the reason is that we se the same baseband for every step in sweep
	
	#the only delay factor is the RF freqs thru the xmission lines.
	#in this case it is 30ns only. 
	
	fbase=fa.frequency_list[3-resnum]
	
	print "sweep fbase %f"%(fbase)
	
	carrfs=arange(fa.start_carrier,fa.end_carrier, fa.inc_carrier)
	
	freqs=carrfs - fbase
	
	print "sweep center freq %f"%(freqs[100])
	
	
	

	
	
	#iqp2=fa.RectToPolar(iq2)
	figure(1)
	
	figure(1)
	clf()
	subplot(2,1,1)
	plot(freqs,iqp[0][:200])
	subplot(2,1,2)
	plot(freqs,iqp[1][:200])
	draw()
	
	
#
#	subplot(2,1,1)
#	plot(freqs, iqp2[0])
#	subplot(2,1,2)
#	plot(freqs, iqp2[1])
#	draw()
#	
	
	figure(2)
	clf()
	plot(iq[0],iq[1])
	#plot(iq2[0],iq2[1])
	

	

	#get 1st nosie trace##############
	fa.iq_index=resnum*5 + 2
	
	print fa.iq_index
	
	spec=fa.hdfReadIQ()
	
	
	fbase=fa.frequency_list[0]
	#iqnp=	fa.extractTimeSeries(fbase)
	
	#iqn=fa.PolarToRect(iqnp)
	
	print "noise fbase %f"%(fbase)
	iqn=fa.I_raw
	iqnp=fa.RectToPolar(iqn)
	#the phase of iqnp[0] should be same as the phase in the sweep 
	freqn=fa.carrierfreq-fbase
	

	print "noise freq %f"%(freqn)
	
	#iqn2=fa.calcSweepDelay(iqn,freqn)
	
	#iqnp2=fa.RectToPolar(iqn2);
	
	
	
	figure(1)


	subplot(2,1,1)
	plot(array([freqn]*len(iqnp[0])),iqnp[0],'.')
	subplot(2,1,2)
	plot(array([freqn]*len(iqnp[1])),iqnp[1],'.')
#
#	subplot(2,1,1)
#
#	plot(array([freqn]*len(iqnp2[0])),iqnp2[0],'.')
#	subplot(2,1,2)
#	plot(array([freqn]*len(iqnp2[1])),iqnp2[1],'.')
#	




	
	figure(2)
	plot(iqn[0],iqn[1],'.')
	#plot(iqn2[0],iqn2[1],'.')
	



	return(spec)


###########################################################################################
#
#
#
#
#
#
###########################################################################################
def dbgfits2():
	global MKID_list
	
	filename='/local/tmadden/data/newdev/resdata8.h5'
	
	mkidLoadData(filename)
	
	resdata=MKID_list[0].reslist[0]
	
	




###########################################################################################
#
#
#
#
#
#
###########################################################################################

