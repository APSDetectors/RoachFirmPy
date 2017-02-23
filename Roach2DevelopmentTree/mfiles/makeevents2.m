
%(-sin(3*2*pi*(0:(SL-1))/SL)) .* hamming(SL)'

%cos(3*2*pi*(0:(SL-1))/SL) .* hamming(SL)'


T=50000;

L=100;
L2= L+2;
SL=L;


evtlen=timeseries(ones(1,T)*(L));

isflxdemod = timeseries( ones(1,T)  );
saveflraw = timeseries( ones(1,T)  ); 
clrfifo_= zeros(1,T);
clrfifo_(100)=1;
clrfifo   = timeseries( clrfifo_  );




rst   = timeseries( zeros(1,T)  );

newevt_ =  zeros(1,T);
datain_= zeros(1,T);
fifowrite_ =  zeros(1,T);


numevents = 40;
deadtime = 100;

Tc = 2000;

fftph=zeros(1,numevents);
phbin = 3;
anginc = 0.1;
phsinc = 0.0;
ang = 0;
phsoffs = -1;
figure(10)
clf()
hold on;
mymag =0.006;
maginc=0.00;

for e=1:numevents
 mag =mymag +  0.0001 * rand(1,L);
phs = 0.1*cos(ang + (phbin*2*pi*(1:L)/L));
phs = phs +  0.000005*2*pi * rand(1,L);
phs=phs+phsoffs;

phsoffs = phsoffs + phsinc;
ang = ang +anginc;
mymag = mymag + maginc;
FF=fft(phs);
fftph(e)=angle(FF(phbin+1));

plot(phs)
drawnow


event = makeAAAAEvent(mag,phs,192,0,0);

Tc = Tc + deadtime;

datain_(Tc:(Tc+L2-1)) = event;
fifowrite_(Tc:(Tc+L2-1)) = 1;
newevt_(Tc+L2+1) = 1;

Tc = Tc + L2;

end

datain = timeseries(datain_);
fifowrite = timeseries(fifowrite_);
newevt = timeseries(newevt_);


figure(1)
 subplot(3,1,1)
 plot(datain_(1:Tc))
  
 subplot(3,1,2)
 plot(fifowrite_(1:Tc))
  
 subplot(3,1,3)
 plot(newevt_(1:Tc))
  
 
 figure(2)
 plot(fftph)
 
 

 
 
 %after simulation
 
 dftvld =  ScopeData6.signals(3).values;
 dftI=ScopeData6.signals(1).values;
 dftQ = ScopeData6.signals(2).values;
 
 dftIvld = dftI(find(dftvld==1));
 
 dftQvld = dftQ(find(dftvld==1));
 
 dftPh = atan2(dftQvld,dftIvld);
 figure(103)
 plot(dftPh)
 
 
 
 %after simulation
 
 odv =  outdftdata.signals(3).values;

 odp = outdftdata.signals(2).values;
 
 odp2 = odp(find(odv==1));
 

 figure(104)
 plot(odp2*pi)
 

 
 
 figure(105)
 clf()
 hold on
 
 outdata = output.signals(1).values;
 outwr = output.signals(2).values;
 
 outdata2=outdata(find(outwr==1));
 
 k=1;
 fangles0=zeros(1,5000);
 fangles1=zeros(1,5000);
 aa = 1;
 
 while((k+110)<length(outdata2))
  fives = outdata2(k);
  %dec2hex(fives)
  k=k+1;
  if uint32(fives/65536)==hex2dec('5555') 
      
      
    flr=outdata2(k);k=k+1;
    
    flrf = double(flr)/(2^13);
    if flrf>=4.0
        flrf = flrf - 8.0;
    end
    
    
   % dec2hex(flr)
    aaaa=outdata2(k);k=k+1;
    %dec2hex(aaaa)
    head=outdata2(k);k=k+1;
    %dec2hex(head)
    
    magphs = uint32(outdata2(k:(k+99)));
    %dec2hex(magphs)
    phs = bitand(magphs,uint32(65535));
    mag = bitand(magphs,uint32(65535*65536))/65536;
    magf = double(mag)/65536;
    
    phsf = double(phs)/(2^13);
    for m = 1:length(phsf)
        if phsf(m)>=4.0
            phsf(m) = phsf(m)-8.0;
        end
    end
    
    plot(phsf)
    drawnow
    
    
    FF=fft(phsf);
    fangles0(aa) = angle(FF(4));
    fangles1(aa) = pi*flrf;
    k=k+100;
    aa=aa+1;
    
  end
  
     
     
 end
 
 figure(106)
 clf()
 plot(fangles0(1:50))
 plot(fangles0(1:50),'bo')
 hold on
 plot(fangles1(1:50),'rx')
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 