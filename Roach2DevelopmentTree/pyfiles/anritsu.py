"""


execfile('anritsu.py')


an = anritsu()

an.testSweep()

an.shut()


fa.an.shut()
fa.an=anritsu()


"""

import os
import subprocess
import time


class anritsu:

    def __init__(self,is_connect = True):
    

        #mapping of bits in regs
        #this is based opnm the FW in theroach board. which bit in the SW register in the FW maps
        #to which pin on the gpio on roach, and IF board

        self.anritsu_freqghz_=0
        self.anritsu_power_=0
        self.anritsu_is_on_=0



        self.ANRITSUCMD='/home/oxygen31/TMADDEN/ROACH/vx11/vxi11_1.10/anritsuOsc'
        self.ANRITSUIP='192.168.0.68'  
        self.is_connect = is_connect
        
        self.freq_time_delay = 0.02
        
        if is_connect:
            self.devnull = open(os.devnull, 'wb')

        
           # self.anritproc = subprocess.Popen(
           #     [self.ANRITSUCMD ,  self.ANRITSUIP  ], 
           #      stdin=subprocess.PIPE,stdout=self.devnull)


            self.anritproc = subprocess.Popen(
                [self.ANRITSUCMD ,  self.ANRITSUIP  ], 
                 stdin=subprocess.PIPE,stdout=self.devnull)
            
    ########################################################################
    #
    #
    #
    #
    #######################################################################
    #

    def setFreqPower(self,freqghz,power,is_on):



        self.anritsu_freqghz_=freqghz
        self.anritsu_power_=power
        self.anritsu_is_on_=is_on

        os.system('%s %s :FREQ:FIX %fGHz'%(self.ANRITSUCMD,self.ANRITSUIP,freqghz))
        os.system('%s %s :POW %f'%(self.ANRITSUCMD,self.ANRITSUIP,power))

        if is_on==1:
            os.system('%s %s :OUTP ON'%(self.ANRITSUCMD,self.ANRITSUIP))
        else:
            os.system('%s %s :OUTP OFF'%(self.ANRITSUCMD,self.ANRITSUIP))



    ########################################################################
    #
    #
    #
    #
    #######################################################################
    #

    def setFreq(self,freqghz):
    
    

        self.anritsu_freqghz_=freqghz
      
        if self.is_connect:
            self.anritproc.stdin.write(':FREQ:FIX %fGHz \n'%(freqghz))
            self.anritproc.stdin.flush()
    
        time.sleep(self.freq_time_delay)
    
    ########################################################################
    #
    #
    #
    #
    #######################################################################
    #
    
    def setOnOff(self,is_on):
      
        self.anritsu_is_on_=is_on
       
        if self.is_connect:

            if is_on==1:
                self.anritproc.stdin.write(':OUTP ON \n')
                self.anritproc.stdin.flush()
            else:
                self.anritproc.stdin.write(':OUTP OFF \n') 
                self.anritproc.stdin.flush()


    ########################################################################
    #
    #
    #
    #
    #######################################################################
    #

    def setPower(self,power):
        self.anritsu_power_=power
        if self.is_connect:
            self.anritproc.stdin.write(':POW %f \n'%(power))
            self.anritproc.stdin.flush()

    ########################################################################
    #
    #
    #
    #
    #######################################################################
    #
 
    
    def shut(self):
        if self.is_connect:
     
            self.anritproc.stdin.write('q\n')
            self.anritproc.stdin.flush()
            
            self.devnull.close()
            self.anritproc.terminate()
            #self.anritproc.terminate()
            
            
    ########################################################################
    #
    #
    #
    #
    #######################################################################
    #
 
 
    def testSweep(self,waitx = 0):
    
        freqs=arange(3.0, 5.0, 0.001)

        time.sleep(waitx);
        
        for f in freqs: 
            self.setFreq(f)
            print f
