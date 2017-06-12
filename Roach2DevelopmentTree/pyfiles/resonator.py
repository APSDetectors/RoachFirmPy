'''
execfile('resonator.py')

'''

import os

import scipy        
import scipy.linalg
import mpfit

import struct
from numpy import *
import time,fractions, math,inspect,random
import threading

import numpy

import h5py


print "Loading resonator.py"


#seed rand num gen when loading  module
random.seed()


#
# global list of MKID objects
#

MKID_list=[]



#
# read a list of freqs in python [ 5e9, 5.1e9]. make MKID_list
#

def pyListToMkidList(pylist,multiplier=1.0):
    global MKID_list
    MKID_list = []
    n = 0
    for f in pylist:
        m = MKID(N=n,fc=f*multiplier)
        n = n+1
        MKID_list.append(m)

#
# read a list of freqs in python resonator_freqs = [ 5e9, 5.1e9]. make MKID_list
#


def pyListFileToMkidList(fname):
    execfile(fname)
    pyListToMkidList(resonator_freqs)


def mkidList2(mlist):
        for m in mlist:
                print "\n--------------------------------------------------------\n"
                print 'Res %d  fc %4.1fMHz'%(m.resonator_num, m.rough_cent_freq/1e6)



def mkidList():
        k=0
        for m in MKID_list:
                print "\n--------------------------------------------------------\n"
                print 'Res %d  fc %4.1fMHz'%(m.resonator_num, m.rough_cent_freq/1e6)
                print 'MKID_list[%d]'%(k)
                k=k+1



def mkidList2Str2():
    strx = 'mdir={'
    for m in MKID_list:                
        strx = strx+ '%d:%f,'%(m.resonator_num, m.rough_cent_freq)   
    strx = strx[:-1]  + '}'                    
    return(strx)
    


def mkidList2Str():
    strx = '['
    for m in MKID_list:                
        strx = strx+ '%5.2f,'%(m.rough_cent_freq/1e6)   
    strx = strx[:-1]  + ']'                    
    return(strx)

    
def mkidList2Pickle():
    strx = pickle.dumps(MKID_list)
    return(strx)
    
    
             
                    
def mkidDump():
        for m in MKID_list:
                print "\n-----------------------------------------------------------\n"
                print 'Res %d  fc %4.1fMHz'%(m.resonator_num, m.rough_cent_freq/1e6)                
                
                for r in m.reslist:
                        print "\n###########\n"
                        r.info()


def mkidDump2(mlist):
        for m in mlist:
                print "\n-----------------------------------------------------------\n"
                print 'Res %d  fc %4.1fMHz'%(m.resonator_num, m.rough_cent_freq/1e6)                                
                for r in m.reslist:
                        print "\n###########\n"
                        r.info()


def mkidGetFreqs():
    flist=[]
    for m in MKID_list:
        flist.append(m.getFc2()) 
    return(flist)
    
              

#
# Save all resonators to resonator file in MKID_list                        
   
   
def mkidSaveData(filename):  
    hdf = hdfSerdes()
    hdf.open(filename,'w')
    hdf.write(MKID_list,'MKID_list')
    hdf.close()
    


def mkidLoadData(filename):
    global MKID_list
    
    hdf = hdfSerdes()
    
    hdf.open(filename,'r')
    MKID_list = hdf.read()
    hdf.close()
    
             
