lutx=lutcos.data + j*lutsin.data;
modx=mcos.data + j*msin.data;
dmodx = dmcos.data + j*dmsin.data;

sw = swcos.data + j*swsin.data;


figure(1)
plot(abs(fft(lutx)))

figure(2)
plot(abs(fft(sw)))

figure(3)
plot(abs(fft(modx)))



figure(4)
plot(abs(fft(dmodx)))


