

class roachFFT:

    def __init__(self,roach_,fw_block_name_):
    
        self.dftLen=128
        self.fftLen=512
        
        self.fw_block_name = fw_block_name_
        self.roach = roach_
        
        self.is_casper_fft=False
        
        self.timestamp_reset=0
        
        self.controlReg =0
        self.start_ffts =0
        self.stop_ffts = 0

        self.fft_run_forever=0
    
        self.roach_fft_shift=255

        self.roach_num_ffts=65536
        
    
        self.fftsynctime=512*5

        self.fft_bins_requested=[]
        self.fft_bin_flags=[]
        self.startFreq_Hz=0.0
        self.startFreq_Hz=0.0
        
        self.fft_bin_list=[]
        self.frequency_list=[]
        
        self.chan_to_bin4=dict()
            
        self.bin_to_chan=dict()
        self.chan_to_bin=dict()
        self.bin_to_srcfreq = dict()
        self.srcfreq_to_bin = dict()
        
        self.bin_to_leg=dict()
        self.bin_to_legchan=dict()
        
        self.num_mapped_addresss=0
        
        self.last_chan_to_read=0
        
        
        self.isneg_freq = 1
        self.dac_clk = 512e6
        self.sys_clk = 128e6
        
        
    ###########################################################################
    #FOR THE CASPER FFT
    #order of fft bins out of the fft block. counting from 0 to 511. output 0 gives 0,4,8,...
    #output 1 gives 1,5,9... output 2 gives 2,6,10..., output 3 gives 3,7,11 ...
    #
    #the tim madden FFT based on xilinx FFT blocks has a differet order for output coef.
    # output 1 gives 0,1,2,3...127
    # out 2 gives 128..255
    #out 3 give 256...383
    #out4 give 384...511
    #
    #
    #self.fft_bin_flags is calculated. it is array of len fftLen/4, or 128
    # we have 4 toutput of fft block, so bits 0 to 3 are flags for readout of each fft output.
    # buts 4 to 10 are channel number from 0 to 127. actauuly we onluy use 0 to 63, as we only 
    #have that may fifos per block. we have 2 blocks of 64 cgabels, so 
    #self.fft_bin_list, list of bins we are readng out, from 0 to 511. 
    #if we try to assign more then 128 bins to channels, then we will restart at chan 0.
    #so if we have blist of 256 bins, for 1/2 of FFT coef, (max possible for this fw) then
    #chan 0 get bin0 and bin 128, chan1 get bin1, bin129. these will be interleaved. so do not use
    #pulse finder mode. also need to have space in ffts, so set fftsynctime to 128*5 or so.
    #need SW to de-interleave the stuff
    ###########################################################################



    def fftBinFlags(self,blist):
        
    
        #if self.isneg_freq==1:
         #   blist = self.fftLen - blist -1
    
        
        self.fft_bins_requested=sort(blist)
        
        self.fft_bin_flags=[0] * 1024
        
        #this is for backwards compatibility- start and end freq are valid for
        #sweep fw, but not necessaryl for fft fw.
        freqs_=self.getFreqsFromBins(self.fft_bins_requested)
        self.startFreq_Hz=freqs_[0]
        

        
        self.endFreq_Hz = freqs_[len(freqs_)-1]
        #we just calc average incrFreq... it is correct for getting full fft
        #bins, but not for just selecting some bins at wierd freq intervals.    
        self.incrFreq_Hz=(self.endFreq_Hz - self.startFreq_Hz)/len(freqs_)
        
        
        
            

        #we must recalc fftbin list, so clear it.
        self.fft_bin_list=[]

        #here we assign fifo channels to each read out bin. start w/ 0
        #tghis is a bit complex:
        # we have four 64 chan fifosm, so the fifo chan in each fifo wants 6 bit address.
        #but we have 256 channels total w/ 4 fifos.
        # Another problem is that we cannot arbitraruoly assign fft bins to channels
        #for pos freq, 
        #
        #chans 0-63 is fifo0, 64-127 is fifo1, 128-191 is fifo2, 192-255 is fifo4
        #this is address in a fifo, 0 to 63 for foer the 4 fifos
        fifo_address=[0,0,0,0]    
        mapped_address=[0,0,0,0]
        #max fifo chan
        max_mapped_chan = 0;

        self.chan_to_bin4=dict()
            
        self.bin_to_chan=dict()
        self.chan_to_bin=dict()
        
        self.bin_to_leg=dict()
        self.bin_to_legchan=dict()
        
        self.num_mapped_addresss=len(blist)
        #set flags that need to be set
        #binx in range(512), bin4 in range(128)
        #for binx 0,1,2,3,4,5,6, bin4 will be 0 0 0 0,1,1,1,1
        for binx in blist:
            
            self.fft_bin_list.append(binx)

            if self.is_casper_fft:
                #we get 128 bins spit out of each fft output for 512 fft.
                #bin4 couns from 0 to 127 telling when our bin will spit out    
                bin4=(binx)>>2
                #this is which output of fft blobk the bin will com out.
                which_out = (binx%4)
            else:
                #tim madden FFT
                #we get 128 bins spit out of each fft output for 512 fft.
                #bin4 couns from 0 to 127 telling when our bin will spit out    
                bin4=binx % self.dftLen
                #this is which output of fft blobk the bin will com out.
                which_out = binx/self.dftLen
                
                
            
            #we readout 4 coef at once in 4 fft outs.
            #0 gives 0,4,8
            #1 is 1,5,9
            #2 is 2,6,10
            #3 is 3,7,11

            #binx is the actual bin we want to readout.

            
            #keep track of already-set flags.
            fftwesync0=self.fft_bin_flags[bin4] &1
            fftwesync1=self.fft_bin_flags[bin4] &2
            fftwesync2=self.fft_bin_flags[bin4] &4
            fftwesync3=self.fft_bin_flags[bin4] &8
 
                
            mapped_address[0]=(self.fft_bin_flags[bin4]&0x000003f0)>>4
            mapped_address[1]=(self.fft_bin_flags[bin4]&0x0000fc00)>>10 
            mapped_address[2]=(self.fft_bin_flags[bin4]&0x003f0000)>>16 
            mapped_address[3]=(self.fft_bin_flags[bin4]&0x0fc00000)>>22
            

            #we houdl be setting fftwezunc 0,1,2,3 but becauswe we cannot
            #read both halves of coef in FW we just use 0 and 1
            #see commented lines below...
            if which_out==0: fftwesync0=1;
            elif which_out==1: fftwesync1=2;
            elif which_out==2: fftwesync2=4;
            else: fftwesync3=8;
            
            
            mapped_address[which_out]=fifo_address[which_out]
            fifo_address[which_out] = (fifo_address[which_out] + 1)%64
            
    
        
            mapped_channel=mapped_address[which_out] + (which_out<<6)
            
            
            self.bin_to_chan[binx]=mapped_channel
            if mapped_channel>127:
                self.bin_to_leg[binx]=1
            else:
                self.bin_to_leg[binx]=0
                
            self.bin_to_legchan[binx] =  mapped_channel&127
               
            
            if self.chan_to_bin.has_key(mapped_channel)==False:
                self.chan_to_bin[mapped_channel]=[]
                self.chan_to_bin4[mapped_channel]=[]


            self.chan_to_bin4[mapped_channel].append(bin4)
            self.chan_to_bin[mapped_channel].append(binx)
            

            if max_mapped_chan<mapped_channel: 
                max_mapped_chan=mapped_channel


            #!!else:
                #this happens when we have low fifo to a bin4, and hi fifo to same bin4.
                #then we can reuse channels if 
            #!!    mapped_address= self.bin4_to_addr[bin4]
                
               
    
                #set flags for which fft outputs to read out to save to fifos.
            #current FW only pays atten to fftwesync0 and 1, so we cannot readout
            #bins 256 to 511 as of now.
            self.fft_bin_flags[bin4]=fftwesync0 +  fftwesync1 +fftwesync2 +fftwesync3;
                    

            
            self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[0]<<4)
            self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[1]<<10)
            self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[2]<<16)
            self.fft_bin_flags[bin4] = self.fft_bin_flags[bin4] + (mapped_address[3]<<22)

            
            
            
            
        self.fft_bin_list=sorted(self.fft_bin_list)
        
        
        self.last_chan_to_read=max_mapped_chan    
        
        self.progRoach()
        

    def regs(self):
        #get list of tuples ('regname', val)
        a=self.roach.readAllReg()
        
        #return items that have self.fw_block_name in reg name
        found = [b for b in a if self.fw_block_name in b[0]]
        
        return(found)

    def info(self):
    
        print 'chan_to_bin %s'%self.chan_to_bin
        print 'fft_bin_flags %s'%self.fft_bin_flags[:self.dftLen]
        print 'chan_to_bin4 %s'%self.chan_to_bin4
        print 'bin_to_chan %s'%self.bin_to_chan
    
        
        

    ###########################################################################
    #
    #
    ###########################################################################
    
    def showBinFlags(self):
        for bin4 in range(self.dftLen):
            if self.fft_bin_flags[bin4]>0:
                print "bin4 %d  addr3 %d  addr2 %d  addr1 %d  addr0 %d   wr3 %d  wr2 %d  wr1 %d  wr0 %d "%\
                    (bin4, 
                    (self.fft_bin_flags[bin4]&0x0fc00000)>>22, 
                    (self.fft_bin_flags[bin4]&0x003f0000)>>16, 
                    (self.fft_bin_flags[bin4]&0x0000fc00)>>10, 
                    (self.fft_bin_flags[bin4]&0x000003f0)>>4, 
                    self.fft_bin_flags[bin4]&8,
                    self.fft_bin_flags[bin4]&4,
                    self.fft_bin_flags[bin4]&2,
                    self.fft_bin_flags[bin4]&1)    








    ###########################################################################
    #
    #
    ###########################################################################



    def stopFFTs(self):
        
        roachlock.acquire()        
        
        self.start_ffts=0    
        self.stop_ffts=1    
        self.progRoach1()
        roachlock.release()
    
        

    ###########################################################################
    #
    #
    ###########################################################################









    ###########################################################################
    #
    #
    ###########################################################################


    def trigFFT(self):
        self.stopFFTs()
        
        self.stop_ffts=0    
        self.progRoach1()


        #self.rewindFFTMem()
        self.start_ffts=1    
        
        self.progRoach1()
        






    ###########################################################################
    #
    #
    ###########################################################################

    def numFFTs(self,n):
        self.roach_num_ffts=n
        
        
        self.fft_run_forever=0;
        
        if n<0:
            self.fft_run_forever=1;
        
        
        self.progRoach()
        
    ###########################################################################
    #
    # enable writing to fft mem, pulse start fft 1, 0. 
    ###########################################################################





    ###########################################################################
    #
    #
    ###########################################################################




    def calcRegs(self):
        
        
        self.controlReg=0
        self.controlReg = self.controlReg + (self.start_ffts<<2)

        self.controlReg = self.controlReg + (self.fft_run_forever<<1)
        self.controlReg = self.controlReg + (self.timestamp_reset<<0)
        self.controlReg = self.controlReg + (self.stop_ffts<<3)
        
        
        

    



    ###########################################################################
    #
    #
    ###########################################################################


        
    def sendBinFlags(self):
        #clear the rams
        try:
        #self.roach.write('BinData',self.convertToBinary16([0]*2048));
        
    
    
            self.roach.write('%s_BinData'%self.fw_block_name,self.convertToBinary(self.fft_bin_flags));
        

        
        except:
            print "sendBinFlagsNo ROACH"




    ###########################################################################
    #
    #
    ###########################################################################

    def progRoach1(self):
        
        self.calcRegs()    
        
        
        roachlock.acquire()
        
        self.roach.write_int('%s_settings_reg'%self.fw_block_name, self.controlReg)

        roachlock.release()
               



    ###########################################################################
    #
    #
    ###########################################################################

    def progRoach(self):
        
        self.calcRegs()    
        
      
        
        roachlock.acquire()
        try:

            self.roach.write_int('%s_settings_reg'%self.fw_block_name, self.controlReg)





            #!!self.roach.write_int('dram_controller', 0)
            #need to write -1 because of = in the fpga code...
            self.roach.write_int('%s_fftsynctime'%self.fw_block_name,self.fftsynctime-1);


            self.roach.write_int('%s_fftshift'%self.fw_block_name,self.roach_fft_shift)

            #!!self.roach.write_int('fftshift',self.roach_fft_shift)

            self.roach.write_int('%s_numffts'%self.fw_block_name,self.roach_num_ffts)





            self.sendBinFlags()



    

        except:
            print "progRoach NO ROACH"

        roachlock.release()
               

  
    def convertToBinary(self,data1):
        """ Converts  data points to 32-bit binary .

            @param data             Decimal data to be converted  for FPGA.
            """
        binaryData = ''
        for i in range(0, len(data1)):
            x = struct.pack('>I', data1[i])
            binaryData = binaryData + x

        return binaryData 
    
    
    #calc phase increase per fft for some given freq.
    def getPhasePerFFT(self,freq):
        
        
        ##freq in rad per sec. how much the phase changes in radians in 1 sec
