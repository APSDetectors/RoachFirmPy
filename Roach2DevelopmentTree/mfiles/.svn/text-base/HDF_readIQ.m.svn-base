



function [i,q,freqs,f_cent,f_span,timestamp]=HDF_readIQ(filename, sweep_index)
%hdf file is a list of sweeps doen by net analuyzer. give filename
%and which sweep as an integer from 1 to 4096 (max size of file for now...)
%it returns i,q and freq vector as well as center freq, span and string
%timestamp as to when the sweep was taken.
%call as such
%[i,q,f]=HDF_readIQ('myfile.hdf', 22)
%or for more info
%[i,q,freqs,f_cent,f_span,timestamp]=HDF_readIQ('myfile.hdf', 29)
%the 22 and 29 are just examples for sweep 22 and 29.


iq=h5read(filename,'/IQData/IQ',[1 1 sweep_index],[2048,2,1]);
 i=iq(:,1);
 q=iq(:,2);

 i=i(2048:-1:1,1);
 q=q(2048:-1:1,1);
 
 stf=h5read(filename,'/Settings/SweepStFreq',[sweep_index],[1]);
 edf=h5read(filename,'/Settings/SweepEdFreq',[sweep_index],[1]);
 incf=h5read(filename,'/Settings/SweepIncFreq',[sweep_index],[1]);
rawfreqs=stf:incf:(edf-incf);

LO=h5read(filename','/Settings/LOFreq',[sweep_index],[1]);


freqs=LO - fliplr(rawfreqs);


freqs=freqs';
f_cent=LO - (stf+edf)/2;
f_span = edf-stf;

timestamp = h5read(filename,'/IQData/Times',[sweep_index],[1]);


end

