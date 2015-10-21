
fftMemWE= [zeros(1,8)   0 0 0 0 0 0 0 0   1 1 1 1 1 1 1 1 ones(1,8192)  0 0 0 0 0 0 0 0   1 1 1 1 1 1 1 1 ones(1,8192) ];
startFFTs=[zeros(1,8)   0 0 0 0 1 1 1 1   1 1 1 1 1 1 1 1 ones(1,8192)  0 0 0 0 1 1 1 1   1 1 1 1 1 1 1 1 ones(1,8192) ];


len=length(fftMemWE)


mainRst=[1 zeros(1,len-1)];



startfftsimd= [ ones(1,9500) zeros(1,500)  ones(1,9500) zeros(1,500)]

startfftsim=timeseries(startfftsimd);




seeaddress=[zeros(1,len)];
startDac=[ones(1,len)];


adcwavememStart=[zeros(1,len)];
adcwavememWE=[zeros(1,len)];
adcwavememSel=[zeros(1,len)];
adcforcesync=[zeros(1,len)];
dacLoopBack=[ones(1,len)];
useTestFreq=[zeros(1,len)];
resetDAC=[zeros(1,len)];
dumpFifo=[ones(1,len)];


stFFTMem=[ 0 0 0 0 0 0 0 1 zeros(1,len-8)];




control_regd=mainRst + 2*stFFTMem + 4*fftMemWE + 8*seeaddress ;
control_regd = control_regd + 16*startDac + 64*startFFTs + 128*adcwavememStart;
control_regd = control_regd + 256*adcwavememWE + 512*adcwavememSel + 4096*adcforcesync;

control_regd = control_regd + 8192*dacLoopBack + 16384*useTestFreq + 32768*resetDAC;
control_regd = control_regd + 65536*dumpFifo;


controlReg=timeseries(control_regd);