#        freqrad=2*pi*freq
#        
#        #
#        #time between ffts.
#        #
#        
#        #fpga clk period in sec
#        sys_period=1.0/self.sys_clk
#        
#        #time in sec between successive ffts
#        
#        fftperiod=self.fftsynctime * sys_period;
#        
#        #calc how much the phase change is in fftperiod
#        
#        phase_per_fft = freqrad*fftperiod
#        
#        
#        phase_per_fft =2.0*pi *  ( phase_per_fft/(2.0*pi) - floor(phase_per_fft/(2*pi))  )
#        
    
        #num samples of 1 cycle of freq at fpga freq
        
        f_wavelen=self.sys_clk / freq
        
    
        #number of samples between fft is self.fftsynctime, or 8192
        #number of wavelens bween ffts
        waves_per_fft = self.fftsynctime / f_wavelen
    
        #get the fraction part of the num waves
        waves_per_fft_frac=waves_per_fft - floor(waves_per_fft)
        
        #convert to radians
        phase_per_fft = 2.0*pi*waves_per_fft_frac
    
        return(phase_per_fft)
        
        
        
        
        
    
    #calc phase increase per fft for some given freq.no PI in here
    def getPhasePerFFTNoPi(self,freq):
        
        
        ##freq in rad per sec. how much the phase changes in radians in 1 sec
