

evtlen_=[95];
evtlen=timeseries(evtlen_);



fifoempty_=[false];
fifoempty=timeseries(fifoempty_);

mags = uint32(16000*ones(1,10000));

T = 95/2;
numcos = 10000 / T;
phs =0.1*cos(numcos* 2*pi*(1:10000)/10000   );
figure(1)
subplot(3,1,1)
plot(phs(1:95))


dpoint = 13;
nbits = 16;

phs = phs.*(2^dpoint);
subplot(3,1,2)
plot(phs(1:95))

for i =1:length(phs)
    if phs(i)<0
    phs(i) = (2^nbits) - phs(i);
    end
end

phs = uint32(phs);

subplot(3,1,3)
plot(phs(1:95))








datain_ = uint32(mags*65536 + phs);





newevt_=zeros(1,10000);
i = 290:150:10000;
newevt_(i) = 1;
newevt=timeseries(newevt_);


head = 150:150:10000;
datain_(head)=hex2dec('aaaa0000');
datain_(head+1)=0;

fifowrite_=zeros(1,10000);
for wr=head
    fifowrite_(wr:(wr+96))=1;
end
fifowrite=timeseries(fifowrite_);





datain=timeseries(datain_);


rst_=[false];
rst=timeseries(rst_);


clrfifo_=[false];
clrfifo=timeseries(clrfifo_);




isflxdemod_=[false];
isflxdemod=timeseries(isflxdemod_);


saveflraw_=[true];
saveflraw=timeseries(saveflraw_);


wrxx=output.signals(2).values
ooxx=uint32(output.signals(1).values);

oolo=bitand(65535,ooxx);

oohi=bitshift(ooxx,-16);

dec2hex(oohi);

dec2hex(datain_);

find(datain_==hex2dec('aaaa0000'));


%   dec2hex(outfsm1.signals(1).values(find(outfsm1.signals(2).values==1)))
%   aa=outfsm1.signals(1).values(find(outfsm1.signals(2).values==1));
%   aa=uint32(output.signals(1).values(find(output.signals(2).values==1)));


% dec2hex(aa(1:99))

%   plot(outfsm1.signals(1).values(find(outfsm1.signals(2).values==1)))




dec2hex(ooxx)

 clf;
 subplot(2,1,1)
 plot(wrxx(300:500))
subplot(2,1,2)
 plot(ooxx(300:500))
