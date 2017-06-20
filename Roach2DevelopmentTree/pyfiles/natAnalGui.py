import sys, os, random, math, array, fractions
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
import thread

import socket
import matplotlib, time, struct, numpy
#from bitstring import BitArray

import matplotlib.pyplot as mpl
mpl.rcParams['backend.qt4']='PyQt4'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import h5py

import Queue

#from tables import *
#from lib import iqsweep

#Things to update:
#DONE...make filename_NEW.txt only hold information for channel that is changed
#DONE...delete resonator (change FIR?)
#DONE...Do not add custom threshold when zooming or panning plot
#DONE...roughly calculate baseline from snapshot data and show on plot
#WORKING...show originally calculated median/threshold as faded line


execfile('fftAnalyzerR2.py')
execfile('fitters.py')
execfile('katcpNc.py')
execfile('resView.py')
execfile('resonator.py')
execfile('mkidMeasure.py')


execfile('sim928.py')

execfile('agt33250A.py')
execfile('roachEpics.py')

#from fftAnalyzerR2 import *

#from resView import *
#from katcpNc import *




#name of firmware in /boffiles/ on the roach board.

#no windowing i think...
#fwname='networkanalyzer_2013_Dec_10_0946.bof'
#optional 256 len window
#fwname='networkanalyzerwa_2014_Feb_12_1134.bof'
#w/ 32 window
#fwname = 'networkanalyzerwa_2014_Feb_18_1452.bof'


#new- seems to work well




def shutdownEverything():

    
  
    roachlock.acquire();
   
    

    try: fa.capture.shut()
    except: pass


    try: fa.an.shut()
    except: pass

    try: roach.closeFiles()
    except: pass


    roachlock.release()
    form.message_timer.stop()
    


roach_fast_setup = 0

def setupEverything(ip = '192.168.0.70'):

    global roach
    global fit
    global fa
    global na
    global measure
    global sim
    global hdf
    global roachlock
    
     
    roachlock.acquire();
   
    

    try:
    
       
        form.message_timer.start()

        
        roach=katcpNc(ipaddr = ip)
        roach.startNc()
        
        if roach_fast_setup==0:
            fa = fftAnalyzerR2(roach)
        else:
            fa = fftAnalyzerR2(
                roach_ = roach,
                is_calqdr=False)
#        fa = fftAnalyzerR2(
#            roach_=roach,
#            is_powerup=True,
#            is_loadFW=True, 
#            is_calqdr=False,
#            is_anritsu_lo_ = True,
#            is_anritsu_clk_=True, 
#            is_datacap_=False)
#
     
        
        na = fa
        fit=fitters();
        measure = mkidMeasure()
        fa.sourceCapture([10e6],20000)
        time.sleep(.5)
        fa.stopCapture()

        hdf=hdfSerdes()
        status = 0
        
        sim = simNULL()
        
    except:
        print "Error w/ setupEverything"
        status = 1
        traceback.print_exc()

    
    roachlock.release()
    return(status)


is_epics_running = False


temp_ip='192.168.0.70'

fwnames=[
'networkanalyzer_2014_Jun_25_1330.bof' , 
 'fftanalyzeri_2015_Feb_18_1436.bof']


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Channelizer 2')
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        self.is_multitone=False

    #list of ints. which rows in gui are checked in the mkid list on resData tab
        self.checked_list_rows=[]

    
        self.dacStatus = 'off'
        self.dramStatus = 'off'
        self.tapStatus = 'off'
        socketStatus = 'off'
        self.numFreqs=0
        self.ch_all = []
        attens = numpy.array([1. for i in range(256)])
        self.freqRes = 7812.5
        sampleRate = 512e6
        self.zeroChannels = [0]*256
        #writing threshold to register
        self.thresholds, self.medians = numpy.array([0.]*256), numpy.array([0.]*256)
        self.customThresholds = numpy.array([360.]*256)
        self.customResonators=numpy.array([[0.0,-1]]*256)   #customResonator[ch]=[freq,atten]
        self.lastNoiseFFT = None
        self.lastNoiseFFTFreqs = None

        self.is_saveres=False;

        self.is_sweeping=0
        self.plottype=0
        self.plotmode=0

        self.clearplot=1

        #1 for no pulse det, but get raw data. 0 for puse det, get opnly pulses
        self.prawdata=1

        # dictiionary to remember plot zoom settings before clearing..
        self.plot_zoom_settings={"pltype":"NULL" , "autoscale":1}

        #self.extract_thresh=5


        signal_plot=Signal()

        #self.connect(SIGNAL('signal_plot()'), self.updatePlot)
        self.connect(self,SIGNAL('signal_plot()'), self.updatePlot)

     
            
        self.signal_store_text = 'hello'
        
        #true to add a resonance freq on plot click
        self.is_addres_onclick=False

        self.selectwave_points=[-1000,-1000]
        self.selectwave_onclick=True
        self.selectwave_counter = 0

        #true to add a marker, 'x'  on plot click
        self.is_addmark_onclick=False


        self.button_StSweep.setEnabled(True)
       


        #markers on plot, little x's. each entry is an x,y coord on plot.
        self.markerlistx=[]
        self.markerlisty=[]


        # 1 for calc fft on plot, 2 for calc running add fft
        self.is_calc_fft=0
        #running sum of ffts
        self.runfft1=zeros(2048)
        self.runfft2=zeros(2048)
        #1 if we have a sum in the running sum. 0 if it was cleared

        self.is_acc_fft=0;
    
        self.current_resnumber=1;



        #0 for net analuzer FW. names in global fwnames[]
        # 1 for 2k FFT FW.
        self.current_fw_index=0

        self.gui_settings_file='roachpref.py'

        self.fftreslist=[]
    
        global message_queue 
        message_queue = Queue.Queue()
        
        self.message_timer=QTimer()    
        
        self.message_timer.timeout.connect(self.readMessageQueue)    
        self.message_timer.start(500)
        self.timer_count = 0
        #self.pool=QThreadPool()
        #self.pool.setMaxThreadCount(10)
   
#    def get_fit_queue(self):
#        stat=getMkidFitQueue()
#    self.fit_queue_timer_cnt=self.fit_queue_timer_cnt+1
#    #stat==0, running, no mkid retrived
#    #stat==2, fits are done, no mkid retrieved
#    #stat==1, got a new mkid, we should update gui
#    
#        if stat==1:
#        self.is_fits_mp_running=1
#        self.signalPlot()
#
#
#    if stat==2:
#        self.is_fits_mp_running=0
#        
#    if stat==0:
#        self.is_fits_mp_running=1
#
  
        

    def readMessageQueue(self):
    
        self.timer_count = self.timer_count + 1
        try:
            while True:

                self.signal_dict = message_queue.get_nowait()
                if (is_epics_running):
                    epics_queue_fromroach.put(self.signal_dict)


                for kk in self.signal_dict.keys():
   
                    if kk=='LOFreq':
                        lo = self.signal_dict[kk]
                        messx = 'LO = %f'%lo
                        self.status_text.setText(messx)

                    elif kk=='status_string':

                        self.status_text.setText(self.signal_dict[kk])

                    elif kk == 'signalPlot':
                        self.plottype = self.signal_dict[kk]   
                        self.signalPlot()
                        roachlock.acquire()
                        try:
                            iqdata = ccopy.deepcopy(fa.iqdata)
                            freqs_sweep=ccopy.deepcopy(fa.freqs_sweep)
                            iqdata_raw = ccopy.deepcopy(fa.iqdata_raw)
                            iqp =fa.dataread.RectToPolar(fa.iqdata)
                        except:
                            print "problem copying data from fa"

                        roachlock.release()
                        chan = 192
                        try:
                            if is_epics_running:
                                epics_queue_fromroach.put( {'FreqSweepMag':iqp[0]} )
                                epics_queue_fromroach.put( {'FreqSweepPhase':iqp[1]} )
                                epics_queue_fromroach.put( {'FreqSweepI':iqdata[0]} )
                                epics_queue_fromroach.put( {'FreqSweepQ':iqdata[1]} )
                                epics_queue_fromroach.put( {'SweepFreqs':freqs_sweep} )
                                epics_queue_fromroach.put( {'TimeStamps':iqdata_raw[chan]['timestamps']} )
                                epics_queue_fromroach.put( {'RawNoiseMag':iqdata_raw[chan]['stream_mag']} )
                                epics_queue_fromroach.put( {'RawNoisePhase':iqdata_raw[chan]['stream_phase']} )
                                epics_queue_fromroach.put( {'FluxRampPhase':iqdata_raw[chan]['flux_ramp_phase_unwrap']} )

                                reslist_str = mkidList2Str()
                                epics_queue_fromroach.put( {'ResListText':reslist_str} )


                        except:
                            print "problem sending iqdata to epicsQ"


        except:
            pass
            
            
    
        try:
            #this will run as long as there is stuff in epics_queue_toroach. the get no wait will throw exception and
            #exit while loop if the wueue is empty. generally it will just throw... if many things in q then it gets all of them
            while (is_epics_running):                     
                self.epicsmessage_dict = epics_queue_toroach.get_nowait()
                print 'got epics message'
                
                message = self.epicsmessage_dict['message']
                value = self.epicsmessage_dict['value']

                print "qt got %s"%(message)
                
                if message=='form.openClient':
                    if self.epicsmessage_dict['value']>0:
                        self.openClient()
                if message=='form.reOpenClient':
                    if self.epicsmessage_dict['value']>0:
                        self.reOpenClient()
                elif message=='form.closeClient':
                    if self.epicsmessage_dict['value']>0:
                        self.closeClient()
                elif message=='form.startSweep':
                    if self.epicsmessage_dict['value']>0:
                        self.startSweep()
                elif message=='form.runStop':
                    if self.epicsmessage_dict['value']>0:
                        self.runStop()
                        
                elif message=='form.spinbox_SpanFreq':
                    value =  self.epicsmessage_dict['value']
                    self.spinbox_SpanFreq.setValue(value)           
                elif message=='form.spinbox_CenterFreq':
                    value =  self.epicsmessage_dict['value']
                    self.spinbox_CenterFreq.setValue(value)           
                elif message=='form.spinbox_numSwPts':
                    value =  self.epicsmessage_dict['value']
                    self.spinbox_numSwPts.setValue(value)     
                    
                    
                elif message=='form.extractRes':
                    if self.epicsmessage_dict['value']==1:
                        self.extractRes()
                        reslist_str = mkidList2Str()
                        epics_queue_fromroach.put( {'ResListText':reslist_str} )
                     
                elif message=='form.clearResList':
                    if self.epicsmessage_dict['value']==1:
                        self.clearResList()
                        reslist_str = mkidList2Str()
                        epics_queue_fromroach.put( {'ResListText':reslist_str} )
               

                elif message=='form.res_list_text':
                    fliststr = self.epicsmessage_dict['char_value']
                    fliststr = 'resonator_freqs = ' + fliststr
                    print fliststr
                    exec(fliststr)
                    
                    pyListToMkidList(resonator_freqs,1e6)         
                    reslist_str = mkidList2Str()
                    epics_queue_fromroach.put( {'ResListText':reslist_str} )
               
               
                       
                elif message=='form.savePlot2':
                    if self.epicsmessage_dict['value']==1:
                        self.savePlot2()
                
                elif message=='form.loadSweepPlot2':
                    if self.epicsmessage_dict['value']==1:
                        self.loadSweepPlot2()
                        sweepCallback()
                
                elif message=='form.temp_sweep_fname':                    
                    self.temp_sweep_fname = self.epicsmessage_dict['char_value']

                elif message=='form.signalPlot':
                    if self.epicsmessage_dict['value']==1:
                        message_queue.put({'signalPlot':1})   
   
                elif message=='form.checkbox_BBLoopback':                  
                    form.checkbox_BBLoopback.setChecked(
                        self.epicsmessage_dict['value'])
 
                elif message=='form.checkbox_RFLoopback':                  
                    form.checkbox_RFLoopback.setChecked(
                        self.epicsmessage_dict['value'])

                elif message=='form.checkbox_FPGALoopback':                  
                    form.checkbox_FPGALoopback.setChecked(
                        self.epicsmessage_dict['value'])

                elif message=='form.checkbox_extClk':                  
                    form.checkbox_extClk.setChecked(
                        self.epicsmessage_dict['value'])
 
                elif message=='form.calibrateIQCircles':
                    if self.epicsmessage_dict['value']==1:
                        self.calibrateIQCircles2()
 
                elif message=='form.loadIQCircleCal2':
                    if self.epicsmessage_dict['value']==1:
                        self.loadIQCircleCal2() 
 
 
                elif message=='form.saveIQCircleCal':
                    if self.epicsmessage_dict['value']==1:
                        self.saveIQCircleCal2() 
 
 
                elif message=='form.temp_iqcircalfname':                    
                    self.temp_iqcircalfname = self.epicsmessage_dict['char_value']

                elif message=='form.temp_ivvoltspecs':                    
                    self.temp_ivvoltspecs = self.epicsmessage_dict['char_value']
                    self.textbox_ivrange.setText(self.temp_ivvoltspecs)
                    vlisttxt = self.temp_ivvoltspecs.split(':')
                    vlista = []
                    for vt in vlisttxt:
                        vlista.append( float(vt)  )
                   
                    vlist = numpy.arange(vlista[0], vlista[1], vlista[2])
                    fa.iv_vlisttemp = vlist
                    
                    
                elif message=='form.temp_ivfilename':                    
                    fa.iv_fnametemp = self.epicsmessage_dict['char_value']
                    self.textbox_ivfilename.setText(fa.iv_fnametemp)
 
                elif message=='form.noisetemp_fname':                    
                    fa.noisetemp_fname = self.epicsmessage_dict['char_value']
 
 
                elif message=='form.combobox_str_frd':
                    value =  self.epicsmessage_dict['value']
                    self.combobox_str_frd.setCurrentIndex(value) 
                    fa.temp_frdci = value         
 
                elif message=='form.combobox_syncsource':
                    value =  self.epicsmessage_dict['value']
                    self.combobox_syncsource.setCurrentIndex(value)
                    self.temp_combobox_syncsource  =  value
                           
                
                elif message=='form.checkbox_teson':                  
                    self.checkbox_teson.setChecked(
                        self.epicsmessage_dict['value'])
                    self.temp_checkbox_teson = self.epicsmessage_dict['value']
                    

                elif message=='form.textbox_flxRmpPrd':                    
                    cvalue = self.epicsmessage_dict['char_value']
                    self.textbox_flxRmpPrd.setText(cvalue)
                    fa.temp_numprd = float(cvalue)

                elif message=='form.noisetemp_timesec':                    
                    cvalue = self.epicsmessage_dict['char_value']
                    self.textbox_streamsec.setText(cvalue)
                    self.noisetemp_timesec = float(cvalue)

                         
 
                elif message=='form.streamRun':
                    if self.epicsmessage_dict['value']==1:
                        self.streamRun2()
                elif message=='form.sweepTesIV':
                    if self.epicsmessage_dict['value']==1:
                        self.sweepTesIV2()
 
                      
                else:
                    print "Unsupported epics message %s"%message


                    
                    
        except:
            pass
            
              
    
    def closeClient(self):
    
        thread.start_new_thread(runShutdownEverything,())

    def openClient(self):
            #roach = corr.katcp_wrapper.FpgaClient(self.textbox_roachIP.text(),7147)
        global roach_fast_setup 
        
        roach_fast_setup=0
        
        ip=str(self.textbox_roachIP.text())
        #execfile(self.gui_settings_file);
        
        #setupEverything(ip)
        
        global temp_ip
        temp_ip = ip

        #self.status_text.setText('connection established')
        #print 'Connected to ',self.textbox_roachIP.text()
        thread.start_new_thread(runSetupEverything,())
        

    def reOpenClient(self):
    
        global roach_fast_setup 
        
        roach_fast_setup=1
        
        ip=str(self.textbox_roachIP.text())
        #execfile(self.gui_settings_file);
        
        #setupEverything(ip)
        
        global temp_ip
        temp_ip = ip

        #self.status_text.setText('connection established')
        #print 'Connected to ',self.textbox_roachIP.text()
        thread.start_new_thread(runSetupEverything,())
  
    def setBiasSource(self,ci):
        print 'setBiasSource'
        #ci = self.combobox_biassource.currentIndex()
        #null vsource
        fa.temp_biassource_index=ci
        thread.start_new_thread(runSetupBiasSource,())
        
                
  
    def setRampGenerator(self,ci):
        print 'setRampGenerator'
        #ci = self.combobox_biassource.currentIndex()
        #null vsource
        fa.temp_rampgenerator_index=ci
        thread.start_new_thread(runSetupRampGenerator,())
        
