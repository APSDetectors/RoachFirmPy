import sys, os, random, math, array, fractions
from PySide.QtCore import *
from PySide.QtGui import *
 

import socket
import matplotlib, time, struct, numpy
from bitstring import BitArray
import matplotlib.pyplot as mpl
mpl.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import h5py



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

#from fftAnalyzerR2 import *

#from resView import *
#from katcpNc import *



global is_use_multiprocess

try:
    is_use_multiprocess
except:
    is_use_multiprocess=0


#name of firmware in /boffiles/ on the roach board.

#no windowing i think...
#fwname='networkanalyzer_2013_Dec_10_0946.bof'
#optional 256 len window
#fwname='networkanalyzerwa_2014_Feb_12_1134.bof'
#w/ 32 window
#fwname = 'networkanalyzerwa_2014_Feb_18_1452.bof'


#new- seems to work well


#!!fwnames=['networkanalyzer_2014_Jun_25_1330.bof' , 'fftanalyzerd_2014_Jun_26_1427.bof' ]
#!!fwnames=['networkanalyzer_2014_Jun_25_1330.bof' , 'fftanalyzerdfast_2014_Sep_23_1725.bof' ]

#fwnames=[
#'networkanalyzer_2014_Jun_25_1330.bof' , 
# 'fftanalyzeri_2015_Feb_04_1632.bof']


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

        self.clearplot=1

        #1 for no pulse det, but get raw data. 0 for puse det, get opnly pulses
        self.prawdata=1

        # dictiionary to remember plot zoom settings before clearing..
        self.plot_zoom_settings={"pltype":"NULL" , "autoscale":1}

        #self.extract_thresh=5


        signal_plot=Signal()

        self.connect(SIGNAL('signal_plot()'), self.updatePlot)


        #true to add a resonance freq on plot click
        self.is_addres_onclick=False



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

        self.timer=QTimer()    
   
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
    def closeClient(self):
    
        global roach
        global fit
        global fa
        global na
        global measure
        
        try: fa.capture.shut()
        except: pass
        

        try: fa.an.shut()
        except: pass

        try: roach.closeFiles()
        except: pass
        
        
        

    def openClient(self):
            #roach = corr.katcp_wrapper.FpgaClient(self.textbox_roachIP.text(),7147)

        global roach
        global fit
        global fa
        global na
        global measure
        global sim
        global hdf
        
        ip=self.textbox_roachIP.text()
        roach=katcpNc(ipaddr = ip)
        roach.startNc()

        self.status_text.setText('connection established')
        print 'Connected to ',self.textbox_roachIP.text()


        execfile(self.gui_settings_file);


        fa = fftAnalyzerR2(roach)
        fa.ifSetup()
        
        na = fa

        fit=fitters();


        measure = mkidMeasure(na,fit)
        

        self.button_StSweep.setEnabled(True)


        fa.sourceCapture([10e6],20000)
        time.sleep(.5)
        fa.stopCapture()

        if False:
            sim=sim928()
            sim.open()
            sim.connport(8)
            sim.getId()
           

      

        hdf=hdfSerdes()

        

        #if is_use_multiprocess==1:
        if False: 
            startQMP();
            #start process that gets queue items and dies fits. this runs on local system
            #if already running then not started again..
            startFitServeMP('')


    
        
    

#na.setDelay(30e-9); print na.delay
    def plotPolar(self):
        self.status_text.setText('Plotting')

    
    
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
    
  
    def getSelMkid(self):
        return(self.getMkidSelectedChecked(self.list_reslist2)[0])
      
  
    #get selected or checked MKID obhects in the gui list
    def getMkidSelectedChecked(self,wlist):
        
     

        selected=wlist.selectedItems()
        #selected list
        slist=[]
        #checked list
        clist=[]

        if len(selected)>0:
            slist.append(selected[0].data(0,100))

        for row in range(wlist.topLevelItemCount()):
            item=wlist.topLevelItem(row)
            if item.checkState(0)==Qt.Checked:
                clist.append(item.data(0,100))
                item.data(0,100).checked=1
            else:
                item.data(0,100).checked=0




        return([clist,slist])

    #get list of ints, the rows, of the checked items in gui list
    def getRowsChecked(self):


        #checked list
        clist=[]
        wlist = self.list_reslist2

        for row in range(wlist.topLevelItemCount()):
            item=wlist.topLevelItem(row)
            if item.checkState(0)==Qt.Checked:
                clist.append(row)


        return(clist)



    #get list of ints, the rows, of the checked items in gui list
    def setRowsChecked(self,clist):
        
   
        #checked list

        wlist = self.list_reslist2
        #uncheck all     
        for row in range(wlist.topLevelItemCount()):
            item=wlist.topLevelItem(row)
            item.setCheckState(0,Qt.Unchecked)
        #check the req rows
        for row in clist:
            item=wlist.topLevelItem(row)
            item.setCheckState(0,Qt.Checked)

     
    #get list of ints, the rows, of the checked items in gui list
    def setRowsAllChecked(self):
        

        #checked list

        wlist = self.list_reslist2
        #uncheck all     
        for row in range(wlist.topLevelItemCount()):
            item=wlist.topLevelItem(row)
            item.setCheckState(0,Qt.Checked)


    #get list of ints, the rows, of the checked items in gui list
    def setRowsAllUnChecked(self):
        

        #checked list

        wlist = self.list_reslist2
        #uncheck all     
        for row in range(wlist.topLevelItemCount()):
            item=wlist.topLevelItem(row)
            item.setCheckState(0,Qt.Unchecked)


    def runNoise(self):
         

        #runs on THIS thread
        #na.powerSweep(self.at_inst,self.at_st,self.at_inend,self.at_step,self.at_sweeps,self.resonator_span,self.mlist)
        measure.measspecs.num_noise_traces = self.spinbox_numNoise.value()
        ntime = float(self.textbox_noisesec.text())
        
        measure.setNoiseTime(ntime)
        measure.runNoise()


    #run power sweep, already setup, on calling thread
    def powersweep2(self): 
        
        measure.powerSweep()

       
    
    #setup power sweep from gui settings    
 
    def powersweepSetup(self): 

   
        
        


        self.status_text.setText('Busy')       
        print "Spawn power sweep 10:0.5:30"

        sweep_specs = measSpecs()
        #self.at_inst=self.spinbox_pwrsw_atinst.value()
        sweep_specs.attStart=self.spinbox_pwrsw_atst.value()
        #self.at_inst=self.spinbox_pwrsw_atTotal.value() - 10 -self.spinbox_pwrsw_atst.value()
        sweep_specs.attInStart=self.spinbox_pwrsw_atinst.value()
        sweep_specs.attEnd=self.spinbox_pwrsw_atend.value()
        sweep_specs.numSweeps=self.spinbox_pwrsw_atsweeps.value()
        sweep_specs.resonator_span = 1.0e6*self.spinbox_pwrsw_span.value()
        sweep_specs.attIncr = self.spinbox_pwrsw_atstep.value()



        sweep_specs.num_res_freq_points = self.spinbox_nswfreqs.value()

        #copy and clear the markerlist so it plots correctly
        sweep_specs.atU6=self.spinbox_pwrsw_atTotal.value() ;
      

    #see if something is selected, power sweep that,else power sweep checked items.
    
    

        sweep_specs.mlist=  self.getMkidSelectedChecked(self.list_reslist2)[0]


        measure.powersweepSetup(sweep_specs)
        
        
        if len(self.mlist)==0:
            print "No resonators selected or checked"
            return(0)

        print "Sweeping %d Resonators"%(len(self.mlist))


        #na.TpowerSweep(at_inst,at_st,at_inend,at_sweeps,mlist)
        #self.status_text.setText('Sweeping')       
        #self.is_sweeping=1


   #calculate IQ velocity
    def IQvelocity(self):
        print "------Calculating IQ velocity ----------"

        #figure(111)
        #clf()
        for m in self.mlist: #loops through list of resonators
            fit.reslist=m.reslist
            print "Calc IQVel, MKID %fHz"%(m.getFc())
            fit.IQvelocityCalc()



        


   
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
    
    
    
    def repeatRunIt(self):
        self.button_runbyhour.setStyleSheet("background-color: red")
        self.runIt()
        self.timer=QTimer()    
        self.timer.timeout.connect(self.runIt)    

        minutes = float(self.textbox_repeatmin.text())
        self.timer.start(1000*60*minutes)




    def stopRepeat(self):
        self.timer.stop()
        self.button_runbyhour.setStyleSheet("background-color: grey")
    

    def runIt(self):
    
