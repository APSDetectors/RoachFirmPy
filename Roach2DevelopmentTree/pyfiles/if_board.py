

"""
for i in range(500): if_board.progIfBoard(); time.sleep(.5)

#toggle a bit on.off for 120sec, so we can look at it on scope 
if_board.freqToBit(5,120.0)



if_board.progLocalOsc(if_board.LO,if_board.lo_sle)

if_board.progLocalOsc(if_board.s,if_board.clk_sle)


for i in range(500): if_board.progLocalOsc(if_board.s,if_board.clk_sle); time.sleep(0.5)







execfile('if_board.py')
if_board=ifBoard(roach2,'if_board')


if_board.LO.setFreq(3500e6)

if_board.rf.lo_source = 1

if_board.rf.baseband_loop=0
if_board.progIfBoard()

if_board.rf.report()


#sram.setLutFreqs(arange(10e6,100e6,10e6),3000)

#sram.setLutFreqs(10e6,30000)

if_board.oscdata


if_board.fillOscFreqRam(3000e6,7000e6,bigendian=True,isflip=True)
if_board.zeroFreqAddr()



#read back some ram...
roach2.read_int('if_board_LoFreqOscReg01',0)



#roach2.write('if_board_LoFreqOscReg0','AABBCCDDEEFFGGHH',0);

#aa=roach2.read('if_board_LoFreqOscReg0',32,0);

roach2.write_int('PulseTrain_numpulses',1000);roach2.write_int('PulseTrain_waitclks',1.0*128e6)

#settings_reg
# 0 na
# 1 pulse train en
# 2 pulse train trig
# 3 wrLoFreq



if_board.zeroFreqAddr()

if_board.setFreqAddr(0)

if_board.oscdata['rfoutfreq'][20]

if_board.setFreqAddr(40)

roach2.write_int('settings_reg',0);roach2.write_int('settings_reg',8);roach2.write_int('settings_reg',0)


for k in range(800): roach2.write_int('settings_reg',1);roach2.write_int('settings_reg',5); time.sleep(.01); print k

r = if_board.oscdata['rdata'][0]
if_board.wr32bit(r,if_board.lo_sle)

















"""


#import matplotlib.pyplot as plt
import struct
from numpy import *
import time,fractions, math,inspect,random

import threading
import copy as ccopy
import pickle
import traceback

import scipy.io


###########################################################################3
# class for controlling if board serial download
# expects FW with  if_board  block
#also has mutex for roach board, so only process can program it
##########################################################################



#
# global mutex for roach board. so onluy one thread can program it 
#






########################################################################
#
#
#
#
#######################################################################

class attenSetting:

    def __init__(self):
    
        #range = 0-31.5 dB; attenuation from DAC to RF_output
        self.atten_U6= 3
        self.atten_U7= 3
        
        
        
        
        #range = 0-31.5 dB; attenuation from RF_input to AD
        self.atten_U28=3
        
        
        #ser data floes from U6,7,28. So we send 28, then 7, then 6
        
        self.reg_U28=0
        self.reg_U6=0
        self.reg_U7=0
        
        self.setAtten()
        
    

    def setAtten(self):
        
        self.reg_U28=63-int(2.0*self.atten_U28)
        self.reg_U6=63-int(2.0*self.atten_U6)
        self.reg_U7=63-int(2.0*self.atten_U7)
        
    def report(self):
        contents= inspect.getmembers(self)
        for c in contents:
             print c
    
    


########################################################################
#class that has all register and bit settings in ADF4350 PLL chip on IF board.
#each bit/reg has a field in the class you can change to set up the pll
#calcNumbers method sets frac,int, mod, divsel for setting full range on
#pll.
# give req frequency in Hz in the ocnstructor.
# of you chage self.f, the req freeq, you must run self.calcNumbers() to
#recalc the int, frac, mod clkdiv settings.
#pass object to function progLocalOsc to prog the pll chip on IF /Roach
#######################################################################