"""

        
def mkidSaveData(filename):

        if len(MKID_list)==0:
            return(-1)
            
        fp=h5py.File(filename,'w')
        
                    
        devgrp=fp.create_group('Device_%s'%(MKID_list[0].chip_name))
        
        devgrp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
        
        for m in MKID_list:
            
            resgrp=devgrp.create_group('Resonator_%d'%(m.resonator_num))
            resgrp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
            fc=resgrp.create_dataset("Freq_Cent", (1,), dtype='f8', maxshape=(None))
            
            fc[0]=m.rough_cent_freq

            pfat=resgrp.create_dataset("preferred_out_atten", (1,), dtype='f8', maxshape=(None))
            pfat[0]=m.preferred_out_atten

            pfat2=resgrp.create_dataset("preferred_return_atten", (1,), dtype='f8', maxshape=(None))
            pfat2[0]=m.preferred_return_atten

            
            sweep=0
            
            for r in m.reslist:
                r.info()
                r.writeHDF(resgrp,sweep)
                sweep=sweep+1
            
        fp.flush()    
           
        fp.close()    


#
# save one MKID object to file
#                
                        
        
def mkidSaveDataOne(filename,mkid):

        if len(MKID_list)==0:
            return(-1)
            
        fp=h5py.File(filename,'w')
        
                    
        devgrp=fp.create_group('Device_%s'%(MKID_list[0].chip_name))
        devgrp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
        
        m=mkid

        resgrp=devgrp.create_group('Resonator_%d'%(m.resonator_num))
        resgrp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
        
        fc=resgrp.create_dataset("Freq_Cent", (1,), dtype='f8', maxshape=(None))

        fc[0]=m.rough_cent_freq


        pfat=resgrp.create_dataset("preferred_out_atten", (1,), dtype='f8', maxshape=(None))
        pfat[0]=m.preferred_out_atten

        pfat2=resgrp.create_dataset("preferred_return_atten", (1,), dtype='f8', maxshape=(None))
        pfat2[0]=m.preferred_return_atten



        sweep=0

        for r in m.reslist:
            r.info()
            r.writeHDF(resgrp,sweep)
            sweep=sweep+1
            
        fp.flush()    
           
        fp.close()    



                
def mkidSaveList(filename):

        if len(MKID_list)==0:
            return(-1)
            
        fp=h5py.File(filename,'w')            
        
                    
        devgrp=fp.create_group('Device_%s'%(MKID_list[0].chip_name))
        devgrp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
        
        for m in MKID_list:
            
            resgrp=devgrp.create_group('Resonator_%d'%(m.resonator_num))
            resgrp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
            
            fc=resgrp.create_dataset("Freq_Cent", (1,), dtype='f8', maxshape=(None))
            
            fc[0]=m.rough_cent_freq
            pfat=resgrp.create_dataset("preferred_out_atten", (1,), dtype='f8', maxshape=(None))
            pfat[0]=m.preferred_out_atten

            pfat2=resgrp.create_dataset("preferred_return_atten", (1,), dtype='f8', maxshape=(None))
            pfat2[0]=m.preferred_return_atten


        

        
            
        fp.flush()    
           
        fp.close()    



def mkidLoadList(filename):
        global MKID_list
        global MKID_list_save
        
        MKID_list_save=MKID_list
        
        MKID_list=[]
            
        fp=h5py.File(filename,'r')            

        devgrp=None
        
        for k in fp.keys():
            if k[0:6]=='Device':
                devgrp=k
        
        if devgrp==None:
            print "No device data"
            fp.close()
            return(-1)
            
        device_name=devgrp[7:].encode('utf8')


        #cycle through Resonator_x
        for k in fp[devgrp].keys():
        
            resnum=int(k[10:])
        
        
            resgrp=k

            fc =fp[devgrp][resgrp]['Freq_Cent'][0]
                        
            m=MKID(resnum,device_name,fc)
        
            try: m.preferred_out_atten=fp[devgrp][resgrp]['preferred_out_atten'][0]
            except:pass

            try: m.preferred_return_atten=fp[devgrp][resgrp]['preferred_return_atten'][0]
            except:pass
         
            
            MKID_list.append(m)
            
           
        fp.close()    


def mkidLoadData(filename):
        global MKID_list
        global MKID_list_save
        
        MKID_list_save=MKID_list
        
        MKID_list=[]
            
        fp=h5py.File(filename,'r')            

        devgrp=None
        
        for k in fp.keys():
            if k[0:6]=='Device':
                devgrp=k
        
        if devgrp==None:
            print "No device data"
            return(-1)
            
        device_name=devgrp[7:].encode('utf8')


        #cycle through Resonator_x
        for k in fp[devgrp].keys():
        
            resnum=int(k[10:])
        
        
            resgrp=k

            fc =fp[devgrp][resgrp]['Freq_Cent'][0]
                        
            m=MKID(resnum,device_name,fc)
            
            try: m.preferred_out_atten=fp[devgrp][resgrp]['preferred_out_atten'][0]
            except:pass

            try: m.preferred_return_atten=fp[devgrp][resgrp]['preferred_return_atten'][0]
            except:pass


            
            MKID_list.append(m)
            
            
            for rd in fp[devgrp][resgrp].keys():
                    if rd[0:7]=='ResData':
                
                        grprnum=int(rd[8:])   
                    res=resonatorData(resnum,device_name)
                    res.readHDF(fp[devgrp][resgrp],grprnum)
                    res.parent_mkid = m
                    m.reslist.append(res)
                    
            m.preferred_trace = m.findTracePrefAtten()    
           
        fp.close()    





def HDFR_List(filename):
        hdffile_r = h5py.File(filename,'r')

        devdir=hdffile_r.keys()[0]


        settings=[]
        print '-----Resonators---------'
        for k in hdffile_r[devdir].keys(): 
            print ' '
            print k
            print "    Fc %4.1fMHz"%(hdffile_r[devdir][k]['Freq_Cent'][0]/1e6)
            
            try:print "    PrefAtten %4.1fdB"%(hdffile_r[devdir][k]['PrefAtten'][0])
            except:pass
            
            print '\n    --------Traces---------\n'
        
            for k2 in hdffile_r[devdir][k].keys():
                if (k2!= 'Freq_Cent' and k2!= 'PrefAtten'):
                    print '    %s'%(k2)
                    
                    
                    if len(settings)==0:
                      for k3 in hdffile_r[devdir][k][k2].keys():
                        settings.append(k3)
                        


        if (len(settings)!=0):
            print "\n\n---------Trace Settings------------"
            for s in settings:
              print "    %s"%(s)


            
        hdffile_r.close()


MKID_list =


def HDFR_getSettings(filename, resnum,mysetting):


            
        hdffile_r = h5py.File(filename,'r')

        devdir=hdffile_r.keys()[0]


        setting=[]
        
        
        resgrp='Resonator_%d'%(resnum)
        
        

        #go thru traces
        for k2 in hdffile_r[devdir][resgrp].keys():
            if k2!= 'Freq_Cent':
                

                
                setting.append(hdffile_r[devdir][resgrp][k2][mysetting][0])

            
        hdffile_r.close()

        return(array(setting))




def HDFR_readIQ(filename, resnum,tracenum):



        hdffile_r = h5py.File(filename,'r')

        devdir=hdffile_r.keys()[0]

        resgrp='Resonator_%d'%(resnum)



        #go thru traces


        trgrp='ResData_%d'%(tracenum)

        i = hdffile_r[devdir][resgrp][trgrp]['iqdata'][0]
        q = hdffile_r[devdir][resgrp][trgrp]['iqdata'][1]
        f = hdffile_r[devdir][resgrp][trgrp]['freqs'][:]

        hdffile_r.close()

        return( (i,q,f) )

"""

