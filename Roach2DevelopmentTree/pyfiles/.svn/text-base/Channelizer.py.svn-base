#####################################################################################################
#
#
#
#
#####################################################################################################


class Channelizer:

#####################################################################################################
#
#
#
#
#####################################################################################################

   
    def __init__(self,roach_):
        self.roach=roach_

        self.settings=0

        self.b_dump_fifo=0
        self.b_rst=0
        self.b_wr_raw_data=0  
        self.b_is_calc_mean=0
        self.b_flush_fifo=0
        self.b_fifo_rst=0
        self.b_rst_full_counters=0

        self.last_read_chan=128

        self.fullOutA=0
        self.fullOutB=0;
        self.fulleventA = 0
        self.fulleventB = 0
        self.fullmultiA = 0
        self.fullmultiB = 0
        self.fullmultiC = 0
        self.fullmultiD = 0
       

        self.fwnames={'last_read_chan':'lastReadChanA','settings':'fifoRdSettingsA_reg' }

#####################################################################################################
#
#
#
#
#####################################################################################################

    def checkFull(self,is_print = True):
    
        
        self.fullOutA   =self.roach.read_int('fullOutA')
        self.fullOutB   =self.roach.read_int('fullOutB')
        self.fulleventA =self.roach.read_int('fulleventA')
        self.fulleventB =self.roach.read_int('fulleventB')
        self.fullmultiA =self.roach.read_int('fullmultiA')
        self.fullmultiB =self.roach.read_int('fullmultiB')
        self.fullmultiC =self.roach.read_int('fullmultiC')
        self.fullmultiD =self.roach.read_int('fullmultiD')
  
        if is_print:
            print ' %s  = %d'%('fullOutA  ' , self.fullOutA  )
            print ' %s =  %d'%('fullOutB  ' , self.fullOutB  )
            print ' %s  = %d'%('fulleventA' , self.fulleventA)
            print ' %s  = %d'%('fulleventB' , self.fulleventB)
            print ' %s  = %d'%('fullmultiA' , self.fullmultiA)
            print ' %s  = %d'%('fullmultiB' , self.fullmultiB)
            print ' %s  = %d'%('fullmultiC' , self.fullmultiC)
            print ' %s  = %d'%('fullmultiD' , self.fullmultiD)
     



#####################################################################################################
#
#
#
#
#####################################################################################################

    def clearFull(self):
        self.b_rst_full_counters=1
        self.progRoach()
        
        self.b_rst_full_counters=0
        self.progRoach()
        
#####################################################################################################
#
#
#
#
#####################################################################################################

    
    def calcRegs(self):
    
        self.settings =  (self.b_dump_fifo << 0) + (self.b_rst<<1) + (self.b_wr_raw_data<<2) + \
            (self.b_is_calc_mean<<3) + (self.b_flush_fifo<<4) + (self.b_fifo_rst<<5) + \
            (self.b_rst_full_counters << 8)
            

#####################################################################################################
#
#
#
#
#####################################################################################################

        
    def progRoach(self):

        self.calcRegs()	


        roachlock.acquire()

        self.roach.write_int(self.fwnames['settings'], self.settings)

        self.roach.write_int(self.fwnames['last_read_chan'], self.last_read_chan)

        roachlock.release()

#####################################################################################################
#
#
#
#
#####################################################################################################



    def flushFifos(self):
        self.b_flush_fifo=1
        self.progRoach()
        self.b_flush_fifo=0
        self.progRoach()

#####################################################################################################
#
#
#
#
#####################################################################################################

      
    def writeRaw(self,val):
         self.b_wr_raw_data=val
         self.progRoach()

#####################################################################################################
#
#
#
#
#####################################################################################################

      
    def setLastReadChan(self,val):
        self.last_read_chan=val
        self.progRoach()
      

#####################################################################################################
#
#
#
#
#####################################################################################################

    def readFifos(self,val):     
        
        self.b_dump_fifo=val
        self.progRoach()
            
