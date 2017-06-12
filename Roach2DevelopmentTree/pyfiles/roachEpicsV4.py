import time
from pvaccess import INT, PvaServer, PvObject,Channel,STRING,DOUBLE,PvInt
import Queue


epics_queue_toroach=None
epics_queue_fromroach = None

def makeQueues():
   global epics_queue_toroach
   global epics_queue_fromroach
   
   epics_queue_toroach=Queue.Queue()
   epics_queue_fromroach=Queue.Queue()
   
def startPvaServer():

    roachsets =PvObject( {
        'atU6':INT,
        'atU7':INT ,
        'atU28':INT ,
        'bbloop':INT ,
        'rfloop':INT ,
        'extLO':INT ,
        'centfreq':DOUBLE ,
        'spanfreq':DOUBLE ,
        'isconnected':INT,
        'status':STRING
        })

    roachconn=PvInt(0)
    roachdisconn=PvInt(0)

    roachsweep=PvInt(0)
    
    pvaServer = PvaServer('DP:roach1:settings', roachsets)
    pvaServer.addRecord('DP:roach1:connect',roachconn)
    pvaServer.addRecord('DP:roach1:disconnect',roachdisconn)
    pvaServer.addRecord('DP:roach1:sweep',roachsweep)



#pv2 = PvObject({'x': INT, 'y' : INT})
#pvaServer.addRecord('p2',pv2)
#r=PvObject( {'x':INT, 'array':[INT]})
#pvaServer.addRecord('r',r)
#r['array']=range(1000)

def roach_sweep_callback(x):
    print 'sweep'
    epics_queue_toroach.put({'sweep':x.getInt()})

def roach_conn_callback(x):
    print 'conn'
    epics_queue_toroach.put({'conn':x.getInt()})

def roach_disconn_callback(x):
    print 'disconn'
    epics_queue_toroach.put({'disconn':x.getInt()})

def roachsetscallback(rsets):
    print 'settings' 
    #print type(rsets)
    #print rsets.toDict()
    epics_queue_toroach.put({'settings':rsets.toDict()})

makeQueues()
startPvaServer()

roachsetsmon = Channel('DP:roach1:settings')
roachsetsmon.monitor(roachsetscallback,'')

c2= Channel('DP:roach1:sweep')
c2.monitor(roach_sweep_callback,'')

c3= Channel('DP:roach1:disconnect')
c3.monitor(roach_disconn_callback,'')

c4= Channel('DP:roach1:connect')
c4.monitor(roach_conn_callback,'')



xxx="""
do this:

for k in range(10):  print epics_queue_toroach.get()

"""


print xxx




