'''
execfile('roachEpics.py')


'''
import epics
import os
import subprocess
import time

import threading

import Queue

execfile('epicsParse.py')
execfile('epicsDb2Docs.py')

epics_iocbin = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/bin/linux-x86_64/myexample'
epics_stdir = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/iocBoot/iocmyexample'
epics_iocdb = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/db'
epics_ioctop = '/home/beams0/TMADDEN/EPICS/maddogsoftioc'

iocname = 'DP:roach1:'


global db

def stopEpics():
    global is_epics_running
    global is_daemon_running
    
    is_epics_running = False
    
    epics.ca.finalize_libca()
    is_daemon_running = False
    
    
    

epics_queue_toroach=None
epics_queue_fromroach = None

def makeQueues():
   global epics_queue_toroach
   global epics_queue_fromroach
   
   epics_queue_toroach=Queue.Queue()
   epics_queue_fromroach=Queue.Queue()
   


def startEpics():
    global db
    global epics_queue_toroach
    global epics_queue_fromroach
    global is_epics_running
    
    
    makeQueues()
    
    db = createDatabase()
    
    writeDb(db, epics_iocdb + '/mydatabase.db')
    createStCmd()
    startIOC()
    
    addCallbacks(db)
    is_epics_running=True
    startEpicsDaemon()




def startIOC():

    os.system('xterm -e ' + epics_iocbin + ' ' + epics_stdir +'/myst.cmd &')


epics_function_map = {}