#        freqrad=2*pi*freq
#        
#        #
#        #time between ffts.
#        #
#        
#        #fpga clk period in sec
#        sys_period=1.0/self.sys_clk
#        
#        #time in sec between successive ffts
#        
#        fftperiod=self.fftsynctime * sys_period;
#        
#        #calc how much the phase change is in fftperiod
#        
#        phase_per_fft = freqrad*fftperiod
#        
#        
#        phase_per_fft =2.0*pi *  ( phase_per_fft/(2.0*pi) - floor(phase_per_fft/(2*pi))  )
#        
    
        #num samples of 1 cycle of freq at fpga freq
        
        f_wavelen=self.sys_clk / freq
        
    
        #number of samples between fft is self.fftsynctime, or 8192
        #number of wavelens bween ffts
        waves_per_fft = self.fftsynctime / f_wavelen
    
        #get the fraction part of the num waves
        waves_per_fft_frac=waves_per_fft - floor(waves_per_fft)
        
        #convert to radians
        phase_per_fft = 2.0*waves_per_fft_frac
    
        return(phase_per_fft)
        
            
        

    
    
    #calc phase increase per fft for some given freq.
    def getPhasePerFFT(self,freq):
        
        
        ##freq in rad per sec. how much the phase changes in radians in 1 sec
