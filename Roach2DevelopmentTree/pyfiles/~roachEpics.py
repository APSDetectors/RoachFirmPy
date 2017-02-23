'''
execfile('roachEpics.py')


'''
import epics
import os
import subprocess
import time

import threading

execfile('epicsParse.py')
execfile('epicsDb2Docs.py')

epics_iocbin = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/bin/linux-x86_64/myexample'
epics_stdir = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/iocBoot/iocmyexample'
epics_iocdb = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/db'
epics_ioctop = '/home/beams0/TMADDEN/EPICS/maddogsoftioc'



global db

def stopEpics():
    epics.ca.finalize_libca()

def startEpics():
    global db
    
    db = createDatabase()
    
    writeDb(db, epics_iocdb + '/mydatabase.db')
    createStCmd()
    startIOC()
    
    addCallbacks(db)




def startIOC():

    os.system('xterm -e ' + epics_iocbin + ' ' + epics_stdir +'/myst.cmd &')


epics_function_map = {}


def createDatabase():
    global epics_function_map
    
    epics_function_map = {}
    
    iocname = 'ROACH:'
    db = []
       
    db.append(
        makeSoftLongout(iocname+"Connect"))
        
    epics_function_map[iocname+"Connect"] = (epicsButton,form.openClient)  
    
    db.append(
        makeSoftLongout(iocname+"Disconnect"))
        
    epics_function_map[iocname+"Disconnect"] = (epicsButton,form.closeClient)  
    
  
  
    db.append(
        makeSoftLongout(iocname+"StartSweep"))
    epics_function_map[iocname+"StartSweep"] = (epicsButton,form.startSweep)  

    db.append(
        makeSoftLongout(iocname+"StopRun"))
    epics_function_map[iocname+"StopRun"] = (epicsButton,form.runStop)  


    db.append(
        makeSoftAo(iocname+"Span"))       
    epics_function_map[iocname+"Span"] = (numberSpinBox,form.spinbox_SpanFreq) 
      
      

    db.append(
        makeSoftAo(iocname+"Center"))
    epics_function_map[iocname+"Center"] = (numberSpinBox,form.spinbox_CenterFreq) 
      
    db.append(
        makeSoftLongout(iocname+"RunChecked"))
    epics_function_map[iocname+"RunChecked"] = (epicsButton,form.runIt)  

    db.append(
        makeSoftMBBO(iocname+"PowerSweep",{'unchecked':0 , 'checked':1 }))
    epics_function_map[iocname+"PowerSweep"] = (epicsCheck,form.check_powersweep)  

    db.append(
        makeSoftMBBO(iocname+"IQVelocity",{'unchecked':0 , 'checked':1 }))
    epics_function_map[iocname+"IQVelocity"] = (epicsCheck,form.check_runIQvelocity)  


    db.append(
        makeSoftMBBO(iocname+"TesOn",{'unchecked':0 , 'checked':1 }))
    epics_function_map[iocname+"TesOn"] = (epicsCheck,form.checkbox_teson)  


    db.append(
        makeSoftMBBO(iocname+"GetResonatorNoise",{'unchecked':0 , 'checked':1 }))
    epics_function_map[iocname+"GetResonatorNoise"] = (epicsCheck,form.check_getnoise)  


    db.append(
        makeSoftLongout(iocname+"CalIQCircles"))
    epics_function_map[iocname+"CalIQCircles"] = (epicsButton,form.calibrateIQCircles)              
                
    db.append(
        makeSoftLongout(iocname+"StartStream"))        
    epics_function_map[iocname+"StartStream"] = (epicsButton,form.streamRun)  

    db.append(
        makeSoftLongout(iocname+"StartTesIVSweep"))
    epics_function_map[iocname+"StartTesIVSweep"] = (epicsButton,form.sweepTesIV)  
     
     
    db.append(
        makeCharWaveform(iocname + "faRa"))
          
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
     
        

def epicsButton(pvname=None, value=None,char_value = None):
    print '######Button##########'
    runfunction = epics_function_map[pvname][1]
    if value==1:
        runfunction()
    
    #print 'PV Changed!! ', pvname, char_value, time.ctime()
    
def epicsCheck(pvname=None, value=None, char_value=None):   
    widget = epics_function_map[pvname][1]
    if value==0:
        widget.setCheckState(Qt.Unchecked)
    else:
        widget.setCheckState(Qt.Checked)
        
     #print 'PV Changed!! ', pvname, char_value, time.ctime()  
    
def numberTextField(pvname=None, value=None, char_value=None):  
    widget = epics_function_map[pvname][1]
    widget.setText('%f'%(value))
    



def numberSpinBox(pvname=None, value=None, char_value=None):  
    widget = epics_function_map[pvname][1]
    widget.setValue(value)
 
def onChanges(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed!! ', pvname, char_value, time.ctime()
    runfunction = epics_function_map[pvname][0]
    
    runfunction(pvname, value, char_value)


def addCallbacks(db):

    clientpvs = []
    
    montypes = ['longout', 'ao', 'mbbo']
    for pv in db:
        if pv.getRecType() in montypes:
            name = pv.getPvName()
            clientpvs.append( epics.PV(name,auto_monitor=True))
            print 'Add Monitor to %s'%name
    


    for pv in clientpvs:   
        pv.add_callback(onChanges)
    
  
   
