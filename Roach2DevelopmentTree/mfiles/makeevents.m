FRT=12800/3;
FRA=1.0;
T=12.8;
V=0.01;

%(-sin(3*2*pi*(0:(SL-1))/SL)) .* hamming(SL)'

%cos(3*2*pi*(0:(SL-1))/SL) .* hamming(SL)'
compiletime = now

T=50000;

L=100;
L2= L+2;
SL=L;


evtlen=timeseries(ones(1,T)*(L));

isflxdemod = timeseries( ones(1,T)  );
saveflraw = timeseries( zeros(1,T)  ); 
savefltran = timeseries( ones(1,T)  ); 

clrfifo_= zeros(1,T);
clrfifo_(100)=1;
clrfifo   = timeseries( clrfifo_  );




rst   = timeseries( zeros(1,T)  );

newevt_ =  zeros(1,T);
datain_= zeros(1,T);
fifowrite_ =  zeros(1,T);


transtable = zeros(1024,1);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% set up translation
%


xtr =rand() - 0.5
ytr= rand() - 0.5


%xtr =  -6.464950048486657e-01
%ytr =   1.126503644473278e-01

%xtr =  -4.221468669050195e-01
%ytr =   7.252160700325976e-01


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%set up translator bin vars



transtable(65) = transTable(0.065,0.055);

transtable(66) = transTable(-0.054,-0.056);
transtable(67) = transTable(-0.085,0.015);
transtable(68) = transTable(-0.070,0.045);

transtable(1) = transTable(xtr,ytr);
%%%%%%%%%%%%%%%%%%%%%%%%%%
% num events and how far apart in time

numevents = 8;
deadtime = 1;

Tc = 2000;


%%%%%%%%%%%%%%%%%%%%%%
% Set up phase mags


fftph=zeros(1,numevents);
phbin = 3;
anginc = 0.1;
phsinc = 0.0;
ang = 0;
%phsoffs = rand() * 2.0*pi;
%mymag =rand()/2
phsoffs = pi;
mymag =0.1;
maginc=0.00;


%%%%%%%%%%%%%%%%%%%%%%%%%
% make events
%
figure(3)
clf()
hold on;

allmagin = []
allphsin = []

ptr = 1

for e=1:numevents
 mag =mymag +  0.0001 * rand(1,L);
phs = 2*pi*0.1*cos(ang + (phbin*2*pi*(1:L)/L));
phs = phs +  0.000005*2*pi * rand(1,L);
phs=phs+phsoffs;

phsoffs = phsoffs + phsinc;
ang = ang +anginc;
mymag = mymag + maginc;


xin = mag.*cos(phs);
yin = mag.*sin(phs);
xin = xin - xtr;
yin = yin -ytr;

mag =sqrt( xin.*xin + yin.*yin);
phs = atan2(yin,xin);


FF=fft(phs);
fftph(e)=angle(FF(phbin+1));
figure(3)
plot(xin,yin,'.')
drawnow


event = makeAAAAEvent(mag,phs/pi,0,0,0);
%[event , ptr]=extractAAAAEvent(ptr,roachrawdata);

Tc = Tc + deadtime;

datain_(Tc:(Tc+L2-1)) = event;
fifowrite_(Tc:(Tc+L2-1)) = 1;
newevt_(Tc+L2+1) = 1;

Tc = Tc + L2;


