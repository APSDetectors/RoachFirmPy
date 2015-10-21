function [ph,mg,phaseperfftdeg]=makephasedata(simlen,lutlen,nwaves,fftlen)
%for simulation phase circuit. makes one vector of phase data.




phasepersampledeg = 360.0* (nwaves/lutlen);


phaseperfftdeg = mod(phasepersampledeg * fftlen,360.0);





phdegmean = 360*rand() - 180;
%phdegmean=179.5

%start w/ mean phase., add phase noise.
phdeg=phdegmean*ones(simlen,1);
phdegstd = 5*rand()
phdeg = phdeg + phdegstd*randn(simlen,1);

%add phase offset per fft
phdeg = phdeg  + (1:simlen)'.*phaseperfftdeg;
%mod to 2pi, so it stays in a circle
phdeg = mod(phdeg,360);
%convert from degrees to normalized to 2.0. 360deg--> 2.0  like 2pi.
ph = phdeg / 180;


%set up magnitude term to a const plus noise.

mgmean = 0.5 * rand();
mgstd = 0.05 * rand();
mg=mgmean*ones(simlen,1);
mg = mg + mgstd*randn(simlen,1);
end 