#
#        try:
#            na.dbgclear()
#        except:
#            pass
#
#
#
#	    na.fft_num_sweep_pts = self.spinbox_num_fft_sw_pts.value()
#
#        gain_indx = self.combobox_fft_gain.currentIndex()
#        fftgains=[2047,1023,511,255,127,63,31]
#        na.roach_fft_shift=fftgains[gain_indx]
#        na.progRoach()

        #get checked MKIDs
        self.mlist= self.getMkidSelectedChecked(self.list_reslist2)[0]
        #get checked rows in the gui, same as mkids, but row nimbers so we can remember the checked on gui
        self.checked_list_rows = self.getRowsChecked()
        self.powersweepSetup()
#
#        threadflag=0

        #if self.check_multiprocess.isChecked():
        #    is_use_multiprocess=1
        #else:
        #    is_use_multiprocess=0



        if self.check_powersweep.isChecked():
            
         #   if is_use_multiprocess>0:        
         #       threadflag=threadflag | 1
         #   else:
            self.powersweep2();

            time.sleep(1.0)
        if self.check_runFits.isChecked():
#            if is_use_multiprocess>0:    
#                threadflag=threadflag | 2
#            else:   
            self.runFits2()
#
        if self.check_runIQvelocity.isChecked():
            self.IQvelocity()
                       
#       if is_use_multiprocess>0:    
#                threadflag=threadflag | 4
#            else:   
#                self.IQvelocity()
#
        time.sleep(1.0)
        if self.check_getnoise.isChecked():
            self.runNoise()

        time.sleep(1.0)

