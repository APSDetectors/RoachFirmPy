'''

execfile('dataCapture.py')

capture = dataCapture()


capture.saveEvents('/localc/asdf')

capture.clearEvents()

capture.setCircleSpecs({192:(1.2,2.3),193:(1.4,1.3)})

capture.shut()


'''


import os
import subprocess
from socket import *


try:
    ROACH_DIR =  os.environ['ROACH']
except:
    print 'Please set env var ROACH to your roach install dir'
    print 'Using /localc/roach'
    ROACH_DIR='/localc/roach'


ten_G_ipaddr = '192.168.1.102'
ten_G_device = 'enp5s0f0'



class dataCapture:

    def __init__(self,                    
        path = ROACH_DIR+'/Roach2DevelopmentTree/QT/build-testEnet-Desktop-Debug/'):
     
        self.devnull = open(os.devnull, 'wb')
        cmd = path + 'testEnet'


        os.system('ifconfig %s %s up'%(ten_G_device,ten_G_ipaddr))
      #  self.streamproc = subprocess.Popen(
      #      [cmd  ], 
      #       stdin=subprocess.PIPE,stdout=self.devnull)
        
        self.streamproc = subprocess.Popen(
            [cmd  ], 
             stdin=subprocess.PIPE,stdout=subprocess.PIPE)

        self.sendcmd = self.streamproc.stdin
        self.getcmd = self.streamproc.stdout

        
    def capture(self,iss=True):
        if iss:
            self.sendcmd.write('roachstream w on_checkBox_streamUDP_clicked 1 bool 1\n')
            self.sendcmd.flush()
        else:
            self.sendcmd.write('roachstream w on_checkBox_streamUDP_clicked 1 bool 0\n')  
            self.sendcmd.flush()
            #send a packet to the qt program to assure the socket stops blocking on rcv data and closes.
            qt_addr = ("192.168.1.102",50000)
            UDPSock = socket(AF_INET,SOCK_DGRAM)
            UDPSock.sendto( '\xff'*2048,qt_addr)
            UDPSock.close()
            
    def clearEvents(self):
        self.sendcmd.write('roachstream w on_pushButton_clearEvents_clicked 0\n')  
        self.sendcmd.flush()
      
    def dumpPacketFifo(self):
        self.sendcmd.write('roachstream w on_pushButton_dumpPacketFifo_clicked 0\n')  
        self.sendcmd.flush()
        
        
    def getCmd(self):
        return(self.getcmd.readline()) 
        
    def saveEvents(self,dsname):
    
        self.sendcmd.write('roachstream saver_a setFileName 1 QString %s_A.h5 \n'%dsname)  
        self.sendcmd.flush()
        self.sendcmd.write('roachstream saver_b setFileName 1 QString %s_B.h5 \n'%dsname)  
        self.sendcmd.flush()
        
        self.sendcmd.write('roachstream parser_a queueEvents 0 \n')
        self.sendcmd.flush()
        self.sendcmd.write('roachstream parser_b queueEvents 0 \n')
        self.sendcmd.flush()
        
        #!! need a call back or someting here from the cpp program
        time.sleep(1.0)        
        
        self.sendcmd.write('roachstream saver_a doSaveAll 0 \n')  
        self.sendcmd.flush()
        self.sendcmd.write('roachstream saver_b doSaveAll 0 \n')  
        self.sendcmd.flush()
        
        print self.getCmd()
        print self.getCmd()
  
    def setStream2Disk(self,is_stream, dsname):
        #if starting stream, then set file name
        if is_stream:
            self.sendcmd.write('roachstream saver_a setFileName 1 QString %s_A.h5 \n'%dsname)  
            self.sendcmd.flush()
            self.sendcmd.write('roachstream saver_b setFileName 1 QString %s_B.h5 \n'%dsname)  
            self.sendcmd.flush()

        
        self.sendcmd.write('roachstream w on_checkBox_streamEv2Disk_clicked 1 bool %d\n'%is_stream)
        self.sendcmd.flush()
        
        
        # if we are turning file stream off, then we block here, until cpp program tells us the saving is done.
        if not is_stream:
            print self.getCmd()
            print self.getCmd()
        
        
    def shut(self):
     
        self.sendcmd.close()
        self.devnull.close()
        self.streamproc.terminate()

  
    def printMaps(self):
           
        self.sendcmd.write('roachstream parser_a printMaps 0  \n')
        self.sendcmd.flush()

        self.sendcmd.write('roachstream parser_b printMaps 0  \n')
        self.sendcmd.flush()

    
    
    
    def setPipeNameOpen(self,fname='packetParse.pipe',is_open=True):
      

        self.sendcmd.write('roachstream w on_lineEdit_pipeName_textEdited 1 QString %s \n'%fname)
        self.sendcmd.flush()

        self.sendcmd.write('roachstream w on_checkBox_readpipe_clicked 1 bool %d \n'%is_open)
        self.sendcmd.flush()
    
         
    ##
    # fftx fftAnaluzerR2, and the data is is dict of { int:int , int:int }
    #
    #      
    def mapChannels(self,fftx):
    
        kys=fftx.chan_to_bin.keys()
        strx = ''
        

            
        self.sendcmd.write('roachstream parser_a clearMaps 0  \n')
        self.sendcmd.flush()
            
        self.sendcmd.write('roachstream parser_b clearMaps 0  \n')
        self.sendcmd.flush()


        for k in kys:
            strx = ''
            chan = k
            bin = fftx.chan_to_bin[chan][0]
            strx = strx + '%d:%d,'%(chan,bin)

            self.sendcmd.write('roachstream parser_a mapChanToBin 1 QString %s  \n'%(strx))
            self.sendcmd.flush()

            self.sendcmd.write('roachstream parser_b mapChanToBin 1 QString %s  \n'%(strx))
            self.sendcmd.flush()
            
        self.sendcmd.write('roachstream parser_a printMaps 0  \n')
        self.sendcmd.flush()

        self.sendcmd.write('roachstream parser_b printMaps 0  \n')
        self.sendcmd.flush()

            
    
                     
      
    ##
    # circle is dict of { int:(float,float) , int:(flaot,float) }
    #  channel, (xc,yc)
    #      
    def setCircleSpecs(self,circle):
    
        print "dataCapture.setCircleSpecs DISABLED"
        return
        
        kys=circle.keys()
       
        strx = ''
        for k in kys:
            strx = ''
            chan = k
            (xc,yc) = circle[chan]
            strx = strx + '%d:%f:%f,'%(chan,xc,yc)


            print     'roachstream parser_a setCircleCoord 1 QString %s \n'%strx
            self.sendcmd.write('roachstream parser_a setCircleCoord 1 QString %s \n'%strx)
            self.sendcmd.flush()

            self.sendcmd.write('roachstream parser_b setCircleCoord 1 QString %s \n'%strx)
            self.sendcmd.flush()

    
                     
    def setFluxRampBin(self,bin):
        self.sendcmd.write('roachstream parser_a setFluxBin 1 double %f\n'%bin)
        self.sendcmd.flush()
            
        self.sendcmd.write('roachstream parser_b setFluxBin 1 double %f\n'%bin)
        self.sendcmd.flush()
    
    def setIsFluxRampDemod(self,is_demod):
    
        if is_demod:
            self.sendcmd.write('roachstream parser_a setIsFluxDemod 1 bool 1\n')
            self.sendcmd.flush()
            
            self.sendcmd.write('roachstream parser_b setIsFluxDemod 1 bool 1\n')
            self.sendcmd.flush()
        else:
            self.sendcmd.write('roachstream parser_a setIsFluxDemod 1 bool 0\n')
            self.sendcmd.flush()
            
            self.sendcmd.write('roachstream parser_b setIsFluxDemod 1 bool 0\n')
            self.sendcmd.flush()
            
            
            
            
    def setTimeDelay(self,fa_, delay_sec):
                 
        print "dataCapturesetTimeDelay DISABLED "
        return
                  
        fftx = fa_.rfft
        lo = fa_.carrierfreq
        
        kys=fftx.chan_to_bin.keys()
        strx = ''
        
        for k in kys:
            strx = ''
            chan = k
            bin = fftx.chan_to_bin[chan][0]
            bb_freq = fftx.bin_to_srcfreq[bin]
            rf_freq = lo - bb_freq
            phase_delay = rf_freq * 2 * pi * delay_sec
            
            strx = strx + '%d:%f,'%(chan,phase_delay)


            print     'roachstream parser_a setTimeDelay 1 QString %s \n'%strx
            self.sendcmd.write('roachstream parser_a setTimeDelay 1 QString %s \n'%strx)
            self.sendcmd.flush()

            self.sendcmd.write('roachstream parser_b setTimeDelay 1 QString %s \n'%strx)
            self.sendcmd.flush()