def createDatabase():
    global epics_function_map
    
    epics_function_map = {}
    
    
    db = []
   
         
    db.append(
        makeSoftLongin(iocname+"IsRunning"))
   
    db.append(
        makeSoftLongout(iocname+"Refresh"))
        
    epics_function_map[iocname+"Refresh"] = (epicsMessage,"form.signalPlot")  
   
       
    db.append(
        makeSoftLongout(iocname+"Connect"))
        
    epics_function_map[iocname+"Connect"] = (epicsMessage,"form.openClient")  
    
    db.append(
        makeSoftLongout(iocname+"Reconnect"))
        
    epics_function_map[iocname+"Reconnect"] = (epicsMessage,"form.reOpenClient")  
  

    db.append(
        makeSoftLongout(iocname+"Disconnect"))
        
    epics_function_map[iocname+"Disconnect"] = (epicsMessage,"form.closeClient")  
    
  
     
    db.append(
        makeSoftLongout(iocname+"BBLoop"))        
    epics_function_map[iocname+"BBLoop"] = (epicsMessage,"form.checkbox_BBLoopback")  
    
    db.append(
        makeSoftLongout(iocname+"RFLoop"))        
    epics_function_map[iocname+"RFLoop"] = (epicsMessage,"form.checkbox_RFLoopback")  

    db.append(
        makeSoftLongout(iocname+"FPGALoop"))        
    epics_function_map[iocname+"FPGALoop"] = (epicsMessage,"form.checkbox_FPGALoopback")  

    db.append(
        makeSoftLongout(iocname+"ExtLO"))        
    epics_function_map[iocname+"ExtLO"] = (epicsMessage,"form.checkbox_extClk")  
  
    
  
    db.append(
        makeSoftAo(iocname+"AttenU6"))       
    epics_function_map[iocname+"AttenU6"] = (epicsMessage,"form.spinbox_AttOut0") 
    
    db.append(
        makeSoftAo(iocname+"AttenU7"))       
    epics_function_map[iocname+"AttenU7"] = (epicsMessage,"form.spinbox_AttOut1") 
    
    db.append(
        makeSoftAo(iocname+"AttenU28"))       
    epics_function_map[iocname+"AttenU28"] = (epicsMessage,"form.spinbox_AttIn0") 
   

    db.append(
        makeSoftLongout(iocname+"StartSweep"))
    epics_function_map[iocname+"StartSweep"] = (epicsMessage,"form.startSweep")  

    db.append(
        makeSoftLongout(iocname+"StopRun"))
    epics_function_map[iocname+"StopRun"] = (epicsMessage,"form.runStop")  


    db.append(
        makeSoftAo(iocname+"Span"))       
    epics_function_map[iocname+"Span"] = (epicsMessage,"form.spinbox_SpanFreq") 
      
      

    db.append(
        makeSoftAo(iocname+"Center"))
    epics_function_map[iocname+"Center"] = (epicsMessage,'form.spinbox_CenterFreq') 
      
    db.append(
        makeSoftAo(iocname+"NumSweepPoints"))
    epics_function_map[iocname+"NumSweepPoints"] = (epicsMessage,'form.spinbox_numSwPts') 

    db.append(
        makeSoftLongout(iocname+"ExtractResonators"))
    epics_function_map[iocname+"ExtractResonators"] = (epicsMessage,"form.extractRes")  

    db.append(
        makeSoftLongout(iocname+"ClearResList"))
    epics_function_map[iocname+"ClearResList"] = (epicsMessage,"form.clearResList")  


    db.append(
        makeSoftLongout(iocname+"SaveSweepPlot"))
    epics_function_map[iocname+"SaveSweepPlot"] = (epicsMessage,"form.savePlot2")  
    
    
    db.append(
        makeSoftLongout(iocname+"LoadSweepPlot"))
    epics_function_map[iocname+"LoadSweepPlot"] = (epicsMessage,"form.loadSweepPlot2")  
    
    db.append(
        makeCharWaveform(iocname+"ResListText",nelm=2000))
    
    db.append(
        makeCharWaveform(iocname+"SweepFilename",nelm=256))
    epics_function_map[iocname+"SweepFilename"] = (epicsMessage,"form.temp_sweep_fname")  

    #db.append(
    #    makeSoftLongout(iocname+"RunChecked"))
    #epics_function_map[iocname+"RunChecked"] = (epicsButton,form.runIt)  

    #db.append(
    #    makeSoftMBBO(iocname+"PowerSweep",{'unchecked':0 , 'checked':1 }))
    #epics_function_map[iocname+"PowerSweep"] = (epicsCheck,form.check_powersweep)  

    #db.append(
    #    makeSoftMBBO(iocname+"IQVelocity",{'unchecked':0 , 'checked':1 }))
    #epics_function_map[iocname+"IQVelocity"] = (epicsCheck,form.check_runIQvelocity)  


    #db.append(
    #    makeSoftMBBO(iocname+"TesOn",{'unchecked':0 , 'checked':1 }))
    #epics_function_map[iocname+"TesOn"] = (epicsCheck,form.checkbox_teson)  


    #db.append(
    #    makeSoftMBBO(iocname+"GetResonatorNoise",{'unchecked':0 , 'checked':1 }))
    #epics_function_map[iocname+"GetResonatorNoise"] = (epicsCheck,form.check_getnoise)  


    db.append(
        makeSoftLongout(iocname+"CalIQCircles"))
    epics_function_map[iocname+"CalIQCircles"] = (epicsMessage,"form.calibrateIQCircles")              
 
 
 
                
    db.append(
        makeSoftLongout(iocname+"LoadIQCirCal"))
    epics_function_map[iocname+"LoadIQCirCal"] = (epicsMessage,"form.loadIQCircleCal2")              

    db.append(
        makeSoftLongout(iocname+"SaveIQCirCal"))
    epics_function_map[iocname+"SaveIQCirCal"] = (epicsMessage,"form.saveIQCircleCal2")              

    db.append(
        makeCharWaveform(iocname + "IQCirCalFilename"))

    epics_function_map[iocname+"IQCirCalFilename"] = (epicsMessage,"form.temp_iqcircalfname")  



 
    db.append(
        makeSoftMBBO(
            iocname+"ReturnData",
                {'Return Raw Data': 0,
                'Return Raw + FRD':1,
                'Return FRD only':2,
                'Return FRD + IQCentered': 3}))           
    epics_function_map[iocname+"ReturnData"] = (epicsMessage,"form.combobox_str_frd")              

    db.append(
        makeSoftMBBO(
            iocname+"IsSyncRamp",
                {'Open Loop (no FRD)': 0,
                'Closed Loop (FRD)':1}))           
    epics_function_map[iocname+"IsSyncRamp"] = (epicsMessage,"form.combobox_syncsource")              



    db.append(
        makeSoftAo(iocname+"FluxRampPeriods"))        
    epics_function_map[iocname+"FluxRampPeriods"] = (epicsMessage,"form.textbox_flxRmpPrd")  


    db.append(
        makeCharWaveform(iocname + "IVVoltSpecs"))
    epics_function_map[iocname+"IVVoltSpecs"] = (epicsMessage,"form.temp_ivvoltspecs")  


    db.append(
        makeSoftLongout(iocname+"StartStream"))        
    epics_function_map[iocname+"StartStream"] = (epicsMessage,"form.streamRun")  

    db.append(
        makeSoftLongout(iocname+"StartTesIVSweep"))
    epics_function_map[iocname+"StartTesIVSweep"] = (epicsMessage,"form.sweepTesIV")  
     
  
    db.append(
        makeCharWaveform(iocname + "IVFilename"))

    epics_function_map[iocname+"IVFilename"] = (epicsMessage,"form.temp_ivfilename") 
    
                 
    db.append(
        makeSoftLongout(iocname+"TesOn"))
    epics_function_map[iocname+"TesOn"] = (epicsMessage,"form.checkbox_teson")              
    


    db.append(
        makeSoftAo(iocname+"NoiseSeconds"))        
    epics_function_map[iocname+"NoiseSeconds"] = (epicsMessage,"form.noisetemp_timesec")  

  
    db.append(
        makeCharWaveform(iocname + "NoiseStreamFilename"))

    epics_function_map[iocname+"NoiseStreamFilename"] = (epicsMessage,"form.noisetemp_fname") 
            

    db.append(
        makeCharWaveform(iocname + "RoachStatMessage"))
        
        

    db.append(
        makeFloatWaveform(iocname + "FreqSweepMag"))
 
    db.append(
        makeFloatWaveform(iocname + "FreqSweepPhase"))
 
    db.append(
        makeFloatWaveform(iocname + "FreqSweepI"))

    db.append(
        makeFloatWaveform(iocname + "FreqSweepQ"))

    db.append(
        makeFloatWaveform(iocname + "SweepFreqs"))

    db.append(
        makeFloatWaveform(iocname + "TimeStamps",length = 10000))

    db.append(
         makeFloatWaveform(iocname + "RawNoiseMag",length = 10000))

    db.append(
         makeFloatWaveform(iocname + "RawNoisePhase",length = 10000))

    db.append(
         makeFloatWaveform(iocname + "FluxRampPhase",length = 10000))

    db.append(
        makeSoftLongin(iocname+"NumSweepFreqs"))




    return(db)