#        if self.check_getnoise.isChecked():
#            if is_use_multiprocess>0:    
#                threadflag=threadflag | 8
#            else:   
#                self.runNoise()
#
#
#        self.thread=QNetThread(threadflag);
#        self.thread.start()
#



    def stopIt(self):
        #tell processes to stop fits. we may have several cpus connected, so we should send several times.
        stopFitsMP()
        stopFitsMP()
        stopFitsMP()
        stopFitsMP()
        stopFitsMP()
        stopFitsMP()
        stopFitsMP()

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

            mkid=selected[0].data(100)

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
    
        print 'x %f y %f'%(event.xdata,event.ydata)
    
        if self.is_addres_onclick:
            print "Adding Resonator"
            #we get radisns from 0 to 2pi for polar plot, 
            #make sure not a polar plot
            if self.plottype==1:

                ff=event.xdata

                ap=event.ydata

                measure.device_name = self.textbox_devicename.text()
                mkid = measure.newMkid(ff)
                mkid.chip_name = self.textbox_devicename.text()
                MKID_list.append(mkid)



                self.updatePlot()

            else:
                print "Cant add resonance on this plot"

        

    def extractRes(self):
        global MKID_list
        
        measure.device_name = self.textbox_devicename.text()
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





    #load FW, sweep res and stream
    def streamRun(self):
    
      


        mlist =self.getSelMkid()
        if len(mlist) == 0:
            print "no selected resonators"
            return
            
            
        rffreqs = []
        
        for mkid in mlist:
            res = mkid.reslist[0]
            rffreqs.append(res.getFc())
            print res.getFc()
            
            
        bbfreqs = []
             
        (LO, bbfreqs ) = fa.calcBBLOFromRFFreqs( numpy.array(rffreqs) )
        
        if len(bbfreqs)==0:
            print "No resonators!!"
            return
            
        print LO
        print bbfreqs
             
        fa.setCarrier(LO)
        
        amp = 30000.0 * (1.0 / len(bbfreqs))
        print amp
        
        fa.sourceCapture(bbfreqs, amp)
        
        




    def streamStop(self):
        fa.stopCapture()

        time.sleep(1.0)
        fa.getIQ()
        
        fa.dataread.plotStreams(nsamples=2000)







    def saveSweep(self):
    
        hdf=hdfSerdes()
        
        fname = QFileDialog.getSaveFileName(
            caption='Hdf File Name',
            options=QFileDialog.DontConfirmOverwrite)[0]
            
        hdf.open(fname,'a')
        gname = 'sweep_%s'%time.asctime().replace(' ','_')
        hdf.write(fa,gname)
        hdf.close()
        
        
    def savePlot(self):
    
        hdf=hdfSerdes()
        
        fname = QFileDialog.getSaveFileName(
            caption='Hdf File Name',
            options=QFileDialog.DontConfirmOverwrite)[0]
            
        hdf.open(fname,'a')
        gname = 'plot_%s'%time.asctime().replace(' ','_')
        iqp = fa.dataread.RectToPolar(fa.iqdata)
        pldata = {'iqp':iqp , 'iq':fa.iqdata, 'freqs': fa.freqs_sweep }
        hdf.write(pldata,gname)
        hdf.close()
        
        #pickle.dump(pldata,open(fname+'.pic','wb'))
        
    
    def startSweep(self):
    
        cf = self.spinbox_CenterFreq.value()
    
    
        sf = self.spinbox_SpanFreq.value()

        st = cf - sf/2
        ed = cf + sf/2
        
        self.textbox_LOFreq.clear()
        self.textbox_LOFreq.insert('%1.3e'%(cf+10))

        self.textbox_StFreq.clear()
        self.textbox_StFreq.insert('%1.3e'% (st))

        self.textbox_EdFreq.clear()
        self.textbox_EdFreq.insert('%1.3e'%ed)
     
        #self.button_StSweep.setEnabled(False)


        #self.pool=QThreadPool()
        #self.pool.setMaxThreadCount(10)
        
        #pystring = 'fa.sweep(span_Hz=%f*1e6, center_Hz=%f*1e6, pts=2048)\n'%(sf,cf)
        #pystring = pystring + 'form.signalPlot()\n'
        
        #runnable = QRunPyThread( pystring)
            
            
        #status=self.pool.tryStart( runnable )
        npts = self.spinbox_numSwPts.value()
        fa.sweep(span_Hz=sf*1e6, center_Hz=cf*1e6, pts=npts)

        #self.button_StSweep.setEnabled(True)
        
        
        self.updatePlot()
        
        print "startSw return"



    


    def setAttenFromGUI(self):
    
        attu6=self.spinbox_AttOut0.value()
        attu7=self.spinbox_AttOut1.value()
        attu28=self.spinbox_AttIn0.value()
    
        self.setAttenuatorsOut0(attu6)
        self.setAttenuatorsOut1(attu7)
        self.setAttenuatorsIn0(attu28)

   
    
    

    def setReadoutFreq(self):
        #cf = 1e6*self.spinbox_CenterFreq.value()
    

        readf=float(self.textbox_RdFreq.text())*1e6
        cf=readf



            #sf = 1e6*self.spinbox_SpanFreq.value()
        sf=0;


        self.calcFreqVals(cf,sf)



        
    
        
  

    def stopSweep(self):
    
       pass

  
    def findDeletedResonators(self):
        a=1 
 
    def loadCustomAtten(self):
        a=1 
 
    def displayResonatorProperties(self):
        a=1 
        
    
        
    def bbLoopback(self,state):
        
        if state==2:
            fa.if_board.rf.baseband_loop=1
        else:
            fa.if_board.rf.baseband_loop=0
        
        fa.if_board.progIfBoard()
            




    def extClk(self,state):
        if state==2:
            fa.if_board.rf.lo_internal=0
        else:
            fa.if_board.rf.lo_internal=1
        
        fa.if_board.progIfBoard()
    
    #self.rfOutEn(0)    


    def rfOutEn(self,state):
    
        if state==2:
            fa.if_board.LO.rfouten=1
        else:
            fa.if_board.LO.rfouten=0
        
    
        fa.if_board.progIfBoard()


    def rfLoopback(self,state):
        if state==2:
            fa.if_board.rf.rf_loopback=1
        else:
            fa.if_board.rf.rf_loopback=0
        
        fa.if_board.progIfBoard()
            
            
    def fpgaLoopback(self,state):
        if state==2:
            na.is_digital_loopback=1
        else:
            na.is_digital_loopback=0
        
        
        
        
    def setAttenuatorsOut0(self,val):
    
        fa.if_board.at.atten_U6=val
        fa.if_board.progAtten(fa.if_board.at)
        
        

        
    def setAttenuatorsOut1(self,val):
   
        fa.if_board.at.atten_U7=val
        fa.if_board.progAtten(fa.if_board.at)
       

    def setAttenuatorsIn0(self,val):
   
        fa.if_board.at.atten_U28=val
        fa.if_board.progAtten(fa.if_board.at)
       
    

    
        
    def resetDAC(self):
        pass
       
    
    
    
    def hdfResSave(self):

        #save a copy as a rand name, because the files get overwritten

        #randname='backup_%f.h5'%(rand())
        #mkidSaveData(randname)

        
        filename = QFileDialog.getSaveFileName(
            caption='Hdf File Name')[0]
            


        #make backup files, save 5 of them
        for n in range(4):
            #n=0,1,2,3   nn=5,4,3,2
            nn=5-n;   
            #mv 4,3,2,1 to   5,4,3,2    
            try: os.system('mv backup_%d.h5 backup_%d.h5'%(nn-1,nn))
            except: pass

        try: os.system('mv %s backup_1.h5'%(filename))
        except: pass

        mkidSaveData(filename)

    
    def hdfResRead(self):
        filename = QFileDialog.getOpenFileName(caption='Hdf File Name')[0]
        #filename=self.textbox_HDF5ResName.text()
        mkidLoadData(filename)
        self.populateListWidget()

    def hdfResReadL(self):


        filename = QFileDialog.getOpenFileName(caption='Hdf File Name')[0]
        #filename=self.textbox_HDF5ResName.text()
        mkidLoadData(filename)
        for m in MKID_list:
            m.reslist=[]
            
        self.populateListWidget()
   
  


    def updatePlot(self):
    
        try:
    #if 1==1:

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


        except:
        #else:
            print 'natAnalGui::updatePlot- Exception'
            print 'plot type %d, %s'%(self.plottype,self.plot_names[self.plottype])
            traceback.print_exc()

    
        self.populateListWidget()

        #if is_thread_running>0:
        #    self.label_threadrun.setVisible(True)
        #else:
        #    self.label_threadrun.setVisible(False)

        
    def signalPlot(self):
        self.signal_plot.emit()


    
    def getTimestamp(self):    
       timestamp = "T".join( str( datetime.datetime.now() ).split() )
       return(timestamp)

    
    
    
    
    def getIQF(self):
    
       
        return([fa.iqdata,fa.freqs_sweep])



    



    def magPhasePl(self):
        self.status_text.setText('Plotting')


        #!!na.setDelay(1e-9*float(self.textbox_Dly.text()));
        iqf=self.getIQF()
        iq=iqf[0]
        freqs=iqf[1]



        #na.plotFreq(iq)


        #record zoom settings before clearing or replotting
        #self.plot_zoom_settings={"pltype":"NULL" , "autoscale":1}
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



        if self.clearplot==1:
            self.axes0.clear()
            self.axes1.clear()
        


        global IQp_
        global freqs_
        IQp_=IQp
        freqs_=freqs
        self.axes0.plot(freqs,IQp[0])
        self.axes1.plot(freqs,IQp[1])
        self.axes0.set_ylabel('Magnitude')
        self.axes1.set_ylabel('Phase')        
        self.axes1.set_xlabel('Frequency')

        if len(MKID_list)>0:

            self.markerlistx=[]

            for m in MKID_list:
                self.markerlistx.append(m.rough_cent_freq)

            ind1=find(self.markerlistx>freqs[0])
            ind2=find(self.markerlistx<freqs[len(freqs)-1])
            ind = list(set(ind1).intersection(set(ind2)))

            yvals=(0.5*(max(IQp[0]) + min(IQp[0])))*ones(len(ind))


            self.axes0.plot(array(self.markerlistx)[ind],yvals,'rx')


        if False:

            #if not autoscaling, then we recover the x,y lims

            if self.plot_zoom_settings["pltype"]=="magPhasePl":
                self.axes0.set_xlim(self.plot_zoom_settings["axes0xlim"])
                self.axes0.set_ylim(self.plot_zoom_settings["axes0ylim"])
                self.axes1.set_xlim(self.plot_zoom_settings["axes1xlim"])
                self.axes1.set_ylim(self.plot_zoom_settings["axes1ylim"])


        self.plot_zoom_settings={}
        self.plot_zoom_settings["pltype"]="magPhasePl"
        self.plot_zoom_settings["axes0xlim"]=self.axes0.get_xlim()
        self.plot_zoom_settings["axes0ylim"]=self.axes0.get_ylim()
        self.plot_zoom_settings["axes1xlim"]=self.axes1.get_xlim()
        self.plot_zoom_settings["axes1ylim"]=self.axes1.get_ylim()



        self.canvas.draw();
        print "plot done"    



    #    if (self.is_sweeping==1):
    #            self.timer=QTimer()    
    #        self.timer.timeout.connect(self.magPhasePl)
    #        self.timer.setSingleShot(True)
    #        self.timer.start(1000)
    #    



    def IQPlots(self):
        self.status_text.setText('Plotting')


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
        self.status_text.setText('Plotting')


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


        if self.clearplot==1:
            self.axes0.clear()
            self.axes1.clear()

            self.axes2.clear()

            self.axes3.clear()

        self.axes0.plot(freqs,IQp[0])

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


    
        for resdata in self.fftreslist:

            fbase=na.findBasebandFreq(resdata.rough_cent_freq)
            ts=na.extractTimeSeries(fbase)
            tsr=na.dataread.PolarToRect(ts)
            tsr_tr=fit.trans_rot3(resdata, tsr)



            #!!self.axes0.plot(resdata.trot_xf,resdata.trot_yf)
            self.axes0.plot(resdata.iqdata[0],resdata.iqdata[1])
            self.axes0.plot(tsr[0],tsr[1],'.')
            #!!self.axes0.plot(tsr_tr[0],tsr_tr[1],'.')



            #self.axes0.plot(resdata.iqdata[0], resdata.iqdata[1])
            #self.axes0.plot(tsr[0],tsr[1],'.')


        self.canvas.draw();
    
    def plotChan3D(self):

        if self.clearplot==1:

            self.fig.clear()

        self.axes0 = self.fig.gca(projection='3d')    

        k=0.0

        zranges=[]
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




    
    def plotMultiChanMagPh(self):
        if self.clearplot==1:

            self.fig.clear()

        self.axes0 = self.fig.add_subplot(2,1,1)
        self.axes1 = self.fig.add_subplot(2,1,2)

        self.axes0.set_xlabel('Time')
        self.axes0.set_ylabel('Mag')

        self.axes1.set_xlabel('Time')
        self.axes1.set_ylabel('Degrees')

        if self.clearplot==1:

            self.axes0.clear()

        self.axes0.plot()


        k=0.0

        try:
            for f in na.frequency_list:
                print 'here 1'
                print f
                ts = na.extractTimeSeries(f)
                tsr=na.dataread.PolarToRect(ts)
                ts[0] = ts[0] - median(ts[0])
                ts[1] = ts[1] - median(ts[1])


                stdmag=numpy.std(ts[0])
                stdph=numpy.std(ts[1]) * (180.0/pi)


                print 'here 2'
                self.axes0.plot(k*stdmag +  ts[0]-median(ts[0]))

                self.axes1.plot(k*stdph +   (ts[1] - median(ts[1]))*(180.0/pi))

                k = k+3.0


            self.axes0.set_ylim((-3*stdmag,k*stdmag))
            self.axes1.set_ylim((-3*stdph,k*stdph))

        except:
            print "exception somewhere"

        self.canvas.draw();


    
    def plotIvQ(self):

        self.status_text.setText('Plotting')
   
 

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


  
  
    def resPlots(self):
        
    

        selected=self.list_reslist2.selectedItems()

        if len(selected)>0:
            obj=selected[0].data(0,100)

            if obj.__class__.__name__ == "MKID":
                fit.reslist = obj.reslist
                fit.plotResonators()    

            if obj.__class__.__name__ == "resonatorData":
                obj.info()
                obj.plotFreq() #this function exists in both netAnalyzer.py and fitters.py? This seems to call the fitters.py version
                if obj.is_ran_fits==1 and obj.is_fit_error==0:
                    fit.resonator=obj
                    fit.lorentzPlots()




    def medFilter(self):
        
    

        selected=self.list_reslist2.selectedItems()

        if len(selected)>0:
            obj=selected[0].data(0,100)

            if obj.__class__.__name__ == "MKID":
                fit.reslist = obj.reslist
                fit.medianFilter()    

            if obj.__class__.__name__ == "resonatorData":
                
                fit.reslist = [obj]
                fit.medianFilter()



    def lowPassFilter(self):
        
    

        selected=self.list_reslist2.selectedItems()

        if len(selected)>0:
            obj=selected[0].data(0,100)

            if obj.__class__.__name__ == "MKID":
                fit.reslist = obj.reslist
                fit.lowPassFilter()    

            if obj.__class__.__name__ == "resonatorData":
                
                fit.reslist = [obj]
                fit.lowPassFilter()


  
  
  
    def clearNoise(self):
        
    

        selected=self.list_reslist2.selectedItems()

        if len(selected)>0:
            obj=selected[0].data(0,100)

            if obj.__class__.__name__ == "MKID":
                for r in obj.reslist:
                    r.clearNoise()

            if obj.__class__.__name__ == "resonatorData":
                obj.clearNoise()



  
    def clearTraces(self):
        
    

        selected=self.list_reslist2.selectedItems()

        if len(selected)>0:
            obj=selected[0].data(0,100)

            if obj.__class__.__name__ == "MKID":
                obj.clearResList()


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




    def checkAllList(self):
        global MKID_list
    
    for mkid in MKID_list:
        mkid.checked=1

        self.populateListWidget()

        self.setRowsAllChecked()
        self.checked_list_rows = self.getRowsChecked()




    def unCheckAllList(self):
        global MKID_list
    
        for mkid in MKID_list:
            mkid.checked=0

        self.populateListWidget()

        self.setRowsAllUnChecked()
        self.checked_list_rows = self.getRowsChecked()




     


    
    #