########################################################################
#
# This class is a list of resonatorData obj associated w/ one resonator on one chip
#
#
#######################################################################

class MKID:
    def __init__(self,N=0,cname='nutty',fc=3e9):
        self.resonator_num=N
        self.chip_name=cname
        
        self.manual_cent_freq=0
        
        self.rough_cent_freq=fc
        #no preferred attane set for -1/ preferred atten is the atten we want to run the 
        #the mkid at. That is, total inpuyt power, measured by atten. atten is sum of atten from
        #two atten on IF board, and atten of amp in sine lookup table
        #proper output signal atteunation uncl U6,7 and sinewave amp rel to fill scale.
        #in +dB
        self.preferred_out_atten=-1;
        #pref out atten + U28 ret atten in dB
        self.preferred_return_atten=-1;
        #reference to the resonatorData obj that user picekd as proper attenation- this is the resdata that
        #has the pref attens
        self.preferred_trace = -1;
        
        self.reslist=[]

        #remember if the user checked this in the gui...
        self.checked=0

    def clearResList(self):
        self.reslist=[]
        
    def removeRes(self,res):
        self.relist.remove(res) 

    #return resonatorData obj ref that has same attenations as preferred atten in MKID obj.
    def findTracePrefAtten(self):
    
        for res in self.reslist:
            (atout, atret)=res.calcTotalAttenDb()
            if (atout==self.preferred_out_atten) and (atret==self.preferred_return_atten):
                return(res)
                
        return(-1)
            
            
            
    def setResPrefAtten(self,res):
    
        (self.preferred_out_atten , self.preferred_return_atten) = \
                res.calcTotalAttenDb()
                
                
        self.preferred_trace = res        
        
        for rr in self.reslist:
                rr.is_pref_atten = 0
                
        
        res.is_pref_atten=1;
            
                
    def addRes(self,res):
            self.reslist.append(res)
            res.resonator_num=self.resonator_num
            #res.parent_mkid = self
            

    def clearResList(self):
            self.reslist=[]


    def listResonators(self):
            for rr in self.reslist:
                    rr.info()


    def addResList(self,rl):
            for r in rl:
                self.reslist.append(r)
                r.resonator_num=self.resonator_num

                
  
    def report(self):
        contents= inspect.getmembers(self)
        for c in contents:
            print c

 
    def report2(self):
        contents= inspect.getmembers(self)
        return(contents)
        
    #return fitted center freq for preferred atten. use max vel freq calc.         
    def getFc2(self):
        if len(self.reslist)>0:
            if self.preferred_out_atten<=0.0:
                #no set preferred attan, so use 1st trace.
                res=self.reslist[0]
                return(res.getFc())
                
                
                
        
        else: 
            return(self.getFc())
            
            
    #return rough cent freq of mkid        
    def getFc(self):
        if self.manual_cent_freq!=0.0:
            return(self.manual_cent_freq)
        else:
            return(self.rough_cent_freq)

    def getResNum(self):
            return(self.resonator_num)
                        
   
########################################################################
#
# This class is one sweep, one fit, one resonator on one chip.
#
#
#######################################################################


