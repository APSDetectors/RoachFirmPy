function [device_name, resnumbers ,numtraces,centfreqs,devgroup,resgroups,tracegroups,tracefields]=HDFR_Info(filename)
%**************************************************************************
%
%  This example shows how to iterate over group members using
%  H5Giterate.
%
%  This file is intended for use with HDF5 Library version 1.8
%**************************************************************************
%filename      = 'test11.hdf';

%
% Open file.
%
file = H5F.open (filename, 'H5F_ACC_RDONLY', 'H5P_DEFAULT');

group_id = H5G.open(file,'/');


%
% Begin iteration.
%
%fprintf ('Objects in root group:\n');


opdata_in=cell(100,1);
opdata_in(1)=num2cell(2);


%get dirs in root
[status,idx_out,opdata_out]= H5L.iterate(group_id ,'H5_INDEX_NAME','H5_ITER_INC',0,@op_func,opdata_in);


H5G.close(group_id);


%should just have one troup Device_M153 or something...
devgroup=cell2mat(opdata_out(2));


device_name = devgroup(8:length(devgroup));

dev=strcat('/',devgroup);


%now list resonator groups in /Device_M153
group_id = H5G.open(file,dev);




opdata_in=cell(100,1);
opdata_in(1)=num2cell(2);
[status,idx_out,opdata_out]= H5L.iterate(group_id ,'H5_INDEX_NAME','H5_ITER_INC',0,@op_func,opdata_in);
H5G.close(group_id);


lenx=cell2mat(opdata_out(1));
lenx=lenx-1;
resgroups=opdata_out(2:lenx);

resnumbers=zeros(length(resgroups),1);

for k=1:length(resgroups)
    stx=cell2mat(resgroups(k));
    
    stxnum=str2num(stx(11:length(stx)));
    
    
    resnumbers(k)=stxnum;
end


numtraces=zeros(length(resgroups),1);
centfreqs=zeros(length(resgroups),1);

tracegroups=cell(length(resgroups),100);

%tracefields = cell(100,1);

is_resfields = 0;


%
% Now for each resonator group, get the num of traces and cent freq.
%
for k=1:length(resgroups)
    
    resname = cell2mat(resgroups(k));
    
    dir = strcat('/',devgroup,'/',resname);
    
    
    
    
    
    group_id = H5G.open(file,dir);
    
    
    %get dataset for cent freq
    dset_id = H5D.open(group_id,'Freq_Cent');
    centfreqs(k) = H5D.read(dset_id);

    dset_id.close();
    
    
    opdata_in=cell(100,1);
    opdata_in(1)=num2cell(2);
    [status,idx_out,opdata_out]= H5L.iterate(group_id ,'H5_INDEX_NAME','H5_ITER_INC',0,@op_func,opdata_in); 
    H5G.close(group_id);
    
    lenx=cell2mat(opdata_out(1));
    lenx=lenx-1;
    tracegroups(k,(1:lenx-1))= opdata_out(2:lenx);
    
    
    numtraces(k)=cell2mat(opdata_out(1))-2;
    
    %iteraete dataset names in the 1st res trace found, just to have one
    %lsting of fields...
    if numtraces(k)>0
        if is_resfields==0
            trname = cell2mat(tracegroups(k,1));
             
            dir2 = strcat('/',devgroup,'/',resname,'/',trname);
            group_id2 = H5G.open(file,dir2);
            opdata_in2=cell(100,1);
            opdata_in2(1)=num2cell(2);
            [status2,idx_out2,opdata_out2]= H5L.iterate(group_id2 ,'H5_INDEX_NAME','H5_ITER_INC',0,@op_funcds,opdata_in2); 
            H5G.close(group_id2);
            
            
            lenx=cell2mat(opdata_out2(1));
            lenx=lenx-1;
            tracefields(k,(1:lenx-1))= opdata_out2(2:lenx);
    
            
            
            
            is_resfields=1;
            
   
        end
        
    end
    
    
    
    
end    





%
% Close and release resources.
%
H5F.close (file);



end

%**************************************************************************
%
% Operator function.  Prints the name and type of the object
% being examined.
%
%**************************************************************************
function [status, opdata_out]=op_func (loc_id, name,opdata_in)

%
% Get type of the object and display its name and type.
% The name of the object is passed to this function by
% the Library.
%
statbuf=H5G.get_objinfo (loc_id, name, 0);

opdata_out=opdata_in;
switch (statbuf.type)
    case H5ML.get_constant_value('H5G_GROUP')
        %fprintf ('  Group: %s\n', name);
        
        index=cell2mat(opdata_in(1));
        
        opdata_out(index)={name};
        index=index+1;
        opdata_out(1)=num2cell(index);
        
    case H5ML.get_constant_value('H5G_DATASET')
        %fprintf ('  Dataset: %s\n', name);
        
    case H5ML.get_constant_value('H5G_TYPE')
        fprintf ('  Datatype: %s\n', name);
        
    otherwise
        fprintf ( '  Unknown: %s\n', name);
end

status=0;

end


%**************************************************************************
%
% Operator function.  Prints the name and type of the object
% being examined.
%
%**************************************************************************
function [status, opdata_out]=op_funcds (loc_id, name,opdata_in)

%
% Get type of the object and display its name and type.
% The name of the object is passed to this function by
% the Library.
%
statbuf=H5G.get_objinfo (loc_id, name, 0);

opdata_out=opdata_in;
switch (statbuf.type)
    case H5ML.get_constant_value('H5G_GROUP')
        %fprintf ('  Group: %s\n', name);
        
       
        
    case H5ML.get_constant_value('H5G_DATASET')
        %fprintf ('  Dataset: %s\n', name);
        index=cell2mat(opdata_in(1));
        
        opdata_out(index)={name};
        index=index+1;
        opdata_out(1)=num2cell(index);
    case H5ML.get_constant_value('H5G_TYPE')
        fprintf ('  Datatype: %s\n', name);
        
    otherwise
        fprintf ( '  Unknown: %s\n', name);
end

status=0;

end