allmagin = [allmagin; mag'];
allphsin = [allphsin; phs'/pi];

end



%%%%%%%%%%%%%%%%%%5
% initial plots before sim


plot(0,0,'rx');
plot(1,0,'rx');
plot(0,1,'rx');
plot(-1,0,'rx');
plot(0,-1,'rx');





datain = timeseries(datain_);
fifowrite = timeseries(fifowrite_);
newevt = timeseries(newevt_);


%figure(1)
% subplot(3,1,1)
% plot(datain_(1:Tc))
  
% subplot(3,1,2)
% plot(fifowrite_(1:Tc))
  
% subplot(3,1,3)
% plot(newevt_(1:Tc))
  
 
 figure(2)
 plot(fftph)
 
 
 figure(4)
 clf()
subplot(2,1,1)
plot(allmagin)
subplot(2,1,2)
plot(allphsin)

 
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
 %sim('fluxrampdemodulationb')
 
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
 
 %after simulation
 
 dftvld =  ScopeData6.signals(3).values;
 dftI=ScopeData6.signals(1).values;
 dftQ = ScopeData6.signals(2).values;
 
 dftIvld = dftI(find(dftvld==1));
 
 dftQvld = dftQ(find(dftvld==1));
 
 dftPh = atan2(dftQvld,dftIvld);
% figure(103)
% plot(dftPh)
 
 
 
 %after simulation
 
 odv =  outdftdata.signals(3).values;

 odp = outdftdata.signals(2).values;
 
 odp2 = odp(find(odv==1));
 

 %figure(104)
 %plot(odp2*pi)
 

 
 
% figure(105)
% clf()
% hold on
 
 outdata = output.signals(1).values;
 outwr = output.signals(2).values;
 
 outdata2=outdata(find(outwr==1));
 
 k=1;
 fangles0=zeros(1,5000);
 fangles1=zeros(1,5000);
 aa = 1;
 
 allmags = []
 allphs = []
 
 
 while((k+110)<length(outdata2))
  fives = outdata2(k);
  %dec2hex(fives)
  k=k+1;
  if uint32(fives/65536)==hex2dec('5555') 
      
    evtlenx = bitand(fives,255);
    evtype = bitand(fives,255*256) / 256;
    
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
    
      
    allmags = [allmags; magf];
    allphs = [allphs ; phsf];
    
    
   % plot(phsf)
   % drawnow
    
    
    FF=fft(phsf);
    fangles0(aa) = angle(FF(4));
    fangles1(aa) = pi*flrf;
    k=k+100;
    aa=aa+1;
    
  end
  
     
     
 end
 
 evtlenx
 evtype
 
 
 figure(106)
 clf()
 plot(fangles0(1:50))
 plot(fangles0(1:50),'bo')
 hold on
 plot(fangles1(1:50),'rx')
 
 
 
 figure(107)
 clf()
subplot(2,1,1)
plot(allmags);
subplot(2,1,2);
plot(allphs);

 
 
 allx = allmags .* cos(pi*allphs);
 
 ally = allmags .* sin(pi*allphs);
 
 
 figure(108)
 clf()
 hold on
 
plot(allx,ally)
 plot(0,0,'rx')
 
 plot(0.2,0,'rx')
 plot(0,0.2,'rx')
 plot(-0.2,0,'rx')
 plot(0,-0.2,'rx')
 
 
 
 
 
 
  
 pretranslateI =  scope_beforetr.signals(1).values;
pretranslateQ =  scope_beforetr.signals(2).values;
 ptvld = scope_beforetr.signals(3).values;
 
pretranslateI  = pretranslateI(find(ptvld==1));
 pretranslateQ  = pretranslateQ(find(ptvld==1));
 

  
 afttranslateI =  scope_aftertr.signals(1).values;
afttranslateQ =  scope_aftertr.signals(2).values;
 atvld = scope_aftertr.signals(3).values;
 
  afttranslateI= afttranslateI(find(atvld==1));
  afttranslateQ =afttranslateQ(find(atvld==1));
 

 
 figure(109)
 clf()
 plot(pretranslateI,pretranslateQ,'b')
 hold on;
 plot(afttranslateI,afttranslateQ,'r')
 
 
 
  plot(0,0,'rx')
 
 plot(0.2,0,'rx')
 plot(0,0.2,'rx')
 plot(-0.2,0,'rx')
 plot(0,-0.2,'rx')
 

 
 
 
 
 
 