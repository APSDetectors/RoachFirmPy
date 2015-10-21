function [i_sig, q_sig,ph_rotation_rate] = makepulses(L)


%radian convert
rad=pi/180.0;

%data len
%L = 8192;

%base gnale in degrees w/ no pilse. center of iq circle
cir_angle=360.0*rand() * rad;
%cir_angle=30 * rad;


%dstx of origin to center of circle
cir_z=.5;

%radius of iq circ
cir_r=0.05;

%phase noise , deg
ph_noise_mag=1 * rad;

%amp noise in iq units
amp_noise_mag=0.0012;


%number of pulses per 1000 samples
np1k=4;
npL=floor(np1k*(L/1000.0));

% rotation due to fft bin being not at correct freq.
%rad per sample. up to +/-5deg per sample 
ph_rot_mag = 5.0;
ph_rotation_rate=ph_rot_mag*(2.0*rand() - 1.0)*rad;


%
% raw pulse function
%

%pulse len in samples
PL = 30.0;

%cos window

%number from 0 to 1, to correspond from 0 to 2pi
ph1=(0:(PL-1))./PL;

%sqrt it, to change shape of the cos to look like a pulse
ph1=sqrt(ph1);
ph1=sqrt(ph1);



cwind=0.5 * (1.0 - cos(ph1 .* 2.0 * pi));
figure(2);
clf();
plot(cwind);










%
% assume origin is at center of circle for this calc.
%

%angle on cir where noise cloud is
noise_ang = rad*180.0 + cir_angle;

%make noiseless IQ signal, in amp and angle.
%tr mans translated,,, maning iq cir is at orgin.

is_stat=0;

if is_stat==1

%this is our signal, to add pulses to
amp_sig_tr = normrnd(cir_r, amp_noise_mag,1, L);

phase_sig_tr = normrnd(noise_ang, ph_noise_mag, 1,L);


%make 2nd signal, as a noise reference.
amp_noise_tr = normrnd(cir_r, amp_noise_mag, 1,L);

phase_noise_tr = normrnd(noise_ang, ph_noise_mag,1, L);

else
    
    %this is our signal, to add pulses to
amp_sig_tr =cir_r +  amp_noise_mag*rand(1,L); 

phase_sig_tr =noise_ang + ph_noise_mag*rand(1,L);



%make 2nd signal, as a noise reference.
amp_noise_tr =cir_r + amp_noise_mag*rand(1,L);

phase_noise_tr =noise_ang + ph_noise_mag*rand(1,L)
end




%
% Add the pulses to the raw noise signals at random heights and at randon places.
%

num_pulses = floor(npL*rand());
pulse_ang_max=-120.0 * rad;
pulse_amp_max = cir_r * 0.1;


for k =1:num_pulses
    %start of pulse in the data vector
    pulse_st = floor(rand() * (L - PL));


    %pulse_amp = rand() ;  
    pulse_amp = 0.5;
    pulse_sig_ph = cwind * pulse_amp*pulse_ang_max;
    pulse_sig_amp = cwind * pulse_amp*pulse_amp_max;

    amp_sig_tr(pulse_st:(pulse_st+PL-1)) = amp_sig_tr(pulse_st:(pulse_st+PL-1)) + pulse_sig_amp;
    phase_sig_tr(pulse_st:(pulse_st+PL-1)) = phase_sig_tr(pulse_st:(pulse_st+PL-1)) + pulse_sig_ph;


end




%
% Calc I and Q
%

%here is i q signal on iq cir, w. center at orgin.
i_sig_tr= amp_sig_tr .* cos(phase_sig_tr);
q_sig_tr= amp_sig_tr .* sin(phase_sig_tr);

%iq sig no pulses, 

i_noise_tr= amp_noise_tr .* cos(phase_noise_tr);
q_noise_tr= amp_noise_tr .* sin(phase_noise_tr);



%
%now convert w/ cir not at orgin. not rotated yet
%


i_sig_nr = i_sig_tr + cir_z * cos(cir_angle);
q_sig_nr = q_sig_tr + cir_z * sin(cir_angle);


i_noise = i_noise_tr + cir_z * cos(cir_angle);
q_noise = q_noise_tr + cir_z * sin(cir_angle);

i_exp_val = mean(i_noise);
q_exp_val = mean(q_noise);

%
% Add the phase rotation due to freq offset in fft bin
%

%calc phase rot ramp
phase_rot =ph_rotation_rate*(1:L);

%polar i and q, no rot yet
amp_sig_nr=sqrt( i_sig_nr.^2 + q_sig_nr.^2 );
phase_sig_nr = atan2(q_sig_nr,i_sig_nr);

%add in the rotation
phase_sig = phase_sig_nr + phase_rot;

%convert to I and Q

i_sig=amp_sig_nr .* cos(phase_sig);
q_sig=amp_sig_nr .* sin(phase_sig);


%
%plots
%

figure(1)
clf()
hold on
plot(i_sig-i_exp_val)
plot(q_sig-q_exp_val,'g')


figure(3)
clf()
plot(i_sig,q_sig,'r.')

%
% make x and y vectors to plot the iq circle.
%

%num points on circle
N=50;

ph=rad * 370*((1:50)/50);

xc=cir_z * cos(cir_angle) + cir_r * cos(ph);
yc = cir_z * sin(cir_angle) +   cir_r * sin(ph);
hold on
plot(xc,yc)
hold on
plot(0,0,'x')






end