#na.setDelay(30e-9); print na.delay
    def plotPolar(self):
        roachlock.acquire()
    

    
    
        #!!na.setDelay(1e-9*float(self.textbox_Dly.text()));

        iqf=self.getIQF()
        iq=iqf[0]
        freqs=iqf[1]

        iqp=na.dataread.RectToPolar(iq)

        if na.incrFreq_Hz<0.001:
            freqs=numpy.arange(na.memLen/8);

        
    #na.plotFreq(iq)

        if self.clearplot==1:
            self.fig.clear()


        self.axes0 = self.fig.add_subplot(1,1,1,polar='true')
        self.axes0.set_xlabel('I')
        self.axes0.set_ylabel('Q')    

        if self.clearplot==1:
            self.axes0.clear()

        self.axes0.set_autoscalex_on(False)
        self.axes0.set_autoscaley_on(True)
        self.axes0.plot(iqp[1],iqp[0])

        self.canvas.draw();

        roachlock.release()
        print "plot done"

    

    
#    if (self.is_sweeping==1):    
#        self.timer=QTimer()    
#        self.timer.timeout.connect(self.plotPolar)
#        self.timer.setSingleShot(True)
#        self.timer.start(1000)
                
     
    def find_nearest(self, array, value):
        idx=(numpy.abs(array-value)).argmin()
        return idx

    def loadCustomThresholds(self):
        a=1 
 
    def rmCustomThreshold(self):
        a=1 
 
    def setCustomThreshold(self,event):
        a=1 
 
    def loadThresholds(self):
        a=1 
 

    def loadSingleThreshold(self,ch):
        a=1 
        
    def snapshot(self):       
        a=1 
    
      
  
    #get selected or checked MKID obhects in the gui list
    def getMkidSelectedChecked(self,wlist):
        
     

        selected=wlist.selectedItems()
        #selected list
        slist=[]
        #checked list
        clist=[]

        if len(selected)>0:
            #slist.append(selected[0].data(0,100))
            slist.append(selected[0].mkid)
            
        for row in range(wlist.topLevelItemCount()):
            item=wlist.topLevelItem(row)
            if item.checkState(0)==Qt.Checked:
                #clist.append(item.data(0,100))
                clist.append(item.mkid)
                #item.data(0,100).checked=1
                item.mkid.checked=1
            else:
                #item.data(0,100).checked=0
                item.mkid.checked=0




        return([clist,slist])

    #get list of ints, the rows, of the checked items in gui list



    #get list of ints, the rows, of the checked items in gui list




    def runNoise(self):
         

        #runs on THIS thread
        #na.powerSweep(self.at_inst,self.at_st,self.at_inend,self.at_step,self.at_sweeps,self.resonator_span,self.mlist)
        measure.measspecs.num_noise_traces = self.spinbox_numNoise.value()
        ntime = float(self.textbox_noisesec.text())
        
        measure.setNoiseTime(ntime)
        measure.runNoise()


       
    
    #setup power sweep from gui settings    
 

   #calculate IQ velocity
    def IQvelocity(self):
        print "------Calculating IQ velocity, Fit Circle ----------"

        #figure(111)
        #clf()
        for m in self.mlist: #loops through list of resonators
            fit.reslist=m.reslist
            print "Calc IQVel, MKID %fHz"%(m.getFc())
            fit.IQvelocityCalc()
            print "Fit Circle %fHz"%(m.getFc())
            fit.fitCircleCalc()


        


   
    #run fits on gui thread

    def runFits2(self):
        
        for m in self.mlist:

            print "------------Fitting Resonator %d----------"%(m.resonator_num)

            fit.reslist = m.reslist

            fit.fitResonators()

    #run fits on a group of threads

    def runFits3(self):
    
        pool=QThreadPool()
        pool.setMaxThreadCount(10)


        for m in self.mlist:

            print "------------Fitting Resonator %d----------"%(m.resonator_num)

            #fit.reslist = m.reslist

            #fit.fitResonators()

            for res in m.reslist:
                runnable=QRunFit(res)
                status=pool.tryStart(runnable)
                while status==False:
                    print "Out of threads- wait and try again"
                    time.sleep(10)
                    status=pool.tryStart(runnable)


                print "Started thread for resonator"


        while pool.waitForDone(5000)==False:
            print "\n\n---Still Running fits---\n\n"


    #run fits on separate processes, 
    def runFits4(self):        
    #on controlscripts.py, starts Queue that any computer can get to via tcp 
    #if queue is already running it won't start it again.
        startQMP();
    #start process that gets queue items and dies fits. this runs on local system
    #if already running then not started again..
        startFitServeMP('')

    #send the selected resonators to the fitting quque for multiproc fitting
        putMkidFitQueue(self.mlist)
    



    def startMPQueue(self,state):
        global is_use_multiprocess
        is_use_multiprocess=0
    
        #!!
        #!!if state>0:
        if False:
            is_use_multiprocess=1
            print "Using Queue and  fit server"
            startQMP()
            time.sleep(2)
            startFitServeMP('')
    
    



    def stopRepeat(self):
        self.timer.stop()
        self.button_runbyhour.setStyleSheet("background-color: grey")
    



    def stopIt(self):
        #tell processes to stop fits. we may have several cpus connected, so we should send several times.

        #stop polling thread. stops polling for fit quque, finished fits. also stops power sweep thread
        global is_thread_running
        is_thread_running=0
        na.thread_running=0
        self.is_saveres=False


    def naTrace2ResTrace(self):
        
        global MKID_list
        selected=self.list_reslist.selectedItems()
    
        if len(selected)>0:

            #get selected mkid

            #mkid=selected[0].data(100)
            mkid=selected[0].mkid
            
            #get current trace into res data object
            res=na.getResonator()
            #add this trace to the res
            mkid.addRes(res)    
            self.updatePlot()

        
                
  
    def addResonator(self,state):  
        self.is_addres_onclick=False
        if (state>0):
            self.is_addres_onclick=True
        




    def addMark(self,state):
        pass;
    
 
    def plotClick(self,event):
    
        print 'xdata %f ydata %f but %d '%(event.xdata,event.ydata,event.button)
    
        if self.is_addres_onclick:
            print "Adding Resonator"
            #we get radisns from 0 to 2pi for polar plot, 
            #make sure not a polar plot
            if self.plottype==1:

                ff=event.xdata

                ap=event.ydata

                measure.device_name = str(self.textbox_devicename.text())
                mkid = measure.newMkid(ff)
                mkid.chip_name = str(self.textbox_devicename.text())
                MKID_list.append(mkid)



                self.updatePlot()

            else:
                print "Cant add resonance on this plot"

        if  self.selectwave_onclick and self.plottype ==  12 and event.button==2:
            if self.selectwave_counter%3==0:
                print "select 1st point %f"%event.xdata
                self.selectwave_points[0] = event.xdata
            elif self.selectwave_counter%3==1:
                print "select 2nd point %f"%event.xdata
                self.selectwave_points[1] = event.xdata
                # self.selectwave_onclick=False
                self.updatePlot()
            else:
                print "no selection"
                self.selectwave_points =[-1000,-1000] 
                self.updatePlot()

            self.selectwave_counter=self.selectwave_counter+1 

        if self.selectwave_points[0]>=0 and self.selectwave_points[1]>=0:
            k = fa.iqdata_raw.keys()[0]
            evtlen = fa.iqdata_raw[k]['event_len'][0]
 
            sel_len = int(round(abs(self.selectwave_points[1] - self.selectwave_points[0]  )))
            if sel_len > fa.max_event_len:
                sel_len = fa.max_event_len

            sel_start = int(round(min( self.selectwave_points[0], self.selectwave_points[1])))
            sel_delay = sel_start%evtlen
            print 'sel_len %d sel_start  %d sel_delay  %d'%(sel_len ,sel_start ,sel_delay )
            self.textbox_FRDLen.setText('%d'%(sel_len)) 
            self.textbox_FRDDly.setText('%d'%(sel_delay)) 
            self.updatePlot()




    def extractRes(self):
        global MKID_list
        
        measure.device_name = str(self.textbox_devicename.text())
        mkid = measure.newMkid(0)
        res=measure.getResonator(mkid)
        nsg=float(self.textbox_extract_thresh.text())
        rr=fit.extractResonators(res,nsg)

        for rx in rr:
            mkid =measure.newMkid(rx.rough_cent_freq)
            MKID_list.append(mkid)
            

        self.updatePlot()
       

  
    def channelInc(self):
        a=1 
        
    def toggleDAC(self):
        a=1 
  
    def loadIQcenters(self):
        a=1 
  
    def select_bins(self, readout_freqs):
        a=1 
  
    def loadLUTs(self):
        a=1 
   
    def importFreqs(self):
        a=1



    def sweepTesIV(self):
  

      
        vrangetxt =  str(self.textbox_ivrange.text()  )
        vlisttxt = vrangetxt.split(':')
        vlista = []
        for vt in vlisttxt:
            vlista.append( float(vt)  )
            
        
        vlist = numpy.arange(vlista[0], vlista[1], vlista[2])
        fname = str(self.textbox_ivfilename.text())
        
        
          
        (frd,frdci) =self.flxRampComboDecode()
          
        numprd = float(self.textbox_flxRmpPrd.text())
        
        frdlen = float(self.textbox_FRDLen.text())
        frddly = float(self.textbox_FRDDly.text())
        ci = self.combobox_syncsource.currentIndex()
       
       
        roachlock.acquire()
             
         
        fa.syncdelay_temp = 128* frddly
        fa.frdlen_temp = frdlen
        fa.temp_open_or_closedloop = ci
  
        fa.temp_numprd =  numprd
        fa.temp_frd = frd
        fa.temp_frdci = frdci
 
        fa.iv_vlisttemp = vlist
        fa.iv_fnametemp = fname
        fa.iv_bbtemp = measure.measspecs.andata_trans['fa.sram.frequency_list']
        fa.iv_lotemp = measure.measspecs.andata_trans['fa.LO']
        roachlock.release()
        self.plottype = 10
       
        
        #!!status=self.pool.tryStart( runnable )
        thread.start_new_thread(runSweepTesIV,())
        

             
  #load FW, sweep res and stream
    def calibrateIQCircles(self):

  

        mlist = MKID_list

            
            
        fa.temp_rffreqs_rough = []
        
        for mkid in mlist:
            fa.temp_rffreqs_rough.append(mkid.getFc())

        self.setAttenFromGUI()

        
        self.noisetemp_timesec =  float( self.textbox_streamsec.text()  )
        self.noisetemp_fname = str(self.textbox_streamfilename.text())
        
        thread.start_new_thread(runSweepProgTranslators,())
        #fa.sweepProgTranslators(rffreqs_rough)      
 
   
    def plotTranslatorCal(self):        
        
        figure(1)
        clf()
        #print rffreqs_
        for m in measure.measspecs.mlist_trans: 
           m.reslist[0].plotFreq(isclf=0,is_pl_trot=False)        
            


    def saveIQCircleCal(self):
    
        
        
        self.temp_iqcircalfname = str(QFileDialog.getSaveFileName(
            caption='Hdf File Name',
            options=QFileDialog.DontConfirmOverwrite))
    
        self.saveIQCircleCal2()

    def saveIQCircleCal2(self):
    
        if self.temp_iqcircalfname != '':
            measure.saveTranslatorSweepData(self.temp_iqcircalfname)    
   


    def loadIQCircleCal(self):
    
        self.temp_iqcircalfname = str(QFileDialog.getOpenFileName(caption='Hdf File Name'))
        self.loadIQCircleCal2()

    def loadIQCircleCal2(self):
    

        if self.temp_iqcircalfname!='':
            measure.loadTranslatorSweepData(self.temp_iqcircalfname)    
    
        self.plottype = 11
        self.signalPlot()
        
    
    
      
    #load FW, sweep res and stream
    def streamRun(self):
        print "form.streamRun()"
        #calc amps for multuitones on MKID list
        self.is_multitone=True    
        
        timesec_ =  float( self.textbox_streamsec.text()  )
        fname_ = str(self.textbox_streamfilename.text())
        
     
        
        
      
        
        tesvolts =  float(self.textbox_tesVolts.text())
        is_tes_on = self.checkbox_teson.isChecked()
        
        ci = self.combobox_syncsource.currentIndex()
          
        (frd,frdci) =self.flxRampComboDecode()
          
        numprd = float(self.textbox_flxRmpPrd.text())
        rampon = self.checkbox_rampon.isChecked()
        rampvolts =  float(self.textbox_rampvolts.text())       
        
        rampfreq = float(self.textbox_rampfreq.text())


        frdlen = float(self.textbox_FRDLen.text())
        frddly = float(self.textbox_FRDDly.text())

        #!!maxfrddly = (fa.rfft.dac_clk / fa.rfft.fftLen) / rampfreq
        #!!if frddly>=maxfrddly:
        #!!   frddly =  0
        #!!   print "ERROR max sync delay too large"
        
        roachlock.acquire()       
        fa.temp_is_tes_on = is_tes_on
        fa.temp_tesvolts = tesvolts
        #rffreqs_ = measure.measspecs.rffreqs
     
        fa.temp_open_or_closedloop = ci
  
        fa.temp_numprd =  numprd
        fa.temp_frd = frd
        fa.temp_frdci = frdci
        fa.temp_rampon = rampon
        fa.temp_rampvolts = rampvolts
        fa.temp_rampfreq = rampfreq 

        fa.noisetemp_timesec = timesec_
        fa.noisetemp_fname = fname_
        
        
        fa.syncdelay_temp = 128* frddly
        fa.frdlen_temp = frdlen
        self.setAttenFromGUI()
        roachlock.release()
        
        self.plottype=5;
        print "starting new theead"
        thread.start_new_thread(runCaptureNoise,())
      

 
    def saveSweep(self):
    
        hdf=hdfSerdes()
        
        fname = str(QFileDialog.getSaveFileName(
            caption='Hdf File Name',
            options=QFileDialog.DontConfirmOverwrite))
            
        roachlock.acquire()
        hdf.open(fname,'a')
        gname = 'sweep_%s'%time.asctime().replace(' ','_')
        hdf.write(fa.getUsefulData(),gname)
        hdf.close()
        roachlock.release()    
  
    def savePlot(self):
        self.temp_sweep_fname = str(QFileDialog.getSaveFileName(
            caption='Hdf File Name',
            options=QFileDialog.DontConfirmOverwrite))
            
        self.savePlot2()
        
        
    def savePlot2(self):
      
        fname = self.temp_sweep_fname
        hdf=hdfSerdes()    
        roachlock.acquire()
        hdf.open(fname,'w')
        gname = 'plot_%s'%time.asctime().replace(' ','_')
        iqp = fa.dataread.RectToPolar(fa.iqdata)
        pldata = fa.getUsefulData()
        pldata['fa.iqdata_polar']=iqp     
             
             
        hdf.write(pldata,gname)
        hdf.close()
        roachlock.release()    
        #pickle.dump(pldata,open(fname+'.pic','wb'))
        
        
         
    def loadSweepPlot(self):     
        self.temp_sweep_fname = str(QFileDialog.getOpenFileName(caption='Hdf File Name'))
        self.loadSweepPlot2()
        self.plottype = 1
        self.signalPlot()
        
    def loadSweepPlot2(self):
    
        fname = self.temp_sweep_fname
        hdf=hdfSerdes()    
        
        hdf.open(fname,'r')
        dat = hdf.read()
        hdf.close()
        roachlock.acquire()
        pldata = fa.setUsefulData(dat)
        roachlock.release()    
    
    
    def startSweep(self):
    
        cf = self.spinbox_CenterFreq.value()
        self.is_multitone=False
    
        sf = self.spinbox_SpanFreq.value()

        st = cf - sf/2
        ed = cf + sf/2
        
        self.setAttenFromGUI()     
        #status=self.pool.tryStart( runnable )
        npts = self.spinbox_numSwPts.value()
        
        success = roachlock.acquire()
       
        fa.temp_span_Hz = sf*1e6
        fa.temp_center_Hz = cf*1e6
        fa.temp_pts = npts

        roachlock.release()
        #self.button_StSweep.setEnabled(True)
        
        
        
        
        thread.start_new_thread(runIQSweep,())
        



    
    ##
    # Called when we run Noise, Sweep, or adjust attens. When sweep, we use ONE tone. When noise we use all
    #freqs in MKID_list. 

    def setAttenFromGUI(self):
    
 
        pwrdbm =self.spinbox_ResPwrOut.value()
        if self.is_multitone:
            num_tones = len(MKID_list);
            if num_tones ==0: num_tones = 1
        else:
            num_tones = 1
        
        (amp, atu6, atu7, atu28) = calcSineampAttensFromResPower(num_tones, pwrdbm)
        rfout =calcRfPowerOutputDBm(amp,atu6,atu7)


        self.label_AttenSets.setText("Amp=%5.0f, U6=%2.1f, U7=%2.1f,U28=%2.1f RF2Cryo=%2.1f RF2Res=%2.1f,Ntones=%d"%(
                amp, atu6, atu7, atu28,rfout, pwrdbm,num_tones))
        
        roachlock.acquire()
        fa.if_board.at.atten_U6=-atu6
        fa.if_board.at.atten_U7=-atu7
        fa.if_board.at.atten_U28=-atu28
        fa.if_board.progAtten(fa.if_board.at)
        fa.amplitude = amp

        fa.power_at_resonator = pwrdbm 
        fa.power_at_ifboard_rfout=rfout
        roachlock.release()
        

    

   
    
    
    
        
    def bbLoopback(self,state):
        
        roachlock.acquire()
        if state==2:
            fa.if_board.rf.baseband_loop=1
        else:
            fa.if_board.rf.baseband_loop=0
        
        fa.if_board.progIfBoard()
        roachlock.release()   




    def extClk(self,state):
    
        roachlock.acquire();
        if state==2:
            fa.if_board.rf.lo_internal=0
        else:
            fa.if_board.rf.lo_internal=1
        
        fa.if_board.progIfBoard()
        roachlock.release()
    
    #self.rfOutEn(0)    


    def rfOutEn(self,state):
    
        roachlock.acquire()
        if state==2:
            fa.if_board.LO.rfouten=1
        else:
            fa.if_board.LO.rfouten=0
        
    
        fa.if_board.progIfBoard()
        roachlock.release()


    def rfLoopback(self,state):
        roachlock.acquire();
        
        if state==2:
            fa.if_board.rf.rf_loopback=1
        else:
            fa.if_board.rf.rf_loopback=0
        
        fa.if_board.progIfBoard()
        roachlock.release()
            
            
    def fpgaLoopback(self,state):
        roachlock.acquire()
        if state==2:
            na.is_digital_loopback=1
        else:
            na.is_digital_loopback=0
        roachlock.release()
        
        
        
    ##
    # save list of resonator freqs as a text file, in python language list
    #
 
    
    def textResSave(self):
        
        filename = str(QFileDialog.getSaveFileName(
            caption='Hdf File Name'))

        mlist2Pylist(filename)
    

    
    ##
    # load list of resonator freqs as a text file, in python language list
    #
    def textResRead(self):
        filename = str(QFileDialog.getOpenFileName(caption='Hdf File Name'))
        #filename=self.textbox_HDF5ResName.text()
        pyListFileToMkidList(filename)
        self.populateListWidget()
    

        
    ##
    # Main functio for calling all the plots, based on whcuh plot you want. is a slot, signal_plot() calls this
    #
    def updatePlot(self):
    
        #try:
        if 1==1:

            if (self.plottype==3):
                self.plotPolar()


            if (self.plottype==0):
                self.fourPlots()

            if (self.plottype==4):
                self.plotIvQ()


            if (self.plottype==1):
                self.magPhasePl()



            if (self.plottype==2):
                self.IQPlots()


            if (self.plottype == 7):
                    self.plotIQCircle()

            if (self.plottype ==  5):
                    self.plotMultiChanMagPh();


            if (self.plottype ==  9):
                    self.plotChan3D();

            if self.plottype == 10:
                self.plotIVCurves()
            
            if self.plottype==11:
                self.plotTranslatorCal()                
            
            if self.plottype==12:
                self.plotRampPhaseSelection()

        #except:
        else:
            print 'natAnalGui::updatePlot- Exception'
            print 'plot type %d, %s'%(self.plottype,self.plot_names[self.plottype])
            traceback.print_exc()
            roachlock.release()

    
        self.populateListWidget()
        self.updateCalResListDisplay()
    
    ##
    # Emit signal to call def updatePlot
    def signalPlot(self):
        self.emit(SIGNAL('signal_plot()'))


    ##
    # print list of res freqs on the NoiseIV tab on gui.
    #
    def updateCalResListDisplay(self):
        
        try:
            strx = ''
            for m in measure.measspecs.mlist_trans:
                strx = strx + '%5.2fMHz, '%(m.getFc()/1e6)
            self.label_resListCalIQ.setText(strx)
        except:
            pass
           
    def getTimestamp(self):    
       timestamp = "T".join( str( datetime.datetime.now() ).split() )
       return(timestamp)

    
       
    ##
    # update gui where transmission line delay in ns is printed
    # 
    def updateXMLineDelay(self):
        delaysec = float(self.textbox_Dly.text()) * 1e-9
        measure.xmission_line_delay = delaysec
    ##
    # get iq data from the fftAnaluzer. IQ is the sweep data. as [ I, Q] where I . Q are anumpy arrays
    #
    def getIQF(self):
        iqp = fa.dataread.RectToPolar(fa.iqdata)
        delaysec = measure.xmission_line_delay
        iqpdly = measure.calcLineSweepDelay2(iqp,fa.freqs_sweep,delaysec)
       
        iqdly = fa.dataread.PolarToRect(iqpdly)
        
        return([iqdly,fa.freqs_sweep])



    


    ##
    # plit magnitude and phase
    #
    def magPhasePl(self):
        

        iqf=self.getIQF()
        iq=iqf[0]
        freqs=iqf[1]

        if self.plot_zoom_settings["pltype"]=="magPhasePl":
            self.plot_zoom_settings={}
            self.plot_zoom_settings["pltype"]="magPhasePl"
            self.plot_zoom_settings["axes0xlim"]=self.axes0.get_xlim()
            self.plot_zoom_settings["axes0ylim"]=self.axes0.get_ylim()
            self.plot_zoom_settings["axes1xlim"]=self.axes1.get_xlim()
            self.plot_zoom_settings["axes1ylim"]=self.axes1.get_ylim()


    

        if self.clearplot==1:
            self.fig.clear()

        self.axes0 = self.fig.add_subplot(2,1,1)
        self.axes0.set_ylabel('Magnitude')

        self.axes1 = self.fig.add_subplot(2,1,2)
        self.axes1.set_ylabel('Phase')        
        self.axes1.set_xlabel('Frequency')

        IQp=na.dataread.RectToPolar(iq)


        magdbm = self.convertMagnitudePerPlotMode(IQp[0])

        if self.clearplot==1:
            self.axes0.clear()
            self.axes1.clear()
        


        global IQp_
        global freqs_
        IQp_=IQp
        freqs_=freqs
        self.axes0.plot(freqs,magdbm)
        self.axes1.plot(freqs,IQp[1])
        self.axes0.set_ylabel('Magnitude')
        self.axes1.set_ylabel('Phase')        
        self.axes1.set_xlabel('Frequency')

        if len(MKID_list)>0:

            self.markerlistx=[]

            for m in MKID_list:
                self.markerlistx.append(m.getFc())

         
            
            ind1=numpy.where(self.markerlistx>freqs[0])[0]
            ind2=numpy.where(self.markerlistx<freqs[len(freqs)-1])[0]
            ind = list(set(ind1).intersection(set(ind2)))

            yvals=(0.5*(max(magdbm) + min(magdbm)))*ones(len(ind))


            self.axes0.plot(array(self.markerlistx)[ind],yvals,'rx')


        self.plot_zoom_settings={}
        self.plot_zoom_settings["pltype"]="magPhasePl"
        self.plot_zoom_settings["axes0xlim"]=self.axes0.get_xlim()
        self.plot_zoom_settings["axes0ylim"]=self.axes0.get_ylim()
        self.plot_zoom_settings["axes1xlim"]=self.axes1.get_xlim()
        self.plot_zoom_settings["axes1ylim"]=self.axes1.get_ylim()



        self.canvas.draw();
        print "plot done"    




    def IQPlots(self):


        #!!na.setDelay(1e-9*float(self.textbox_Dly.text()));
        iqf=self.getIQF()
        iq=iqf[0]
        freqs=iqf[1]


        #na.plotFreq(iq)


        if self.clearplot==1:
            self.fig.clear()

        self.axes0 = self.fig.add_subplot(2,1,1)
        self.axes0.set_ylabel('I')

        self.axes1 = self.fig.add_subplot(2,1,2)
        self.axes1.set_ylabel('Q')
        self.axes1.set_xlabel('Frequency')



        IQp=na.dataread.RectToPolar(iq)


        if self.clearplot==1:
            self.axes0.clear()
            self.axes1.clear()



        self.axes0.plot(freqs,iq[0])
        self.axes0.set_ylabel('I')
        self.axes1.plot(freqs,iq[1])
        self.axes1.set_ylabel('Q')
        self.axes1.set_xlabel('Frequency')




        self.canvas.draw();
        print "plot done"    


    #    
    #    if (self.is_sweeping==1):
    #            self.timer=QTimer()    
    #        self.timer.timeout.connect(self.IQPlots)
    #        self.timer.setSingleShot(True)
    #        self.timer.start(1000)
    #    






        
    def fourPlots(self):


        #!!na.setDelay(1e-9*float(self.textbox_Dly.text()));
        iqf=self.getIQF()
        iq=iqf[0]
        freqs=iqf[1]


        #na.plotFreq(iq)


        if self.clearplot==1:
            self.fig.clear()

        self.axes0 = self.fig.add_subplot(4,1,1)
        self.axes1 = self.fig.add_subplot(4,1,2)
        self.axes2 = self.fig.add_subplot(4,1,3)
        self.axes3 = self.fig.add_subplot(4,1,4)        

        IQp=na.dataread.RectToPolar(iq)


        magdbm = self.convertMagnitudePerPlotMode(IQp[0])

        if self.clearplot==1:
            self.axes0.clear()
            self.axes1.clear()

            self.axes2.clear()

            self.axes3.clear()

        self.axes0.plot(freqs,magdbm)

        self.axes0.set_ylabel('Magnitude')
        self.axes1.plot(freqs,IQp[1])
        self.axes1.set_ylabel('Phase')    
        self.axes2.plot(freqs,iq[0])
        self.axes2.set_ylabel('I')
        self.axes3.plot(freqs,iq[1])
        self.axes3.set_ylabel('Q')
        self.axes3.set_xlabel('Frequency')
        #!!exit()


        self.canvas.draw();
        print "plot done"    


    #    
    #    if (self.is_sweeping==1):
    #            self.timer=QTimer()    
    #        self.timer.timeout.connect(self.fourPlots)
    #        self.timer.setSingleShot(True)
    #        self.timer.start(1000)



    def plotIQCircle(self):    
    

        if self.clearplot==1:

            self.fig.clear()


            self.axes0 = self.fig.add_subplot(1,1,1)
            self.axes0.set_xlabel('I')
            self.axes0.set_ylabel('Q')


    
        roachlock.acquire();
        for resdata in self.fftreslist:

            fbase=na.findBasebandFreq(resdata.getFc())
            ts=na.extractTimeSeries(fbase)
            tsr=na.dataread.PolarToRect(ts)
            tsr_tr=fit.trans_rot3(resdata, tsr)



            #!!self.axes0.plot(resdata.trot_xf,resdata.trot_yf)
            self.axes0.plot(resdata.iqdata[0],resdata.iqdata[1])
            self.axes0.plot(tsr[0],tsr[1],'.')
            #!!self.axes0.plot(tsr_tr[0],tsr_tr[1],'.')



            #self.axes0.plot(resdata.iqdata[0], resdata.iqdata[1])
            #self.axes0.plot(tsr[0],tsr[1],'.')

        roachlock.release()
        self.canvas.draw();
    
    def plotChan3D(self):

        if self.clearplot==1:

            self.fig.clear()

        self.axes0 = self.fig.gca(projection='3d')    

        k=0.0

        zranges=[]
        roachlock.acquire();
        for f in na.frequency_list:
          try:
            ts = na.extractTimeSeries(f)

            z=ts[0]
            zranges.append(median(z))
            y=arange(len(z))

            x = numpy.array( [ f ]*len(z) )
            self.axes0.plot(x, y, z,label='zz')
          except:
            pass

        zlim=[0.0, 2.0*median(array(zranges))]    
        self.axes0.set_zlim(bottom=zlim[0], top=zlim[1])

        self.canvas.draw();
        roachlock.release()


    def subplot(self,a,b,c):
        if (a,b,c) in self.axislist.keys():
            self.curaxis = self.axislist[(a,b,c)]
        else:
            self.curaxis = self.fig.add_subplot(a,b,c)
            self.axislist[(a,b,c)] = self.curaxis
        
        self.canvas.draw();
        
    def clf(self):
        self.fig.clear()
        self.axislist = {}
        
        self.curaxis = None
        
        self.canvas.draw();
        
    def set_xlabel(self,st):
        self.curaxis.set_xlabel(st)
        
    def set_ylabel(self,st):
        self.curaxis.set_ylabel(st)

    def plot(self,*args):
        if self.curaxis==None:
            self.subplot(1,1,1)
        
        if len(args)==1:    
            self.curaxis.plot( args[0] )

        if len(args)==2:    
            self.curaxis.plot( args[0],args[1] )

        if len(args)==3:    
            self.curaxis.plot( args[0],args[1],args[2] )
            
        if len(args)==4:    
            self.curaxis.plot( args[0],args[1],args[2],args[4] )

        self.canvas.draw();
         
