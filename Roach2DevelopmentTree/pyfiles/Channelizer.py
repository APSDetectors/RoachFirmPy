
'''
execfile('Channelizer.py')

fa.chanzer = Channelizer(roach)


'''


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
        self.b_is_look_sync=0
        self.b_flush_fifo=0
        self.b_fifo_rst=0
        self.b_drop_all_events = 0
        self.b_ethernet_rst=0
        self.b_rst_full_counters=0
        # internal or ext ramp gen
        self.b_sync_source = 0
        #en internal ramp gen
        self.b_en_int_rampgen = 0
        #on roach calc flux demod
        self.b_flux_demod=0
        #if doing flux demod-incl raw data as well.
        self.b_savefluxraw = 0
        self.b_savefluxtrans = 0

        self.last_read_chan=128
        self.read_fifo_size = 100
        self.sync_delay = 128*55

        self.fullOutA=0
        self.fullOutB=0;
        self.fulleventA = 0
        self.fulleventB = 0
        self.fullmultiA = 0
        self.fullmultiB = 0
        self.fullmultiC = 0
        self.fullmultiD = 0
       

        self.fwnames={'last_read_chan':'lastReadChanA','settings':'fifoRdSettingsA_reg',
            'read_fifo_size':'readFifoSize', 'sync_delay':'syncDelay'}

        self.chan_to_translate={}


        #!!self.sync_delay_extgenerator = 55*128
        self.sync_delay_extgenerator = 0
        self.sync_delay_intgenerator = 5*128
        

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
# 0 for external ramp. 1 for internal ramp
#
#####################################################################################################

    def setSyncSource(self,syncsourcebit):
        #trigger in internal if 1, else trig on external
        self.b_sync_source=syncsourcebit
        #turn on internal ramp if 1
        self.b_en_int_rampgen = syncsourcebit
        if self.b_sync_source==1:
            self.setSyncDelay(sync_delay_intgenerator)    
        else:
            self.setSyncDelay(self.sync_delay_extgenerator)    
        
        
        self.progRoach()

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
#####################################################################################################

    
    def calcRegs(self):
    
        self.settings =  (self.b_dump_fifo << 0) + (self.b_rst<<1) + (self.b_wr_raw_data<<2) + \
            (self.b_is_look_sync<<3) + (self.b_flush_fifo<<4) + (self.b_fifo_rst<<5) + \
            (self.b_drop_all_events << 6) + (self.b_ethernet_rst<<7) + \
            (self.b_rst_full_counters << 8) + (self.b_sync_source<<9) + \
            (self.b_en_int_rampgen << 10) + (self.b_flux_demod<<11) +\
            (self.b_savefluxraw << 12) + (self.b_savefluxtrans<<13)
 
 
 

#####################################################################################################
#
#
#
#
#####################################################################################################

        
    def progRoach(self):

        self.calcRegs()	



        self.roach.write_int(self.fwnames['settings'], self.settings)

        self.roach.write_int(self.fwnames['last_read_chan'], self.last_read_chan)

        self.roach.write_int(self.fwnames['read_fifo_size'], self.read_fifo_size)

        self.roach.write_int(self.fwnames['sync_delay'], self.sync_delay)


#####################################################################################################
#
#
#
#
#####################################################################################################



    def flushFifos(self):
        
        self.b_flush_fifo=1
        self.progRoach()
        time.sleep(.1)
        self.b_flush_fifo=0
        self.progRoach()





#####################################################################################################
#
#
#
#
#####################################################################################################



    def rstFifos(self):
        
        self.b_fifo_rst=1
        self.progRoach()
        time.sleep(.1)
        self.b_fifo_rst=0
        self.progRoach()


#####################################################################################################
#
#
#
#
#####################################################################################################



    def resetEnet(self):
        
        self.b_ethernet_rst=1
        self.progRoach()
        time.sleep(.1)
        self.b_ethernet_rst=0
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
            

#####################################################################################################
#
#
#
#
#####################################################################################################
    def setSyncDelaySamples(self,nsamp):
        self.setSyncDelay(nsamp)
        
        

    def setSyncDelay(self,val):
        if fwtype=='tesd':
            self.sync_delay=val/2
        else:
            self.sync_delay=val
            
        self.progRoach()


#####################################################################################################
#
#
#
#
#####################################################################################################


    def setReadFifoSize(self,val):
    
        if fwtype == 'tesd':           
            self.read_fifo_size=val/2
        else:
            self.read_fifo_size=val
        
        self.progRoach()


#####################################################################################################
#
#
#
#
#####################################################################################################


    def setIsSync(self,val):
        self.b_is_look_sync=val
        self.progRoach()


