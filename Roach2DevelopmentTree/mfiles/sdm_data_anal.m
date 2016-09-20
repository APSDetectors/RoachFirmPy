sd = sdmdata.signals(2).values;

SD = abs(fft(sd.*hamming(length(sd))));

figure(1);
freqs = (1:length(SD) ).*128e6/length(SD);
SD = 4*SD/length(SD);

subplot(2,1,1)
semilogy(freqs,SD.^2);

axis([0 5000e3 1e-10 1e-1]);

subplot(2,1,2)
semilogy(freqs,SD.^2);

axis([0 64e6 1e-10 1e-1]);