class resonatorData:
    def __init__(self,N=0,cname='null'):

        #manually set center freq.
        self.manual_cent_freq=0.0

        #ampunt of delauy applied to the iqdata and iqnopise traces. 
        self.applied_delay = 0.0

        #list- year,mon,day,hr,min,sec]
        self.createtime = list(time.localtime()[:6])
        #current time- in sec since unix epoch, like 1970 or somthing,. can convert to str date time
        self.createtimefl = time.time()
        
        #channel from channelizer for this res. 
        self.channel=192
        
        #self.delayraw=30e-9
        
        #which fw used for sweeping. 0 for netAnaluzer, 1 for fftanaluzer. -1 for not set.
        self.sweep_fw_index=-1

        #which fw used for taking nosie. 0 for netanal, 1 for fftanal, -1 for bnot set
        self.noise_fw_index = -1
        
        
        #dac sweep amplitide, as a percentatge of dac fuill scale        
        self.dac_sine_sweep_amp=0.6
        
        #fft trace dac amplitude, as a percentage of fuill scale.
        self.lut_sine_amp=.6

        #this means that there is noise data added to this object
        self.is_noise = 0
        #1 if runFits was run on this trace
        self.is_ran_fits = 0
        #1 if we ran fits and there was an error
        self.is_fit_error=0

        #self.desc='Resonator'

        #reference to MKID that has this trace in its list
        #self.parent_mkid = -1
        #tells which MKID this trace goes with.
        self.resonator_num=N
        #self.chip_name=cname

        #if 1 then this res is at a preferred atten in parent mkid
        self.is_pref_atten=0
        
        #unique id for this object, which trace this is in the mkid
        #well, to be honest there is 1 in 10e8 chance that these numbers are not unique... but because it is a pseudo rand
        #counter, in one run , we are OK...
        self.trace_id=random.randint(0,100000000)
        
        
        #Len of data
        self.datalen=2048


        #raw IQdata from ROA?CH board, no phase calcs.
        #we never touch this in fits.. it is for reference..in case we want to go back to raw data
        #self.IQ_raw=[]
        

        #iQ data
        
        self.iqdata=[arange(self.datalen), arange(self.datalen)]
        self.isneg_freq=1
        self.carrierfreq=3500e6
        #start frequency Hz- baseband
        self.startFreq_Hz=10e6
        #end freq Hz, baseband
        self.endFreq_Hz=50e6
        #freq incr Hz, baseband
        self.incrFreq_Hz=0.1e6
        
     
        #rf delay if xmission line. not baseabnad
        #self.delay=0.0;
        
        #self.firmware_delay=0
                
                
        self.xmission_line_delay=30e-9
        
        #delay of adc convertion 
        #self.adcdelay=230e-9
        
        #phases for dealing w/ delay
        self.phasesRe=ones(self.datalen);
        self.phasesIm=zeros(self.datalen);
        
        
        self.freqs=arange(self.datalen)
                

        #rough center freq- center freq of the freqs var.
        self.rough_cent_freq=0;
        
        #initial guess at resonators.
        self.ig_numresfreq=0
        self.ig_resfreqlist=[0]
        self.ig_indices=[0]
        self.ig_bump=zeros(self.datalen)


        #circle fit
        self.cir_xc=0
        self.cir_yc=0
        self.cir_R=0
        
        #transrot data
        self.trot_S21=zeros(self.datalen)
        self.trot_xf=zeros(self.datalen)
        self.trot_yf=zeros(self.datalen)
        self.trot_Fcenter=0
        

        #phase initial guess
        #phase_guesses = [Qguess,  Fcenter,  median(phase),sgn];
        self.phig_phase_guesses=[0,0,0,0]
        #atan like curve.
        self.phig_phase=zeros(self.datalen)
        self.phig_IQcentered=[zeros(self.datalen),zeros(self.datalen)]
        self.phig_mag2s21=zeros(self.datalen)
        self.phig_mag2s21dB=zeros(self.datalen)
        
        
        #Phase fitting
        self.ph_Qf=1
        self.ph_theta=0
        self.ph_sgn=1
        self.ph_fr=0;
        
        
        
        #Lorentz guess
        self.lrnzig_params=[0,0,0,0,0]
        
        #Lorentz Fit
        self.lorentz_Q = 1;
        self.lorentz_Qc = 1;
        self.lorentz_Qi = 1;
        self.lorentz_fr = 0;
        self.lorentz_theta = 0; 
        self.lorentz_ssq = 0;
        self.lorentz_iter = 0;
        self.lorentz_s21min = 0;
        self.lorentz_params=[0,0,0,0,0]
        
        #Skewcircle guess
        self.skewcircle_params = [0,0,0,0,0]

        #Skewcircle fit #added by cecil
        self.skewcircle_Q = 1;
        self.skewcircle_Qc = 1;
        self.skewcircle_Qi = 1;
        self.skewcircle_fr = 0;
        self.skewcircle_dw = 0;
        self.skewcircle_ssq = 0;
        self.skewcircle_iter = 0;
        self.skewcircle_s21min = 0;
        self.skewcircle_params=[0,0,0,0,0]        


        #
        # IQ Vel calcs
        #
        self.maxIQvel = 0;
        self.maxIQvel_freq = 0;
        self.maxIQVel_z=[0]
        self.maxIQVel_gz=[0]
        self.maxIQvel_ratio=0;

        # Device Powers in dBm calculated using Qs from Skewcircle fit. Assume LO at -5dBm
        self.Pg = -1        
        self.Pint = -1 
        self.Pdiss = -1
        self.cryoAtt = 45 

        self.NUM_GUESSES_PHASE=5000
        self.NUM_GUESSES_LORENTZ=30
        self.NUM_GUESSES_SKEWCIRCLE = 100
        

        self.anritsu_power= 0


        self.atten_U6=0
        self.atten_U7=0
        self.atten_U28=0


        self.baseband_loop=0
        self.rf_loopback=0
        self.clk_internal=0
        self.lo_internal=0
        self.lo_source = 0



        #
        # The fittings have a function addLineToPhase to remove time delay errors
        #
        
        #a line of phases, in radians we add to actyal iqdata phase to level the phase plot
        self.newline=zeros(200)
        #the slope of the line in radians per sample of new line
        self.newline_slope=0.0
        #amount we alter the phase of thenoise traces when doint this correction.
        self.noise_linephase=0.0
        
        #
        #
        #

        #setting sof netanaluyzer fw. dftlen is num points integrated in dft
        self.dftLen =0
        #sd mod if signal dalta mod on, for more accurate sinwave freqs
        self.sd_mod=0

        #gain of fft- used in fft FW onlyshift setting of fft
        self.roach_fft_shift=2047
        
        #for fft sweep, the base freq in the lut
        self.sweep_fbase=0
        #fft bin used in sweep
        self.sweep_binnumber=0
       

        self.sweep_tes_bias =0
        
        #
        # Here is where we put noise data.
       
        #
        self.num_noise_traces=0
        
       
        
        #len of ffe for noise
        self.fftLen=[]
        #fpga clocks between successive ffts- this gives sample rate of noise traces. 
        self.fftsynctime=[]
        #phase delay due to xmission lines and delays in dig filters etc. same as delay
        #but need seperate number
        self.fftdelay=[]
        #here is noise data. 
        #we can have any number of noise traces. the format is a list of noise traces,
        #where noise trace is list of arrays, I and Q.
        # [   [I,Q] , [I,Q], etc...  ]
        self.iqnoise=[  ]
       
        
        self.noise_tes_bias = []
        self.noise_tes_bias_on = []
        
       
        #freq of actual sin, BASEBAND
        self.srcfreq=[]
        #freq if LO, for fft- shoul be same as carrierfreq!!!
        self.fftcarrierfreq=[]
        #  freq of RF when taking noise. in Hz
        self.noise_rf_freq = []
        self.noisetrace_len=[]
        
        #self.fftsynctimes=[0]
        
       
    def clearNoise(self):
        #
        # Here is where we put noise data.
       
        #
        self.num_noise_traces=0
        
       
        
        #len of ffe for noise
        self.fftLen=[]
        #fpga clocks between successive ffts- this gives sample rate of noise traces. 
        self.fftsynctime=[]
        #phase delay due to xmission lines and delays in dig filters etc. same as delay
        #but need seperate number
        self.fftdelay=[]
        #here is noise data. 
        #we can have any number of noise traces. the format is a list of noise traces,
        #where noise trace is list of arrays, I and Q.
        # [   [I,Q] , [I,Q], etc...  ]
        self.iqnoise=[  ]
       
        
      
       
        #freq of actual sin, BASEBAND
        self.srcfreq=[]
        #freq if LO, for fft- shoul be same as carrierfreq!!!
        self.fftcarrierfreq=[]
        #  freq of RF when taking noise. in Hz
        self.noise_rf_freq = []
        self.noisetrace_len=[]
        
        #self.fftsynctimes=[0]
            
    def addNoiseFile(self,fname):
            
        if self.num_noise_files==0:
            self.noisefilenames=[];
            
        self.num_noise_files=  self.num_noise_files+1
        self.noisefilenames.append(str(fname))
        self.is_noise=1;
        

    #for debugging generally. we use global function mkidSaveData above
    #for our normal work. this is just to save one res obj to a file.
    def save(self,filename,grpname="ResData",sweepnum=0):
    
    
        fp=h5py.File(filename,'w')
        
                    
        devgrp=fp.create_group(grpname)
        
        devgrp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
        
        
        self.info()
        self.writeHDF(devgrp,sweepnum)
                
            
        fp.flush()    
           
        fp.close()    



    #for debugging generally. we use global function mkidSaveData above
    #for our normal work. this is just to save one res obj to a file.
    def load(self,filename,grpname="ResData",sweepnum=0):
    
    
        fp=h5py.File(filename,'r')
        
                    
        devgrp=fp[grpname]
        
        
        
        
        self.readHDF(devgrp,'%d'%sweepnum)

           
        fp.close()    

        self.info()        



    #return attenuations, sum of output atten and return atten as tuple
    def calcTotalAttenDb(self):
        total_out_atten = self.atten_U6 + self.atten_U7
        total_out_atten = total_out_atten - 20*log10(self.dac_sine_sweep_amp)
        total_return_atten = total_out_atten + self.atten_U28;
        return( (total_out_atten,total_return_atten ) )


    #set parent mkid pref. atten to this resData
    def setParentMKIDprefAtten(self):
            #self.parent_mkid.setResPrefAtten(self)
            print "ERROR fix parent mkid stuff on resonator"
        
    #return center freq.        
    def getFc(self):
        if self.manual_cent_freq!=0.0:
            return(self.manual_cent_freq)
        elif self.maxIQvel_freq!=0:
            return(self.maxIQvel_freq)
        else:
            return(self.rough_cent_freq)
        
    #wrirte this resdata to hdf file        
    def writeHDF(self,parent,sweepnum):
    
        jfkdlskdjf
        
    def readHDF(self,parent,gname):
    
        jfkdlskfjlsdkjf
                   

    def openHDFR(self,fname):
        fp=h5py.File('ResData_%s.hdf'%(fname),'r')
        return(fp)


    def openHDF(self,fname):
        fp=h5py.File('ResData_%s.hdf'%(fname),'w-')
        return(fp)
        
    def closeHDF(self,fp):
        fp.flush();
        fp.close();
        
    
    def report(self):
        contents= inspect.getmembers(self)
        for c in contents:
            print c

 
    def report2(self):
        contents= inspect.getmembers(self)
        return(contents)
                
        
    def info(self):
        print "Trace %d Freq range  %f, %f, %f "%(self.trace_id,self.startFreq_Hz, self.incrFreq_Hz, self.endFreq_Hz)
        print "Carrier FO %f"%(self.carrierfreq)
        print "Datalength %d"%(self.datalen)
        print "Aprox Freqs:"
        print self.ig_resfreqlist
        print "Span %f MHz"%((self.endFreq_Hz - self.startFreq_Hz)*1e-6)
        print "Fitted Fr %f GHz"%(self.lorentz_fr/1e9)
        print "Fitted Q %f"%(self.lorentz_Q)
        width=self.lorentz_fr/self.lorentz_Q
        print "Fitted width %f MHz"%(1e-6*width)
        print "Fitted Start %f GHz, End %f GHz"%(  1e-9*(self.lorentz_fr-width/2), 1e-9*(self.lorentz_fr+width/2))
        
        print "Attens U6 %f U7 %f U28 %f"%(self.atten_U6, self.atten_U7, self.atten_U28)
        print "FFT gain %d"%(self.roach_fft_shift)
        print "FFT base freq %f"%(self.sweep_fbase)
        print "Num Noise Traces %d"%(self.num_noise_traces)
        
        print "Lut Sine amp %f"%(self.lut_sine_amp)
        print "Fits Ran %d Fits Err %d"%(self.is_ran_fits, self.is_fit_error)
        
        print "Rough Center Freq %fMHz"%(self.rough_cent_freq/1e6)
        
        print "maxIQvel=%f,maxIQvel_freq=%f"%(self.maxIQvel,self.maxIQvel_freq)
        print "xc %f  yc=%f Radius %f"%(self.cir_xc, self.cir_yc,self.cir_R)
        print "xc %f  yc=%f Radius %f"%(self.cir_xc, self.cir_yc,self.cir_R)
        print " trot_Fcenter %f"%(self.trot_Fcenter)


    def setData(self,iq,f,d,fc):
        self.datalen=len(iq[0])
        
        self.freqs=zeros(self.datalen)
        self.iqdata=[zeros(self.datalen), zeros(self.datalen)]
        
        for k in range(self.datalen):
                self.freqs[k]=f[k]
                self.iqdata[0][k] = iq[0][k]
                self.iqdata[1][k] = iq[1][k]
        
        
        self.startFreq_Hz=self.freqs[0]
        self.endFreq_Hz=self.freqs[self.datalen-1]
        self.incrFreq_Hz=self.freqs[1]-self.freqs[0]                

        
        self.rough_cent_freq=(self.endFreq_Hz + self.startFreq_Hz)/2.0
                
        
        self.carrierfreq=fc
        
        self.setDelay(d)
        

    ##
    # remove any applied delay from sweep trace uqdata and iqnoise traces
    #
    def removeDelay(self):
        delaysave = self.xmission_line_delay
        self.xmission_line_delay  = 0.0 -  self.applied_delay 
        self.applyDelay()
        self.xmission_line_delay = delaysave
        
    ##
    #set in sec. set delay time in sec of the xmission line in rf.
    #
    def setDelay(self,d):
        #230e9 is ADC/DAC time delay in ns- we add that to xmission line dly
        self.xmission_line_delay=d

       
        
        self.phasesRe= numpy.cos(2*pi*self.freqs*self.xmission_line_delay)
        self.phasesIm= numpy.sin(2*pi*self.freqs*self.xmission_line_delay)

    ##
    # add delay in sec (should be about 30ns) of cable in rf. baseband delaus not dealt with, but only rf.
    # apply delay in sweep and in rf noise traces.
    # return new 

    def applyDelay(self):
                    
        #
        # keep track of how much delay we ahve applied to iqdata. incase we want to undo it.
        #
        self.applied_delay = self.xmission_line_delay
        
        #
        # apply delay to sweep trace.
        #

        #IQ in polar form. [mags, radians]
        iqp=self.RectToPolar(self.iqdata);
        #polar version of phase delay, should be 1Arg(phases).
        phasep=self.RectToPolar([self.phasesRe,self.phasesIm]);


        if (self.incrFreq_Hz<0.00001):
                iqp[1] = iqp[1] + phasep[1][0]
        else:        
                iqp[1] = iqp[1] + phasep[1]

        

        self.iqdata_dly = self.PolarToRect(iqp)
        
        #
        # do noise traces, apply delay there too.
        #
        i=0
        self.iqnoise_dly = ccopy.deepcopy(self.iqnoise)
        
        for noise_trace in self.iqnoise_dly:
            
            #calc phase delay
            try:
                d_ph = 2*pi*self.noise_rf_freq[i]*self.xmission_line_delay
                #add delay to phase term of noise
                noise_trace[192]['stream_phase'] = \
                    noise_trace[192]['stream_phase'] + d_ph
                i=i+1
            except:
                print "problem w/ noise traice/ no 192" 
            
   
  ##
    # add delay to phase of nosie traces, . return noise. do not alter contents of res data

    def applyDelayN(self):
                    
        noiselist = []
        #
        # do noise traces, apply delay there too.
        #
        i=0
        for noise_trace in self.iqnoise:
            
            #calc phase delay
           
            d_ph = 2*pi*self.noise_rf_freq[i]*self.xmission_line_delay
            #add delay to phase term of noise
            nmag = noise_trace[192]['stream_mag']
            nphs =noise_trace[192]['stream_phase'] + d_ph
            i=i+1
            noiselist.append( (nmag,nphs) )

        return(noiselist)   
   ##
    # calc phase adjuected for delau. return resut. do not alter data in res obj.
    # iq only
    #  

    def applyDelayIQ(self):
                    
        #
        # keep track of how much delay we ahve applied to iqdata. incase we want to undo it.
        #
        #self.applied_delay = self.applied_delay + self.delay
        
        #
        # apply delay to sweep trace.
        #

        #IQ in polar form. [mags, radians]
        iqp=self.RectToPolar(self.iqdata);
        #polar version of phase delay, should be 1Arg(phases).
        phasep=self.RectToPolar([self.phasesRe,self.phasesIm]);


        if (self.incrFreq_Hz<0.00001):
                iqp[1] = iqp[1] + phasep[1][0]
        else:        
                iqp[1] = iqp[1] + phasep[1]

        

        iqr = self.PolarToRect(iqp)
        
      
   
   
        return( iqr )


    def plotFreq(self,isclf=1,isnoise=1,fnum=0,is_pl_trot = True):
        

        #return self.iqdata after addediong delay in. self.iqdata is inaltered, 
        self.applyDelay()
        
        IQ=self.iqdata_dly
        freqs=self.freqs

        IQp=self.RectToPolar(IQ)

        figure(1+fnum)
        if isclf:clf()
        
        
        
        dbref = -40
        
        subplot(4,2,1)
        title("Delay=%dns"%(floor(self.xmission_line_delay*1e9)))
        dat=20*log(IQp[0]) - dbref
        plot(freqs,dat)
       
        #
        # Plot x at center freq. 
        #
       
        fcenter = self.getFc()
        #find mag resp at that freq
        #find index of freq:
        
        found_index = 0
        for i in range(len(freqs)):
            if freqs[i]>=fcenter:
                found_index=i
                break
                
        plot(freqs[found_index],dat[found_index],'rx')
        
        #
        # Set axis ranges, labels etc.
        #
        toprange = 10+10.0*ceil(max(dat)/10.0)
        botrange = -10+10.0*ceil(min(dat)/10.0)
        ylim(botrange,toprange)
        grid(True)
        
        ylabel('20Log10 Mag.')
        subplot(4,2,3)
        plot(freqs,self.removeTwoPi(IQp[1]))
        ylabel('Phase')
        subplot(4,2,5)
        plot(freqs,IQ[0])
        ylabel('I')
        subplot(4,2,7)
        plot(freqs,IQ[1])
        ylabel('Q')
        draw()
        
        figure(1+fnum)