class clkGenSetting:

    def __init__(self,freq):

        
        #actual freq of rf output
        self.rfout_freq=0
        
        #req frequncy
        self.f=freq;
        #approx freq of vco
        self.f_vco=freq;
        
        self.REFin=10e6
        
        #ref freq div/2
        self.T = 0
        #ref freq double
        self.D = 0
        #ref freq div /R
        self.R = 1
        #fres in Hz
        self.fres=10000
       
        self.lonoise=0;
        #1 to use VCO raw rf in pll. 0 to use /16 divider.
        self.feedbacksel=1;
            #dub buff reg4 if set to 1. leave at 0.
        self.doubbuff=0
        #phase term=-== just set to 1
        self.PHASE = 1
        #reset counters in pll
        self.cntrst=0
        self.ldf=0;
        #power down chip
        self.pd = 0
        
        self.csr=0
        #0,1,2,3,4. VCO output to RF, Aux by 1,2,4,8, 16 for lower freq
        self.divsel=0;
        #1 to mute rf when lock lost
        self.mtld=0;
        #sel raw vco or div. vco on aux output
        self.auxoutsel=0
        
        #rf output power
        self.power = 1
        #aux output power
        self.aux_power = 1
        #3 for ref clk, 4 for vco/N  0 for gnd.
        self.MUX = 3
        #1 for lockdetect, 0 for trist LD output lin. 1 for gnd, 2 for hi?
        self.LOCK_DETECT = 1
        #en aux rf output
        self.auxouten=1
        #enable rf output
        self.rfouten=1
        #trustate the ch pumnp output
        self.cptrist=0;

        #0 or 1. 5/6 or 7/8 or something like that.
        self.prescale=1
        #1 for VCO piower down
        self.vcopd = 0

    
        #time delayt for testing to see if we have lock.     
        self.clkdiv8=80
        
        self.clkdiv12=150
        #charge pump current
        self.cpcurrent=7
        
        self.ldp=1;
        #phase detect polarity.
        self.pdpol=1
        
        #min/max vco freq
        self.vco_max = 4400e6
        self.vco_min =2200e6
        
        self.calcNumbers()
        
        print "use obj.report() to report settings"

    def report(self):
        contents= inspect.getmembers(self)
        for c in contents:
             print c

    def setFreq(self,freq):
    
        self.f=freq;
        
        self.f_vco=freq;
        self.calcNumbers()
    
    def calcNumbers(self):
        self.f_pfd = self.REFin * ( (1+self.D)/(self.R * (1+self.T))  )
        print "f_pfd = %f"%(self.f_pfd)
    
    
        #VCO from 2200MHz to 4400MJHz
        #figure out the divsel based on what req. f is.
        self.divsel=0
      
        
        
        if (self.f< (self.vco_min/16)  ):
            self.f= self.vco_min/16
        
        #f is req freq from 137MJHz to 4.4GHz
        while(self.f <  (self.vco_min/ (1 << self.divsel) ) ):
            self.divsel = self.divsel + 1
        
        print "req freq %d  divsel %d "%(self.f,self.divsel)
        
        
        self.f_vco=self.f * (1<<self.divsel)
        
        print "f_vco %d"%(self.f_vco)
        
        
        self.INT = int(self.f_vco)/int(self.f_pfd)
        
        #self.MOD = int(self.REFin / self.fres)
        
        self.MOD = 4000
        self.fres = self.REFin/ self.MOD
        
        self.FRAC = int(round(self.MOD*(self.f_vco/self.f_pfd-self.INT)))
       

        if self.FRAC != 0:
            self.gcd = fractions.gcd(self.MOD,self.FRAC)
            if self.gcd != 1:
                self.MOD = self.MOD/self.gcd
                self.FRAC = int(self.FRAC/self.gcd)

        print 'INT %d\n'%(self.INT)
        print 'FRAC %d \n'%(self.FRAC)
        print 'MOD %d\n'%(self.MOD)
    
        self.rfout_freq=self.f_pfd * (self.INT + (self.FRAC/self.MOD))



#######################################################################
#
# class that holds info about the state of rf switches on if board.
#
#
#########################################################################


