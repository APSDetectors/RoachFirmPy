

"""

execfile('sramLut.py')

sram = sramLut(roach2,'SRAM_LUT')


sram.setLutFreqs(arange(10e6,30e6,10e6),15000)


sram.plotLutIQF()






sram.sample_order = [2,3,0,1][::-1]

sram.sample_order = [0,0,0,0]


sram.setLutFreqs(10e6,30000)


sram.setLutFreqs(arange(10e6,200e6,10e6),10000)

clf();plot(sram.lut_i)


i = sram.singleFreqSAW(1e6, 'I', 512e6, 1024, 0, 32000)
q = sram.singleFreqSAW(1e6, 'Q', 512e6, 1024, 0, 32000)

iqr=sram.convertToBinary128(i,q)

sram.writeSram(iqr)
sram.streamSram()
        

"""
import numpy

class sramLut:

    def __init__(self,rch_,fwn_):
        self.fwname = fwn_

        self.roach = rch_

        self.wr_toggle = 0;
        self.rd_toggle = 1;

    
        self.which_write = 'cpu';

        self.sram_test_nbuffers=1

        self.div_lutlen = 2;
    
        self.sample_order = [0,1,2,3]
    
    #len of SRAM mem. it is lut_length /4
        self.lutsize=0
    
    #max amp in normailzed 0 to 1
        self.lut_sine_amp=0
    
        #freqs in Hz. Baseband. requested freqs
        self.req_frequency_list=[]

        # actual legal freqs in lut
        self.frequency_list=[]
        #len of the raw sines, not diveded by parallel mem size (4)
        self.lut_length=1024*16


        #I signal raw waveform
        self.lut_i=[]

        #Q raw waveform
        self.lut_q=[]

        #phase of each freq in radians?
        self.lut_phase_list=[]

        #sample rate of dac
        self.dac_clk=512e6

        #offset freq of Q rel to I
        self.Q_freq_offset=0.0
        #offset phase in radians from a sin
        #found by measuring... about 18 degree error in Dacs and IQ mix output.
        #used spec anal for this
        #use -18.5 for pos sideband
        #self.Q_phase_offs=0.02 * 18.5
        self.Q_phase_offs=0
        
        #in ns, can be pos or neg. rel to I
        #-.12ns found empiracally w/ bb loopback
        #self.Q_time_delay = -0.12
        self.Q_time_delay = 0
        #phase of each Q sin due to time delay.
        self.Q_time_phase_list=[0.0]
        
        #rel amp of Q to I
        #use 1 for neg sideband, -1 for pos sideband
        self.Q_amp_factor=1.0

        #binary waveform stored in SRAM.the 128 bit data
        self.lut_binaryIQ=[]
        #ampl;itudes of each sine
        self.amplist=[]
    

        self.maxi =0;
        self.maxq = 0
        
        self.maxiq = 0
        self.clipfactor=0.0;
        
        #
        # for add test pulses to waveform
        #
        #len in samples
        self.test_pulse_len=256
        #in degrees
        self.test_pulse_amp =20.0
	
        #true of false

        self.is_test_pulse = False
          
        #
        # FM modulation of the freq tones.
        #
        
        #do we use FM?
        self.is_mod_freq = False    
        # amplitude of phase modulation in radians    
        self.mod_amp=0.1 
        #period of modultion in samples.
        self.mod_period=12000.0
        #use a integration time of 190 samples, 4.0 periods
    
    
    def plotLutIQF(self):
    
        LIQ = fft.fft( self.lut_i + 1j*self.lut_q)
        figure(1);clf()
        Liqa = abs(LIQ)
        P = 20*log10(Liqa + 1)
        P = P - max(P)
        plot(P) 
        


    def setLutFreqs(self,freqs,amp,is_prog = True,is_start = True):


        if type(freqs)==numpy.ndarray:
            freqs = freqs.tolist()

        if type(freqs)!=list:
            freqs = [freqs]


        #amp can be a list of amps w/ len = len(freqs). or a single number. 
        if type(amp)==list:
            self.amplist=amp
            self.lut_sine_amp=max(amp)/32768.0
        else:
          self.lut_sine_amp=amp/32768.0
          self.amplist=[amp]*len(freqs)

        self.req_frequency_list = freqs
        self.frequency_list=self.getLegalFreqs(freqs)
        iq=[zeros(self.lut_length) , zeros(self.lut_length)]


        self.lut_i=iq[0];
        self.lut_q=iq[1];    

        self.lut_phase_list=[]
        self.Q_time_phase_list=[0.0] * len(self.frequency_list)

        for k in range(len(self.frequency_list)):

            freq = self.frequency_list[k]
            #amp = amps[k]
            #if k==0:
            #    phase = 0.0;
            #else:
            #    phase = random.uniform(-math.pi, math.pi)

            phase =2.0*math.pi* double(k)/double(len(self.frequency_list))

            self.lut_phase_list.append(phase)
            self.lut_i=self.lut_i + self.singleFreqLUT(freq, 'I', self.dac_clk,self.lut_length , phase, self.amplist[k])

            self.Q_time_phase_list[k] = (self.Q_time_delay*1e-9)   *  freq*2*pi
            self.lut_q=self.lut_q + self.singleFreqLUT(
                    freq+self.Q_freq_offset, 
                    'Q', 
                    self.dac_clk,
                    self.lut_length , 
                    phase + self.Q_phase_offs +self.Q_time_phase_list[k]  , 
                    self.amplist[k]*self.Q_amp_factor)


        #fa.lut_i==fa.singleFreqLUT(freq, 'I', fa.dac_clk,fa.dac_clk/fa.lut_length , 0, 50000.0)



        self.maxi = max( abs(self.lut_i) );
        self.maxq = max( abs(self.lut_q) );
        
        self.maxiq = max( [self.maxi, self.maxq] )
        self.clipfactor=0.0;
        
        if self.maxiq>32768:
            print "Max iq Greater then 32k"
            
            self.clipfactor = self.maxiq/32768.0;
            A = 32768.0
            print "Clipfactor = %5.2f"%self.clipfactor
            
            self.lut_i=A * scipy.special.erf(   self.lut_i /A); 
            self.lut_q=A * scipy.special.erf(   self.lut_q /A); 

        self.lut_binaryIQ=self.convertToBinary128(self.lut_i,self.lut_q)
        
        try:
            if is_prog:
                self.writeSram(self.lut_binaryIQ)

            if is_start:
                self.streamSram()
        

        except:
            print "No Roach "

    def getLegalFreqs(self,freqs):


        for k in range(len(freqs)):
            if freqs[k] < 0:
                freqs[k] = self.dac_clk-freqs[k]

        resolution = self.dac_clk/self.lut_length;

        freq_fix=[]
        for freq in freqs:
            #0.0001 so round does not randomize 0.5...
            newfreq=resolution * round(0.0001 + freq/resolution)
            freq_fix.append(newfreq)
            #if freq!=newfreq:
            #    print "Error: not enough resolution for req. frequncies"

        return(freq_fix)



    def addPulse2Phase(self,phaseterm):


        #make test pulse.it is inserted in random part of the waveform.
        #calc where pulse will be in the wave

        pulse_st=int(round(rand() * (len(phaseterm)- 2*self.test_pulse_len)))
        pulse_ed = pulse_st+self.test_pulse_len

        #now get a piece of the phase term
        pulsephase = phaseterm[pulse_st:pulse_ed]
        #now add a new phase term to it, a ramp
        pulsephase = pulsephase + (pi*self.test_pulse_amp / 180.0 ) * (1.0/len(pulsephase))*arange(len(pulsephase))

        #now put the ramp into the wave		
        phaseterm[pulse_st:pulse_ed] = pulsephase
        return(phaseterm)



    def addModFreq2Phase(self,phaseterm):


        #make test pulse.it is inserted in random part of the waveform.
        #calc where pulse will be in the wave

        modfreq = self.mod_amp*numpy.sin(\
                (2*pi*numpy.arange(len(phaseterm))) / (self.mod_period ) )
        
        phaseterm = phaseterm + modfreq
        return(phaseterm)



    def singleFreqLUT(self,f, iq, sampleRate, size, phase, amplitude):
        """ Returns data points for the DAC look-up table.

        @param f       List of desired freqs, e.g., 12.34e6 if resolution = 1e4.
        @param sampleRate       Sample rate of DAC.
        @param resolution       Example: 1e4 for resolution of 10 kHz.
        @param phase            Constant phase offset between -pi and pi.
        """



        #data = []



        #phaserad=numpy.pi * phase / 180.0;
        phaserad = phase
        phaseterm= phaserad + 2*math.pi*(f/sampleRate)*numpy.arange(size)


        if self.is_test_pulse:
            phaseterm = self.addPulse2Phase(phaseterm)
        
        
        if self.is_mod_freq:
            phaseterm = self.addModFreq2Phase(phaseterm)
            
        #make test pulse.it is inserted in random part of the waveform.
        #calc where pulse will be in the wave




        if iq == 'I':
            data=numpy.round(amplitude * numpy.cos(phaseterm))
                #data.append(int(amplitude*math.sin(2*math.pi*f*t)))
        else:
            sign = 1.0;


            data=numpy.round(sign*amplitude * numpy.sin(phaseterm))


        return data




    def singleFreqSAW(self,f, iq, sampleRate, size, phase, amplitude):
        """ Returns data points for the DAC look-up table.

        @param f       List of desired freqs, e.g., 12.34e6 if resolution = 1e4.
        @param sampleRate       Sample rate of DAC.
        @param resolution       Example: 1e4 for resolution of 10 kHz.
        @param phase            Constant phase offset between -pi and pi.
        """



        #data = []


            #phase from 0 to 1 is 0 to 360 degrees
        phaseone=phase / 180.0;
        phaseterm= phaseone + (f/sampleRate)*numpy.arange(size)
        #remove ints, to saw repeats.. opnluy want decimals
        phaseterm = phaseterm - numpy.floor(phaseterm)

        #make test pulse.it is inserted in random part of the waveform.
        #calc where pulse will be in the wave




        if iq=='I':
            data=numpy.round(amplitude * phaseterm)
        else:
            data=numpy.round(amplitude * (1.0-phaseterm))


        return data





        def convertToBinary128_2(self,data1,channel):
            """ Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

                @param data             Decimal data to be converted  for FPGA.
                """
            binaryData = ''
            for i in range(0, len(data1)):
                if channel==0:
                    x = struct.pack('>hhhhhhhh',
                        data1[i],
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0)

                elif channel==1:
                    x = struct.pack('>hhhhhhhh',
                        0,
                        data1[i],
                        0,
                        0,
                        0,
                        0,
                        0,
                        0)

                elif channel==2:
                    x = struct.pack('>hhhhhhhh',
                        0,
                        0,
                        data1[i],
                        0,
                        0,
                        0,
                        0,
                        0)

                elif channel==3:
                    x = struct.pack('>hhhhhhhh',
                        0,
                        0,
                        0,
                        data1[i],
                        0,
                        0,
                        0,
                        0)


                elif channel==4:
                    x = struct.pack('>hhhhhhhh',
                        0,
                        0,
                        0,
                        0,
                        data1[i],
                        0,
                        0,
                        0)

                elif channel==5:
                    x = struct.pack('>hhhhhhhh',
                        0,
                        0,
                        0,
                        0,
                        0,
                        data1[i],
                        0,
                        0)

                elif channel==6:
                    x = struct.pack('>hhhhhhhh',
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        data1[i],
                        0)

                elif channel==7:
                    x = struct.pack('>hhhhhhhh',
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        data1[i])



                binaryData = binaryData + x

        return binaryData


    def convert128To256(self,datastr128):


        lenbytes = len(datastr128);
        lenword128 = lenbytes / 16;
        lenword256 = lenword128/2;


        stra=''
        strb=''

        cnt_128 = 0

        for cnt_256 in range(lenword256):
            stra = stra + datastr128[cnt_128:(cnt_128+16)]
            cnt_128 = cnt_128 + 16
            strb = strb + datastr128[cnt_128:(cnt_128+16)]
            cnt_128 = cnt_128 + 16

        return((stra,strb))


    def convert128To64(self,datastr128):


        lenbytes = len(datastr128);
        lenword128 = lenbytes / 16;
        lenword64 = lenword128;


        stra=''
        strb=''

        cnt_128 = 0

        for cnt_64 in range(lenword64):
            stra = stra + datastr128[cnt_128:(cnt_128+8)]
            cnt_128 = cnt_128 + 8
            strb = strb + datastr128[cnt_128:(cnt_128+8)]
            cnt_128 = cnt_128 + 8

        return((stra,strb))



    def convertToBinary128(self,data1, data2):
        """ Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

            @param data             Decimal data to be converted  for FPGA.
            """
        binaryData = ''
        for i in range(0, len(data1)/4):


            x = struct.pack('>hhhhhhhh', 
            data1[4*i+self.sample_order[0]], 
            data1[4*i+self.sample_order[1]], 
            data1[4*i+self.sample_order[2]], 
            data1[4*i+self.sample_order[3]],
            data2[4*i+self.sample_order[0]], 
            data2[4*i+self.sample_order[1]], 
            data2[4*i+self.sample_order[2]], 
            data2[4*i+self.sample_order[3]])


            binaryData = binaryData + x

        return binaryData


    def convertFrom128(self,bindata):


        nlongs = len(bindata)/16;

        data0=[]
        data1=[]
        data2=[]
        data3=[]

        data4=[]
        data5=[]
        data6=[]
        data7=[]

        for ptr in range(nlongs):
            longone = bindata[ (ptr*16):(ptr*16+16) ]
            shorts = struct.unpack('>hhhhhhhh',longone)    

            data0.append(shorts[0])
            data1.append(shorts[1])
            data2.append(shorts[2])
            data3.append(shorts[3])

            data4.append(shorts[4])
            data5.append(shorts[5])
            data6.append(shorts[6])
            data7.append(shorts[7])

        return( (data0, data1, data2, data3, data4, data5, data6, data7 )  )

    def convertToBinary128_3(self,
        data0,data1,data2,data3,
        data4,data5,data6,data7):

        """ Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

            @param data             Decimal data to be converted  for FPGA.
            """
        binaryData = ''
        for i in range(0, len(data0)):
            x = struct.pack('>hhhhhhhh', 
            data0[i], 
            data1[i], 
            data2[i], 
            data3[i],
            data4[i], 
            data5[i], 
            data6[i], 
            data7[i])

            binaryData = binaryData + x

        return binaryData



    def convertToBinary128_4(self,
        data0,data1,data2,data3,
        data4,data5,data6,data7):

        """ Converts two successive data points to 16-bit binary and concatenates to one 32-bit word.

            @param data             Decimal data to be converted  for FPGA.
            """
        binaryData = ''
        for i in range(0, len(data0)):
            x = struct.pack('>HHHHHHHH', 
            data0[i], 
            data1[i], 
            data2[i], 
            data3[i],
            data4[i], 
            data5[i], 
            data6[i], 
            data7[i])

            binaryData = binaryData + x

        return binaryData


    def stopSram(self):
        control_reg='%s_control'%self.fwname

        ctrl = (self.rd_toggle<<5) ;
        self.roach.write_int(control_reg, ctrl)

    

    #for setting wave table length to get desired freq resolution
    def setLutSize(self,ls):
         self.lut_length = ls
    

    #for debugging the sram state machine onlu.
    def setLutSizeDBG(self,lutsize_):
        self.lutsize = lutsize_
        lutsize_reg = '%s_LUTSize'%self.fwname
        self.roach.write_int(lutsize_reg, self.lutsize);

    def streamSram(self):
        control_reg='%s_control'%self.fwname
        lutsize_reg = '%s_LUTSize'%self.fwname


        startdac_bit = 0

        ctrl = (self.rd_toggle<<5) ;
        self.roach.write_int(control_reg, ctrl)


        ctrl = ctrl + (1<<startdac_bit);

        self.roach.write_int(control_reg, ctrl)


    def dumpBrams(self,lenx):
        buffmem0_reg = '%s_rambuffer0'%self.fwname
        return(self.roach.read(buffmem0_reg,lenx))


    def dumpSrams(self,which,lenx,issh=False):

        bindata = self.roach.read('qdr%d_memory'%which,lenx)
        if issh:
            shorts = struct.unpack('>%dh'%(lenx/2),bindata)
            return(shorts)

        return(bindata)

 #bindata is bin string, mult of 128 bits long.

    def writeSram(self,bindata):
        if self.which_write=='cpu':
            self.writeSram1(bindata)

        else:
            self.writeSram2(bindata)


    def writeSram1(self,bindata_ab):
        print 'CPU interface'

        (bindata , bindata_b) = self.convert128To64(bindata_ab)

        control_reg='%s_control'%self.fwname
        lutsize_reg = '%s_LUTSize'%self.fwname
        buffmem0 = 'qdr0_memory'
        buffmem1 = 'qdr1_memory'

        startdac_bit = 0


        #in bytes
        datalen=len(bindata)
        #in octobytes    
        datalen_word=datalen/8

        print 'nbytes %d lutsizewords %d'%(datalen, datalen_word)


        #
        #set address speeds of bram and sram
        #
        control = (self.rd_toggle<<7);

        self.roach.write_int(control_reg, control);


        offaddr = 0
        dataptr = 0

        #size of indiv writes in octobytes
        buffsize_word = 64

        #bufsize in bytes
        buffsize = buffsize_word*8

        #the this is address into qdr memory, measured in bytes
        addrinc = buffsize


        #lut size must be datalen_word, or the number of 288 size workds in mem.
        # the 8 is because the sram addr must inc by 8, as lower 3 bits are not used.
        #we add fudge factor because we want the mem to count farther when we are wrting it
        #or else the state machine may overwrite the 1st word... fudge of 16 words
        fudge = 8;
        lutsize = 1*datalen_word + fudge
        self.roach.write_int(lutsize_reg, lutsize);


        while dataptr<datalen:
            #
            #set control to all bits 0 except the rd and wer toggles.
            #
            control = (self.rd_toggle<<7) 
            self.roach.write_int(control_reg, control)

            #get 128 * 16 bytes of data for on bram size of data.
            datawr=bindata[(dataptr):(dataptr+buffsize)]
            datawr_b=bindata_b[(dataptr):(dataptr+buffsize)]




            #
            # write data to brams
            #
            self.roach.write(buffmem0,datawr,offaddr);
            self.roach.write(buffmem1,datawr_b,offaddr)
            #print "write %d bytes: %s at %d"%(len(datawr),datawr[:64],offaddr)
            #print "writeb %d bytes: %s at %d"%(len(datawr_b),datawr_b[:64],offaddr)



            #
            #inc mem ptrs to get next block of data, and next block address in sram
            #

            #inc ptr into the raw data to send to next bram size block
            dataptr= dataptr + buffsize
            #inc the sram mem
            offaddr = offaddr + addrinc




        #lut size must be datalen_word, or the number of 288 size workds in mem.
        # the 8 is because the sram addr must inc by 8, as lower 3 bits are not used.
        # we sub 8 because instead of 256*8 we want 255*8. ordinal numbers..
        lutsize = (datalen_word/self.div_lutlen)-1
        self.lutsize = lutsize
        self.roach.write_int(lutsize_reg, lutsize);



        #bindata is bin string, mult of 128 bits long.

        def writeSram2(self,bindata):


            #(bindata , bindata_b) = self.convert128To64(bindata_ab)

            control_reg='%s_control'%self.fwname
            lutsize_reg = '%s_LUTSize'%self.fwname
            buffmem0_reg = '%s_rambuff0'%self.fwname
            writelen_hexbytes_reg='%s_writeLength'%self.fwname
            offsetaddr_reg = '%s_offsetAddress'%self.fwname

            startdac_bit = 0
            write_bit = 2


            #in bytes
            datalen_bytes=len(bindata)
            #in hexadecabytes    
            datalen_hexbytes=datalen_bytes/16

            print 'nbytes %d lutsizewords %d'%(datalen_bytes, datalen_hexbytes)


            #
            #set address speeds of bram and sram
            #
            control = (self.rd_toggle<<7) + (self.wr_toggle<<5);

            self.roach.write_int(control_reg, control);


            offaddr_hexbytes = 0
            dataptr_bytes = 0

            #size of indiv writes in octobytes
            buffsize_hexbytes = 256
            #the sram offset addr incs by 1  for each 64bit+64bit word
            offset_addrinc_hexbytes = buffsize_hexbytes
            #bufsize in bytes
            buffsize_bytes = buffsize_hexbytes*16



            #
            # write the burst write length
            #
            self.roach.write_int(writelen_hexbytes_reg, buffsize_hexbytes-1);

            #lut size must be datalen_word, or the number of 288 size workds in mem.
            # the 8 is because the sram addr must inc by 8, as lower 3 bits are not used.
            #we add fudge factor because we want the mem to count farther when we are wrting it
            #or else the state machine may overwrite the 1st word... fudge of 16 words
            fudge = 16;
            lutsize_hexbytes = 1*datalen_hexbytes + fudge
            self.roach.write_int(lutsize_reg, lutsize_hexbytes);


            while dataptr_bytes<datalen_bytes:
                #
                #set control to all bits 0 except the rd and wer toggles.
                #
                control = (self.rd_toggle<<7) + (self.wr_toggle<<5);
                self.roach.write_int(control_reg, control)

                #get 256 * 16 bytes of data for on bram size of data.
                datawr=bindata[(dataptr_bytes):(dataptr_bytes+buffsize_bytes)]


                #
                # write data to brams
                #
                self.roach.write(buffmem0_reg,datawr);
                print "write %d bytes: %s"%(len(datawr),datawr[:64])

                #
                # write offset addr in sram
                #
                self.roach.write_int(offsetaddr_reg,offaddr_hexbytes)


                #
                # do the xfer from bram to sram
                #

                control = control + (1<<write_bit)
                self.roach.write_int(control_reg, control)
                time.sleep(0.001)

                control = control - (1<<write_bit)
                self.roach.write_int(control_reg, control)
                time.sleep(0.001)

                #
                #inc mem ptrs to get next block of data, and next block address in sram
                #

                #inc ptr into the raw data to send to next bram size block
                dataptr_bytes= dataptr_bytes + buffsize_bytes
                #inc the sram mem
                offaddr_hexbytes = offaddr_hexbytes + offset_addrinc_hexbytes




            #lut size must be datalen_word,
            # 
            #lutsize_hexbytes = datalen_hexbytes-1;
            lutsize = (datalen_hexbytes/self.div_lutlen)-2
            self.lutsize = lutsize
            self.roach.write_int(lutsize_reg, lutsize_hexbytes);




    def sramTestData(self,chan=7):



        sig3=list('ABCDEFGHIJKLMNOP')

        #convert the chars to ascii values in the list
        sig2=[]
        for ss in sig3:
            ss=ord(ss)
            sig2.append(ss)

        #make it longer, 16*len(sig3) will be 256 items, or 128 256 bit workds
        sig2=numpy.array(sig2*16*self.sram_test_nbuffers)

        #make AA,BB,CC etc. into a 16 bit workd
        sig = sig2*256
        sig = sig + sig2

        data =  self.convertToBinary128_2(sig,chan)
        self.writeSram(data)


    def sramTestData2(self,rlen = 128):



        bindata = self.convertToBinary128_3(\
        numpy.arange(rlen),
            128+numpy.arange(rlen),
            2*128+numpy.arange(rlen),
            3*128+numpy.arange(rlen),
            4*128+numpy.arange(rlen),
            5*128+numpy.arange(rlen),
            6*128+numpy.arange(rlen),
            7*128+numpy.arange(rlen))

        self.testdata = bindata

        self.writeSram(bindata)



    def reverseBits(self,data):
        data2=[]
        for d in data:
            d2 = int(bin(d)[:1:-1], 2)
            data2.append(d2)
        return(data2)

    ############################################3
    #
    ########################################33            

    #get freq resultion of lut
    def getResolution(self):
        resolution = self.dac_clk/self.lut_length
        return(resolution);


