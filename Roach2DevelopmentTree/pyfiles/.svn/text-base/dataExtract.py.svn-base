
'''

import os

#
# use qdrtest.slx as the firmware
#



execfile('dataExtract.py')

dd=dataExtract(fa.sram,fa.rfft)

fname = '/localc/temp/trigffts'

dd.readEvents(fname)

dd.plotChan3D(fignum=1,zlim=-1,stspec = 0, nspec=2000,ampphase='stream_mag')


dd.plotChan3D(fignum=2,zlim=-1,stspec = 0, nspec=2000,ampphase='stream_phase')


dd.plotEvents2D(fignum=5, chans=-1,data=-1,stevent = 20000, nevents=1000)



dd.lsevents(isplot = 2)

clf();plot(dd.extractSpectrum(23432)[0])

dd.extractBinSeries(10e6)

dd.extractTimeSeries(10e6)

dd.getEventFromStream(chan=128, index=23432)

clf()

ev.keys()

ev[0].keys()


dd.waterfall()


dd.plotTimestamps()



'''


class dataExtract:

    def __init__(self,sram_,rfft_):
    
        self.rfft = rfft_
        self.sram = sram_
    
        self.fftLen = self.rfft.fftLen
        self.dftLen = self.rfft.dftLen
	
        self.dac_clk = self.rfft.dac_clk
        self.isneg_freq=self.rfft.isneg_freq

        #
        #we get data in retuyrned memory in packets. we have two rams, for phase and mag
        #phase has the header data.preceeding phse data
        #header is 0x10000 followed by int, chan number . The length of the data is set in     
        #fifoFSMPh.m, or the firmware. it is 32 words long in the memory.
        self.outmem_headerlen=2;
        #32 ints long
        self.outmem_datalen=32;
        #mem is 32 bits wide.
        self.outmem_width=32;
        #below is sign buts, total buts, num frac buts
        self.outmem_mag_datatype = [0,16,16]
        self.outmem_phs_datatype = [1,16,13]

        self.outmem_ts_masklow = 0x0000ffff<<9
        self.outmem_ts_maskhi = 0xffff0000
        self.outmem_ts_norm= 65536
        self.outmem_fff_mask=0xffff
        self.outmem_chan_mask=0xff
        self.outmem_pulse_mask=0x100

        #last bit of memory to carry over t next mem read
        self.carrydata=[numpy.array([0,0,0]),numpy.array([0,0,0])]

        
        
        #where latest iqdata is stored
        self.iqdata=[ zeros(2048), zeros(2048)]
	
    	#default channel to fft bin map
        self.chan_to_bin=self.rfft.chan_to_bin
        
        self.chan_to_srcfreq={}
        for chan in self.chan_to_bin.keys():
            self.chan_to_srcfreq[chan] = self.rfft.bin_to_srcfreq[self.chan_to_bin[chan][0]]
        
        
        
        #self.defaultChanMap()
    
    
    ####################################33
    #
    #######################################
    
    def defaultChanMap(self):
        for c in range(256):
            self.chan_to_bin[c]=[c*2]
            self.chan_to_srcfreq[c]  = self.getFreqFromBin(c*2)
            
    
    #################################################################################
    #
    # Open bin file. it is raw file with two streams embedded from 10gb enet on roach
    # get a block of data from one of the streams
    # whichstream 0,1
    # blocksize is num longs in ret block.
    # foffset is offset from top of file
    #
    ##################################################################################
    
    def readBinFile(self,fname,whichstream=0,blocksize=65536,foffset=0):
        
        fp=open(fname,'rb')
        fp.seek(foffset*8,0)
        b2=fp.read(blocksize*4*2)
        block2=struct.unpack('>' + 'I'*blocksize*2,b2)

       
        
        block = list(block2[whichstream::2])
        
        #remove 0xffffffff
        fff = 0xffffffff
        
        block3 = []
        for b in block:
            if b!=fff:
                block3.append(b)
                
        
        
       
        return(numpy.array(block3))
        
     
    def readEvents(self,dirname):
      
        dirs=[ dirname+'_A'  , dirname+'_B']
        events = {}    
       
        for d1 in dirs:
            dirs2 = os.listdir(d1)   
            
            for d2 in dirs2:
                dirx = d1 + '/' + d2
                tokens=d2.split('_')
                channel = int(tokens[1])
                bin = int(tokens[3])
                events[channel]={}
                
                files=os.listdir(dirx)   
                for fn in files:
                    fx = dirx + '/' + fn
                    
                    fp=open(fx,'rb')
                    bdata = fp.read()
                    fdata = struct.unpack('f'*(len(bdata)/4),bdata)
                    events[channel][fn]=numpy.array(fdata)
                    fp.close()
        
        self.iqdata = events
        return(events)
                     
                
        
       
        
           
            
            

    ###########################################################################
    #
    #take int data from two memories, mag and phase, and make floating ppoint 
    #guve int data from both memorues, raw int 32 bit words.
    #
    # events is a dict.
    #    events[channel] = { 
    #		'bin':int_binnumber ,
    #		'timestamps': [int_ts, int_ts, ....]
    #		'is_pulse': [int_is_pulse, int_is_pulse, ...]
    #		'stream': [  numpy.array([float_mag, float_mag, ....]) ,  numpy.array([float_phs, float_phs, ....]) ]
    #
    #
    ###########################################################################
    def extractEvents(self,magphs,append=0):
        
        
        if append==0: events=dict()
        else: events=self.iqdata


        searches=0
        carryover=0
        evtcnt=0
        nbad_events=0

        endsearch = len(magphs) - (self.outmem_headerlen + self.outmem_datalen)
        #rtry in case we go out of bounds...k+1 etc...
        if 1==1:
            k = 0
            while k<endsearch:
                print 'while %d magphs 0x%x'%(k,magphs[k])
                if magphs[k]&self.outmem_fff_mask == 0xaaaa:
                    print "FOUND aaaa\n"
                    if True:
                
                        chan=magphs[k+1]&self.outmem_chan_mask
                        timestamp = int(magphs[k]&self.outmem_ts_maskhi) 
                        timestamp = timestamp + (int(magphs[k+1]&self.outmem_ts_masklow) >>9)
                        is_pulse = magphs[k+1]&self.outmem_pulse_mask
                        dp=(magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff
                        dm=((magphs[(k+2):(k+2+self.outmem_datalen)])&0xffff0000)>>16
                        dataph=self.convToFloat(dp,self.outmem_phs_datatype)
                        dataph=dataph*pi
                        datamag=self.convToFloat(dm,self.outmem_mag_datatype)

                        if events.has_key(chan)==False:
                            print 'chan %d'%(chan)
                            events[chan]=dict()
                            events[chan]['stream']=[array([]), array([])]

                            events[chan]['timestamp']=[]
                            events[chan]['is_pulse']=[]
                            events[chan]['bin']=self.chan_to_bin[chan][0]
                            #events[chan]['bin']=-1
                            
                        events[chan]['timestamp'].append(timestamp)
                        events[chan]['is_pulse'].append(is_pulse)
                        stm=events[chan]['stream'][0]
                        stp=events[chan]['stream'][1]
                        events[chan]['stream'][0] = numpy.append(stm,datamag )
                        events[chan]['stream'][1] = numpy.append(stp,dataph )

                        print 'chan   %d  k  %d  is_pulse  %d  timestamp  %x    '%\
                              (chan,k,is_pulse,timestamp)

                        nextk=k+self.outmem_headerlen + self.outmem_datalen        


                        k = nextk
                        evtcnt=evtcnt+1
                    else:
                        print "bad event"
                        nbad_events=nbad_events+1
                        k=k+32
                else:
                    k=k+1
                    searches=searches+1        
                    print k

        else:
            pass

        print k
        print 'badevents = %d'%(nbad_events)
        self.carrydata=[magphs[k:]]
        self.searches = searches
        print 'searches =%d'%(searches)
        
        self.carryovers=carryover
        self.eventcount = evtcnt
        print 'evt cnt %d'%evtcnt
        self.iqdata = events
	
        return(events)




    ###########################################################################
    # give chan, event dict which default to iqdata.
    #give ts or index into timestamps. return mag and phs at that ts
    #
    ###########################################################################
    
    def getEventFromStream(self,chan=0,index=-1,ts=-1,events=-1):
    
        if events==-1: events=self.iqdata
        
        if ts>-1:
            #find the timestamp and get index
            index = 0
        
	    if index==-1:
	        while (
           	  events[chan]['timestamp'][index]!=ts  and 
           	  index<len(events[chan]['timestamp'])):
           
           	    index=index+1
        
        #case if index and ts being -1
        if index==-1: index==0
        #case of not found ts
        if index >= len(events[chan]['timestamp']):index=0
        
    
        ts=events[chan]['timestamp'][index]
        st_=index*32
        ed_=st_+32
        mag=events[chan]['stream_mag'][st_:ed_]
        phs=events[chan]['stream_phase'][st_:ed_]    
        is_pulse=events[chan]['is_pulse'][index]
        
        answer={ 'mag':mag,
                'phs':phs,
            'timestamp':ts,
            'is_pulse':is_pulse}
        return(answer)
        


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



    ###########################################################################
    #
    #
    ###########################################################################
    
    
    def extractBinSeries(self,freq):

        freq=self.sram.getLegalFreqs([freq])[0]
        #recordlen=self.getRecordLen()

        
        
        nspectra= self.getNumSpectra()
        
        #find which bin in fft this freq cooresponds to
        whichbin=self.rfft.getBinFromFreq(freq)
        print whichbin
        
    

        aa=where(array(self.rfft.fft_bins_requested)==whichbin)[0]
        if len(aa)==0:
            print "dataextract.extractBinSeriesError- that freq not in  fft_bins_requested"
            return

       
        chan=self.rfft.bin_to_chan[whichbin]
        print chan

        if self.iqdata.has_key(chan)==False:
            print 'dataextract.extractBinSeries- ERROR - no data for that channel'
            return

     

        sP=[self.iqdata[chan]['stream_mag'],  self.iqdata[chan]['stream_phase'] ]
        sR=self.PolarToRect(sP)

        #
        #extract the bin we want and make into a array, R and I.
        #

    

        return(sR)





    def RectToPolar(self,data):
    
        mags = numpy.sqrt(data[0]*data[0] + data[1]*data[1])
        phase=numpy.arctan2(data[1],data[0])
        return([mags,phase])
        
    def PolarToRect(self,data):
        mags=data[0]
        phase=data[1]
        re=mags*numpy.cos(phase)
        im=mags*numpy.sin(phase)
        return([re,im])
    


    ###########################################################################
    #
    #
    ###########################################################################
            
        
        
    def getNumSpectra(self):
        
        
        #famemlen-1 because of bug on last point in the memory.. fw bug
        #for long spectra do not worry about last point... so dont do -1...
        #if recordlen<200:
         #    nspectra= int(floor((self.memLen-1) / recordlen))
        #else:
        
        try:
            bin=self.iqdata.keys()[0]
            nspectra=len(self.iqdata[bin]['stream_mag'])
        except: 
            nspectra = 0
        

        return(nspectra)

    ###########################################################################
    #
    #
    ###########################################################################
            
        
        
        
    def getNumSpectra2(self,chan):
        
        
        #famemlen-1 because of bug on last point in the memory.. fw bug
        #for long spectra do not worry about last point... so dont do -1...
        #if recordlen<200:
         #    nspectra= int(floor((self.memLen-1) / recordlen))
        #else:
        
        
        nspectra=len(self.iqdata[chan]['stream_mag'])
        

        return(nspectra)
    



#say we readback 20 bins. then we make time series of one of these bins.
    #We supply freq, that is the freq in Hz we soured. If we are actually reading ot that bin,
    #then we retrive all samples of that bin and return in polar coord
    def extractTimeSeries(self,freq):

        binIQ=self.extractBinSeries(freq)

        #convert to polar, mag and phase
        bP=self.RectToPolar(binIQ)

        
        #bP[0]= bP[0] - bP[0][0]
        
        return(bP)        





    ###########################################################################
    #
    #
    ###########################################################################

    def extractSpectrum(self,spec_num):    
            

        spectrum_P=zeros(self.rfft.fftLen)
        spectrum_M=zeros(self.rfft.fftLen)

        #iqdata is no longer 2 arrauys, but a dict.
        #
        if 1==1:
            for chan in self.iqdata.keys():
                binx=self.chan_to_bin[chan][0]
                spectrum_P[binx]=self.iqdata[chan]['stream_phase'][spec_num]
                spectrum_M[binx]=self.iqdata[chan]['stream_mag'][spec_num]
        else:
            print "fftAnalzeri.extractSpectrum--bad spec_num"

        #put in freq order. We have carrier or DC at bin fftLen/2. bins 0-fftLen/2 are
        #right of DC. bins fftLen/2 are reverszed order (they are negative freqs), and put on left of DC.
        left=spectrum_P[(self.rfft.fftLen/2):]
        right=spectrum_P[:(self.rfft.fftLen/2)]
        spectrum_P=numpy.concatenate((left,right))
        

        left=spectrum_M[(self.rfft.fftLen/2):]
        right=spectrum_M[:(self.rfft.fftLen/2)]
        spectrum_M=numpy.concatenate((left,right))

        
        return([spectrum_M,spectrum_P])
        





    ###########################################################################
    #
    #data type is (18,15) where we have 18 bits data, 15 fraction bits
    #converts vector of binary twos comp to floats.
    ###########################################################################

    def convToFloat(self,data, datatype):

        nfrac=2
        nbits=1
        sbit=0
        
        #pow(2,(datatype[output][1]+1), 
        #if we have 16 fraction bits, this is
        #pow(2,16)-1 = 0x10000 - 1 = 0xffff
        if datatype[nfrac]>0:
            fracmask = int(pow(2,datatype[nfrac])-1)
            fracnorm=float(pow(2.0,datatype[nfrac]))
        else:
            fracmask = 0
            fracnorm=1.0
            
        #mask for int part not including sign bit.
        #datatype[output][0] - datatype[output][1] - 1 is 18-15-1=2, where we have 2 bits
        #fir int part not counting sign bit.
        numintbits =   datatype[nbits] - (datatype[sbit] + datatype[nfrac])
        #for 2 int buits, we take 3<<numfracbits, 3<<15    
        #this is int portion mask not incl the     
        if numintbits>0:    
            intmask=(pow(2,numintbits)-1) << datatype[nfrac]
        else:
            intmask=0

        #sign mask is numbuts-1
        if datatype[sbit]>0:
            signmask = int(pow(2,(datatype[nbits]-1)))
            signval = -1.0 * float(signmask)/fracnorm
        else:
            signmask=0
            signval=0.0

        #print 'fracmask %x fracnorm  %f numintbits  %d intmask  %x signmask  %x signval  %f '%\
        #    (fracmask,fracnorm,numintbits,intmask,signmask,signval)
        
        newdata = []
        for d in data:

            fracpart=int(d) &  fracmask
            frac =  float(fracpart)/fracnorm
            
            intpart = int(d) & intmask;
            intval = float(intpart) / fracnorm

            #if we have 18 bit data, sign but is but 17.
            #signbit will be 1 or 0, below becayse of > sign
            signbit=float((int(d) & signmask)>0);
            signval_ = signbit*signval
            

            val = signval_ + intval + frac

            #print ' fracpart  %d   frac %f intpart  %d  intval %f signbit  %d signval_  %f  val %f'%\
            #    (fracpart,frac,intpart,intval,signbit,signval_,val)

            newdata.append(val)
            
        return(array(newdata))
        
        
        
        
        
    ########################################################################
    #
    # 3dplot- plots events in iqdata, time vs freq vs amp or phase.
    # gibue zlim to limit the z axis as a tuyple (bottomlim,toplim)
    # ampphase=1 to plot phase instead of amp. 0 for amps
    ############################################################################

    def plotChan3D(self,fignum=1,zlim=-1,stspec = 0,nspec=-1,ampphase='stream_mag'):
        fig = figure(fignum)
        clf()
        ax = fig.gca(projection='3d')
        
        zranges=[]
        for chan in self.iqdata.keys():    
            try:
                if nspec==-1:
                    nspec=len(self.iqdata[chan][ampphase])        
                
                
                
                z=self.iqdata[chan][ampphase][stspec:(stspec+nspec)]
               
                
                zranges.append(median(z))
                y=arange(len(z))
                bin = self.chan_to_bin[chan]
                x = numpy.array( [ bin  ]*len(z) )
                ax.plot(x, y, z,label='zz')
            except:
                print "bad chan?"
            #ax.legend()

        rng=median(array(zranges))

        if zlim==-1: ax.set_zlim(bottom=rng/2, top=rng*2)
        else:ax.set_zlim(bottom=zlim[0], top=zlim[1])
        
        #plt.show()


        return(ax)


    ########################################################################
    #
    #2d plot of iqdata. chans is list of channels, or -1. data is an iqdata struct
    #or -1
    #
    ############################################################################

    def plotEvents2D(self,fignum=5, chans=-1,data=-1,stevent=20000,nevents=100):
    
        if data ==-1: data = self.iqdata
        
        if chans==-1: chans=data.keys()

        figure(fignum)
        clf()
        pcolors = ['b','g','r','c','m','y','k']
        ccount = 0
        
        for c in chans:
            i=0  
            for evcnt in range(stevent,stevent+nevents):   
            
                ts_ = data[c]['timestamp'][evcnt]
                #!!ts = e[3]
                print ts_
                evx=self.getEventFromStream(c,index=evcnt,events=data)
                amp=evx['mag']
                phs=evx['phs']
                timevec=numpy.arange(ts_,ts_+32)
                subplot(2,1,1)
                plot(timevec,amp,pcolors[ccount])
                subplot(2,1,2)
                plot(timevec,phs,pcolors[ccount])

            
            ccount=(ccount+1)%(len(pcolors))

          
        


    ########################################################################
    #
    #
    #
    ############################################################################

    def plotTimestamps(self,fignum=4, chans=-1,data = -1):
        figure(fignum)
        clf()

        if data ==-1: data = self.iqdata
        
        if chans==-1: chans=data.keys()

    

        for c in chans:
            ll=[]        
            for ts in data[c]['timestamp']:
            
                ll.append(ts)

            plot(ll)

                    

    ########################################################################
    #
    #
    #
    ############################################################################

    def plotTimestampsD(self,fignum=6, chans=-1,data = -1):
        figure(fignum)
        clf()

        if data ==-1: data = self.iqdata
        
        if chans==-1: chans=data.keys()

    

        for c in chans:
            ll=[]        
            for ts in data[c]['timestamp']:
            
                ll.append(ts)

            plot(numpy.diff(ll))

                
    ########################################################################
    #
    #
    #
    ############################################################################

    def waterfall(self,fignum=3,numspec=20,skip=1):
        figure(fignum);clf()
        yy=arange(self.fftLen)
        yoffs=0
        xoffs=0
        xinc=max(self.extractSpectrum(0)[0])/20.0
        poffs = 0.0
        for k in range(0,numspec,skip):
            try:  
                sp=self.extractSpectrum(k)
                subplot(2,1,1)
                
                subplot(2,1,1)
                plot(yy+yoffs, xoffs+sp[0])
                subplot(2,1,2)
                plot(yy+yoffs,poffs+sp[1])

                yoffs=yoffs + self.fftLen/50
                xoffs=xoffs + xinc
                poffs = poffs + pi/20
            except:
                break


        


    ########################################################################
    #
    #list events retrieved, stored in iqdata
    #
    ############################################################################


    def lsevents(self,ev=0,isplot=0):

        if ev==0:ev=self.iqdata

        print "Channels:"
        print ev.keys()

        if isplot>1:
          
            
            self.waterfall(fignum=11,numspec=20,skip=32)


        for chan in ev.keys():
            print "\n\n-------------------------"
            print "channel %d"%(chan)
           
            

            sf=0
            if self.chan_to_srcfreq.has_key(chan): sf=self.chan_to_srcfreq[chan]
            
            try:    
                print 'bin   %d  \nnumevents  %d  \nstreamlen  %d \nbinfreq %f \nsrcfreq %f\n'%\
                    (ev[chan]['bin'][0],
                    len(ev[chan]['timestamp']),
                    len(ev[0]['stream_mag']),
                    self.getFreqFromBin(ev[chan]['bin'][0]),
                    sf)

            except:
              
                print 'ERROR\n\n'

            
            if isplot>0: 
                figure(1000+chan)
                
                maxindex= len(ev[chan]['timestamp'])
                if maxindex>100: maxindex=100
                
                for index in range( maxindex ):
                    evx=self.getEventFromStream(chan,index)
            
                    print "    timestamp %d  ispulse %d"%(
                        evx['timestamp'],evx['is_pulse'])
                
                   
                    subplot(2,1,1);plot(evx['mag'])
                    subplot(2,1,2);plot(evx['phs'])

            if isplot>1:
                figure(12)
                subplot(2,1,1)
                plot(ev[chan]['stream_mag'][:10000])
        
                subplot(2,1,2)
                plot(ev[chan]['stream_phase'][:10000])

        #!!print '\nsearches %d'%(self.searches)
        #!!print 'carryovers %d'%(self.carryovers)
        #!!print 'eventcount %d'%(self.eventcount)

    ###########################################################################
    #
    #    carry data is when we get 1/2 event at end of fpga mem, and
    #    we must store in SW, before we grab more data from foga.    
    #    then we stich the event back together this happens when    
    #    a pulse or waveform is half sent to fpga output ram
    ###########################################################################

    def clearCarry(self):

        self.carrydata=[numpy.array([]),numpy.array([])]


    def clearEvents(self):
        self.iqdata=dict()
  
  
  
  
	############################################3
	#
	########################################33			

    def getFreqFromBin(self,bin):
	

        if self.rfft.isneg_freq==1:
            whichbin = self.rfft.fftLen - bin
        else:
            whichbin=bin
	    
	    
	    
        freq=whichbin * (self.rfft.dac_clk / self.rfft.fftLen)
	    
        return(freq)
	      
