

class phaseCorrect:

    def __init__(self,sram_,rfft_,fwname_,which_legB_,nsampdly_=0):
    
        self.sram = sram_
        self.rfft = rfft_
        self.phase_inc_array=[0.0] * 256
        self.roach = self.sram.roach
        self.fwname = fwname_
        self.legB = which_legB_
        #is FFT delayed rel to another fft, for 2 FFT FW?
        self.num_samples_delay=nsampdly_
        self.inital_acc_value=[0.0]*256

    ###########################################################################
    #
    #
    ###########################################################################
        
    def zeroPhaseIncs(self):
        

        self.inital_acc_value=[0.0]*256
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
        
        self.phase_inc_array=[0.0] * 64
        blist = self.rfft.getBinsFromFreqs(self.sram.frequency_list)

        #bin center freqs
        bin_cf = self.rfft.getFreqsFromBins(blist)

        
    
        for k in range(len(blist)):
            bin = blist[k]
            binf=bin_cf[k];
            f=self.sram.frequency_list[k]
            
            if self.rfft.bin_to_legB[bin] == self.legB:
                
                dphase = self.rfft.getPhasePerFFTNoPi(f)
                chan = self.rfft.bin_to_legBchan[bin]
            
           
                print "bin  %d  chan  %d freq  %fMHz  dphase %f*pi"%\
                (bin, chan, f/1e6,dphase)
                #we now put the negative intot he phase acc, to cancle the phase change
                self.phase_inc_array[chan]= dphase

                iniphase = self.rfft.getPhasePerDelayNoPi(f,float(self.num_samples_delay))
                
                self.inital_acc_value[chan]=iniphase




    ###########################################################################
    # called by progRoach
    #
    ###########################################################################



    def progPhaseCorrect(self):
    
        L=len(self.phase_inc_array)    
        nchans = self.rfft.num_mapped_addresss
        bin_inc = self.toTwoComp(self.phase_inc_array,32,30)

        bin_acc = self.toTwoComp(self.inital_acc_value,32,30)

        #program mode
        #self.roach.write_int('%s_settings'%(self.fwname),1)
        
        for k in range(L):
            
            #write phase increment to BRAM
            self.roach.write_int('%s_PhaseIncrement1'%(self.fwname), bin_inc[k],k)
            
            #write address and initial accum val to sw registers
            self.roach.write_int('%s_iniacc'%(self.fwname), bin_acc[k],k)
         
    

        #trigger load acc and claer ... 
        self.roach.write_int('%s_settings'%(self.fwname),1)
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





        