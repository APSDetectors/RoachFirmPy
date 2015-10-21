


filename = 'test11.hdf';


HDFR_List(filename);

resnum=2;
delays= HDFR_getSetting(filename,resnum,'delay');




tracenum=find(delays==delays(1));


 [i,q,freqs]=HDFR_readIQ(filename,resnum, tracenum(1));
 
 
 clf();
 plot(freqs, i.^2 + q.^2);
 

 
 filename = 'test15.hdf'
 
 %now do a loop on resonators
 [device_name, resnumbers ,numtraces,centfreqs,devgroup,resgroups,tracegroups,tracefields]=HDFR_Info(filename);
 
 

 for k=1:length(resnumbers)
     
     resnum=resnumbers(k);
     
     
     fprintf('Res number %2.0f  CentFreq %4.2fMHz\n',resnum, centfreqs(k)/1e6);
     att= HDFR_getSetting(filename,resnum,'atten_U7');
     
     indx=find(att==5);
     
     [i,q,freqs]=HDFR_readIQ(filename,resnum, indx);
     
     
 end
 
     
     
     