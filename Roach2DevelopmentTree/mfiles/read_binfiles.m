



fileID = fopen('res57575_2_sweep_I.bin')
sweepI = fread(fileID,'double')';
fclose(fileID);


fileID = fopen('res57575_2_sweep_Q.bin')
sweepQ = fread(fileID,'double')';
fclose(fileID);


swmag = abs( sweepI + j*sweepQ);

swph = angle( sweepI + j*sweepQ);

figure(1)
subplot(2,1,1)
plot(swmag)
subplot(2,1,2)
plot(swph)

figure(3)
plot(sweepI,sweepQ)


fileID = fopen('res57575_2_stream_mag_ramp.bin')
mags = fread(fileID,'double')';
fclose(fileID);


fileID = fopen('res_57575_2_stream_phase_ramp.bin')
phasesr = fread(fileID,'double')';
fclose(fileID);



nI = mags .* cos(phasesr);
nQ = mags .* sin(phasesr);


figure(3)
hold on
plot(nI,nQ,'r.')





phases = phasesr / (pi);
phases = phases - 346;



phases = [swph/pi , phases];
figure(4)
plot(phases(1:1000))


mags = [swmag , mags];

magtime = timeseries(mags);
phasetime = timeseries(phases);


sync = zeros(1,length(phases));

ping = 350;

i = ping:100:length(phases);
sync(i) = 1;


synctime = timeseries(sync)

figure(4)

subplot(3,1,1)
plot(mags(1:400))
subplot(3,1,2)
plot(phases(1:400))
subplot(3,1,3)
plot(sync(1:400))