class rfSwitchSetting:

    def __init__(self):

        #local osc, interal/n_external
        #1 for internal
        self.lo_internal=1
        #rf loopback
        self.rf_loopback = 0
        #local osc source- lo doubler
        #source set to 1 is source A. Use A. pin 8 input
        self.lo_source = 1
        #baseband loop- set to 1 for BB loop
        self.baseband_loop=0
        
        #clock internal / n_external
        #controls source of ADC/DAC clock. 
        #internal is local osc. external is a jack n if board.
        #set internal to 1 fore interal OSC
        self.clk_internal=1
        
    def report(self):
        contents= inspect.getmembers(self)
        for c in contents:
             print c





#########################################################################
# class for if board control
#
#
############################################################################

class ifBoard:

    def __init__(self,roach_,fw_block_name_):

        self.roach=roach_
        self.fw_block_name = fw_block_name_

        self.sw_stb=0
        self.ser_clk=1
        self.ser_di=2
        self.lo_sle=3
        self.swat_le=4
        self.clk_sle=5

        self.endian='big'
        self.invclk=True

        self.n_atten_bits=18


        #
        # Saved settings of the if_board
        #


        self.dac_clk_freq=512e6


        self.rf=rfSwitchSetting()



        print "INT CLOCK"
        self.rf.clk_internal=1

        print "BB LOOP ON"
        self.rf.baseband_loop=1
        self.rf.rf_loopback=0
        print "INT LO"
        self.rf.lo_internal=1
        self.rf.lo_source=0


        self.at=attenSetting()
        self.at.atten_U28=0.0
        self.at.atten_U6=15.0
        self.at.atten_U7=0.0    


        #clock for dacs/fpga
        self.s= clkGenSetting(self.dac_clk_freq)
        #lo freq
        self.LO= clkGenSetting(3500e6)



    #
    # prog RF, osc and atten.
    #

    def progIfBoard(self):

        self.progLocalOsc(self.LO,self.lo_sle)

        self.progLocalOsc(self.s,self.clk_sle)


        self.progRFSwitches(self.rf)




        self.progAtten(self.at)

        self.progRFSwitches(self.rf)    


    def freqToBit(self,bit,timesec):

        starttime = time.time()

        endtime = starttime + timesec
        while time.time()<endtime:
            regval = (1<<bit)
            self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
            regval = 0
            self.roach.write_int('%s_regs'%(self.fw_block_name), regval)


    ########################################################################
    #write 32 bit number in sp1 format. generate all clocks. set global self.endian to 'big' or 'little'
    #if board needs big endien for pll chips.
    #can send inverted clock by settignb self.invclk to True. Should use False for IF board.
    #tell which load bit. use self.clk_sle or lo_osc for the pll chuiops.
    #sets that load bit low, all otheres high, during sending. then raises the load buit and
    #pulses 2 more clokcs.
    #######################################################################

    def wr32bit(self,data,lebit):


        #setup for raw ser write.
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 1)


        for b in range(32):
            if self.endian=='big':
                bitmask = 1<<(31-b)
            else:
                bitmask = 1<<b

            if data&bitmask!=0:
                bitval = 1;
            else:
                bitval=0;    

            #clk is low. all le bits are high. at must be low..
            regval=(0<<self.clk_sle)+(0<<self.swat_le)+(0<<self.lo_sle)+ \
                (int(bitval)<<self.ser_di)+(0<<self.ser_clk)
                
           

            #make a version w/ the serial clock hi
            regvalclk=regval | (1<<self.ser_clk)

            if self.invclk==False:
                self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
            else:

                self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)

        #now give 2 clocks w/ the le high, and databit low.

        #lebit is hi .
        bitval=0
        regval=(0<<self.clk_sle)+(0<<self.swat_le)+(0<<self.lo_sle)+ \
            (int(bitval)<<self.ser_di)+(0<<self.ser_clk)

        regval = regval | (1<<lebit)

        regvalclk=regval | (1<<self.ser_clk)



        if self.invclk==False:

            self.roach.write_int('%s_regs'%(self.fw_block_name), regval)

        else:

            self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)





        #lebit is low. .
        bitval=0
        regval=(0<<self.clk_sle)+(0<<self.swat_le)+(0<<self.lo_sle)+ \
                (int(bitval)<<self.ser_di)+(0<<self.ser_clk)



        regvalclk=regval | (1<<self.ser_clk)



        if self.invclk==False:

            self.roach.write_int('%s_regs'%(self.fw_block_name), regval)

        else:

            self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)






    

