
phdegmean = 360*rand() - 180
%phdegmean=179.5

phdeg=phdegmean*ones(20000,1);


mgmean = 0.5 * rand()

mgstd = 0.05 * rand()
phdegstd = 5*rand()

mg=mgmean*ones(20000,1);

phdeg = phdeg + phdegstd*randn(20000,1);


phdeg = mod(phdeg,360);
ph = phdeg / 180;

mg = mg + mgstd*randn(20000,1);

chan=zeros(20000,1);

pdlen = 10*ones(20000,1);

magphmeanmem = zeros(1024,1);
threshmem = zeros(1024,1);

phmeanb=double(toTwoComp(phdegmean/180.0,16,13));
mgmeanb=double(toTwoComp(mgmean,16,14));

threshv= 6*2*(mgstd + phdegstd/180)

thresh=double(toTwoComp(threshv,18,16));

magphmeanmem(1)=mgmeanb + 2.^16 * phmeanb;


threshmem(1) = thresh;




plen = 10;
npulses =10

mgsign = sign(rand()-0.5);
phsign = sign(rand()-0.5);
for k=1:npulses
   
    tt=floor(1 + (20000-2*plen)*rand());
    
    mg(tt:(tt+plen))=mg(tt:(tt+plen)) + mgsign*0.1;
    ph(tt:(tt+plen))=ph(tt:(tt+plen)) + phsign*0.5;

end


phasedata = timeseries(ph);
magdata = timeseries(mg);
chandata = timeseries(chan);

PulseDetector_pulselength = timeseries(pdlen);