#hdf.open('superduper.h5','r')
#aa=hdf.read()
#aa
#fa.iqdata_raw = aa['iqdata_raw']
#hdf.close()
#form.plotMultiChanMagPh()
    def plotIVCurves(self):
    
        roachlock.acquire()
        if self.clearplot==1:
            self.clf()
            
     
        k=0.0
        colorlist = ['b','g','r','c','m','y','k']


        cind = 0
        for k in fa.iqdata_raw.keys():
            color = colorlist[ cind%len(colorlist) ]

            frd = fa.iqdata_raw[k]['flux_ramp_phase_unwrap'][::-1]  
            mv =   fa.iqdata_raw[k]['timestamp'][::-1]   /1000.0
            self.plot(mv,frd,colorlist[cind])
            cind = cind+1
    
        roachlock.release()
    ##
    # Plot phase term from ROACH with dots where "events" begin, and if we have selected points.
    #


    def plotRampPhaseSelection(self):
        if self.clearplot==1:

            self.clf()


        roachlock.acquire();
      

        k=0.0
        colorlist = ['b','g','c','m','y','k']
        
        cind = 0
        for k in fa.iqdata_raw.keys():
            color = colorlist[ cind%len(colorlist) ]
            
            if 'stream_mag' in fa.iqdata_raw[k].keys():
                ld = len(fa.iqdata_raw[k]['stream_mag'])
                if ld>1000: ld = 1000

                self.plot(fa.iqdata_raw[k]['stream_phase'][:ld],color)

                cind=cind+1

            if 'stream_mag' in fa.iqdata_raw[k].keys():

                self.set_xlabel('Sample')
                self.set_ylabel('Radians')
                
                #plot red dots where events start
                evtlen = fa.iqdata_raw[k]['event_len'][0]
                for x in range(0,ld,evtlen):
                    self.plot(x,fa.iqdata_raw[k]['stream_phase'][x],'ro')


                #if open loop noise, we can show selection of event length and delay teim
                #!!  how to tell if openloop noise, look at one of the fields on fa.iqdata_raw.. wich one?
                sel_evt_len =int(self.textbox_FRDLen.text())         
                sel_evt_dly =int(self.textbox_FRDDly.text())         

                for x in range(0,ld,evtlen):
                    self.plot(
                        range(x+sel_evt_dly,x+sel_evt_dly+sel_evt_len),
                        fa.iqdata_raw[k]['stream_phase'][x+sel_evt_dly:x+sel_evt_dly+sel_evt_len],
                        'r')



        roachlock.release()

    ##
    # Plot on left, Mag, Phase, FluxRampDemod. On ruight , roach cal resonator curve, and noise signal on IQ curve,. 
    #

    def plotMultiChanMagPh(self):
        if self.clearplot==1:

            self.clf()


        roachlock.acquire();
      

        k=0.0
        colorlist = ['b','g','c','m','y','k']
        
        if True:
            cind = 0
            for k in fa.iqdata_raw.keys():
                color = colorlist[ cind%len(colorlist) ]
                
                if 'stream_mag' in fa.iqdata_raw[k].keys():
                    ld = len(fa.iqdata_raw[k]['stream_mag'])
                    if ld>1000: ld = 1000

                    self.subplot(3,2,1)
                    self.plot(fa.iqdata_raw[k]['stream_mag'][:ld],color)
                    self.subplot(3,2,3)
                    self.plot(fa.iqdata_raw[k]['stream_phase'][:ld],color)
                
                    self.subplot(3,2,5)
                    self.plot(fa.iqdata_raw[k]['flux_ramp_phase_unwrap'],color)


                    IQ = fa.dataread.PolarToRect(\
                        [  fa.iqdata_raw[k]['stream_mag'][:ld],
                        fa.iqdata_raw[k]['stream_phase'][:ld]])

                    self.subplot(1,2,2)
                    self.plot(IQ[0],IQ[1],'%s.'%color)
                    cind=cind+1
                else:
                
                    
                    self.plot(fa.iqdata_raw[k]['flux_ramp_phase_unwrap'],color)

            if 'stream_mag' in fa.iqdata_raw[k].keys():
                self.subplot(3,2,1)        
                self.set_xlabel('Sample')
                self.set_ylabel('Mag')

                self.subplot(3,2,3)
                self.set_xlabel('Sample')
                self.set_ylabel('Radians')
                    
                self.subplot(3,2,5)
                self.set_xlabel('Sample')
                self.set_ylabel('FRD Phase')

                self.subplot(1,2,2)

                frdci = self.combobox_str_frd.currentIndex()
                if frdci==0 or frdci==1:
                    mlist = measure.measspecs.mlist_raw1
                else:
                    mlist = measure.measspecs.mlist_trans

                cind = 0
                for m in mlist:
                    color = colorlist[ cind%len(colorlist) ]
                    res = m.reslist[0]
                    self.plot(res.iqdata[0],res.iqdata[1],color)
                    cind = cind+1
            else:
                self.set_xlabel('Sample')
                self.set_ylabel('FRD Phase')     

        else:
            print "exception form.plotMultiChanMagPh"

        

        roachlock.release()
    
    def plotIvQ(self):

   
 

        #!!na.setDelay(1e-9*float(self.textbox_Dly.text()));

        iqf=self.getIQF()
        iq=iqf[0]

        if self.clearplot==1:

            self.fig.clear()

        self.axes0 = self.fig.add_subplot(1,1,1)
        self.axes0.set_xlabel('I')
        self.axes0.set_ylabel('Q')

        if self.clearplot==1:

            self.axes0.clear()

        self.axes0.plot(iq[0],iq[1],'o')
        self.axes0.set_xlabel('I')
        self.axes0.set_ylabel('Q')
        self.canvas.draw();




        print "plot done"    
    #    if (self.is_sweeping==1):
    #        self.timer=QTimer()    
    #        self.timer.timeout.connect(self.plotIvQ)
    #        self.timer.setSingleShot(True)
    #        self.timer.start(1000)

  


  
    #
    # Edit def name
    #
    
    
    def setDeviceName(self,txt):

        #tell net analyzer to put new name into dump file
        na.device_name=txt

        #update res list assuming we are renaming
        for m in MKID_list:
            m.chip_name=txt

        self.populateListWidget()

    #
    # clear res list
    #
    def clearResList(self):
        global MKID_list
        MKID_list=[]

        #markers on plot, little x's. each entry is an x,y coord on plot.
        self.current_resnumber=1
        self.updatePlot()






