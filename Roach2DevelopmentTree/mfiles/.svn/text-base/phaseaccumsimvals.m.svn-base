
simlen = 2000000
lutlen=8192;
nwaves=9431;
nwaves1=6531;

fftlen=512;
[ph0,mg0,phaseperfftdeg0]=makephasedata(simlen/2,lutlen,nwaves,fftlen);

[ph1,mg1,phaseperfftdeg1]=makephasedata(simlen/2,lutlen,nwaves1,fftlen);




%for now we test chan 0

chan0=zeros(simlen/2,1);
chan1=ones(simlen/2,1);

%set uip phase corrector RAM.
phaseincnumbers=zeros(1,256);
phaseincnumbers(1)= (-1 * phaseperfftdeg0)/180.0;
phaseincnumbers(2)= (-1 * phaseperfftdeg1)/180.0;



deadtime=8;
chantime = 2;
blocksize=32;
%interleave the data  in block sizes

incnt0=1;
incnt1=1;
outcnt=1;


dvldout=zeros(simlen,1);
chanout=zeros(simlen,1);
phaseout=zeros(simlen,1);
magout = zeros(simlen,1);

%
% Interlwave two channels
%

while outcnt<=(simlen- (deadtime+2*blocksize + 2*chantime))

    
    for k =1:chantime
        chanout(outcnt)=chan0(incnt0);
        outcnt=outcnt+1;
        
    end
        
    for k=1:blocksize
        chanout(outcnt)=chan0(incnt0);
        dvldout(outcnt)=1;
        phaseout(outcnt)=ph0(incnt0);
        magout(outcnt)=mg0(incnt0);
        outcnt=outcnt+1;
        incnt0=incnt0+1;
    end
    
    outcnt = outcnt+deadtime;
   
    for k =1:chantime
        chanout(outcnt)=chan1(incnt1);
        outcnt=outcnt+1;
        
    end
    
    
    for k=1:blocksize
        chanout(outcnt)=chan1(incnt1);
        dvldout(outcnt)=1;
        phaseout(outcnt)=ph1(incnt1);
        magout(outcnt)=mg1(incnt1);
        outcnt=outcnt+1;
        incnt1=incnt1+1;
    end
    
    outcnt = outcnt+deadtime;
    
    
    
end







phasedata = timeseries(phaseout);
magdata = timeseries(magout);
chandata = timeseries(chanout);

dvlddata = timeseries(dvldout);

PhaseCorrect1_phaseIncVal = timeseries(zeros(1,simlen));

PhaseCorrect1_phaseIncAddr = timeseries(zeros(1,simlen));


PhaseCorrect1_phaseIncProgWe = timeseries(zeros(1,simlen));


figure(1)
subplot(4,1,1);

plot(chanout(1:256))
subplot(4,1,2)
plot(dvldout(1:256))
subplot(4,1,3)
plot(magout(1:256))
subplot(4,1,4)
plot(phaseout(1:256))


