


function outdata = iq(foffset,is_plot)

%is_plot = 1;

Cfreq=20000;
Ifreq=20;
Qfreq=20;


qchange = 0;

sigmoiderr=qchange * ((2./(1+exp( foffset)))-1);

Q=(5000-4900*abs(sigmoiderr));

Ffreq=Cfreq+Ifreq-2*Ifreq + foffset;

L=65536;

plotL=50;

w0=2 * (Ffreq/L);
[b,a]=iirnotch(w0,w0/Q);
%figure(1)
[fh,fw]=freqz(b,a,L/2);


carrierI=cos(Cfreq*2*3.14159*(1:L)./L);

carrierQ=sin(Cfreq*2*3.14159*(1:L)./L);


Idata=2*cos(Ifreq*2*3.14159*(1:L)./L);
Qdata=-2*sin(Qfreq*2*3.14159*(1:65536)./65536);
%Qdata = Idata;

rf = Idata.*carrierI - Qdata.*carrierQ;


frf=filter(b,a,rf);
%frf = rf;

retrvQ=carrierQ.*frf;
retrvI=carrierI.*frf;


IQcmplx=retrvI +i* retrvQ;

F=fft(IQcmplx);
FRF=fft(frf);

if is_plot>0
% 
% figure(4)
% subplot(2,1,1)
% plot(abs(F))
% subplot(2,1,2)
% plot(angle(F))


figure(2)

clf
subplot(4,1,1)
plrf=(Cfreq-plotL):(Cfreq+plotL);
plot(plrf,abs(FRF(plrf)),'b',plrf,L*abs(fh(plrf)),'r')

%plot(2*plrf./L,abs(fh(plrf)),'r')


subplot(4,1,2)
%plot(2*(1:plotL)./L,real(F(1:plotL)))
plot(abs(F(1:plotL))/L)

subplot(4,1,3)
%plot(2*(1:plotL)./L,imag(F(1:plotL)))
plot(angle(F(1:plotL))/L)


subplot(4,1,4)
%plot(2*(1:plotL)./L,imag(F(1:plotL))+real(F(1:plotL)))
plot(1:plotL,real(F(1:plotL)),'b',1:plotL,imag(F(1:plotL)),'r')



% 
% figure(3)
% theta=angle(F(1:plotL));
% mag=abs(F(1:plotL));
% polar(theta,mag)

end

outdata=[abs(F(Ifreq+1))/L 180*angle(F(Ifreq+1))/3.14159];
end

