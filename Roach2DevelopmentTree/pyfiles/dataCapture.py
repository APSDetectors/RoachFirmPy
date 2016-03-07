'''

execfile('dataCapture.py')

capture = dataCapture()


capture.saveEvents('/local/asdf')

capture.clearEvents()

capture.shut()


'''


import os
import subprocess
from socket import *

class dataCapture:

    def __init__(self, 
        
        path = '/home/oxygen31/TMADDEN/ROACH2/projcts/QT/build-testEnet-Desktop-Debug/'):
        
        self.devnull = open(os.devnull, 'wb')
        cmd = path + 'testEnet'

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
            UDPSock.sendto( '\xff'*256,qt_addr)
            UDPSock.close()
            
    def clearEvents(self):
        self.sendcmd.write('roachstream w on_pushButton_clearEvents_clicked 0\n')  
        self.sendcmd.flush()
      
        
    def getCmd(self):
        return(self.getcmd.readline()) 
        
    def saveEvents(self,dsname):
    
        self.sendcmd.write('roachstream parser_a saveEvents 1 QString %s_A \n'%dsname)  
        self.sendcmd.flush()
        self.sendcmd.write('roachstream parser_b saveEvents 1 QString %s_B \n'%dsname)     
        self.sendcmd.flush()
        
    def shut(self):
     
        self.sendcmd.close()
        self.devnull.close()
        self.streamproc.terminate()

  
    def printMaps(self):
           
        self.sendcmd.write('roachstream parser_a printMaps 0  \n')
        self.sendcmd.flush()

        self.sendcmd.write('roachstream parser_b printMaps 0  \n')
        self.sendcmd.flush()

         
          
    def mapChannels(self,fftx):
    
        kys=fftx.chan_to_bin.keys()
        strx = ''
        
        for k in kys:
            chan = k
            bin = fftx.chan_to_bin[chan][0]
            strx = strx + '%d:%d,'%(chan,bin)


            
        self.sendcmd.write('roachstream parser_a clearMaps 0  \n')
        self.sendcmd.flush()
            
        self.sendcmd.write('roachstream parser_b clearMaps 0  \n')
        self.sendcmd.flush()

            
            
        self.sendcmd.write('roachstream parser_a mapChanToBin 1 QString %s  \n'%(strx))
        self.sendcmd.flush()

        self.sendcmd.write('roachstream parser_b mapChanToBin 1 QString %s  \n'%(strx))
        self.sendcmd.flush()
            
        self.sendcmd.write('roachstream parser_a printMaps 0  \n')
        self.sendcmd.flush()

        self.sendcmd.write('roachstream parser_b printMaps 0  \n')
        self.sendcmd.flush()

            
    
                     
        