#        if isclf:clf()
        subplot(1,2,2)
        plot(IQ[0],IQ[1],'bx')
        plot(IQ[0],IQ[1],'b')
        plot(IQ[0][found_index],IQ[1][found_index],'ro')
        
        
        if not is_pl_trot: return
        
        
        
        #to a cirfit, and transrot, plot it.
        fc = self.getFc()
        span = 0.8e6
        fit.setResonator(self)
        fit.fit_circle3(self,fc,span)
        try:
            IQtr = fit.trans_rot3(self,IQ)

            plot(0,0,'rx')
            plot(IQtr[0],IQtr[1],'rx')
        except: 
            print "resonators.py, plotFreq transrot problem"


        #savefig('../../notebooks/latestfig.jpg')

        figure(13)
        clf()
        polar(IQp[1],IQp[0])
        iqptr = self.RectToPolar(  [self.trot_xf ,self.trot_yf ])
        polar(iqptr[1],iqptr[0],'r')


        
        
        try:
            figure(8+fnum)
            
            if isclf:clf()
            
            lf=len(self.freqs)-1
            plot(self.freqs[1:lf],self.maxIQVel_z)
            
            figure(1+fnum)
            subplot(4,2,1)
            iqpoint = self.iqAtFreq(self.maxIQvel_freq)
            
            mag = sqrt( iqpoint[0]* iqpoint[0] + iqpoint[1]* iqpoint[1])
            #plot(self.maxIQvel_freq,mag,'gx')
            

            figure(13+fnum)
            
            
            iqpp  = self.RectToPolar( 
                [ numpy.array([iqpoint[0]]), 
                numpy.array([iqpoint[1]]) ])
                
            polar(iqpp[1],iqpp[0],'gx')


            figure(1+fnum)
            subplot(1,2,2)
            plot(iqpoint[0],iqpoint[1],'gx')


            
            
        except:
            print "Incomplte IQ velocity"
        
        #
        #self.noisefilenames=['NULL']
        #self.num_noise_files = 0
        figure(20+fnum);clf()
        figure(21+fnum);clf()
        
        figure(22+fnum);clf()
        figure(23+fnum);clf()
        
        #return all nosie traces, after time delayed,. by self.delay. do not alter orig iqnoise data.
      
        
        for iqpr in self.iqnoise_dly:

            try:
                iqp = [ iqpr[192]['stream_mag'] , iqpr[192]['stream_phase'] ]
                iq = self.PolarToRect( iqp )
                figure(20+fnum)
                subplot(2,1,1)
                plot(iqp[0][1000:2000])
                subplot(2,1,2)
                plot(iqp[1][1000:2000])
                

                figure(1+fnum)
                subplot(1,2,2)
                plot(iq[0][1000:2000],iq[1][1000:2000],'.')
                iqtr = fit.trans_rot3(self,iq)
                plot(iqtr[0][1000:2000],iqtr[1][1000:2000],'.')
      
                #iqtrcmp = iqtr[0] + complex(0,1)*iqtr[1]
                [nfreq,npwr] = scipy.signal.welch(iqtr[1])
                figure(21+fnum)
                plot(nfreq,npwr)
            except:
                print "No raw nosie data"
             
             
             
            figure(22+fnum)
            plot(   iqpr[192]['flux_ramp_phase'][:1000]  )
              
            [nfreq,npwr] = scipy.signal.welch(iqpr[192]['flux_ramp_phase'] )
            figure(23+fnum)
            plot(nfreq,npwr)
                


    def iqAtFreq(self,fc):
        minerr=10e9
        minerri = 0
        
        for i in range(len(self.freqs)):
            f = self.freqs[i]
            err = abs(f-fc)
            if err<minerr:
                minerri =i
                minerr = err
        
        return( (self.iqdata[0][i], self.iqdata[1][i])  )

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




    def removeTwoPi(self,phases):
        offset=0;
        for k in range(len(phases)-1):


                dphs=phases[k+1]-phases[k]
                if abs(dphs)>3.1416:
                        offset= (-1.0 * sign(dphs) * 2*3.141592653589793)

                        for k2 in range(k,len(phases)-1):
                                phases[k2+1]=phases[k2+1] + offset

        return(phases)

    def fliplr(self):
    
            
        
        self.freqs=(2*self.carrierfreq - self.freqs)[::-1]
        self.iqdata[0]=self.iqdata[0][::-1]
        self.iqdata[1]=self.iqdata[1][::-1]
        
        
        self.startFreq_Hz=self.freqs[0]
        self.endFreq_Hz=self.freqs[self.datalen-1]
        self.incrFreq_Hz=self.freqs[1]-self.freqs[0]                

        self.rough_cent_freq = (self.startFreq_Hz + self.endFreq_Hz)/2
        self.setDelay(self.xmission_line_delay)
        