#        freqrad=2*pi*freq
#        
#        #
#        #time between ffts.
#        #
#        
#        #fpga clk period in sec
#        sys_period=1.0/self.sys_clk
#        
#        #time in sec between successive ffts
#        
#        fftperiod=self.fftsynctime * sys_period;
#        
#        #calc how much the phase change is in fftperiod
#        
#        phase_per_fft = freqrad*fftperiod
#        
#        
#        phase_per_fft =2.0*pi *  ( phase_per_fft/(2.0*pi) - floor(phase_per_fft/(2*pi))  )
#        
    
        #num samples of 1 cycle of freq at fpga freq
        
        f_wavelen=self.sys_clk / freq
        
    
        #number of samples between fft is self.fftsynctime, or 8192
        #number of wavelens bween ffts
        waves_per_fft = self.fftsynctime / f_wavelen
    
        #get the fraction part of the num waves
        waves_per_fft_frac=waves_per_fft - floor(waves_per_fft)
        
        #convert to radians
        phase_per_fft = 2.0*pi*waves_per_fft_frac
    
        return(phase_per_fft)
        
        
        
        
        
    
    #calc phase increase per fft for some given freq.no PI in here
    def getPhasePerFFTNoPi(self,freq):
        
        
        ##freq in rad per sec. how much the phase changes in radians in 1 sec
