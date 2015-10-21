

%number of data chennels
nchans=1;

%len of sim data
L=32768;

%set to in int 1,2,3 etc. how long to hold sample n samples
Wait=2


%final data for sim
datai = zeros(1,L);

dataq = zeros(1,L);

last_channel=ones(1,L).*(nchans-1);

is_calc_mean_=zeros(1,L);
is_calc_mean_(1:8000)=1;

cur_chan=zeros(1,L);
dvld=zeros(1,L);

%data without waits, raw samples of interlaced channels
datai_s = zeros(1,L/Wait);

dataq_s = zeros(1,L/Wait);

dvld_s=zeros(1,L/Wait);
cur_chan_s=zeros(1,L/Wait);


%list of phase rotations for each channel
phase_rots=zeros(1,nchans);

%make pulse/nosie data for each chen
for k =1:nchans
    %len of data for each channel
    PL=L/nchans;
    PL=PL/Wait;
    %make noise and pulses for 1 chan
    [i1,q1,phrot]=makepulses(PL);
    %record phase rotation for that chan
    phase_rots(k) = -1.0*phrot;

    %interlave chan into the data vector
    datai_s(k:nchans:(L/Wait))=i1;

    dataq_s(k:nchans:(L/Wait))=q1;
    
    %set chan and dvld
    dvld_s(k:nchans:(L/Wait))=1;
    
    cur_chan_s(k:nchans:(L/Wait))=k-1;
end

%put the waits in- 
%it will put copies of the raw data decimated by Wait, so the data
%holds for Wait samples for each point
for w=1:Wait
    datai(w:Wait:L)=datai_s;
    dataq(w:Wait:L)=dataq_s;
    
    cur_chan(w:Wait:L)=cur_chan_s;
   
end
dvld(1:Wait:L)=dvld_s;
%compute data for programming the phase accum ram
[inc,addr,we]=phaseincprog(L,phase_rots);

%convert data to timeseries
PhaseCorrect1_phaseIncVal=timeseries(toTwoComp(inc,32,30));
PhaseCorrect1_phaseIncAddr=timeseries(addr);
PhaseCorrect1_phaseIncProgWe=timeseries(we);

figure(4);
clf
subplot(2,1,1)
plot(datai)
subplot(2,1,2)
plot(dataq)


tdataq=timeseries(dataq);
tdatai=timeseries(datai);
tdvld=timeseries(uint32(dvld));
tcur_chan=timeseries(uint32(cur_chan));
is_calc_mean = timeseries(uint32(is_calc_mean_));
tlast_channel=timeseries(last_channel);

%
% dbugging data
%

di0=datai(1:(Wait*nchans):L);
dq0=dataq(1:(Wait*nchans):L);
dm0=sqrt(di0.^2 + dq0.^2);
dp0=atan2(dq0,di0)/pi;
dpd0=diff(dp0);
mdpd0=median(dpd0);

figure(100);
clf();
subplot(2,1,1);
plot(di0);
hold on;
plot(dq0,'g');
subplot(4,1,3)
plot(dm0);
subplot(4,1,4);
plot(dp0);
hold on;
plot(dpd0,'g');
text(L/(2*nchans*Wait),0,sprintf('mdpd0=%f, inc=%f',mdpd0,inc(1)))



figure(5)
clf()
subplot(2,1,1)
plot(sqrt(datai.*datai + dataq.*dataq))
subplot(2,1,2)
plot(atan2(dataq,datai))


