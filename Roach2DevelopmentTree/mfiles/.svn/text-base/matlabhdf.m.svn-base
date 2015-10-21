
%this is example on how to use the matlab hdf reading of roach data


filename ='ResDev150_Feb12_00003.hdf'

%list all settings/attributes in the file. 
%settings are settings in the roach board like atteniation, center freq,
%span etc. All the info you need in addition to IQ sweeps
HDF_ListSettings(filename)


%get all attenuations, spans and cent freqs
AttenU7=HDF_getSetting(filename,'AttenU7');
span=HDF_getSetting(filename,'Freq_Span');
fc=HDF_getSetting(filename,'Freq_Cent');


%find sweeps for att =10dB and span at 2MHz, return list if indices
ind=find(AttenU7==10 & span==2000000)


%list all center frequencies for 10dB attenuation and span is 2MHz
fc(ind)

%get the sweep indeix for  freq at 3.219Ghz, for that resonator.

ind=find(AttenU7==10 & span==2000000 & fc>3.21e9 &fc<3.22e9)


%get IQ data
[i,q,freqs]=HDF_readIQ(filename, ind);

% plot

clf()
subplot(2,1,1)
plot(freqs,i.^2 + q.^2)
subplot(2,1,2)
plot(freqs,atan2(q,i))




