
is_movie=0;

pulslen=64;


pulse = 0.5 - 0.5*cos(3.14159*2*(1:pulslen)./pulslen);
pulse = ((((pulslen:-1:1) - 1)./pulslen).^4).*pulse;
pulse=pulse/max(pulse);


amplitude = 2
pulse=amplitude*pulse;
figure(10);
plot(pulse);


amps=zeros(1,pulslen);
phases=zeros(1,pulslen);

for k=1:pulslen
    
    r=iq(pulse(k),1);
    amps(k)=r(1);
    phases(k)=r(2);
    
    if is_movie>0
   figure(2)
   M2(k)=getframe(2);
    end
    
    figure(11)
    subplot(3,1,1)
    plot(amps)
    subplot(3,1,2)
    plot(phases)


%    figure(12)
    subplot(3,1,3)
    polar(3.14159*phases(1:k)/180,amps(1:k))
    
    if is_movie>0
    M11(k)=getframe(11);

    end
    
end



 if is_movie>0
movie2avi(M2,'m2movie.avi')
movie2avi(M11,'m11movie.avi')
 end
 