#    
#    
#    #set up and test pulse detecotr
#        self.button_progpulsedet = QPushButton("ProgPulseDet")
#    self.button_progpulsedet.setMaximumWidth(170)
#        self.connect(self.button_progpulsedet, SIGNAL('clicked()'), self.progPulseDet)            
#        
#    label_tevtrate = QLabel('EventRate')
#    self.label_test_event_rate = QLabel('0')
#    
##
#    
#    #set up and test pulse detecotr
#        self.button_pulsedetmeasmeans = QPushButton("MeasMeans")
#    self.button_pulsedetmeasmeans.setMaximumWidth(170)
#        self.connect(self.button_pulsedetmeasmeans, SIGNAL('clicked()'), self.measPulseMeans)            
#        



#
#
#
#    def enablePulseDetAvg(self,state):
#        
#    if state==0:
#      fa.recordEvents(0)
#      na.calcMeans(self,1)
#    else:
#      na.calcMeans(self,0)
#      fa.recordEvents(1)
#    
#        



#
# sort res list by center freq, and disp on widget
#

    def populateListWidget(self):
        global MKID_list
    

        #preserved what is checked when list is redrawn by storing if the res is checked.

    #    for row in range(self.list_reslist2.count()):
    #        item=self.list_reslist2.item(row)
    #        if item.checkState()==Qt.Checked:
    #        item.data(100).checked=1
    #        else:
    #            item.data(100).checked=0



        #print form.list_reslist.item(0).data(100).chip_name

        #
        #clear gui lists 
        #
        self.list_reslist.clear()
        self.list_reslist2.clear()

        self.list_reslist2.setColumnCount(9)
        self.list_reslist2.setHeaderLabels(["Res #","Trace #", "Device", "Fc (MHz)", "N. Traces","Atten","Fits","FitErr","Noise"])
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
            item.setData(100,mkid)
            item.setText('Res# %d %s fc=%4.1fMHz  Traces: %d'%(mkid.resonator_num, mkid.chip_name, mkid.rough_cent_freq/1e6,len(mkid.reslist)))
            #item.setFlags(item.flags() | Qt.ItemIsUserCheckable )


            #
            # populate the tree view on the data tab
            #
            item2=QTreeWidgetItem(self.list_reslist2)
            item2.setData(0,100,mkid)

            item2.setText(0,'Res %d '%(mkid.resonator_num))
            item2.setText(2,'%s '%(mkid.chip_name))
            item2.setText(3,'%4.2f'%(mkid.rough_cent_freq/1e6))
            item2.setText(4,'%d'%(len(mkid.reslist)))

            if mkid.checked==1:    
                item2.setCheckState(0,Qt.Checked)

            else:
                item2.setCheckState(0,Qt.Unchecked)


            #
            # add traces to the tree widget
            #
            trcnt=0
            for trace in mkid.reslist:
                item3=QTreeWidgetItem(item2)
                item3.setData(0,100,trace)

                item3.setText(1,'Trc %d '%(trcnt))
                item3.setText(5,'%3.0f'%(trace.atten_U7))
                item3.setText(6,'%3.0f'%(trace.is_ran_fits))
                item3.setText(7,'%3.0f'%(trace.is_fit_error))
                item3.setText(8,'%3.0f'%(trace.is_noise))
                #item3.setText(2,'%4.2f'%(mkid.rough_cent_freq/1e6))
                #item3.setText(3,'%d'%(len(mkid.reslist)))

                trcnt=trcnt+1


            #self.list_reslist2.addItem(item2)
        #preserve the rows that were checked
        self.setRowsChecked(self.checked_list_rows)



        #
        #
        #

    def delResonator(self):
        global MKID_list
        selected=self.list_reslist.selectedItems()

        for ss in selected:
            #get MKID object
            m=ss.data(100)

            MKID_list.remove(m)

        self.updatePlot()


    #
    # Run py code
    #
    def runPython(self):
        print "running py script"
        exec self.textbox_Python.text()
  
  
  
  
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

  
  
    def setRampSyncSource(self):
          
        
        ci = self.combobox_syncsource.currentIndex()
        
        #no ramp
        if ci==0:
            fa.rampgen.setIsSync(0)
            fa.rampgen.setSyncSource(0)
            fa.rampgen.setChannelizerFifoSync()
        
        #ext ramp
        elif ci==1:
        #int ramp
            fa.rampgen.setIsSync(1)
            fa.rampgen.setSyncSource(0)
            fa.rampgen.setChannelizerFifoSync()


        else:
            fa.rampgen.setIsSync(1)
            fa.rampgen.setSyncSource(1)
            self.setRampSpecs()
            ##fa.rampgen.setChannelizerFifoSync()
        
  
  
      
        
        
        
    def setRampSpecs(self):
        r_amp = self.spinbox_RampAmp.value() / 100.0
        r_freq = self.spinbox_RampFreq.value()
        fa.rampgen.setRamp(r_amp,r_freq)
        fa.rampgen.setChannelizerFifoSync()
        
        
  
    def setFluxRampDemod(self):
    
        frd=[0,0]
        
        frdci = self.combobox_flxRmpDmd.currentIndex()
        if frdci==0:
            frd = [0,0]
        elif frdci==1:
            frd= [1,1]
        elif frdci==2:
            frd = [1,0]
        else:
            frd=[0,0]
        
        numprd = float(self.textbox_flxRmpPrd.text())
        
        fa.chanzer.setFluxRampDemod(frd[0],frd[1],fa.chanzer.read_fifo_size,numprd)

    def refreshFRDSettings(self):
        self.setRampSpecs()
        self.setRampSyncSource()
        self.setFluxRampDemod()
        
    
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
        self.button_saveSweep = QPushButton("SaveAnalyzer")
        self.button_saveSweep.setMaximumWidth(200)
        self.connect(self.button_saveSweep, SIGNAL('clicked()'), self.saveSweep)   


  # Start/ Stop Sweep for Net analyzer
        self.button_savePlot = QPushButton("SavePlot")
        self.button_savePlot.setMaximumWidth(200)
        self.connect(self.button_savePlot, SIGNAL('clicked()'), self.savePlot)   


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
            'IQVelocity','IQCircle','ResFit','3DChannels']


        self.combobox_plottype=QComboBox()
        for name in self.plot_names:
            self.combobox_plottype.addItem(name)   

        #self.connect(self.combobox_plottype, SIGNAL('currentIndexChanged'), self.setPlotType) 
        self.combobox_plottype.currentIndexChanged.connect(self.setPlotType)




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

 
 



        #
        # Attenuators on IF Board
        #
        #
        # Frequency entries for sweeping net analuyzer
        #
        self.label_AttOut0 = QLabel('AttenOutU6')
        self.label_AttOut0.setMaximumWidth(120)
    
 
        self.label_AttOut1 = QLabel('AttenOutU7')
        self.label_AttOut1.setMaximumWidth(120)
 
        self.label_AttIn0 = QLabel('AttenInU28')
        self.label_AttIn0.setMaximumWidth(120)
 
 
    
        self.spinbox_AttOut0 = QSpinBox()
        self.spinbox_AttOut0.setRange(0,32)
        self.spinbox_AttOut0.setValue(10)
        self.spinbox_AttOut0.setSingleStep(1)
        self.spinbox_AttOut0.setMaximumWidth(50)
        self.spinbox_AttOut0.valueChanged.connect(self.setAttenuatorsOut0)

        self.spinbox_AttOut1 = QSpinBox()
        self.spinbox_AttOut1.setRange(0,32)
        self.spinbox_AttOut1.setValue(10)
        self.spinbox_AttOut1.setSingleStep(1)
        self.spinbox_AttOut1.setMaximumWidth(50)
        self.spinbox_AttOut1.valueChanged.connect(self.setAttenuatorsOut1)

        self.spinbox_AttIn0 = QSpinBox()
        self.spinbox_AttIn0.setRange(0,32)
        self.spinbox_AttIn0.setValue(10)
        self.spinbox_AttIn0.setSingleStep(1)
        self.spinbox_AttIn0.setMaximumWidth(50)
        self.spinbox_AttIn0.valueChanged.connect(self.setAttenuatorsIn0)







        #
        # For adding resonator markers on plot
        #
        self.checkbox_AddMark=QCheckBox('Mark')
        self.checkbox_AddMark.setMaximumWidth(200)
        self.checkbox_AddMark.stateChanged.connect(self.addMark)




    #      
        # custom Python exe line
        #
    
        self.textbox_Python = QLineEdit('print "Hello"')
        self.textbox_Python.setMaximumWidth(400)

        # Start connection to roach.
        self.button_Python = QPushButton("RunPy")
        self.button_Python.setMaximumWidth(60)
        self.connect(self.button_Python, SIGNAL('clicked()'), self.runPython)
   


    #      
        # hdf5 filename for dumping IQ data.
        #
    
        # Load thresholds.
        #self.button_loadThresholds = QPushButton("(4)load thresholds")
        #self.button_loadThresholds.setMaximumWidth(170)
        #self.connect(self.button_loadThresholds, SIGNAL('clicked()'), self.loadThresholds)

      





        # plotting resonators- 
        self.button_resPlots = QPushButton("ResonatorPlots")
        self.button_resPlots.setMaximumWidth(170)
        self.connect(self.button_resPlots, SIGNAL('clicked()'), self.resPlots)
              

        # plotting resonators- 
        self.button_clrTrace = QPushButton("ClrTrc")
        self.button_clrTrace.setMaximumWidth(100)
        self.connect(self.button_clrTrace, SIGNAL('clicked()'), self.clearTraces)
        
        # plotting resonators- 
        self.button_clrNoise = QPushButton("ClrNoiz")
        self.button_clrNoise.setMaximumWidth(100)
        self.connect(self.button_clrNoise, SIGNAL('clicked()'), self.clearNoise)
        

        # plotting resonators- 
        self.button_medFilter = QPushButton("medFlt")
        self.button_medFilter.setMaximumWidth(100)
        self.connect(self.button_medFilter, SIGNAL('clicked()'), self.medFilter)
        
        
        # plotting resonators- 
        self.button_lowpassFilter = QPushButton("LPF")
        self.button_lowpassFilter.setMaximumWidth(100)
        self.connect(self.button_lowpassFilter, SIGNAL('clicked()'), self.lowPassFilter)
        

        self.label_resPlots = QLabel('ResNum')
        self.label_resPlots.setMaximumWidth(30)

        self.textbox_resPlots = QLineEdit('0')
        self.textbox_resPlots.setMaximumWidth(70)

       
       
               # for adding resonance by clocking on the figure. check then clock res.
        self.checkbox_AddRes=QCheckBox('AddRes')
        self.checkbox_AddRes.setMaximumWidth(200)
        self.checkbox_AddRes.stateChanged.connect(self.addResonator)

        # 
    # reset button- resets msm, restarts DAC
    #restarts sweep
    #
        self.button_resetDAC = QPushButton("Reset")
        self.button_resetDAC.setMaximumWidth(170)
        self.connect(self.button_resetDAC, SIGNAL('clicked()'), self.resetDAC)            
    
   

    #
        # Long time powersweep of a single channel
        #
    #self.button_powersweep = QPushButton("powersweep")
        #self.button_powersweep.setMaximumWidth(170)
        #self.connect(self.button_powersweep, SIGNAL('clicked()'), self.powersweep)            
        

        self.check_powersweep = QCheckBox("Powersweep")

        self.label_pwrsw_atinst = QLabel('AttIn Start (U28)')
        self.label_pwrsw_atinst.setMaximumWidth(120)
 
        self.spinbox_pwrsw_atinst = QSpinBox()
        self.spinbox_pwrsw_atinst.setRange(0,32)
        self.spinbox_pwrsw_atinst.setValue(1)
        self.spinbox_pwrsw_atinst.setSingleStep(1)
        self.spinbox_pwrsw_atinst.setMaximumWidth(50)
    
    
        self.label_pwrsw_atst = QLabel('AttOut Start (U7)')
        self.label_pwrsw_atst.setMaximumWidth(120)
 
        self.spinbox_pwrsw_atst = QSpinBox()
        self.spinbox_pwrsw_atst.setRange(0,21) #Set limits based upon total attenuation
        self.spinbox_pwrsw_atst.setValue(20)
        self.spinbox_pwrsw_atst.setSingleStep(1)
        self.spinbox_pwrsw_atst.setMaximumWidth(50)
    
    
        self.label_pwrsw_atend = QLabel('AttOut End (U7)')
        self.label_pwrsw_atend.setMaximumWidth(120)
 
        self.spinbox_pwrsw_atend = QSpinBox()
        self.spinbox_pwrsw_atend.setRange(0,21) #Set limits based upon total attenuation
        self.spinbox_pwrsw_atend.setValue(20)
        self.spinbox_pwrsw_atend.setSingleStep(1)
        self.spinbox_pwrsw_atend.setMaximumWidth(50)

        self.label_pwrsw_atstep = QLabel('AttOut Step')
        self.label_pwrsw_atstep.setMaximumWidth(120)
 
        self.spinbox_pwrsw_atstep = QSpinBox()
        self.spinbox_pwrsw_atstep.setRange(1,10)
        self.spinbox_pwrsw_atstep.setValue(1)
        self.spinbox_pwrsw_atstep.setSingleStep(1)
        self.spinbox_pwrsw_atstep.setMaximumWidth(50)
    
    
        self.label_pwrsw_numNoise = QLabel('NNoiseTr')
        self.label_pwrsw_numNoise.setMaximumWidth(120)
 
        self.spinbox_numNoise = QSpinBox()
        self.spinbox_numNoise.setRange(1,100)
        self.spinbox_numNoise.setValue(1)
        self.spinbox_numNoise.setSingleStep(1)
        self.spinbox_numNoise.setMaximumWidth(50)
    
    
    
        
    
    
        self.label_pwrsw_atsweeps = QLabel('# of Sweeps')
        self.label_pwrsw_atsweeps.setMaximumWidth(120)
 
        self.spinbox_pwrsw_atsweeps = QSpinBox()
        self.spinbox_pwrsw_atsweeps.setRange(1,1000000)
        self.spinbox_pwrsw_atsweeps.setValue(1)
        self.spinbox_pwrsw_atsweeps.setSingleStep(1)
        self.spinbox_pwrsw_atsweeps.setMaximumWidth(50)
    
    
        self.label_pwrsw_span = QLabel('Span (MHz)')
        self.label_pwrsw_span.setMaximumWidth(120)
 
        self.spinbox_pwrsw_span = QSpinBox()
        self.spinbox_pwrsw_span.setRange(1,6000)
        self.spinbox_pwrsw_span.setValue(1)
        self.spinbox_pwrsw_span.setSingleStep(1)
        self.spinbox_pwrsw_span.setMaximumWidth(200)



        self.label_nswfreqs = QLabel('NumPoints')
        self.label_nswfreqs.setMaximumWidth(120)
 
        self.spinbox_nswfreqs = QSpinBox()
        self.spinbox_nswfreqs.setRange(16,65536)
        self.spinbox_nswfreqs.setValue(256)
        self.spinbox_nswfreqs.setSingleStep(64)
        self.spinbox_nswfreqs.setMaximumWidth(200)








        self.label_pwrsw_atTotal = QLabel('U6CnstOAtt')
        self.label_pwrsw_atTotal.setMaximumWidth(120)
 
        self.spinbox_pwrsw_atTotal = QSpinBox()
        self.spinbox_pwrsw_atTotal.setRange(1,50)
        self.spinbox_pwrsw_atTotal.setValue(31)
        self.spinbox_pwrsw_atTotal.setSingleStep(1)
        self.spinbox_pwrsw_atTotal.setMaximumWidth(50)



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
        self.list_reslist2 = QTreeWidget()

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
        
        self.check_runFits = QCheckBox("runFits")

        self.check_runIQvelocity = QCheckBox("run IQ velocity")
    
    #
    # label that vanishes and reappears as is_thread_running is set to 1 and 0. done in update Plots
    #
        self.label_threadrun=QLabel("<P><b><i><FONT COLOR='#ff0000' FONT SIZE = 4>RUNNING</i></b></P></br>")
        self.label_threadrun.setVisible(False)
    

    #run sweeps and fits and noise. 
        self.button_runIt = QPushButton("RunChecked")
        self.button_runIt.setMaximumWidth(170)
        self.connect(self.button_runIt, SIGNAL('clicked()'), self.runIt)            
        

    #run sweeps and fits and noise. 
        self.button_stopIt = QPushButton("StopChecked")
        self.button_stopIt.setMaximumWidth(170)
        self.connect(self.button_stopIt, SIGNAL('clicked()'), self.stopIt)            
        


    
    #run sweeps and fits and noise. 
        self.button_checkall = QPushButton("CheckAll")
        self.button_checkall.setMaximumWidth(170)
        self.connect(self.button_checkall, SIGNAL('clicked()'), self.checkAllList)            
        


    #run sweeps and fits and noise. 
        self.button_uncheckall = QPushButton("UnCheckAll")
        self.button_uncheckall.setMaximumWidth(170)
        self.connect(self.button_uncheckall, SIGNAL('clicked()'), self.unCheckAllList)            
        




    #run sweeps and fits and noise. 
        self.button_hdfshell = QPushButton("hdfShell")
        self.button_hdfshell.setMaximumWidth(170)
        self.connect(self.button_hdfshell, SIGNAL('clicked()'), hdfshell)            
        


    #run sweeps etc, every hour. 
        self.button_runbyhour = QPushButton("runByHour")
        self.button_runbyhour.setMaximumWidth(170)
        self.connect(self.button_runbyhour, SIGNAL('clicked()'), self.repeatRunIt)            
        

    #stop run every hour. 
        self.button_stoprepeat = QPushButton("stopByHour")
        self.button_stoprepeat.setMaximumWidth(170)
        self.connect(self.button_stoprepeat, SIGNAL('clicked()'), self.stopRepeat)            
        

    # extract threshold N*sigma
        self.textbox_repeatmin = QLineEdit('60')
        self.textbox_repeatmin.setMaximumWidth(50)
        self.label_repeatmin = QLabel('RepeatMin')



    # extract threshold N*sigma
        self.textbox_noisesec = QLineEdit('0.25')
        self.textbox_noisesec.setMaximumWidth(50)
        self.label_noisesec = QLabel('NoiseSec')




        self.check_multiprocess = QCheckBox("MultiProcess")
        self.check_multiprocess.stateChanged.connect(self.startMPQueue)
    
    
        self.check_getnoise = QCheckBox("GetNoise")
    

    #
    #Saving and loading resonator data
    #
    
    
        #self.textbox_HDF5ResName = QLineEdit('dataset')
        #self.textbox_HDF5ResName.setMaximumWidth(400)

        #self.textbox_HDF5filepath = QLineEdit('//local/datacecil')
        #self.textbox_HDF5filepath.setMaximumWidth(400)
    

        self.button_HDF5ResRead = QPushButton("Load")
        self.button_HDF5ResRead.setMaximumWidth(60)
        self.connect(self.button_HDF5ResRead, SIGNAL('clicked()'), self.hdfResRead)
    

        self.button_HDF5ResReadL = QPushButton("LoadL")
        self.button_HDF5ResReadL.setMaximumWidth(60)
        self.connect(self.button_HDF5ResReadL, SIGNAL('clicked()'), self.hdfResReadL)
    

        self.button_HDF5ResSave = QPushButton("Save")
        self.button_HDF5ResSave.setMaximumWidth(60)
        self.connect(self.button_HDF5ResSave, SIGNAL('clicked()'), self.hdfResSave)
    
    
    # Read pulses
        #self.button_readPulses = QPushButton("Read pulses")
        #self.button_readPulses.setMaximumWidth(170)
        #self.connect(self.button_readPulses, SIGNAL('clicked()'), self.readPulses)   
        
        # Seconds for "read pulses."
        #self.textbox_seconds = QLineEdit('1')
        #self.textbox_seconds.setMaximumWidth(50)
        
        # lengths of 2 ms for defining thresholds.
        #self.textbox_timeLengths = QLineEdit('10')
        #self.textbox_timeLengths.setMaximumWidth(50)
        #label_timeLengths = QLabel('* 2 msec       ')


        # lengths of 2 ms steps to combine in a snapshot.
        self.textbox_snapSteps = QLineEdit('10')
        self.textbox_snapSteps.setMaximumWidth(50)
        label_snapSteps = QLabel('* 2 msec')

        # lengths of 2 ms steps to combine in a snapshot.
        #self.textbox_longsnapSteps = QLineEdit('1')
        #self.textbox_longsnapSteps.setMaximumWidth(50)
        #label_longsnapSteps = QLabel('* sec')

        #median
        #self.label_median = QLabel('median: 0.0000')
        #self.label_median.setMaximumWidth(170)

        #threshold
        #self.label_threshold = QLabel('threshold: 0.0000')
        #self.label_threshold.setMaximumWidth(170)

        #attenuation
        #self.label_attenuation = QLabel('attenuation: 0')
        #self.label_attenuation.setMaximumWidth(170)

        #frequency
        #self.label_frequency = QLabel('freq (GHz): 0.0000')
        #self.label_frequency.setMaximumWidth(170)
        
        
    
        self.label_saysf = QLabel('Sweep and You Shall Find')
        




    

        #
        # widgets for noise/readout mode FW
        #

        #acq FFTs button- will load FW if need to.


   
   
   
   
   
    
    #run stream
        self.button_stream_run = QPushButton("StartStream")
        self.button_stream_run.setMaximumWidth(170)
        self.connect(self.button_stream_run, SIGNAL('clicked()'), self.streamRun)            
        
    #stop FFTs
        self.button_stream_stop = QPushButton("StopStream")
        self.button_stream_stop.setMaximumWidth(170)
        self.connect(self.button_stream_stop, SIGNAL('clicked()'), self.streamStop)            
    
    
    
    
   
   
   
   
   
   

        # stream file name
        self.textbox_streamfilename = QLineEdit('0.6')
        self.textbox_streamfilename.setMaximumWidth(400)
        label_lut_strfilename = QLabel('Streamfilename.h5')


        # stream file name
        self.textbox_streamfilename = QLineEdit('/local/superduper.h5')
        self.textbox_streamfilename.setMaximumWidth(400)
        label_lut_strfilename = QLabel('Streamfilename.h5')

   
        # lut amp
        self.textbox_streamsec = QLineEdit('30')
        self.textbox_streamsec.setMaximumWidth(50)
        label_streamsec = QLabel('SecondsStream')
   


   
   
      
    

    
    
    
    #stop qt event loop
        self.button_gui_stop = QPushButton("Exit2Console")
        self.button_gui_stop.setMaximumWidth(170)
        self.connect(self.button_gui_stop, SIGNAL('clicked()'), self.guiStop)            
    
    
    #
    # Ramp and sync tab
    #
    
    
 
    
        self.combobox_syncsource=QComboBox()
       
        self.combobox_syncsource.addItem('No RampSource')   
        self.combobox_syncsource.addItem('Ext RampSource')   
        self.combobox_syncsource.addItem('Int RampSource')   

        #self.connect(self.combobox_plottype, SIGNAL('currentIndexChanged'), self.setPlotType) 
        self.combobox_syncsource.currentIndexChanged.connect(self.setRampSyncSource)

    
    
    
        self.spinbox_RampAmp = QSpinBox()
        self.spinbox_RampAmp.setRange(0,100)
        self.spinbox_RampAmp.setValue(50)
        self.spinbox_RampAmp.setSingleStep(1)
        self.spinbox_RampAmp.setMaximumWidth(150)
        self.spinbox_RampAmp.valueChanged.connect(self.setRampSpecs)
        label_RampAmp = QLabel('Amp 0% - 100%')
    
    
    
    
        self.spinbox_RampFreq = QSpinBox()
        self.spinbox_RampFreq.setRange(1000,2000000)
        self.spinbox_RampFreq.setValue(10000)
        self.spinbox_RampFreq.setSingleStep(1000)
        self.spinbox_RampFreq.setMaximumWidth(150)
        self.spinbox_RampFreq.valueChanged.connect(self.setRampSpecs)
        label_RampFreq = QLabel('Freq Hz 1e3-2e6')
        
        
        
        
    
        self.combobox_flxRmpDmd=QComboBox()
       
        self.combobox_flxRmpDmd.addItem('Raw Data')   
        self.combobox_flxRmpDmd.addItem('Raw + FRD')   
        self.combobox_flxRmpDmd.addItem('FRD only')   

        #self.connect(self.combobox_plottype, SIGNAL('currentIndexChanged'), self.setPlotType) 
        self.combobox_flxRmpDmd.currentIndexChanged.connect(self.setFluxRampDemod)

    
        
        # lut amp
        self.textbox_flxRmpPrd = QLineEdit('3.0')
        self.textbox_flxRmpPrd.setMaximumWidth(50)
        self.textbox_flxRmpPrd.returnPressed.connect(self.setFluxRampDemod)

        label_flxRmpPrd = QLabel('FlxRmp Periods')
   
        
        
        self.button_setupRamp = QPushButton("RefreshSettings")
        self.button_setupRamp.setMaximumWidth(170)
        self.connect(self.button_setupRamp, SIGNAL('clicked()'), self.refreshFRDSettings)            
    
        

        gbox_sync = QVBoxLayout()
        hbox_sync1 = QHBoxLayout()
        hbox_sync1.addWidget(self.combobox_syncsource)
        hbox_sync2 = QHBoxLayout()

        hbox_sync2.addWidget(label_RampAmp)
        hbox_sync2.addWidget(self.spinbox_RampAmp)
        
    
        hbox_sync3 = QHBoxLayout()

        hbox_sync3.addWidget(label_RampFreq)
        hbox_sync3.addWidget(self.spinbox_RampFreq)
        
        
        
        hbox_sync4 = QHBoxLayout()
        hbox_sync4.addWidget(self.combobox_flxRmpDmd)
        hbox_sync4.addWidget(label_flxRmpPrd)
        hbox_sync4.addWidget(self.textbox_flxRmpPrd)
        
        hbox_sync5 = QHBoxLayout()
        hbox_sync5.addWidget(self.button_setupRamp)
        
        gbox_sync.addLayout(hbox_sync1)
        gbox_sync.addLayout(hbox_sync2)
        gbox_sync.addLayout(hbox_sync3)
        gbox_sync.addLayout(hbox_sync4)
        gbox_sync.addLayout(hbox_sync5)
        
    
    #
    # Settings tab
    #
    
    
        gbox0 = QVBoxLayout()
        hbox00 = QHBoxLayout()
        hbox00.addWidget(self.textbox_roachIP)
        hbox00.addWidget(self.button_openClient)
        hbox00.addWidget(self.button_closeClient)
        
        
        gbox0.addLayout(hbox00)




        hbox02 = QHBoxLayout()
        #hbox02.addWidget(self.textbox_coeffsFile)

        hbox02.addWidget(self.label_plottype)
        hbox02.addWidget(self.combobox_plottype)
    
    
    
        gbox0.addLayout(hbox02)

        hbox03 = QHBoxLayout()
        #hbox03.addWidget(self.textbox_timeLengths)
        #hbox03.addWidget(label_timeLengths)
        #hbox03.addWidget(self.textbox_Nsigma)
        #hbox03.addWidget(label_Nsigma)
        #hbox03.addWidget(self.button_loadThresholds)
        gbox0.addLayout(hbox03)
        
        gbox1 = QVBoxLayout()
        #gbox1.addWidget(label_DACfreqs)
        #gbox1.addWidget(self.textedit_DACfreqs)

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
    

        hbox21.addWidget(self.label_AttOut0)
        hbox21.addWidget(self.spinbox_AttOut0)
        hbox21.addWidget(self.label_AttOut1)
        hbox21.addWidget(self.spinbox_AttOut1)
        hbox21.addWidget(self.label_AttIn0)
        hbox21.addWidget(self.spinbox_AttIn0)
       

    
    
    
        #hbox21.addWidget(self.textbox_Python)
        #hbox21.addWidget(self.button_Python)
        gbox2.addLayout(hbox21)

        
        hbox215 = QHBoxLayout()
       
        gbox2.addLayout(hbox215)

        hbox22 = QHBoxLayout()
       
    #hbox22.addWidget(self.label_extract_thresh)
    #hbox22.addWidget(self.textbox_extract_thresh)
        #hbox22.addWidget(self.button_extractRes)
    #hbox22.addWidget(self.button_runFits)
        #hbox22.addWidget(self.textbox_longsnapSteps)
        #hbox22.addWidget(label_longsnapSteps)
        gbox2.addLayout(hbox22)
        
    
    #gbox2.addWidget(self.button_rmCustomThreshold)

        hbox23 = QHBoxLayout()
        #hbox23.addWidget(self.label_resPlots)
        #hbox23.addWidget(self.textbox_resPlots)
        #hbox23.addWidget(self.button_resPlots)
       
        gbox2.addLayout(hbox23)





                
        t1_hbox11 = QHBoxLayout()
        t1_hbox11.addWidget(self.textbox_Python)
        t1_hbox11.addWidget(self.button_Python)
        t1_hbox11.addWidget(self.button_resetDAC)
        t1_hbox11.addWidget(self.button_gui_stop)
        gbox2.addLayout(t1_hbox11)

        


        gbox3 = QVBoxLayout()
        #gbox3.addWidget(self.label_median)
        #gbox3.addWidget(self.label_threshold)
        #gbox3.addWidget(self.label_attenuation)
        #gbox3.addWidget(self.label_frequency)

        hbox = QHBoxLayout()
        hbox.addLayout(gbox0)
        hbox.addLayout(gbox1)     
        hbox.addLayout(gbox2)
        hbox.addLayout(gbox3)
        
    
    
    
    
    
    
    
    
    #
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
    
    
    
        t2_hbox015.addWidget(self.label_LO)
        t2_hbox015.addWidget(self.textbox_LOFreq)
        t2_hbox015.addWidget(self.label_St)
        t2_hbox015.addWidget(self.textbox_StFreq)
    #t2_hbox015.addWidget(self.label_Inc)
        #t2_hbox015.addWidget(self.textbox_IncFreq)
        t2_hbox015.addWidget(self.label_Ed)
        t2_hbox015.addWidget(self.textbox_EdFreq)
    

        t2_gbox1.addLayout(t2_hbox015)




        t2_hbox016 = QHBoxLayout()
        t2_hbox016.addWidget(self.label_Span)
        t2_hbox016.addWidget(self.spinbox_SpanFreq)
        t2_hbox016.addWidget(self.label_Center)
        t2_hbox016.addWidget(self.spinbox_CenterFreq)
       
        t2_gbox1.addLayout(t2_hbox016)




        t2_hbox01 = QHBoxLayout()
        t2_hbox01.addWidget(self.button_StSweep)
        t2_hbox01.addWidget(self.button_saveSweep)
        t2_hbox01.addWidget(self.button_savePlot)
       
       
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


  
  
  
  
  
  
  
      #
    # Stream tab
    #
  
  
  
  
        t5_gbox0 = QVBoxLayout()

        t5_hbox00 = QHBoxLayout()


        t5_hbox00.addWidget(label_lut_strfilename)
        t5_hbox00.addWidget(self.textbox_streamfilename)

        t5_hbox00.addWidget(label_streamsec)
        t5_hbox00.addWidget(self.textbox_streamsec)



        t5_gbox0.addLayout(t5_hbox00)




    



        t5_hbox4 = QHBoxLayout()

        

       




        t5_gbox0.addLayout(t5_hbox4)


        t5_hbox3 = QHBoxLayout()
        t5_hbox3.addWidget(self.button_stream_run)
        t5_hbox3.addWidget(self.button_stream_stop)
       

        t5_gbox0.addLayout(t5_hbox3)

    
    
    
  
  
  
  
  
    #
    # ResData
    #
    #
    
    
    
    
        t3_gbox1 = QVBoxLayout()

        t3_hbox10 = QHBoxLayout()
        t3_hbox10.addWidget(self.label_pwrsw_atTotal)
        t3_hbox10.addWidget(self.spinbox_pwrsw_atTotal)
        t3_hbox10.addWidget(self.label_pwrsw_atinst)
        t3_hbox10.addWidget(self.spinbox_pwrsw_atinst)
        t3_hbox10.addWidget(self.label_pwrsw_atsweeps)
        t3_hbox10.addWidget(self.spinbox_pwrsw_atsweeps)
        t3_hbox10.addWidget(self.label_pwrsw_span)
        t3_hbox10.addWidget(self.spinbox_pwrsw_span)
        
        t3_hbox10.addWidget(self.label_nswfreqs)
        t3_hbox10.addWidget(self.spinbox_nswfreqs)
        
        




        t3_hbox10.addStretch(1)
        t3_gbox1.addLayout(t3_hbox10)

        t3_hbox11 = QHBoxLayout()
        t3_hbox11.addWidget(self.label_pwrsw_atst)
        t3_hbox11.addWidget(self.spinbox_pwrsw_atst)
        t3_hbox11.addWidget(self.label_pwrsw_atend)
        t3_hbox11.addWidget(self.spinbox_pwrsw_atend)
        t3_hbox11.addWidget(self.label_pwrsw_atstep)
        t3_hbox11.addWidget(self.spinbox_pwrsw_atstep)
        t3_hbox11.addWidget(self.label_pwrsw_numNoise)
        t3_hbox11.addWidget(self.spinbox_numNoise)
        
        
 
        
        
        
        t3_gbox1.addLayout(t3_hbox11)


        t3_hbox12 = QHBoxLayout()
        t3_hbox12.addWidget(self.button_checkall)
        t3_hbox12.addWidget(self.button_uncheckall)
        t3_hbox12.addWidget(self.button_hdfshell)
        t3_hbox12.addWidget(self.button_runbyhour)
        t3_hbox12.addWidget(self.button_stoprepeat)
        t3_hbox12.addWidget(self.label_repeatmin)
        t3_hbox12.addWidget(self.textbox_repeatmin)
        t3_hbox12.addWidget(self.label_noisesec)
        t3_hbox12.addWidget(self.textbox_noisesec)

    


    
        t3_hbox12.addStretch(1)
        t3_gbox1.addLayout(t3_hbox12)
  
  
        #hbox22.addWidget(self.textbox_longsnapSteps)
        #hbox22.addWidget(label_longsnapSteps)
       
 
        t3_hbox13 = QHBoxLayout()



    
        t3_hbox13.addWidget(self.check_multiprocess)
        t3_hbox13.addWidget(self.check_powersweep)

        t3_hbox13.addWidget(self.check_runFits)
        t3_hbox13.addWidget(self.check_getnoise)

        t3_hbox13.addWidget(self.check_runIQvelocity)

        t3_hbox13.addWidget(self.button_runIt)
        t3_hbox13.addWidget(self.button_stopIt)
        t3_hbox13.addWidget(self.label_threadrun)





        t3_gbox1.addLayout(t3_hbox13)

        t3_hbox14 = QHBoxLayout()
        #t3_hbox14.addWidget(self.textbox_HDF5filepath)
        #t3_hbox14.addWidget(self.textbox_HDF5ResName)

        t3_hbox14.addWidget(self.button_HDF5ResRead)
        t3_hbox14.addWidget(self.button_HDF5ResReadL)
        t3_hbox14.addWidget(self.button_HDF5ResSave)

        t3_hbox14.addWidget(self.button_resPlots)
        t3_hbox14.addWidget(self.button_clrTrace)
        t3_hbox14.addWidget(self.button_clrNoise)
        t3_hbox14.addWidget(self.button_medFilter)
        t3_hbox14.addWidget(self.button_lowpassFilter)

    


        t3_gbox1.addLayout(t3_hbox14)

        t3_gbox2 = QVBoxLayout()

        t3_gbox2.addWidget(self.list_reslist2)


        t3_hbox = QHBoxLayout()
        t3_hbox.addLayout(t3_gbox1)
        t3_hbox.addLayout(t3_gbox2)
    
   
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


        tab3=QWidget()
        tab3_layout=QVBoxLayout(tab3)
        tab3_layout.addLayout(t3_hbox)



        tab4=QWidget()
        tab4_layout=QVBoxLayout(tab4)
        tab4_layout.addLayout(gbox_sync)
       

        tab5=QWidget()
        tab5_layout=QVBoxLayout(tab5)
        tab5_layout.addLayout(t5_gbox0)


        tab_widget.addTab(tab1,"Settings")
        tab_widget.addTab(tab2,"Sweep")
        tab_widget.addTab(tab4,"FlxRamp")
        tab_widget.addTab(tab5,"Stream")

        tab_widget.addTab(tab3,"ResData")
    
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(tab_widget)
    
    
    #vbox.addLayout(hbox)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
  
    def create_status_bar(self):
        self.status_text = QLabel("Awaiting orders.")
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
   
   

  
   