epics_stcmd = '''
cd "${TOP}"
dbLoadDatabase "dbd/myexample.dbd"
myexample_registerRecordDeviceDriver pdbbase
dbLoadRecords "db/mydatabase.db", "user=tmaddenHost"
cd "${STDIR}"
iocInit
''' 


def createStCmd():
    global epics_stcmd
    epics_stcmd = epics_stcmd.replace('${TOP}',epics_ioctop)
    epics_stcmd = epics_stcmd.replace('${STDIR}',epics_stdir)

    fp=open(epics_stdir+'/myst.cmd','w')
    fp.write(epics_stcmd)
    fp.close()
     
        

def epicsMessage(pvname=None, value=None,char_value = None):
    print '######Message##########'
    message = epics_function_map[pvname][1]
   
    epics_queue_toroach.put(
        {'message':message, 
        'value':value, 
        'char_value':char_value, 
        'pvname':pvname}
        )



def onChanges(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed!! ', pvname, char_value, time.ctime()
    runfunction = epics_function_map[pvname][0]
    
    runfunction(pvname, value, char_value)


def addCallbacks(db):

    clientpvs = []
    
    #montypes = ['longout', 'ao', 'mbbo']
    for pv in db:
        if pv.getPvName() in epics_function_map.keys():
            name = pv.getPvName()
            clientpvs.append( epics.PV(name,auto_monitor=True))
            print 'Add Monitor to %s'%name
    


    for pv in clientpvs:   
        pv.add_callback(onChanges)
    
  

#####################3
# set up python dameon to update pvs every sec. read lonout pv, inc by 1, then write back.
is_daemon_running = False
deamon_count = 0

def daemon():
    global deamon_count
    deamon_count=0
    while is_daemon_running:
        time.sleep(0.5)
        deamon_count=deamon_count+1
        try:
            #runs until except thrown by epics_queue_fromroach.get_nowait, when no messages left
            while(True):
                roach_message = epics_queue_fromroach.get_nowait()
                sweeppv_len =2048.0
                print 'epics deamon got signal'
                for kk in roach_message.keys():
                    print kk
                    if kk=='status_string':
                        print 'epics daemon got stat string'
                        epics.caput(iocname+'RoachStatMessage',str(roach_message[kk]))
                    elif kk=='FreqSweepMag': 
                        dat =  roach_message[kk]  
                        datinterp =  numpy.interp(
                            arange(0,len(dat),float(len(dat))/sweeppv_len),
                            arange(len(dat)),
                            dat)          
                        epics.caput(iocname+'FreqSweepMag',datinterp)
                    elif kk=='FreqSweepPhase':
                        dat =  roach_message[kk]  
                        datinterp =  numpy.interp(
                            arange(0,len(dat),float(len(dat))/sweeppv_len),
                            arange(len(dat)),
                            dat)          
                        epics.caput(iocname+'FreqSweepPhase',datinterp)
                    elif kk=='FreqSweepI':
                        dat =  roach_message[kk]  
                        datinterp =  numpy.interp(
                            arange(0,len(dat),float(len(dat))/sweeppv_len),
                            arange(len(dat)),
                            dat)                             
                        epics.caput(iocname+'FreqSweepI',datinterp)
                    elif kk=='FreqSweepQ':
                        dat =  roach_message[kk]  
                        datinterp =  numpy.interp(
                            arange(0,len(dat),float(len(dat))/sweeppv_len),
                            arange(len(dat)),
                            dat)                             
                        epics.caput(iocname+'FreqSweepQ',datinterp)
                    elif kk=='TimeStamps':
                        epics.caput(iocname+'TimeStamps',roach_message[kk])
                    elif kk=='SweepFreqs':                    
                        dat =  roach_message[kk]  
                        datinterp =  numpy.interp(
                            arange(0,len(dat),float(len(dat))/sweeppv_len),
                            arange(len(dat)),
                            dat)                           
                        epics.caput(iocname+'SweepFreqs',datinterp)                                       
                        epics.caput(iocname+'SweepFreqs.HOPR',max(dat))
                        epics.caput(iocname+'SweepFreqs.LOPR',min(dat))
                        numsweepfreqs = len(dat)
                        epics.caput(iocname+'NumSweepFreqs',numsweepfreqs)
                    elif kk=='RawNoiseMag':
                        epics.caput(iocname+'RawNoiseMag',roach_message[kk])
                    elif kk=='RawNoisePhase':
                        epics.caput(iocname+'RawNoisePhase',roach_message[kk])
                    elif kk=='FluxRampPhase':
                        epics.caput(iocname+'FluxRampPhase',roach_message[kk])

                    elif kk=='ResListText':
                        strx = roach_message[kk]
                        epics.caput(iocname+'ResListText',strx)

        except:
            pass


 
  
 
 

def startEpicsDaemon():
    global is_daemon_running
    is_daemon_running = True
    d = threading.Thread(name='daemon', target=daemon)
    d.setDaemon(True)
    d.start()
   
   
print "Loaded roachEpics.py"