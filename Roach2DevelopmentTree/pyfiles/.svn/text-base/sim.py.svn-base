


#import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import struct
import numpy

import corr, time,fractions, math,inspect,random
import time
import threading
import copy as ccopy
import pickle




def sim_iqpulse2():

    #radian convert
    rad=pi/180.0

    #data len
    L = 8192
    
    #base gnale in degrees w/ no pilse. center of iq circle
    cir_angle=360.0*rand() * rad
    
    #dstx of origin to center of circle
    cir_z=1
    
    #radius of iq circ
    cir_r=0.1
    
    #phase noise , deg
    ph_noise_mag=5 * rad
    
    #amp noise in iq units
    amp_noise_mag=0.012


    
    

    #
    # raw pulse function
    #
    
    #pulse len in samples
    PL = 100.0
    
    #cos window
    
    #number from 0 to 1, to correspond from 0 to 2pi
    ph1=numpy.arange(0,1,1.0/PL)
    
    #sqrt it, to change shape of the cos to look like a pulse
    ph1=numpy.sqrt(ph1)
    ph1=numpy.sqrt(ph1)
    
    
 
    cwind=0.5 * (1.0 - numpy.cos(ph1 * 2.0 * pi))
    figure(2)
    clf()
    plot(cwind)









    
    #
    # assume origin is at center of circle for this calc.
    #
    
    #angle on cir where noise cloud is
    noise_ang = rad*180.0 + cir_angle
    
    #make noiseless IQ signal, in amp and angle.
    #tr mans translated,,, maning iq cir is at orgin.
    
    #this is our signal, to add pulses to
    amp_sig_tr = numpy.random.normal(cir_r, amp_noise_mag, L)
   
    phase_sig_tr = numpy.random.normal(noise_ang, ph_noise_mag, L)
   
   
   #make 2nd signal, as a noise reference.
    amp_noise_tr = numpy.random.normal(cir_r, amp_noise_mag, L)
   
    phase_noise_tr = numpy.random.normal(noise_ang, ph_noise_mag, L)
   



    #
    # Add the pulses to the raw noise signals at random heights and at randon places.
    #
    
    num_pulses = int(10*rand())
    pulse_ang_max=-120.0 * rad
    pulse_amp_max = cir_r * 0.1
    
    print 'Number Pulses %d'%(num_pulses)
    
    pulse_list = []
    
    for k in range(num_pulses):
    
        #start of pulse in the data vector
        pulse_st = int(rand() * (L - PL))


	pulse_amp = rand()   
	pulse_list.append(pulse_st)
		
	pulse_sig_ph = cwind * pulse_amp*pulse_ang_max
	pulse_sig_amp = cwind * pulse_amp*pulse_amp_max
   
        amp_sig_tr[pulse_st:(pulse_st+PL)] = amp_sig_tr[pulse_st:(pulse_st+PL)] + pulse_sig_amp
        phase_sig_tr[pulse_st:(pulse_st+PL)] = phase_sig_tr[pulse_st:(pulse_st+PL)] + pulse_sig_ph
   
   
   
   
   
   
   
   
    #here is i q signal on iq cir, w. center at orgin.
    i_sig_tr= amp_sig_tr * numpy.cos(phase_sig_tr)
    q_sig_tr= amp_sig_tr * numpy.sin(phase_sig_tr)
    
    #iq sig no pulses, 

    i_noise_tr= amp_noise_tr * numpy.cos(phase_noise_tr)
    q_noise_tr= amp_noise_tr * numpy.sin(phase_noise_tr)


    
    #
    #now convert w/ cir not at orgin.
    #
    
    
    i_sig = i_sig_tr + cir_z * cos(cir_angle)
    q_sig = q_sig_tr + cir_z * sin(cir_angle)
   
      
    i_noise = i_noise_tr + cir_z * cos(cir_angle)
    q_noise = q_noise_tr + cir_z * sin(cir_angle)
   
      
      
    #
    # Get expexted values and calc the power
    #  
      
    magnitude_sig =   numpy.sqrt(i_sig*i_sig + q_sig*q_sig)
      
    magnitude_noise =   numpy.sqrt(i_noise*i_noise + q_noise*q_noise)
    
    
    angle_sig=numpy.arctan2(i_sig,q_sig)
    angle_noise = numpy.arctan2(i_noise,q_noise)
    
    
      
    
    magnitude_exp_val = numpy.mean(magnitude_noise)
    angle_exp_val = numpy.mean(angle_noise)
   
   
      
    magnitude_std = numpy.std(magnitude_noise) 
    angle_std = numpy.std(angle_noise) 
    
    
    i_exp_val = numpy.mean(i_noise)
    q_exp_val = numpy.mean(q_noise)
    
   
    
    #
    # make x and y vectors to plot the iq circle.
    #
    
    #num points on circle
    N=50
    
    ph=rad * numpy.arange(0,365.0, 365.0/N)
    
    xc=cir_z * cos(cir_angle) + cir_r * numpy.cos(ph)
    yc = cir_z * sin(cir_angle) +   cir_r * numpy.sin(ph)
    
    figure(1)
    clf()
    plot(xc,yc)
    plot(0,0,'x')
    
    
    # plot the iq signal on circle
    plot(i_sig,q_sig,'.')
    
    
    
    #
    # find pulses w/ threshold
    #
    
    threshold = 5.0* (magnitude_std + angle_std)
    
    test_val = numpy.abs(magnitude_sig - magnitude_exp_val + angle_sig - angle_exp_val) 
    trigger = numpy.zeros(L)

    #how long trig signal stays on after trigger.
    trig_length = 25
    
    trig_cnt = trig_length
    
    for k in range(L-1):
        if (test_val[k] + test_val[k+1]) > threshold:
	    trig_cnt=0
	    
	if trig_cnt<trig_length:
	    trigger[k] = 1
	    trig_cnt = trig_cnt + 1
	    

    
    #
    # Count number of pulses we found
    #
    
    n_found_pulses = 0
    
    for k in range(L-1):
        if trigger[k+1]-trigger[k]>0.0:
	    n_found_pulses=n_found_pulses+1
	    
	    
    print 'Num Found Pulses %d'%(n_found_pulses)
    
    
    #
    # plot iq vers time
    #

    
    figure(3)
    clf()
    #subplot(3,1,1)
    plot(i_sig - i_exp_val)
   
    
    #subplot(3,1,2)
    plot(q_sig-q_exp_val)
   



    #subplot(3,1,3)
    plot(0.03 * trigger)
    	    
    plot(numpy.arange(0.0,L), 0.5*threshold*numpy.ones(L))


    plot(pulse_list, [0]*len(pulse_list),'o')


  
    #
    # plot power vers time
    #

    
    figure(4)
    clf()
    #subplot(3,1,1)
    #plot(test_val)
    
    #plot(numpy.arange(0.0,L), i_exp_val*numpy.ones(L))
  
    plot(angle_sig - angle_exp_val)
    plot(magnitude_sig - magnitude_exp_val)

    #subplot(3,1,3)
    plot(0.03 * trigger)
    	    
    plot(numpy.arange(0.0,L), 0.5*threshold*numpy.ones(L))


    plot(pulse_list, [0]*len(pulse_list),'o')






