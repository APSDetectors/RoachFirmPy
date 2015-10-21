
function [i,q,freqs]=HDFR_readIQ(filename,resnum, tracenum)
%hdf file is a list of sweeps doen by net analuyzer. give filename
%and which sweep as an integer from 1 to 4096 (max size of file for now...)
%it returns i,q and freq vector as well as center freq, span and string
%timestamp as to when the sweep was taken.
%call as such
%[i,q,f]=HDF_readIQ('myfile.hdf', 22)
%or for more info
%[i,q,freqs,f_cent,f_span,timestamp]=HDF_readIQ('myfile.hdf', 29)
%the 22 and 29 are just examples for sweep 22 and 29.



[device_name, resnumbers ,numtraces,centfreqs,devgroup,resgroups,tracegroups,tf]=HDFR_Info(filename);



indx=find(resnumbers==resnum);

dir1=strcat('/',devgroup,'/',cell2mat(resgroups(indx)),'/');


    
    dir2=strcat(dir1,cell2mat(tracegroups(indx,tracenum)),'/','iqdata');
    
     
iq=h5read(filename,dir2,[1 1],[2048,2]);
 i=iq(:,1);
 q=iq(:,2);

 
  

  
    dir2=strcat(dir1,cell2mat(tracegroups(indx,tracenum)),'/','freqs');
    
     
freqs=h5read(filename,dir2,[1],[2048]);
 