########################################################################
#
#
#######################################################################


    def bitOffOnOff(self,bit):

        #setup for raw ser write.
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 1)


        regval=0
        self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
        regvalclk=regval | (1<<bit)
        self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)
        self.roach.write_int('%s_regs'%(self.fw_block_name), regval)


    

########################################################################
# prog the PLL chip. sengs derial data to roach if board. use slow sening
#with if_swith off. so puthon gen each clock pulse from sw.
# pass roach, the refernece to the roach katcp connection.
#pass sets, a clkGenSetting object with all pll settings therein
#pass a bit to toggle, the load en bit. there are 2 chopices., self.clk_sle, or self.lo_sle
#for the clk pll or local osc pll on the of board. these 2 choisec defined at
#top of theis file.
#######################################################################


    def progLocalOsc(self,sets,loadbit,is_write = True):
    


        # initialize LO to 3 GHz
        #f = 3.0e9 
        # step of LO setup have to be 2.5 Khz
        #f = 3206345000.0




        #shifts for reg 0
        control_bits=0
        int_bits=15
        frac_bits=3

        #reg 1
        mod_bits = 3
        phase_bits=15
        prescale_bits=27


        #reg2
        cntrst_bits=3
        cptristb=4
        pd_bits=5
        pdpolb=6
        ldp_bits=7
        ldf_bits=8
        cpcurrentb=9
        doubbuffb=13
        cnt10bit=14
        rdiv2=24
        refdoub=25
        muxout=26
        lonoiseb=29


        #reg3
        clkdiv12bit=3
        clkdivmode=15
        csr_bits=18


        #reg4
        outpower_bits=3
        rfout_en_bits=5
        auxoutpower_bits=6
        auxouten_bits=8
        auxoutselb=9
        mtldb=10
        vcopdb=11
        clkdiv8bit=12
        divselb=20
        feedbackselb=23


        #reg5
        lockdet_bits = 22





        reg5 = (sets.LOCK_DETECT<<lockdet_bits) + (5<<control_bits)


        reg4 = (sets.feedbacksel<<feedbackselb) + (sets.clkdiv8<<clkdiv8bit) + (sets.auxouten<<auxouten_bits)     
        reg4= reg4  + (sets.aux_power<<auxoutpower_bits) + (sets.rfouten<<rfout_en_bits) 
        reg4 = reg4 + (sets.power<<outpower_bits) + (sets.vcopd<<vcopdb) + (4<<control_bits)
        reg4 = reg4 + (sets.divsel<<divselb) + (sets.mtld<<mtldb) + (sets.auxoutsel<<auxoutselb)

        reg3 = (sets.clkdiv12<<clkdiv12bit)  + (3<<control_bits)+ (sets.csr<<csr_bits)


        reg2 = (sets.MUX<<muxout) + (sets.R<<cnt10bit) 
        reg2=reg2 + (sets.cpcurrent<<cpcurrentb) + (sets.ldp<<ldp_bits) + (sets.T<<rdiv2)
        reg2 = reg2 + (sets.pdpol<<pdpolb) + (sets.D<<refdoub) +(2<<control_bits) + (sets.lonoise<<lonoiseb)
        reg2=reg2 + (sets.doubbuff<<doubbuffb) + (sets.ldf<<ldf_bits) + (sets.pd<<pd_bits)
        ret2 = reg2 + (sets.cptrist<<cptristb) + (sets.cntrst<<cntrst_bits)

        reg1 = (sets.prescale<<prescale_bits) + (sets.PHASE<<phase_bits) + (sets.MOD<<mod_bits) 
        reg1 = reg1 + (1<<control_bits)



        reg0 = (sets.INT<<int_bits) + (sets.FRAC<<frac_bits) + (0<<control_bits)

        regs = [reg5, reg4, reg3, reg2, reg1, reg0]

        self.oscregs = regs

        if is_write:
            for r in regs:
                print r

                self.wr32bit(r,loadbit)




        print '...done programming LO'