class QNetThread (QThread):
    def __init__(self, which_function):
        QThread.__init__(self)
        self.which_function = which_function
        
    
    
    def run(self):
    
        global is_thread_running
    
     
        global fit_put_q_count
        global fit_get_q_count
        is_thread_running=is_thread_running+1
    
        sweepCallback()
    
    
        

   
        if (self.which_function&1) >0:
        
            print "Start Sweeping on Thread==============" 
            #runs on this thread
            form.is_saveres=True
            form.powersweep2()
            #power sweep is now done.

        if (self.which_function&2)>0:
        
            print "Starting Fits Thread =================" 
            #run on this thread
                #form.runFits2()
            #run multiproess
            form.runFits4()

               #here all the mkids are queued to fit quieue
            # now we wait until all the mkids return ....


            stat=getMkidFitQueue()

            while(stat!=2):
                if stat==1:
                    form.signalPlot()


                stat=getMkidFitQueue()

                #other thrad can set to 0 to terminate this thread
                if (is_thread_running==0):
                    stat=2


                if (stat!=2):
                    time.sleep(5)    



        if (self.which_function&4) >0:
            print "thread iq vel"
            form.IQvelocity()


        if (self.which_function&8) >0:

            print "starting NOISE on thread=================="
            form.runNoise()


        if (is_thread_running>0):
            is_thread_running=is_thread_running-1


        form.hdfResSave()

        sweepCallback()
        #set these to 0 in case we did a stop process... it makes sure it keeps working...
        fit_put_q_count=0;
        fit_get_q_count=0;

        form.is_saveres=False
        print "Exiting Thread"    



class QRunFit (QRunnable):
    def __init__(self, res):
        QRunnable.__init__(self)
        self.resonator = res
        
    
    
    def run(self):
        myfit=fitters()
        myfit.addRes(self.resonator)
        myfit.fitResonators()





class QRunPyThread (QRunnable):
    def __init__(self, pystring_):
        QRunnable.__init__(self)
        self.pystring = pystring_
        
    
    
    def run(self):
        exec(self.pystring)

   

global app
global form


def main():
    global app
    global form
    print 'hello'
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

def sweepCallback():
    global form
    print "natAnalGui::sweepCallback"
    try:
        form.signalPlot()    
        if form.is_saveres:
            randname='powersweep_backup.h5'
        if rand()>0.9:
            mkidSaveData(randname)
    except:
        pass
    

try:
    sim.close()
except:
    pass
    

#sim=sim928()
#sim.open()
#sim.connport(8)
#sim.getId()


