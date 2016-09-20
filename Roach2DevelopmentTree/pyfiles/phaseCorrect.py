

class phaseCorrect:

    def __init__(self,sram_,rfft_,fwname_,which_leg_):
    
        self.sram = sram_
        self.rfft = rfft_
        self.phase_inc_array=[0.0] * 256
        self.roach = self.sram.roach
        self.fwname = fwname_
        self.leg = which_leg_
        

    ###########################################################################
    #
    #
    ###########################################################################
        
    def zeroPhaseIncs(self):
        

        self.phase_inc_array=[0.0] * 256
        self.progPhaseCorrect()
    
    ###########################################################################
        
    def reprogPhaseIncs(self):
        
        self.calcPhaseIncs()
        self.progPhaseCorrect()

    
        

    ###########################################################################
    #
    #
    ###########################################################################
        
    def calcPhaseIncs(self):
        #bins for each freq
        
        self.phase_inc_array=[0.0] * 256
        blist = self.rfft.getBinsFromFreqs(self.sram.frequency_list)

        #bin center freqs
        bin_cf = self.rfft.getFreqsFromBins(blist)

        self.phase_inc_array=[0.0] * 256
    
        for k in range(len(blist)):
            bin = blist[k]
            binf=bin_cf[k];
            f=self.sram.frequency_list[k]
            
            if self.rfft.bin_to_leg[bin] == self.leg:
                
                dphase = self.rfft.getPhasePerFFTNoPi(f)
                chan = self.rfft.bin_to_legchan[bin]
            
           
                print "bin  %d  chan  %d freq  %fMHz  dphase %f*pi"%\
                (bin, chan, f/1e6,dphase)
                #we now put the negative intot he phase acc, to cancle the phase change
                self.phase_inc_array[chan]= dphase






    ###########################################################################
    # called by progRoach
    #
    ###########################################################################



    def progPhaseCorrect(self):
    
        L=len(self.phase_inc_array)    
        nchans = self.rfft.num_mapped_addresss
        bin_inc = self.toTwoComp(self.phase_inc_array,32,30)


        self.roach.write_int('%s_phaseIncProgWe'%(self.fwname), 2)
        for k in range(L):
            
            self.roach.write_int('%s_phaseIncAddr'%(self.fwname), k)
            self.roach.write_int('%s_phaseIncVal'%(self.fwname), bin_inc[k])
            
            self.roach.write_int('%s_phaseIncProgWe'%(self.fwname), 3)
            self.roach.write_int('%s_phaseIncProgWe'%(self.fwname), 2)
            self.roach.write_int('%s_phaseIncProgWe'%(self.fwname), 0)

    

        #sero the accymlators
        self.roach.write_int('%s_settings'%(self.fwname), 1)
        time.sleep(0.1)
        self.roach.write_int('%s_settings'%(self.fwname), 0)



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
           
        
        
        return(bdata)





        