#
# sort res list by center freq, and disp on widget
#

    def populateListWidget(self):
        global MKID_list
    

        #preserved what is checked when list is redrawn by storing if the res is checked.


        #print form.list_reslist.item(0).data(100).chip_name

        #
        #clear gui lists 
        #
        self.list_reslist.clear()
        #
        #sort res list  by center freq
        #
        MKID_list=sorted(MKID_list,key=MKID.getFc)

        #
        #renumber resonators
        #
        self.current_resnumber=1;

        for m in MKID_list:
            m.resonator_num=self.current_resnumber
            self.current_resnumber= self.current_resnumber+1


        #
        # put resonators into the lists
        #

        for mkid in MKID_list:
            #
            # Put items into list on the Sweep tab- this is a list view
            #
            item=QListWidgetItem(self.list_reslist)
            #the 100 is some random number.. it is like an index for all the data objhects inside of the item.
            #calkuing item.data(100) returns the MKID obhect
            #!!item.setData(100,mkid)
            item.mkid = mkid
            item.setText('Res# %d %s fc=%4.1fMHz  Traces: %d'%(mkid.resonator_num, mkid.chip_name, mkid.getFc()/1e6,len(mkid.reslist)))
            #item.setFlags(item.flags() | Qt.ItemIsUserCheckable )





        #
        #
        #

    def delResonator(self):
        global MKID_list
        selected=self.list_reslist.selectedItems()

        for ss in selected:
            #get MKID object
            #m=ss.data(100)
            m = ss.mkid
            MKID_list.remove(m)

        self.updatePlot()

  
  
    def setPlotMode(self,indx):
        print 'set plot mode %s'%(self.plot_modes[indx])
        self.plotmode=indx

        self.signalPlot()

    def convertMagnitudePerPlotMode(self,magdata):
        atu28_db = fa.if_board.at.atten_U28

        if  self.plotmode == 0: #dbm at hemp input
            return(calcSignalRfInputPowerAtHemt(magdata,atu28_db))
        if  self.plotmode == 1: #dbm at rfin input
            return(calcSignalRfInputPowerAtIfboard(magdata,atu28_db))
        if  self.plotmode == 2: #dbm at mixer input
            return(calcSignalRfInputPowerAtMixer(magdata,atu28_db))
        if  self.plotmode == 3: #raw fft coef
            return(magdata) 
 
    def setPlotType(self,indx):
        print 'set plot type %s'%(self.plot_names[indx])
        self.plottype=indx

        self.signalPlot()

  
    def guiStop(self):
        print "##########################################"
        print "#"
        print "#   Type gui() to start gui again."
        print "#"
        print "##########################################"
        app.quit()

  
  
        
        
    def setRampSpecs(self):
        roachlock.acquire();
        r_amp = self.spinbox_RampAmp.value() / 100.0
        r_freq = self.spinbox_RampFreq.value()
        fa.rampgen.setRamp(r_amp,r_freq)
        fa.rampgen.setChannelizerFifoSync()
        roachlock.release()
        
    def flxRampComboDecode(self):
      
        frdci = self.combobox_str_frd.currentIndex()
        
        frd=[0,0]
        
        
        if frdci==0:
            frd = [0,0]
        elif frdci==1:
            frd= [1,1]
        elif frdci==2:
            frd = [1,0]
        elif frdci==3:
            frd = [1,2]
        else:
            frd=[0,0]
            
            
        return( (frd, frdci) )
             
    def setFluxRampDemod(self):
    
       
        (frd,frdci) =self.flxRampComboDecode()
        
       
        
        numprd = float(self.textbox_flxRmpPrd.text())
        
        
        roachlock.acquire();
        fa.temp_numprd =  numprd
        fa.temp_frd = frd
        fa.temp_frdci = frdci
        
        fa.chanzer.setFluxRampDemod(
            fa.temp_frd[0],
            fa.temp_frd[1],
            fa.chanzer.read_fifo_size,
            fa.temp_numprd)
        roachlock.release()
    

    #DEPRECATE
    def setFluxRampDemod2(self,frdci,numprd):
    
        frd=[0,0]
        
        
        if frdci==0:
            frd = [0,0]
        elif frdci==1:
            frd= [1,1]
        elif frdci==2:
            frd = [1,0]
        elif frdci==3:
            frd = [1,2]
        else:
            frd=[0,0]
        
        #numprd = float(self.textbox_flxRmpPrd.text())
        roachlock.acquire();
        fa.chanzer.setFluxRampDemod(frd[0],frd[1],fa.chanzer.read_fifo_size,numprd)
        roachlock.release()
        
  
        
    
    def file_dialog(self):
        print 'add dialog box here'
        #self.newdatadir = QFileDialog.getExistingDirectory(self, str("Choose SaveDirectory"), "",QFileDialog.ShowDirsOnly)
         #if len(self.newdatadir) > 0:
          #   self.datadir = self.newdatadir
           #  print self.datadir
             #self.ui.data_directory_lineEdit.setText(self.datadir) #put new path name in line edit
            # self.button_saveDir.setText(str(self.datadir))
             
    def create_main_frame(self):
        self.main_frame = QWidget()
        
        # Create the mpl Figure and FigCanvas objects. 
        self.dpi = 100
        self.fig = Figure((9.0, 9.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
    
        self.canvas.setParent(self.main_frame)
        self.axes0 = self.fig.add_subplot(121)
        self.axes1 = self.fig.add_subplot(122)
        #self.axes1.set_ylabel('hello')
        cid=self.canvas.mpl_connect('button_press_event', self.plotClick)
        
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        # Roach board's IP address
        self.textbox_roachIP = QLineEdit('192.168.0.70')
        self.textbox_roachIP.setMaximumWidth(200)
        label_roachIP = QLabel('Roach IP Address:')

        # Start connection to roach.
        self.button_openClient = QPushButton("Connect Roach")
        self.button_openClient.setMaximumWidth(120)
        self.connect(self.button_openClient, SIGNAL('clicked()'), self.openClient)
        
        # Start connection to roach.
        self.button_reopenClient = QPushButton("ReConnect Roach")
        self.button_reopenClient.setMaximumWidth(120)
        self.connect(self.button_reopenClient, SIGNAL('clicked()'), self.reOpenClient)
        
        
        # Start connection to roach.
        self.button_closeClient = QPushButton("Shut Roach")
        self.button_closeClient.setMaximumWidth(120)
        self.connect(self.button_closeClient, SIGNAL('clicked()'), self.closeClient)
        
        
        # DAC Frequencies.
        #self.textedit_DACfreqs = QTextEdit()
        #self.textedit_DACfreqs.setMaximumWidth(170)
        #self.textedit_DACfreqs.setMaximumHeight(100)
        #label_DACfreqs = QLabel('DAC Freqs:')
    
    
        #
        #labels for LO freq, and sweep st, end and incr freqs.
        #
        self.label_LO = QLabel('LO(Hz)')
        self.label_LO.setMaximumWidth(100)
    
        self.label_St = QLabel('St(Hz)')
        self.label_St.setMaximumWidth(100)

        self.label_Inc = QLabel('Inc')
        self.label_Inc.setMaximumWidth(100)

        self.label_Ed = QLabel('Ed(Hz)')
        self.label_Ed.setMaximumWidth(100)




    #
        # Frequency entries for sweeping net analuyzer
        #
        self.textbox_LOFreq = QLineEdit('3500e6')
        self.textbox_LOFreq.setMaximumWidth(100)
        self.textbox_LOFreq.setEnabled(False)
       
        self.textbox_StFreq = QLineEdit('10e6')
        self.textbox_StFreq.setMaximumWidth(100)
        self.textbox_StFreq.setEnabled(False)
       
        self.textbox_IncFreq = QLineEdit('10e3')
        self.textbox_IncFreq.setMaximumWidth(100)

      
        self.textbox_EdFreq = QLineEdit('100e6')
        self.textbox_EdFreq.setMaximumWidth(100)
        self.textbox_EdFreq.setEnabled(False)



      #
        #labels for CentF and Span
    #
        self.label_Center = QLabel('Center(MHz)')
        self.label_Center.setMaximumWidth(100)
    
        self.label_Span = QLabel('Span(MHz)')
        self.label_Span.setMaximumWidth(100)

 


        #
            # Frequency entries for sweeping net analuyzer
            #
        self.spinbox_CenterFreq = QSpinBox()
        self.spinbox_CenterFreq.setRange(2200,8000)
        self.spinbox_CenterFreq.setValue(3500)
        self.spinbox_CenterFreq.setSingleStep(50)
        self.spinbox_CenterFreq.setMaximumWidth(100)
        #self.spinbox_CenterFreq.valueChanged.connect(self.setCenterSpanFreq)


        self.spinbox_SpanFreq = QSpinBox()
        self.spinbox_SpanFreq.setRange(1,6000)
        self.spinbox_SpanFreq.setValue(100)
        self.spinbox_SpanFreq.setSingleStep(10)
        self.spinbox_SpanFreq.setMaximumWidth(100)
        #self.spinbox_SpanFreq.valueChanged.connect(self.setCenterSpanFreq)




    


        # Start/ Stop Sweep for Net analyzer
        self.button_StSweep = QPushButton("StartSweep")
        self.button_StSweep.setMaximumWidth(200)
        self.connect(self.button_StSweep, SIGNAL('clicked()'), self.startSweep)   

        

        # Start/ Stop Sweep for Net analyzer
        #self.button_saveSweep = QPushButton("SaveAnalyzer")
        #self.button_saveSweep.setMaximumWidth(200)
        #self.connect(self.button_saveSweep, SIGNAL('clicked()'), self.saveSweep)   


  # Start/ Stop Sweep for Net analyzer
        self.button_savePlot = QPushButton("SavePlot")
        self.connect(self.button_savePlot, SIGNAL('clicked()'), self.savePlot)   

        self.button_loadPlot = QPushButton("LoadPlot")
        self.connect(self.button_loadPlot, SIGNAL('clicked()'), self.loadSweepPlot)   


        #adc rf and bb loopbacks as checks

        #button to update the plots? a single push button? separate thread to cont uopdate?
        # button to calc the peaks and save to file?

        #need att settings as gui

        #start and stop sing freq readout
        #need entry for dftlen


        #
        # plot tyopes
        #

        self.label_plottype = QLabel('Plot Type')
        self.plot_names=['FourPlots','MagPhase','I and Q','IQPolar','IvQ','MultiNoise',
            'IQVelocity','IQCircle','ResFit','3DChannels', 'IV Curve', 'Trans Cal', 'PhaseTriggers']


        self.combobox_plottype=QComboBox()
        for name in self.plot_names:
            self.combobox_plottype.addItem(name)   

        #self.connect(self.combobox_plottype, SIGNAL('currentIndexChanged'), self.setPlotType) 
        self.combobox_plottype.currentIndexChanged.connect(self.setPlotType)


        #
        # plot powr mode 
        #

        self.label_plotmode = QLabel('Plot Power Mode')
        self.plot_modes=['dBm at HEMT','dBm at RFIn','dBm at MixerIn', 'Raw FFT Coef']

        self.combobox_plotmode=QComboBox()
        for mode in self.plot_modes:
            self.combobox_plotmode.addItem(mode)   

        #self.connect(self.combobox_plotmode, SIGNAL('currentIndexChanged'), self.setPlotType) 
        self.combobox_plotmode.currentIndexChanged.connect(self.setPlotMode)



        self.button_refreshPlot1 = QPushButton("refreshPlot")
        self.connect(self.button_refreshPlot1 , SIGNAL('clicked()'), self.updatePlot)   

        self.button_refreshPlot2 = QPushButton("refreshPlot")
        self.connect(self.button_refreshPlot2 , SIGNAL('clicked()'), self.updatePlot)   

        self.button_refreshPlot3 = QPushButton("refreshPlot")
        self.connect(self.button_refreshPlot3 , SIGNAL('clicked()'), self.updatePlot)   

        #checkboxes for controlling IF board loopbacks
        self.checkbox_BBLoopback=QCheckBox('BBLoop')
        self.checkbox_BBLoopback.setMaximumWidth(200)
        self.checkbox_BBLoopback.stateChanged.connect(self.bbLoopback)

        self.checkbox_RFLoopback=QCheckBox('RFLoop')
        self.checkbox_RFLoopback.setMaximumWidth(200)
        self.checkbox_RFLoopback.stateChanged.connect(self.rfLoopback)

        self.checkbox_FPGALoopback=QCheckBox('FPGALoop')
        self.checkbox_FPGALoopback.setMaximumWidth(200)
        self.checkbox_FPGALoopback.stateChanged.connect(self.fpgaLoopback)

        self.checkbox_RFOutEn=QCheckBox('RFOutEn')
        self.checkbox_RFOutEn.setMaximumWidth(200)
        self.checkbox_RFOutEn.stateChanged.connect(self.rfOutEn)

        self.checkbox_extClk=QCheckBox('ExtLO') #Tom renamed. I believe this is correct and not actually using the extClk.
        self.checkbox_extClk.setMaximumWidth(200)
        self.checkbox_extClk.stateChanged.connect(self.extClk)


        #
        # Transmission line delay
        #

        self.label_Dly = QLabel('Dly_ns')
        self.label_Dly.setMaximumWidth(30)

        self.textbox_Dly = QLineEdit('30')
        self.textbox_Dly.setMaximumWidth(70)
        self.textbox_Dly.textChanged.connect(self.updateXMLineDelay)
        
 



        #
        # Attenuators on IF Board
        #
        #
        # Frequency entries for sweeping net analuyzer
        #
        self.label_AttenSets = QLabel('OutAtten= 0 + 0 = 0, InAtten = 0')
        self.label_AttenSets.setMaximumWidth(650)
    
 
        self.label_ResPwrOut = QLabel('PwrAtResDBM')
        self.label_ResPwrOut.setMaximumWidth(120)
 
 
 
    

        self.spinbox_ResPwrOut = QSpinBox()
        self.spinbox_ResPwrOut.setRange(-180,cryo_max_res_power_dbm)
        self.spinbox_ResPwrOut.setValue(cryo_max_res_power_dbm-20)
        self.spinbox_ResPwrOut.setSingleStep(1)
        self.spinbox_ResPwrOut.setMaximumWidth(50)
        self.spinbox_ResPwrOut.valueChanged.connect(self.setAttenFromGUI)








        #
        # For adding resonator markers on plot
        #
        self.checkbox_AddMark=QCheckBox('Mark')
        self.checkbox_AddMark.setMaximumWidth(200)
        self.checkbox_AddMark.stateChanged.connect(self.addMark)




   


    #      
        # hdf5 filename for dumping IQ data.
        #
    
        # Load thresholds.
        #self.button_loadThresholds = QPushButton("(4)load thresholds")
        #self.button_loadThresholds.setMaximumWidth(170)
        #self.connect(self.button_loadThresholds, SIGNAL('clicked()'), self.loadThresholds)

      




        
        
        

        self.label_resPlots = QLabel('ResNum')
        self.label_resPlots.setMaximumWidth(30)

        self.textbox_resPlots = QLineEdit('0')
        self.textbox_resPlots.setMaximumWidth(70)

       
       
               # for adding resonance by clocking on the figure. check then clock res.
        self.checkbox_AddRes=QCheckBox('AddRes')
        self.checkbox_AddRes.setMaximumWidth(200)
        self.checkbox_AddRes.stateChanged.connect(self.addResonator)

   

    #
        # Long time powersweep of a single channel
        #
    #self.button_powersweep = QPushButton("powersweep")
        #self.button_powersweep.setMaximumWidth(170)
        #self.connect(self.button_powersweep, SIGNAL('clicked()'), self.powersweep)            
        





        #
        #device name, text box
        #
    
        self.textbox_devicename = QLineEdit('NULL_Device_Name')
        self.textbox_devicename.setMaximumWidth(400)
        self.textbox_devicename.textChanged.connect(self.setDeviceName)
    #    self.connect(self.textbox_devicename, SIGNAL('textChanged(arg)'), self.setDeviceName)            

        #
        # Num points in sweep
        #
        self.spinbox_numSwPts = QSpinBox()
        self.spinbox_numSwPts.setRange(32,65536)
        self.spinbox_numSwPts.setValue(2048)
        self.spinbox_numSwPts.setSingleStep(256)
        self.spinbox_numSwPts.setMaximumWidth(100)

        #
        # For clearing resonator list
        #
    
        
        self.button_clearResList = QPushButton("ClearREsList")
        self.button_clearResList.setMaximumWidth(170)
        self.connect(self.button_clearResList, SIGNAL('clicked()'), self.clearResList)            

        #
        # TWO copies of a List box of all resonators.
        #
        self.list_reslist = QListWidget()

    #
    #delete one resonator from list
    #
            
        self.button_delResonator = QPushButton("DelRes")
        self.button_delResonator.setMaximumWidth(170)
        self.connect(self.button_delResonator, SIGNAL('clicked()'), self.delResonator)            
    
    
        #
    #add current trace to selected resonator
        #
        self.button_addResTrace = QPushButton("addTrace")
        self.button_addResTrace.setMaximumWidth(170)
        self.connect(self.button_addResTrace, SIGNAL('clicked()'), self.naTrace2ResTrace)            
    
    
    
    
    
        #
    # find resonancs in the trace, for finding several resonators from one sweep
        #
        self.button_extractRes = QPushButton("extractRes")
        self.button_extractRes.setMaximumWidth(170)
        self.connect(self.button_extractRes, SIGNAL('clicked()'), self.extractRes)            
        
     # extract threshold N*sigma
        self.textbox_extract_thresh = QLineEdit('5.0')
        self.textbox_extract_thresh.setMaximumWidth(50)
        self.label_extract_thresh = QLabel('extract Nsigma')

    # run fits
        #self.button_runFits = QPushButton("runFits")
        #self.button_runFits.setMaximumWidth(170)
        #self.connect(self.button_runFits, SIGNAL('clicked()'), self.runFits)            
        




    # extract threshold N*sigma
        self.textbox_noisesec = QLineEdit('0.25')
        self.textbox_noisesec.setMaximumWidth(50)
        self.label_noisesec = QLabel('NoiseSec')


    
    

        self.button_HDF5ResRead = QPushButton("Load")
        self.connect(self.button_HDF5ResRead, SIGNAL('clicked()'), self.textResRead)
    

    

        self.button_HDF5ResSave = QPushButton("Save")
        self.connect(self.button_HDF5ResSave, SIGNAL('clicked()'), self.textResSave)
    


        # lengths of 2 ms steps to combine in a snapshot.
        self.textbox_snapSteps = QLineEdit('10')
        self.textbox_snapSteps.setMaximumWidth(50)
        label_snapSteps = QLabel('* 2 msec')

     
        
    
        self.label_saysf = QLabel('Sweep and You Shall Find')
        
    #####################################################################################################


        #
        # widgets for noise/readout mode FW
        #

   
 
 
    #run stream
        self.button_stream_run = QPushButton("StartStream")
        self.button_stream_run.setMaximumWidth(170)
        self.connect(self.button_stream_run, SIGNAL('clicked()'), self.streamRun)            
        
        #self.label_fa_running = QLabel('Not Running')
        
        self.button_stop_run = QPushButton("Stop Run")
        self.button_stop_run.setMaximumWidth(170)
        self.connect(self.button_stop_run, SIGNAL('clicked()'), self.runStop)            
        
        
        
        self.checkbox_teson = QCheckBox("TES BiasON")
        self.checkbox_teson.setMaximumWidth(170)
        
        # lut amp
        self.textbox_tesVolts = QLineEdit('0.8')
        self.textbox_tesVolts.setMaximumWidth(50)
        label_testVolts = QLabel('TES Volts')
   

        #
        # qwidgets for setting Flux Ramp Integration Time and length, and delay wrt Trigger pulse
        #
        label_frdlen = QLabel('FRD Len')
        self.textbox_FRDLen = QLineEdit('100')
        self.textbox_FRDLen.setMaximumWidth(50)
        
        
        label_rampvolts= QLabel('RmpVolts')
        self.textbox_rampvolts= QLineEdit('3.0')
        self.textbox_rampvolts.setMaximumWidth(60)
        
        label_rampfreq = QLabel('RmpFreq')
        self.textbox_rampfreq = QLineEdit('40000')
        self.textbox_rampfreq.setMaximumWidth(60)
        
        self.checkbox_rampon= QCheckBox("RampOn")
        self.checkbox_rampon.setMaximumWidth(170)
           
        label_FRDDly = QLabel('FRD Dly')
        self.textbox_FRDDly = QLineEdit('4')
        self.textbox_FRDDly.setMaximumWidth(50)
       
        
    #run stream
        #self.textbox_flxRmpPrd.returnPressed.connect(self.setFluxRampDemod)

    
        self.label_attentext = QLabel('Set Attens on Settings Tab First')
        self.button_progtrans=QPushButton('Cal IQ Circles')
        self.button_progtrans.setMaximumWidth(200)
        self.connect(self.button_progtrans, SIGNAL('clicked()'), self.calibrateIQCircles)            
        
        self.button_savetrans=QPushButton('Save IQ Cirle Cal')
        self.button_savetrans.setMaximumWidth(200)
        self.connect(self.button_savetrans, SIGNAL('clicked()'), self.saveIQCircleCal)            

      
        
        self.button_loadtrans=QPushButton('Load IQ Cirle Cal')
        self.button_loadtrans.setMaximumWidth(200)
        self.connect(self.button_loadtrans, SIGNAL('clicked()'), self.loadIQCircleCal)            

        self.label_resListCalIQ = QLabel('No Calibrated Resonators')
        
        # lut amp
        self.textbox_flxRmpPrd = QLineEdit('3.0')
        self.textbox_flxRmpPrd.setMaximumWidth(50)
        #self.textbox_flxRmpPrd.returnPressed.connect(self.setFluxRampDemod)

        label_flxRmpPrd = QLabel('FlxRmp Periods')

    
        #self.combobox_syncsource=QComboBox()
        self.combobox_syncsource=QComboBox()
        self.combobox_syncsource.addItem('Open Loop (No Trig)')   
        self.combobox_syncsource.addItem('Closed Loop (Trig)')   
        #self.combobox_syncsource.addItem('Int RampSource')   

        #self.connect(self.combobox_plottype, SIGNAL('currentIndexChanged'), self.setPlotType) 
        #self.combobox_syncsource.currentIndexChanged.connect(self.setRampSyncSource)

    
    
         #self.combobox_syncsource=QComboBox()
        self.combobox_rampgenerator=QComboBox()
        self.combobox_rampgenerator.addItem('No Ramp Gen')   
        self.combobox_rampgenerator.addItem('Agilent 332350A')   
       
        self.combobox_rampgenerator.currentIndexChanged.connect(self.setRampGenerator)

     
         #self.combobox_syncsource=QComboBox()
        self.combobox_biassource=QComboBox()
        self.combobox_biassource.addItem('No Volt Source')   
        self.combobox_biassource.addItem('sim 928')   
       
        self.combobox_biassource.currentIndexChanged.connect(self.setBiasSource)

     
    
        self.combobox_str_frd=QComboBox()
       
        self.combobox_str_frd.addItem('Return Raw Data')   
        self.combobox_str_frd.addItem('Return Raw + FRD')   
        self.combobox_str_frd.addItem('Return FRD only')   
        self.combobox_str_frd.addItem('Return FRD + IQCentered')   

       

        # stream file name
        self.textbox_streamfilename = QLineEdit('superduper.h5')
        self.textbox_streamfilename.setMaximumWidth(400)
        label_lut_strfilename = QLabel('Streamfilename.h5')

   
        # lut amp
        self.textbox_streamsec = QLineEdit('1')
        self.textbox_streamsec.setMaximumWidth(50)
        label_streamsec = QLabel('SecondsStream')
   


   
    
    #run stream
        self.button_iv_run = QPushButton("Start TES IV Sweep")
        self.button_iv_run.setMaximumWidth(170)
        self.connect(self.button_iv_run, SIGNAL('clicked()'), self.sweepTesIV)            
        
 
        # stream file name
        self.textbox_ivfilename = QLineEdit('ivdata.h5')
        self.textbox_ivfilename.setMaximumWidth(400)
        label_lut_ivfilename = QLabel('IVFilename.h5')

   
        # lut amp
        self.textbox_ivrange = QLineEdit('10.0 : 0.0 : -0.01')
        self.textbox_ivrange.setMaximumWidth(200)
        label_ivrange = QLabel('StartVolt : EndV: stepV')
   
    #####################################################################################################
    
    
    #stop qt event loop
        self.button_gui_stop = QPushButton("Exit2Console")
        self.button_gui_stop.setMaximumWidth(170)
        self.connect(self.button_gui_stop, SIGNAL('clicked()'), self.guiStop)            
    
    
   
      
    #################################################################################################3
    # Settings tab
    #
    
    
        gbox0 = QVBoxLayout()
        hbox00 = QHBoxLayout()
        hbox00.addWidget(self.textbox_roachIP)
        hbox00.addWidget(self.button_openClient)
        hbox00.addWidget(self.button_reopenClient)
        hbox00.addWidget(self.button_closeClient)
        
        gbox0.addLayout(hbox00)

        hbox02 = QHBoxLayout()

        hbox02.addWidget(self.label_plottype)
        hbox02.addWidget(self.combobox_plottype)
        hbox02.addWidget(self.button_refreshPlot1)

        hbox02.addWidget(self.label_plotmode)
        hbox02.addWidget(self.combobox_plotmode)

        gbox0.addLayout(hbox02)

        hbox03 = QHBoxLayout()
        gbox0.addLayout(hbox03)
        
        gbox1 = QVBoxLayout()

        gbox2 = QVBoxLayout()
        hbox20 = QHBoxLayout()
    
        hbox20.addWidget(self.checkbox_RFOutEn)
        hbox20.addWidget(self.checkbox_BBLoopback)
        hbox20.addWidget(self.checkbox_RFLoopback)
        hbox20.addWidget(self.checkbox_FPGALoopback)
        hbox20.addWidget(self.checkbox_extClk)
    
        hbox20.addWidget(self.label_Dly)
        hbox20.addWidget(self.textbox_Dly)
    
        gbox2.addLayout(hbox20)
        
        hbox21 = QHBoxLayout()
        hbox21.addWidget(self.label_ResPwrOut)
        hbox21.addWidget(self.spinbox_ResPwrOut)
        hbox21.addWidget(self.button_gui_stop)
        gbox2.addLayout(hbox21)
        
        hbox215 = QHBoxLayout()
        gbox2.addLayout(hbox215)
        hbox22 = QHBoxLayout()
       
        gbox2.addLayout(hbox22)

        hbox23 = QHBoxLayout()
       
        gbox2.addLayout(hbox23)

        t1_hbox11 = QHBoxLayout()
        t1_hbox11.addWidget(self.label_AttenSets)
        gbox2.addLayout(t1_hbox11)

        gbox3 = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addLayout(gbox0)
        hbox.addLayout(gbox1)     
        hbox.addLayout(gbox2)
        hbox.addLayout(gbox3)
        
    
    
    
    
    
    
    
    
    ################################################################################################
    # Sweep,ResFind
    #
    #
    
    
    #span, cf spin boxes as on tab 1
    #1 sweep button- does one sweep
    # clear res list button, check for add mode.
    #list box w/ res list.
    
    
    
    
        t2_gbox1 = QVBoxLayout()

   
        t2_gbox1.addWidget(self.label_saysf)
        t2_gbox1.addWidget(self.textbox_devicename)
        t2_gbox1.addWidget(self.spinbox_numSwPts)
   
        t2_hbox015 = QHBoxLayout()
        t2_hbox015.addWidget(self.button_refreshPlot2)
        t2_gbox1.addLayout(t2_hbox015)

        t2_hbox016 = QHBoxLayout()
        t2_hbox016.addWidget(self.label_Span)
        t2_hbox016.addWidget(self.spinbox_SpanFreq)
        t2_hbox016.addWidget(self.label_Center)
        t2_hbox016.addWidget(self.spinbox_CenterFreq)
       
        t2_gbox1.addLayout(t2_hbox016)

        t2_hbox01 = QHBoxLayout()
        t2_hbox01.addWidget(self.button_StSweep)
        #t2_hbox01.addWidget(self.button_saveSweep)
        t2_hbox01.addWidget(self.button_savePlot)
       
        t2_hbox01.addWidget(self.button_loadPlot)
       

        t2_hbox01.addWidget(self.button_HDF5ResRead)
        t2_hbox01.addWidget(self.button_HDF5ResSave)
        t2_gbox1.addLayout(t2_hbox01)

   
   
        t2_hbox02 = QHBoxLayout()
        t2_hbox02.addWidget(self.label_extract_thresh)
        t2_hbox02.addWidget(self.textbox_extract_thresh)
        t2_hbox02.addWidget(self.button_extractRes)
        t2_hbox02.addWidget(self.checkbox_AddRes)
        t2_hbox02.addWidget(self.button_clearResList)
        t2_hbox02.addWidget(self.button_delResonator)
        t2_hbox02.addWidget(self.button_addResTrace)

    
    
        t2_gbox1.addLayout(t2_hbox02)
    
    
    
    
  
  #      t2_hbox13 = QHBoxLayout()
#  
#      t2_hbox13.addWidget(self.checkbox_AddMark)
#       t2_gbox1.addLayout(t2_hbox13)


        t2_gbox2 = QVBoxLayout()

        t2_gbox2.addWidget(self.list_reslist)




        t2_hbox = QHBoxLayout()
        t2_hbox.addLayout(t2_gbox1)
        t2_hbox.addLayout(t2_gbox2)


      ######################################################################################
    # Stream tab
    #
  
  
  
  
        t5_gbox0 = QVBoxLayout()


        t5_hbox03 = QHBoxLayout()
        
        
        t5_hbox03.addWidget(label_flxRmpPrd)
        t5_hbox03.addWidget(self.textbox_flxRmpPrd)
        
        t5_hbox03.addWidget(label_frdlen)
        t5_hbox03.addWidget(self.textbox_FRDLen)
        t5_hbox03.addWidget(label_FRDDly)
        t5_hbox03.addWidget(self.textbox_FRDDly)

        t5_hbox03.addWidget(label_rampfreq)
        t5_hbox03.addWidget(self.textbox_rampfreq)
        t5_hbox03.addWidget(label_rampvolts)
        t5_hbox03.addWidget(self.textbox_rampvolts)
        t5_hbox03.addWidget(self.checkbox_rampon)
  
        t5_hbox03.addWidget(self.combobox_rampgenerator)

        t5_hbox05 = QHBoxLayout()
        t5_hbox05.addWidget(self.label_resListCalIQ)
        
        t5_hbox02 = QHBoxLayout()
             
        t5_hbox02.addWidget(self.combobox_str_frd)
        t5_hbox02.addWidget(self.combobox_syncsource)

        t5_hbox02.addWidget(self.combobox_biassource)

        t5_hbox02.addWidget(self.button_progtrans)
        t5_hbox02.addWidget(self.button_savetrans)
        t5_hbox02.addWidget(self.button_loadtrans)

        t5_hbox00 = QHBoxLayout()
        t5_hbox00.addWidget(label_lut_strfilename)
        t5_hbox00.addWidget(self.textbox_streamfilename)

        
        t5_hbox00.addWidget(label_testVolts)
        t5_hbox00.addWidget(self.textbox_tesVolts)
        t5_hbox00.addWidget(self.checkbox_teson)
        
        
        
        t5_hbox00.addWidget(label_streamsec)
        
        t5_hbox00.addWidget(self.textbox_streamsec)
        
        
        
        
        
        
        t5_hbox00.addWidget(self.button_stream_run)



        t5_hbox01 = QHBoxLayout()
        t5_hbox01.addWidget(label_lut_ivfilename)
        t5_hbox01.addWidget(self.textbox_ivfilename)

        t5_hbox01.addWidget(label_ivrange)
        t5_hbox01.addWidget(self.textbox_ivrange)
        t5_hbox01.addWidget(self.button_iv_run)

        t5_hbox04 = QHBoxLayout()
        #t5_hbox04.addWidget(self.label_fa_running)
        t5_hbox04.addWidget(self.button_stop_run)
        

        t5_hbox04.addWidget(self.button_refreshPlot3)






        t5_gbox0.addLayout(t5_hbox03)
        t5_gbox0.addLayout(t5_hbox05)
        t5_gbox0.addLayout(t5_hbox02)
        t5_gbox0.addLayout(t5_hbox01)
        t5_gbox0.addLayout(t5_hbox00)
        t5_gbox0.addLayout(t5_hbox04)
    
    
  
    #############################################################################################3
    # ResData
    #
    #
    
    
    
   
    #
    # Fill in tabs
    #
    

        tab_widget=QTabWidget()
        tab1=QWidget()

        tab1_layout=QVBoxLayout(tab1)
        tab1_layout.addLayout(hbox)

        tab2=QWidget()
        tab2_layout=QVBoxLayout(tab2)
        tab2_layout.addLayout(t2_hbox)

       

        tab5=QWidget()
        tab5_layout=QVBoxLayout(tab5)
        tab5_layout.addLayout(t5_gbox0)


        tab_widget.addTab(tab1,"Settings")
        tab_widget.addTab(tab2,"Sweep")
        

        #tab_widget.addTab(tab3,"ResData")
        tab_widget.addTab(tab5,"Noise/IV")
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(tab_widget)
    
    
    #vbox.addLayout(hbox)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
  
    def create_status_bar(self):
        self.status_text = QLabel("Roach is Shutdown")
        self.statusBar().addWidget(self.status_text, 1)
        
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",shortcut="Ctrl+S", slot=self.save_plot, tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close, shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, (load_file_action, None, quit_action))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", shortcut='F1', slot=self.on_about, tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def save_plot(self):
        file_choices = "PNG (*.png)|*.png"
        path = unicode(QFileDialog.getSaveFileName(self, 'Save file', '',file_choices))
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            statusBar().showMessage('Saved to %s' % path, 2000)
    
    def on_about(self):
        msg = """ Message to user goes here.
        """
        QMessageBox.about(self, "MKID-ROACH software demo", msg.strip())
   
   

  
    def runStop(self):
        fa.is_running= False
        

def runCaptureNoise():
  
    success = roachlock.acquire(False);
    if not success: return
           
    try:
        #form.signalMessageText("Noise Running")
        message_queue.put({'status_string':'Noise Running'})
        print 'Capture Noise start on thread'            
        fa.setRampGenerator(fa.temp_rampon, fa.temp_rampfreq, fa.temp_rampvolts)
        fa.setTESBias(fa.temp_is_tes_on,fa.temp_tesvolts)       
        fa.progTranslatorsFromIQCircles(measure.iqcenterdata)              
        fa.setRampSyncSource(fa.temp_open_or_closedloop)
        fa.chanzer.setSyncDelay(fa.syncdelay_temp)
        fa.chanzer.setFluxRampDemod(
            fa.temp_frd[0],
            fa.temp_frd[1],
            fa.frdlen_temp,
            fa.temp_numprd)    
            
                     
        fa.setCarrier(
            measure.measspecs.andata_trans['fa.carrierfreq'])
      
        fa.captureNoise(
            timesec=fa.noisetemp_timesec,
            fname = fa.noisetemp_fname,
            BB=measure.measspecs.andata_trans['fa.sram.frequency_list'],
            LO=measure.measspecs.andata_trans['fa.LO'],
            pwr_at_res = measure.measspecs.andata_trans['fa.power_at_resonator'],
            lock= roachlock)                    
        print 'Done Noise'
      
        #form.signalMessageText("Not Running")
        message_queue.put({'status_string':'Not Running'})
    except:
        #form.signalMessageText("Not Running- Detected Error in Noise") 
        message_queue.put({'status_string':'Not Running- Detected Error in Noise'})
        traceback.print_exc()
    
    fa.is_running = False

    roachlock.release()   
    #enqueue a message to update plot on main window. 1 is plot tupe in form.updatePlot
    message_queue.put({'signalPlot':5})

  
def voltSweepCallback():
    strx = 'Voltage=%5.2fV'%fa.temp_volts    
    message_queue.put({'status_string':strx})
    
def runSweepTesIV():  
 
     
    success = roachlock.acquire(False);
    if not success: return
           
    
    try:
        #form.signalMessageText("IV Sweep Running")
        message_queue.put({'status_string':'IV Sweep Running'})
        print 'String voltSweep on thread'
       
       
       
        fa.progTranslatorsFromIQCircles(measure.iqcenterdata)
    
        
        #fa.setRampSyncSource(fa.temp_open_or_closedloop)
        fa.chanzer.setFluxRampDemod(
            fa.temp_frd[0],
            fa.temp_frd[1],
            fa.frdlen_temp,
            fa.temp_numprd)             
        fa.setCarrier(
            measure.measspecs.andata_trans['fa.carrierfreq'])
        fa.voltSweep(
            fa.iv_vlisttemp,
            [5100e6],2000,
            fa.iv_fnametemp,
            fa.iv_bbtemp,
            fa.iv_lotemp,
            lock=roachlock,
            callback = voltSweepCallback,
            issync = fa.temp_open_or_closedloop,
            evtsize2=fa.frdlen_temp,
            syncdelay=fa.syncdelay_temp);
            
        print 'Done IV Sweep'
       
        
        #form.signalMessageText("Not Running")
        message_queue.put({'status_string':'Not Running'})
    except:
        #form.signalMessageText("Not Running- Detected Error in IV Sweep") 
        message_queue.put({'status_string':'Not Running- Detected Error in IV Sweep'})
        traceback.print_exc()
        
    
    fa.is_running = False
    roachlock.release()
    #enqueue a message to update plot on main window. 1 is plot tupe in form.updatePlot
    message_queue.put({'signalPlot':10})

 


def runSetupEverything():

    message_queue.put({'status_string':'Setting up'})
    #form.signalMessageText("Setting up")
    try:
        print 'runSetupEverything on thread'
        stat = setupEverything(temp_ip)
        if not stat:
            message_queue.put({'status_string':'Setup Done- Ready'})
            
            if not fa.qdr_cal_good:
                message_queue.put({'status_string':'Problem with QDR cal, type fa.calQDR()'})
            #form.signalMessageText("Setup Done- Ready ") 
        else:
            message_queue.put({'status_string':'Detected Error in runSetupEverything'})
            #form.signalMessageText("Detected Error in runSetupEverything")   
           
    except:
        #form.signalMessageText("Detected Error in runSetupEverything") 
        
        message_queue.put({'status_string':'Detected Error in runSetupEverything'})
        traceback.print_exc()
    try:
        roachlock.release()
    except:
        pass



def runSweepProgTranslators():
 
    message_queue.put({'status_string':'Sweep/Prog Translators'})
    success = roachlock.acquire(False);
    if not success: return
           
    
    try:
    
    
    
        #form.signalMessageText("IQ Sweep Running")
        print 'Sweep/Prog Translators on thread'
   
        fa.if_board.progAtten(fa.if_board.at)
   
        fa.rampgen.setIsSync(0)
        fa.rampgen.setSyncSource(0)
        fa.rampgen.setChannelizerFifoSync()

        fa.sweepProgTranslators(
            fa.temp_rffreqs_rough,
            pwr_at_res = fa.power_at_resonator,
            lock_=roachlock,
            callback_=sweepCallback2)      
            
        print 'Sweep/Prog Translators'
       
        message_queue.put({'status_string':'Done Sweep/Prog Translators'})

        #form.signalMessageText("Not Running")
    except:
        #form.signalMessageText("Not Running- Detected Error in IQ Sweep") 
        message_queue.put({'status_string':'Error Running Sweep/Prog Translators, Not running'})
        traceback.print_exc()
    
    fa.is_running = False
    roachlock.release()
    #enqueue a message to update plot on main window. 1 is plot tupe in form.updatePlot
    message_queue.put({'signalPlot':11})
  
      
        
def runSweepResCheckedOps():
    message_queue.put({'status_string':'Running Resonators'})
    success = roachlock.acquire(False);
    if not success: return
    measure.lock = roachlock       
    measure.setSweepCallback(sweepCallback)
    measure.setSweepCallback2(sweepCallback2)
    measure.setLock(roachlock)
    
    try:
        if (measure.temp_check_powersweep):
            message_queue.put({'status_string':'Running PowerSweep'})
            print "power sweep running" 
                       
            measure.powerSweep()    
            
            print "power sweep done"
            
         
        if measure.temp_check_runIQvelocity:   
            print "------Calculating IQ velocity, Fit Circle ----------"
            message_queue.put({'status_string':'Running IQVelocity'})
            for m in measure.temp_fitmlist: #loops through list of resonators
                fit.reslist=m.reslist
                print "Calc IQVel, MKID %fHz"%(m.getFc())
                fit.IQvelocityCalc()
                print "Fit Circle %fHz"%(m.getFc())
                fit.fitCircleCalc()

    
        if measure.temp_check_runFits:
            message_queue.put({'status_string':'Running Fits'})
            for m in measure.temp_fitmlist:
                print "------------Fitting Resonator %d----------"%(m.resonator_num)
                fit.reslist = m.reslist
                fit.fitResonators()
     
       
        if measure.temp_check_getnoise:
            message_queue.put({'status_string':'Running Noise'})
            print "running res noise"
            measure.runNoise()
            
        message_queue.put({'status_string':'Done running resonators'})
        #form.signalMessageText("Not Running")
    except:
        #form.signalMessageText("Not Running- Detected Error in IQ Sweep") 
        message_queue.put({'status_string':'Error Running Resonators, Not running'})
        traceback.print_exc()
    
    fa.is_running = False
    roachlock.release()
    measure.lock =None   
    #enqueue a message to update plot on main window. 1 is plot tupe in form.updatePlot
    message_queue.put({'signalPlot':1})
  



def runIQSweep():  
   
    message_queue.put({'status_string':'Running IQSweep'})
    success = roachlock.acquire(False);
    if not success: return
           
    
    try:
        #form.signalMessageText("IQ Sweep Running")
        print 'Sweep on thread'
   
        fa.sweep(
            span_Hz=fa.temp_span_Hz, 
            center_Hz=fa.temp_center_Hz, 
            pts=fa.temp_pts,
            pwr_at_res = fa.power_at_resonator,
            lock=roachlock,
            callback=sweepCallback2)
            
        print 'Done IQ Sweep'
       
        message_queue.put({'status_string':'Done Running IQSweep'})

        #form.signalMessageText("Not Running")
    except:
        #form.signalMessageText("Not Running- Detected Error in IQ Sweep") 
        message_queue.put({'status_string':'Error Running IQSweep, Not running'})
        traceback.print_exc()
    
    fa.is_running = False
    roachlock.release()
    #enqueue a message to update plot on main window. 1 is plot tupe in form.updatePlot
    message_queue.put({'signalPlot':1})
 

       # fa.temp_rampgenerator_index=ci
       # thread.start_new_thread(runSetupRampGenerator,())

 
def runSetupRampGenerator():
    global agt 
    

    if fa.temp_rampgenerator_index==0:  
        
        try: 
            agt.close()
        except: 
            print "Did not close sim928"

        agt = agtNULL()
        message_queue.put({'status_string':'Open NULL Ramp Gen'})

    elif fa.temp_rampgenerator_index==1:

        try: agt.close()
        except: print "Did not close agt33250A"

        message_queue.put({'status_string':'Waiting for Agilent 33250A on comport'})
        agt = agt33250A()
        agt.open()
        
        idstr = agt.getId()
        print idstr
        message_queue.put({'status_string':idstr})


 
def runSetupBiasSource():
    global sim
    

    if fa.temp_biassource_index==0:  
        
        try: 
            sim.close()
        except: 
            print "Did not close sim928"

        sim = simNULL()
        message_queue.put({'status_string':'Open NULL Volt Source'})

    #sim928    
    elif fa.temp_biassource_index==1:

        try: sim.close()
        except: print "Did not close sim928"

        message_queue.put({'status_string':'Waiting for Sim928 on comport'})
        sim = sim928()
        sim.open()
        
        idstr = sim.getId()
        print idstr
        message_queue.put({'status_string':idstr})




def runShutdownEverything():
   
    #form.signalMessageText('Shutting down up')
    message_queue.put({'status_string':'Shutting down'})
   
    try:
        print 'runShutdownEverything on thread'
        shutdownEverything()
        #form.signalMessageText("Roach is Shutdown ") 
        message_queue.put({'status_string':'Roach is Shutdown'})

    except:
        #form.signalMessageText("Detected Error in runShutdownEverything") 
        message_queue.put({'status_string':'Detected Error in runShutdownEverything'})
        
    try:
        roachlock.release()
    except:
        pass
    

    
global app
global form

def mainepics():
    global app
    global form
    global roachlock
    print 'making lock '
    
           

    if 'roachlock' not in globals():
        roachlock = threading.RLock()

    
    
    form = AppForm()
    startEpics()


def main():
    global app
    global form
    global roachlock
    print 'making lock and app'
    
           

    if 'roachlock' not in globals():
        roachlock = threading.RLock()

    
    if app==None:
        app = QApplication(sys.argv)
    
    form = AppForm()
    form.show()
    
    
    app.exec_()



#if __name__=='__main__':
#    if len(sys.argv)!= 2:
#        print 'Usage: ',sys.argv[0],' roachNum'
#        exit(1)
#    roachNum = int(sys.argv[1])
#    datadir = os.environ['FREQ_PATH']
#    main()
roachNum=0
datadir='./'

#cd ROACH/bmazin/SDR
# execfile('channelizerCustom.py')


try:
    app
except:
    app=None
    
    
def gui():app.exec_()


#run by Roach DAQ Threads
def sweepCallback():    
    print 'natAnalgui.sweepCallback'    
    message_queue.put({'signalPlot':1})
     
#run by Roach DAQ Threads
def sweepCallback2():
    message_queue.put({'LOFreq':fa.carrierfreq})



try:
    sim.close()
except:
    pass
    

sim = None

if False:
    try:
        sim=sim928()
        sim.open()
        sim.connport(8)
        sim.getId()
    except:
        sim=None
        print "Problem w. sim 928"

