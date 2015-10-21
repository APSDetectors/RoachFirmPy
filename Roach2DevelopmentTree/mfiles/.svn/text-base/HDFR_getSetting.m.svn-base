

function set= HDFR_getSetting(filename,resnum,setname)
%get a vector of data from /Settings. A vector is returned, one element
%for each analuyzer sweep. Though the file always stores vectors of len
%4096, the returned vector here is only the elements where there is
%valid data, which could be much shorter...
%also we can return vectors of data that arre calculated from stored 
%data in hdf file, like freq span and freq center of sweep.


%find leng of data in the file. if LO is 0, then no data for that sweep.
%the jdf file always has vectors of 4096 len as defailt, but that does
%not mean there is valid data in the whole vector...

[device_name, resnumbers ,numtraces,centfreqs,devgroup,resgroups,tracegroups,tf]=HDFR_Info(filename);



indx=find(resnumbers==resnum);

dir1=strcat('/',devgroup,'/',cell2mat(resgroups(indx)),'/');

set = zeros(numtraces,1);

for trnum=1:numtraces
    
    dir2=strcat(dir1,cell2mat(tracegroups(indx,trnum)),'/',setname);
    
    val=h5read(filename,dir2,[1],[1]);
    
    set(trnum)=val;
    
end


end