########################################################################
#
# convert 0xaaaaaaaa to 0x55555555, or 0x00000001 to 0x80000000
#
########################################################################

    def flipBitsInt(self,val):
        newval = 0
        for bpos in range(32):
            bit = val & (1<<bpos)
            if bit!=0:
                newval = newval | (1<<(31-bpos))
    
        return(newval)
    
    
########################################################################
#
#
#
########################################################################

    def fillOscFreqRam(self,startfreq,endfreq,isflip=True, bigendian=True):
    
        incfreq = (endfreq-startfreq)/1024.0;
    
        freqs = arange(startfreq,endfreq, incfreq )

        bindata = ''
        addr = 0
        rdata = []
        rfout= []
        for f in freqs:
            self.LO.setFreq(f)
            self.progLocalOsc(self.LO,self.lo_sle,is_write = False)
            reg0 = self.oscregs[5];
            reg1 = self.oscregs[4];
            rfout.append(self.LO.rfout_freq)
            #print reg0

            if isflip:
                reg0flip = self.flipBitsInt(reg0)
                reg1flip = self.flipBitsInt(reg1)
            else:
                reg0flip =reg0
                reg1flip =reg1


            if bigendian:
                bindata = bindata + struct.pack('>I',reg0flip)
            else:
                bindata = bindata + struct.pack('<I',reg0flip)


            if bigendian:
                bindata = bindata + struct.pack('>I',reg1flip)
            else:
                bindata = bindata + struct.pack('<I',reg1flip)


            rdata.append(ccopy.deepcopy(self.oscregs))
            #self.roach.write_int('%s_LoFreqOscReg0'%(self.fw_block_name),reg0,addr)
            addr = addr+4

        self.oscdata = {'incfreq':incfreq, 'freqs':freqs,'bindata':bindata,'rdata':rdata,
                'bigendian':bigendian, 'isflip':isflip, 'rfoutfreq':rfout}


        #self.roach.write('%s_LoFreqOscReg0'%(self.fw_block_name),bindata)
        self.roach.big_write('%s_LoFreqOscReg01'%(self.fw_block_name),bindata)


########################################################################
#
#
#
########################################################################

        
    def zeroFreqAddr(self):
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 2)    
        self.roach.write_int('%s_regs'%(self.fw_block_name),0)
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 0)    
        self.roach.write_int('%s_reg1WrWait'%(self.fw_block_name), int(0.001*128e6))    


    def setFreqAddr(self,addr):
        #reset addr cnt
        #self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 2) 
        self.roach.write_int('%s_ramaddrset'%(self.fw_block_name),addr)
        #load addr to addr counter
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 4)    
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 0)    


        #sero serial data reg   
        self.roach.write_int('%s_regs'%(self.fw_block_name),0)
        #set if sw to 0 for fast serial data
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 0)    
        #write time delay for 2nd reg send to 0.001s
        self.roach.write_int('%s_reg1WrWait'%(self.fw_block_name), int(0.001*128e6))    