#        freqrad=2*pi*freq
#        
#        #
#        #time between ffts.
#        #
#        
#        #fpga clk period in sec
#        sys_period=1.0/self.sys_clk
#        
#        #time in sec between successive ffts
#        
#        fftperiod=self.fftsynctime * sys_period;
#        
#        #calc how much the phase change is in fftperiod
#        
#        phase_per_fft = freqrad*fftperiod
#        
#        
#        phase_per_fft =2.0*pi *  ( phase_per_fft/(2.0*pi) - floor(phase_per_fft/(2*pi))  )
#        
    
        #num samples of 1 cycle of freq at fpga freq
        
        f_wavelen=self.sys_clk / freq
        
    
        #number of samples between fft is self.fftsynctime, or 8192
        #number of wavelens bween ffts
        waves_per_fft = self.fftsynctime / f_wavelen
    
        #get the fraction part of the num waves
        waves_per_fft_frac=waves_per_fft - floor(waves_per_fft)
        
        #convert to radians
        phase_per_fft = 2.0*waves_per_fft_frac
    
        return(phase_per_fft)
        
            
        

    ############################################3
    #
    ########################################33            
    
    def setLutSource(self,sramlut_):
        self.sramlut = sramlut_
        
     
    ############################################3
    #
    ########################################33            
    

    #set roach so all fft bins are returned
    def fftBinsAll(self, which="All"):
        
        
        if which=='All':        
            self.fftBinFlags(arange(self.fftLen))
        
        if which=='Low':        
            self.fftBinFlags(arange(self.fftLen/2))

        if which=='High':        
            self.fftBinFlags(arange(self.fftLen/2, self.fftLen))
        
    ############################################3
    #
    ########################################33            
        
    #if we have set a list of freqs to generate into the LUT, we can set the proper bins to readback from the fft.    
    def fftBinsFreqs(self):
    
        #blist=array(self.frequency_list)
        
        #the 0.0001 is so round wont randomly rand x.5 up or down. it gets rid of
        #0.5's
        #blist=numpy.round(0.0001 + blist/(self.dac_clk / self.fftLen))
        blist = self.getBinsFromFreqs(self.sramlut.frequency_list)
        
        self.mapSrcFreqBin()
        
        self.fftBinFlags(blist)
        self.fft_bin_list=sorted(self.fft_bin_list)
    
        
    
    ############################################3
    #
    ########################################33            
    def mapSrcFreqBin(self):
        self.bin_to_srcfreq = dict()
        self.srcfreq_to_bin = dict()
        blist = self.getBinsFromFreqs(self.sramlut.frequency_list)
        for k in range(len(blist)):
            self.bin_to_srcfreq[blist[k]] = self.sramlut.frequency_list[k]
            self.srcfreq_to_bin[self.sramlut.frequency_list[k]] = blist[k]
            
            
    ############################################3
    #
    ########################################33            
        
    def getBinsFromFreqs(self,freqs):
    
        bins=[]
        for f in freqs:
            bins.append(self.getBinFromFreq(f))    
        
        
        
        return(bins)
        
        
    ############################################3
    #
    ########################################33            
        
    def getBinFromFreq(self,freq):
        
        
        if freq<0:
            freq=    self.dac_clk - freq
        
        
        #find which bin in fft this freq cooresponds to
        whichbin=int(round(0.0001 + freq/(self.dac_clk / self.fftLen)))

        if self.isneg_freq==1:
            whichbin = self.fftLen - whichbin
        
        return(whichbin)    
        


        
    ############################################3
    #
    ########################################33            
        
    def getBinFromFreqF(self,freq):
        
        
        if freq<0:
            freq=    self.dac_clk - freq
        
        
        #find which bin in fft this freq cooresponds to
        whichbin=(freq/(self.dac_clk / self.fftLen))

        if self.isneg_freq==0:
            whichbin = float(self.fftLen) - whichbin
        
        return(whichbin)    
        
    ############################################3
    #
    ########################################33            

    def getBinsF(self):
    
        bins=[]
        for f in self.sramlut.frequency_list:
            bins.append(self.getBinFromFreqF(f))    
        
        
        
        return(bins)


    ############################################3
    #
    ########################################33            

    def getFreqFromBin(self,bin):
    

        if self.isneg_freq==1:
            whichbin = self.fftLen - bin
        else:
            whichbin=bin
        
        
        
        freq=whichbin * (self.dac_clk / self.fftLen)
        
        return(freq)
    
    ############################################3
    #
    ########################################33            


    def getFreqsFromBins(self,bins):
    
        freqs=[]
        for b in bins:
            freqs.append(self.getFreqFromBin(b))
    
        return(freqs)
        
        
                     

    ############################################3
    #
    ########################################33            
    #get res of fft bins, Hz per bin    
    def getFFTResolution(self):
        resolution = self.dac_clk/self.fftLen
        return(resolution);
                             
                     
