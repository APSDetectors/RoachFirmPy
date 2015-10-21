
'''

import os

#
# use qdrtest.slx as the firmware
#


execfile('katcpNc.py')
execfile('roachScope.py')
execfile('sramLut.py')
execfile('qdr.py')
execfile('if_board.py')
execfile('mkiddac.py')
execfile('freqSweep.py')

execfile('Channelizer.py')

    # events is a dict.
    #    events[channel] = { 
    #		'bin':int_binnumber ,
    #		'timestamps': [int_ts, int_ts, ....]
    #		'is_pulse': [int_is_pulse, int_is_pulse, ...]
    #		'stream': [  numpy.array([float_mag, float_mag, ....]) ,  numpy.array([float_phs, float_phs, ....]) ]
    #



execfile('dataExtract.py')



dd=dataExtract()

fname = '/home/oxygen26/TMADDEN/ROACH2/datafiles/testdata5.bin'

aa=dd.readBinFile(fname,blocksize = 1024*1024,foffset=0)

ev=dd.extractEvents(aa)


aa=dd.readBinFile(fname,blocksize = 1024*1024,foffset=1024*1024)

ev=dd.extractEvents(aa,append=1)




aa=dd.readBinFile(fname,whichstream=1,blocksize=65536*10,foffset=0)
 
ev=dd.extractEvents(aa)
       


dd.lsevents()

dd.getEventFromStream(chan=60, index=0)

clf()

plot(ev[0]['stream'][0])

plot(ev[1]['stream'][0])

plot(ev[2]['stream'][0])

plot(ev[3]['stream'][0])

ev.keys()

ev[0].keys()

#mags for chan0
ev[0]['stream'][0]



dd.waterfall()


dd.plotTimestamps()

'''


class dataExtract:

    def __init__(self):
    
        self.fftLen = 512
        self.dftLen = self.fftLen/4
	
        self.dac_clk = 512e6
        self.isneg_freq=1

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
        self.chan_to_bin={}
       
        
        self.chan_to_srcfreq={}
        
        self.defaultChanMap()
    
    
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
        mag=events[chan]['stream'][0][st_:ed_]
        phs=events[chan]['stream'][1][st_:ed_]    
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

    def extractSpectrum(self,spec_num):    
            

        spectrum_P=zeros(self.fftLen)
        spectrum_M=zeros(self.fftLen)

        #iqdata is no longer 2 arrauys, but a dict.
        #
        if 1==1:
            for chan in self.iqdata.keys():
                binx=self.chan_to_bin[chan][0]
                spectrum_P[binx]=self.iqdata[chan]['stream'][1][spec_num]
                spectrum_M[binx]=self.iqdata[chan]['stream'][0][spec_num]
        else:
            print "fftAnalzeri.extractSpectrum--bad spec_num"

        #put in freq order. We have carrier or DC at bin fftLen/2. bins 0-fftLen/2 are
        #right of DC. bins fftLen/2 are reverszed order (they are negative freqs), and put on left of DC.
        left=spectrum_P[(self.fftLen/2):]
        right=spectrum_P[:(self.fftLen/2)]
        spectrum_P=numpy.concatenate((left,right))
        

        left=spectrum_M[(self.fftLen/2):]
        right=spectrum_M[:(self.fftLen/2)]
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

    def plotChan3D(self,fignum=1,zlim=-1,nspec=-1,ampphase=0):
        fig = figure(fignum)
        clf()
        ax = fig.gca(projection='3d')
        
        zranges=[]
        for chan in self.iqdata.keys():    
            try:
                if nspec==-1:
                    nspec=len(self.iqdata[chan]['stream'][ampphase])        
                
                
                
                z=self.iqdata[chan]['stream'][ampphase][:nspec]
               
                
                zranges.append(median(z))
                y=arange(len(z))
               
                x = numpy.array( [ self.iqdata[chan]['bin']  ]*len(z) )
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

    def plotEvents2D(self,fignum=5, chans=-1,data=-1):
    
        if data ==-1: data = self.iqdata
        
        if chans==-1: chans=data.keys()

        figure(fignum)
        clf()
        pcolors = ['b','g','r','c','m','y','k']
        ccount = 0
        for c in chans:
            i=0        
            for ts_ in data[c]['timestamp']:
                try:
                    #!!ts = e[3]
                    evx=self.getEventFromStream(c,index=-1,ts=ts_,events=data)
                    amp=evx['mag']
                    phs=evx['phs']
                    timevec=range(ts_,ts_+32)
                    subplot(2,1,1)
                    plot(timevec,amp,pcolors[ccount])
                    subplot(2,1,2)
                    plot(timevec,phs,pcolors[ccount])
                except:
                    print 'Exception in fftAnalyzeri.plotEvents2D'
            
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
            ph=0.0
            if ev[chan].has_key('phase'):ph=ev[chan]['phase']

            sf=0
            if self.chan_to_srcfreq.has_key(chan): sf=self.chan_to_srcfreq[chan]
            
            try:    
                print 'bin   %d  \nphase  %d  \nnumevents  %d  \nstreamlen  %d \nbinfreq %f \nsrcfreq %f\n'%\
                    (ev[chan]['bin'][0],
                    ph,
                    len(ev[chan]['timestamp']),
                    len(ev[0]['stream'][0]),
                    self.getFreqFromBin(ev[chan]['bin'][0]),
                    sf)

            except:
              
                print 'bin   %d  \nphase  %d  \nnumevents  %d  \nstreamlen  %d \nbinfreq %f \nsrcfreq %f\n'%\
                   (ev[chan]['bin'],
                    ph,
                    len(ev[chan]['timestamp']),
                    len(ev[chan]['stream'][0]),
                    self.getFreqFromBin(ev[chan]['bin']),
                    sf)

            
            if isplot>0: 
                figure(1000+chan)
                for index in range(len(ev[chan]['timestamp'])):
                    evx=self.getEventFromStream(chan,index)
            
                    print "    timestamp %d  ispulse %d"%(
                        evx['timestamp'],evx['is_pulse'])
                
                   
                    subplot(2,1,1);plot(evx['mag'])
                    subplot(2,1,2);plot(evx['phs'])

            if isplot>1:
                figure(12)
                subplot(2,1,1)
                plot(ev[chan]['stream'][0])
        
                subplot(2,1,2)
                plot(ev[chan]['stream'][1])

        print '\nsearches %d'%(self.searches)
        print 'carryovers %d'%(self.carryovers)
        print 'eventcount %d'%(self.eventcount)

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
	

        if self.isneg_freq==1:
            whichbin = self.fftLen - bin
        else:
            whichbin=bin
	    
	    
	    
        freq=whichbin * (self.dac_clk / self.fftLen)
	    
        return(freq)
	      
