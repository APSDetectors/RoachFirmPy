
import epics
import os
import subprocess
import time

import threading

execfile('epicsParse.py')
execfile('epicsDb2Docs.py')



'''

You must have base. 
Make an example soft IOC app as below:

setenv EPICS_BASE /home/beams0/TMADDEN/EPICS/base-3.14.12.5
setenv PATH /home/beams0/TMADDEN/EPICS/base-3.14.12.5/bin/linux-x86_64:$PATH
which makeBaseApp.pl

mkdir maddogsoftioc
cd maddogsoftioc/
makeBaseApp.pl -t example myexample
makeBaseApp.pl -i -t example myexample

make

cd maddogsoftioc/
cd iocBoot/
cd iocmyexample/
ls
cat README
../../bin/linux-x86_64/myexample st.cmd

This py script will start this app with python generated DB.
Python will monitor all the PVs and respond to them as they change.
Also, python can run a repeating script to update PVs as needed.


'''


#####################
#  define the pvs in the database
#



#make a few PVs, 

iocname = 'myioc:'
db = []
db.append(
    makeSoftMBBO(
        iocname+'pv1',
        {'idle':0, 'running':1}) )
        
db.append(makeSoftAo(iocname+'pv2'))
db.append(makeSoftAo(iocname+'pv3'))
db.append(makeSoftAo(iocname+'pv4'))
db.append(makeSoftAo(iocname+'pv5'))


db.append(makeSoftLongout(iocname+'pv6'))
db.append(makeSoftLongout(iocname+'pv7'))
db.append(makeSoftLongout(iocname+'pv8'))
db.append(makeSoftLongout(iocname+'pv9'))
db.append(makeSoftLongout(iocname+'pv10'))

#db.append(makeCounterPV(iocname+'counter'))

#print all pvs
printDb(db)



#################3333
# define where softIOC resides, it is basic epics example app.


iocbin = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/bin/linux-x86_64/myexample'
stdir = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/iocBoot/iocmyexample'
iocdb = '/home/beams0/TMADDEN/EPICS/maddogsoftioc/db'
ioctop = '/home/beams0/TMADDEN/EPICS/maddogsoftioc'



##############
#write the database


writeDb(db, iocdb + '/mydatabase.db')




###########################################
# define the startup file, 
##############################

stcmd = '''
cd "${TOP}"
dbLoadDatabase "dbd/myexample.dbd"
myexample_registerRecordDeviceDriver pdbbase
dbLoadRecords "db/mydatabase.db", "user=tmaddenHost"
cd "${STDIR}"
iocInit
'''

stcmd = stcmd.replace('${TOP}',ioctop)
stcmd = stcmd.replace('${STDIR}',stdir)

fp=open(stdir+'/myst.cmd','w')
fp.write(stcmd)
fp.close()

#########################################
# Start the softuic with our PVs
#################################


os.system('xterm -e ' + iocbin + ' ' + stdir +'/myst.cmd &')

gui=screenMaker()

#generate board level pvs	
gui.xw=[300,100,100]
	
gui.width=100
gui.xw=[50,50,200,50,50]
#scr = gui.dbToScreen1(db,'My Python IOC',False,False,32,None)
#scr.writeXML('myscreen.opi')

scr = gui.dbToScreen2(db,'myioc',['']*10,['']*2,None)

scr.writeXML('myscreen.opi')

#open CSS Boy to run this screen.




###############################3
#connect Python to the IOC pvs
##############################

clientpvs = []


def onChanges(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed!! ', pvname, char_value, time.ctime()






def epicsButton(pvname=None, value=None, char_value=None, **kw):
    pass
    #print 'PV Changed!! ', pvname, char_value, time.ctime()
    
def epicsCheckbox(pvname=None, value=None, char_value=None, **kw):
    pass
    #print 'PV Changed!! ', pvname, char_value, time.ctime()  
    
def numberField(pvname=None, value=None, char_value=None, **kw):  
    pass
    
    
for pv in db:
    name = pv.getPvName()
    clientpvs.append( epics.PV(name,auto_monitor=True))
    


for pv in clientpvs:   
    pv.add_callback(onChanges)
    
    

#####################3
# set up python dameon to update pvs every sec. read lonout pv, inc by 1, then write back.
is_daemon_running = True

def daemon():
    while is_daemon_running:
        time.sleep(1.0)
        v = clientpvs[7].value
        v = v+1
        clientpvs[7].value= v


d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)
d.start()

time.sleep(10)
#after 10s stop the daemon
is_daemon_running=False