def sim_iqpulse():

    #radian convert
    rad=pi/180.0

    #data len
    L = 8192
    
    #base gnale in degrees w/ no pilse. center of iq circle
    cir_angle=360.0*rand() * rad
    
    #dstx of origin to center of circle
    cir_z=1
    
    #radius of iq circ
    cir_r=0.1
    
    #phase noise , deg
    ph_noise_mag=5 * rad
    
    #amp noise in iq units
    amp_noise_mag=0.012


    
    

    #
    # raw pulse function
    #
    
    #pulse len in samples
    PL = 100.0
    
    #cos window
    
    #number from 0 to 1, to correspond from 0 to 2pi
    ph1=numpy.arange(0,1,1.0/PL)
    
    #sqrt it, to change shape of the cos to look like a pulse
    ph1=numpy.sqrt(ph1)
    ph1=numpy.sqrt(ph1)
    
    
 
    cwind=0.5 * (1.0 - numpy.cos(ph1 * 2.0 * pi))
    figure(2)
    clf()
    plot(cwind)









    
    #
    # assume origin is at center of circle for this calc.
    #
    
    #angle on cir where noise cloud is
    noise_ang = rad*180.0 + cir_angle
    
    #make noiseless IQ signal, in amp and angle.
    #tr mans translated,,, maning iq cir is at orgin.
    
    #this is our signal, to add pulses to
    amp_sig_tr = numpy.random.normal(cir_r, amp_noise_mag, L)
   
    phase_sig_tr = numpy.random.normal(noise_ang, ph_noise_mag, L)
   
   
   #make 2nd signal, as a noise reference.
    amp_noise_tr = numpy.random.normal(cir_r, amp_noise_mag, L)
   
    phase_noise_tr = numpy.random.normal(noise_ang, ph_noise_mag, L)
   



    #
    # Add the pulses to the raw noise signals at random heights and at randon places.
    #
    
    num_pulses = int(10*rand())
    pulse_ang_max=-120.0 * rad
    pulse_amp_max = cir_r * 0.1
    
    print 'Number Pulses %d'%(num_pulses)
    
    pulse_list = []
    
    for k in range(num_pulses):
    
        #start of pulse in the data vector
        pulse_st = int(rand() * (L - PL))


	pulse_amp = rand()   
	pulse_list.append(pulse_st)
		
	pulse_sig_ph = cwind * pulse_amp*pulse_ang_max
	pulse_sig_amp = cwind * pulse_amp*pulse_amp_max
   
        amp_sig_tr[pulse_st:(pulse_st+PL)] = amp_sig_tr[pulse_st:(pulse_st+PL)] + pulse_sig_amp
        phase_sig_tr[pulse_st:(pulse_st+PL)] = phase_sig_tr[pulse_st:(pulse_st+PL)] + pulse_sig_ph
   
   
   
   
   
   
   
   
    #here is i q signal on iq cir, w. center at orgin.
    i_sig_tr= amp_sig_tr * numpy.cos(phase_sig_tr)
    q_sig_tr= amp_sig_tr * numpy.sin(phase_sig_tr)
    
    #iq sig no pulses, 

    i_noise_tr= amp_noise_tr * numpy.cos(phase_noise_tr)
    q_noise_tr= amp_noise_tr * numpy.sin(phase_noise_tr)


    
    #
    #now convert w/ cir not at orgin.
    #
    
    
    i_sig = i_sig_tr + cir_z * cos(cir_angle)
    q_sig = q_sig_tr + cir_z * sin(cir_angle)
   
      
    i_noise = i_noise_tr + cir_z * cos(cir_angle)
    q_noise = q_noise_tr + cir_z * sin(cir_angle)
   
      
    i_exp_val = numpy.mean(i_noise)
    q_exp_val = numpy.mean(q_noise)
   
   
      
    i_std = numpy.std(i_noise) 
    q_std = numpy.std(q_noise)
   
    
    #
    # make x and y vectors to plot the iq circle.
    #
    
    #num points on circle
    N=50
    
    ph=rad * numpy.arange(0,365.0, 365.0/N)
    
    xc=cir_z * cos(cir_angle) + cir_r * numpy.cos(ph)
    yc = cir_z * sin(cir_angle) +   cir_r * numpy.sin(ph)
    
    figure(1)
    clf()
    plot(xc,yc)
    plot(0,0,'x')
    
    
    # plot the iq signal on circle
    plot(i_sig,q_sig,'.')
    
    
    
    #
    # find pulses w/ threshold
    #
    
    threshold = 5.0* (i_std +q_std)
    
    test_val = numpy.abs(i_sig - i_exp_val)  + numpy.abs(q_sig - q_exp_val)

    trigger = numpy.zeros(L)

    #how long trig signal stays on after trigger.
    trig_length = 25
    
    trig_cnt = trig_length
    
    for k in range(L-1):
        if (test_val[k] + test_val[k+1]) > threshold:
	    trig_cnt=0
	    
	if trig_cnt<trig_length:
	    trigger[k] = 1
	    trig_cnt = trig_cnt + 1
	    

    
    #
    # Count number of pulses we found
    #
    
    n_found_pulses = 0
    
    for k in range(L-1):
        if trigger[k+1]-trigger[k]>0.0:
	    n_found_pulses=n_found_pulses+1
	    
	    
    print 'Num Found Pulses %d'%(n_found_pulses)
    
    
    #
    # plot iq vers time
    #

    
    figure(3)
    clf()
    #subplot(3,1,1)
    plot(i_sig - i_exp_val)
    
    #plot(numpy.arange(0.0,L), i_exp_val*numpy.ones(L))
    
    #subplot(3,1,2)
    plot(q_sig-q_exp_val)
    #plot(numpy.arange(0.0,L), q_exp_val*numpy.ones(L))



    #subplot(3,1,3)
    plot(0.03 * trigger)
    	    
    plot(numpy.arange(0.0,L), 0.5*threshold*numpy.ones(L))


    plot(pulse_list, [0]*len(pulse_list),'o')



