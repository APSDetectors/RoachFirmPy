function HDFR_List(filename)
%list strings you can use in the HDF_getSetting function. these
%strings are all names for data stored in the HDF file, like span,
%start and end freq. some of the settings are actually not in the file
%but calculated from data in the file.


%h5disp(filename,'/','min')
[device_name, resnumbers ,numtraces,centfreqs,devgroup,resgroups,tracegroups,tf]=HDFR_Info(filename);


fprintf('Device Name %s\n',device_name)



for k=1:length(resnumbers)




fprintf (' Resonator: %2.0f  Fc %4.2f MHz Traces %2.0f\n', resnumbers(k),centfreqs(k)/1e6,numtraces(k));



end


disp 'Trace Fields'
tf'