########################################################################
#
#
#
########################################################################


    def progRFSwitches(self,rfsets):


        #setup for raw ser write.
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 1)


        regbase = (0<<self.clk_sle) + (0<<self.swat_le) + (0<<self.lo_sle) 

        #send internal/ext clock source
        regval = regbase  + ( (rfsets.clk_internal)<<self.ser_di)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval + (1<<self.ser_clk))
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)


        #send base band loop
        regval = regbase  + (rfsets.baseband_loop<<self.ser_di)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval + (1<<self.ser_clk))
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)

        #local osc doubler- source
        regval = regbase  + (rfsets.lo_source<<self.ser_di)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval + (1<<self.ser_clk))
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)

        #send rfloopback
        regval = regbase  + ((1-rfsets.rf_loopback)<<self.ser_di)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval + (1<<self.ser_clk))
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)

        #send internal/ext local osc source
        regval = regbase  + ((1-rfsets.lo_internal)<<self.ser_di)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval + (1<<self.ser_clk))
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)



        #clockl out the data- 
        regval = (0<<self.clk_sle) + (0<<self.swat_le) + (0<<self.lo_sle) + \
            (0<<self.ser_di) + (0<<self.ser_clk)

        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval + (1<<self.sw_stb))

        self.roach.write_int('%s_regs'%(self.fw_block_name),regval)
        self.roach.write_int('%s_regs'%(self.fw_block_name),regval + (0<<self.sw_stb))



#execfile('t_brdconfig.py')

    
    
########################################################################
#
#
#
#
#######################################################################

    def progAtten(self,attenset):


        #setup for raw ser write.
        self.roach.write_int('%s_settings_reg'%(self.fw_block_name), 1)


        attenset.setAtten()

        

        if self.invclk==False : 
            clkvalue = 0
        else: 
            clkvalue = (1<<self.ser_clk)
        

        regval = (0<<self.swat_le) + (0<<self.lo_sle) + (0<<self.clk_sle) + \
                (0<<self.ser_di) + clkvalue +  (0<<self.sw_stb)
                
        self.roach.write_int('%s_regs'%(self.fw_block_name), regval)

        if self.endian=='big':
            u28=self.flipEndian(attenset.reg_U28,6)
            u6=self.flipEndian(attenset.reg_U6,6)
            u7=self.flipEndian(attenset.reg_U7,6)
        else:
            
            u28=attenset.reg_U28
            u6=attenset.reg_U6
            u7=attenset.reg_U7
            
        
        data = (u28<<0)+(u7<<6)+(u6<<12)

        for b in range(self.n_atten_bits):
            bitmask = 1<<b
  

            if data&bitmask!=0:
                bitval = 1;
            else:
                bitval=0;    

            #clk is low. all le bits are high.
            regval=(0<<self.clk_sle)+(0<<self.swat_le)+(0<<self.lo_sle)+ \
                    (int(bitval)<<self.ser_di)+(0<<self.ser_clk)+(0<<self.sw_stb)
                    
          

            #make a version w/ the serial clock hi
            regvalclk=regval | (1<<self.ser_clk)

            if self.invclk==False:
                self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
                #print bin(regval)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)
                #print bin(regvalclk)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
                #print bin(regval)
            else:

                self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)
                #print bin(regvalclk)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
                #print bin(regval)
                self.roach.write_int('%s_regs'%(self.fw_block_name), regvalclk)
                #print bin(regvalclk)



        if self.invclk==False : 
            clkvalue = 0
        else: 
            clkvalue = (1<<self.ser_clk)
        
        regval =(0<<self.clk_sle)+ (0<<self.swat_le)+(0<<self.lo_sle)+ \
                (0<<self.ser_di)+clkvalue+(0<<self.sw_stb)
                
        self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
        #print bin(regval)

        regval =(0<<self.clk_sle)+ (1<<self.swat_le)+(0<<self.lo_sle)+ \
                (0<<self.ser_di)+clkvalue+(0<<self.sw_stb)
                
        self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
        #print bin(regval)


        regval =(0<<self.clk_sle)+ (0<<self.swat_le)+(0<<self.lo_sle)+ \
                (0<<self.ser_di)+clkvalue+(0<<self.sw_stb)
                
        self.roach.write_int('%s_regs'%(self.fw_block_name), regval)
        #print bin(regval)



        #self.roach.write_int('%s_if_switch'%(self.fw_block_name), 0)



    def flipEndian(self,val,nbits):
    
        val2=0
        
        for k in range(nbits):
            bpos = 1<<k
            bpos2=1<<( (nbits-1) - k)
            if val&bpos > 0:
                val2 = val2 + bpos2
        return(val2)
            