def simpfb():

    scale=8.0

    N=scale*1024


    sbin=1
    sincph=sbin*2.0*pi*(arange(N)-N/2.0)/N

    snc=numpy.sinc(sincph)

    I=zeros(N)
    Q=zeros(N)
    ph=2.0*pi*arange(N)/N

    for bin in arange(scale*64, scale*128,23.1):
	I=I+ numpy.cos(bin*ph) 
	Q=Q +numpy.sin(bin*ph) 


    w=numpy.hamming(N)*snc

    figure(1);clf();plot(w)

    Iw=I*w
    Qw=Q*w

    #fft len
    Lf=2048.0

    #overlaps window
    ovlps=N/Lf

    #overlap add signal
    Iov=zeros(Lf)
    Qov=zeros(Lf)

    for k in arange(ovlps): 
	Iov=Iov + Iw[(k*Lf):((k+1)*Lf)]
	Qov=Qov + Qw[(k*Lf):((k+1)*Lf)]


    S=Iov + complex(0,1)*Qov


    FF=fft.fft(S)
    figure(2)
    clf();semilogy(abs(FF))

    indx=where(abs(FF)>100)[0]

    for i in indx:
	amp=abs(FF[i])
	ang=(180.0 / pi) * numpy.angle(FF[i])
	print '%f  %f %f'%(i, amp, ang)





 
 
