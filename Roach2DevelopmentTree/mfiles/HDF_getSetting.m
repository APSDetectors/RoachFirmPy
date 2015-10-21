

function set= HDF_getSetting(filename,setname)
%get a vector of data from /Settings. A vector is returned, one element
%for each analuyzer sweep. Though the file always stores vectors of len
%4096, the returned vector here is only the elements where there is
%valid data, which could be much shorter...
%also we can return vectors of data that arre calculated from stored 
%data in hdf file, like freq span and freq center of sweep.


%find leng of data in the file. if LO is 0, then no data for that sweep.
%the jdf file always has vectors of 4096 len as defailt, but that does
%not mean there is valid data in the whole vector...

LO=h5read(filename','/Settings/LOFreq',[1],[4096]);
setlen=length(find(LO));


if (strcmp(setname,'Freq_Span'))

     stf=h5read(filename,'/Settings/SweepStFreq',[1],[4096]);
 edf=h5read(filename,'/Settings/SweepEdFreq',[1],[4096]);
 incf=h5read(filename,'/Settings/SweepIncFreq',[1],[4096]);


LO=h5read(filename','/Settings/LOFreq',[1],[4096]);

f_cent=LO - (stf+edf)./2;
f_span = edf-stf;

set=f_span(1:setlen);   

elseif   (strcmp(setname,'Freq_Cent'))  
    
    
     stf=h5read(filename,'/Settings/SweepStFreq',[1],[4096]);
 edf=h5read(filename,'/Settings/SweepEdFreq',[1],[4096]);
 incf=h5read(filename,'/Settings/SweepIncFreq',[1],[4096]);


LO=h5read(filename','/Settings/LOFreq',[1],[4096]);
f_cent=LO - (stf+edf)/2;
f_span = edf-stf;

set=f_cent(1:setlen);
    
else
    
setx=h5read(filename,strcat('/Settings/',setname),[1],[4096]);
set=setx(1:setlen);
end