#####################################################################################################
#
#
#
#
#####################################################################################################

    def getSyncRate(self):
        
        
        

        

        p1 = self.roach.read_int('numSyncPulses')
        
        time.sleep(1)
        p2 = self.roach.read_int('numSyncPulses')
        
        return(p2-p1)
        
 
#####################################################################################################
#
#is_demod 0 or 1, for turning on flux demod calc
#is_incl_raw_trans 0,1,2 for no rawdata, raw data ,transdata. transdata only for flux demod 1
# evt len is fifo read size, like 100 samples.
# num_cycles how many phi0 cucles in one evt len
#####################################################################################################
       
        
    def setFluxRampDemod(self,is_demod,is_incl_raw_trans, evt_len,num_cycles):
    
    
        
        self.b_flux_demod=is_demod
        #if doing flux demod-incl raw data as well.
        self.b_savefluxraw = 0
        self.b_savefluxtrans = 0
        
        if (is_incl_raw_trans==1):
            self.b_savefluxraw = 1
        elif  is_incl_raw_trans==2: 
            self.b_savefluxtrans=1
            self.b_flux_demod=1
       
        self.setReadFifoSize(evt_len)
        phase = num_cycles*2.0*numpy.pi *numpy.arange(evt_len)/evt_len 
        self.flux_nsin = -32700.0*numpy.sin( phase )
        self.flux_cos = 32700.0*numpy.cos( phase )
        
        self.flux_nsin_b = struct.pack('>'+'h'*len(self.flux_nsin),*self.flux_nsin)
        self.flux_cos_b = struct.pack('>'+'h'*len(self.flux_cos),*self.flux_cos)
        
        roach.write('FRD1_DFT_costable',self.flux_cos_b)
        roach.write('FRD_DFT_costable',self.flux_cos_b)
        
        roach.write('FRD1_DFT_sintable',self.flux_nsin_b)
        roach.write('FRD_DFT_sintable',self.flux_nsin_b)
 
   ###########################################################################
    #
    #convert float data to fixed point twos comp. nbits like 18 for 18 bits.
    #dpoint is number of fraction bits.
    ###########################################################################

    def toTwoComp(self,data,nbits,dpoint):


        bdata=[0] * len(data)

        for k in range(len(data)):
            bdata[k]=floor(abs(data[k]) *(1<<dpoint))
            if data[k]<0:
                bdata[k]=pow(2,nbits) - bdata[k]
        
            bdata[k] = int(bdata[k])
            bdata[k] = bdata[k]&( (1<<nbits)-1 )
        
        
        return(bdata)

               
 
#####################################################################################################
#
#
#FRD1_trIQ_tr
#
#####################################################################################################
  
    def clearTransTable(self):
        self.chan_to_translate = {}
        
  
   
    def setFlxDmodTranTable(self,chan=192,xc=0.0,yc=0.0):
      
            #put neg of xc,yc so they are added to data in FDR
            
        self.chan_to_translate[chan]=(-xc,-yc)
        
       
                            
        xcb =  self.toTwoComp([-xc],16,14)[0]
        ycb =  self.toTwoComp([-yc],16,14)[0]
        
        ramint = (xcb<<16) + ycb
          
    
            
        #!!for fdr1 only!!!!
        chanram = chan-128
            
        self.roach.write_int( 'FRD1_trIQ_tr',  ramint,offset = chanram)
         

    def clearTranslator(self):
        
        #self.translate_intram0 = [0]*128
        self.translate_intram1 = '\0'*128*4
        
        self.roach.write('FRD1_trIQ_tr', self.translate_intram1 )
        

    def progTranslator(self):
    
        self.clearTranslator()
        
        #if chan>=128:
        #    fwname = "FDR1
        #    chan = chan - 128
        #
        #else:
        #    fwname = "FDR"
              
        for chan in  self.chan_to_translate.keys():
            xc = self.chan_to_translate[chan][0]
            yc = self.chan_to_translate[chan][1]
                            
            xcb =  self.toTwoComp([xc],16,14)[0]
            ycb =  self.toTwoComp([yc],16,14)[0]
        
            ramint = (xcb<<16) + ycb
          
            #!!for fdr1 only!!!!
            chanram = chan-128
            
            self.roach.write_int( 'FRD1_trIQ_tr',  ramint,offset = chanram)
            print 'ramint %i, xcb %i,ycb %i,chan %i,chanram %i, xc %f, yc%f'%(ramint,xcb,ycb,chan,chanram,xc,yc)
          
          
          