def simrwind():

#rect window

    L=8192
    FL=256
    
    w=zeros(L)
    w[:FL]=1

    figure(1);clf()
    semilogy(abs(fft.fft(w)))

    yy=zeros(FL)+10e1
    xx=arange(0,L,L/FL)
    semilogy(xx,yy,'ro')


    xlim((0,2*FL))
    ylim((1,1e4))


#2k overlap hamming, sinc

    
    L2=FL*8

    sbin=1
    sincph=sbin*2.0*pi*(arange(L2)-L2/2.0)/L2

    snc=numpy.sinc(sincph)

    
    hw=numpy.hamming(L2)*snc

    figure(2);clf();plot(hw)
    #overlaps window
    #ovlps=L2/FL

    #overlap add signal
    #wov=zeros(FL)
    

    #for k in arange(ovlps): 
    #	wov=wov+ hw[(k*FL):((k+1)*FL)]


    #figure(2);plot(wov)
     
    w=zeros(L)
    w[:L2]=hw

    
    figure(1);semilogy(abs(fft.fft(w)))



''' 

execfile('sim.py');sim_sdm(round(4000*rand()))

execfile('sim.py');sim_sdm(4000*rand())


'''
 
def sim_sdm(bin):

    print bin
    
    N=8192.0

    tablen=1024.0

    ph=arange(0,2*pi,2*pi/tablen)

    costab=cos(ph)
    sintab=sin(ph)

    #phaseacc=0.0

    addrbits=int(log2(tablen))
    phaseaccbits=int(24)

    #bin=1.0

    #want bin waves in N samples. so what is phase acc in wavelengths? or freq in wavelentths
    # bin/N = waves/sample

    freq=bin/N

    freq_d=int(freq*pow(2.0,phaseaccbits))

    phaseacc_d=int(0)

    #for 24, 8 bits, 0xff0000, msbs of the phaseacc
    addrmask=((1<<addrbits)-1) << (phaseaccbits-addrbits)

    #print hex(addrmask)
    
    errmask=(1<< (phaseaccbits-addrbits))-1 


    sig_I=zeros(N)
    sig_Q=zeros(N)
    ph_error_z=0
    
    for k in range(int(N)):


	tab_index=((phaseacc_d & addrmask) >> (phaseaccbits-addrbits))
	
	#print hex(phaseacc_d & addrmask)
	ph_error = (phaseacc_d & errmask)

	#print '0x%s  0x%s 0x%s  0x%s'%(hex(freq_d),hex(tab_index),hex(ph_error), hex(phaseacc_d))
	sig_I[k] = costab[tab_index]
	sig_Q[k] =  sintab[tab_index]


	#replace freq reg lsb w/ random bit. adds 1/2 lsb to freq. very small err.
	# this is +/- 0.05 Hz error for 32bit reg 512e6/(1<<32)=0.12

	phaseacc_d=phaseacc_d+freq_d + ph_error_z +int(round(rand()))

	
	ph_error_z= ph_error
	

	


    figure(1)
    clf()
    plot(sig_I)
    plot(sig_Q)


    hw=hw=numpy.hamming(N)
    figure(2);
    clf()
    semilogy(1e-5+ abs(fft.fft(sig_I*hw))[:N/2])
