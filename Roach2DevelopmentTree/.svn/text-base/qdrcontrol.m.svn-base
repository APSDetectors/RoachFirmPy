
function [dramaddressout, sramrd ,stateout,syncout,bramaddressout,sramwr] =...
    qdrcontrol(startdac,fsmreset, rdtoggle,lutsize,wrtoggle,startwrite,writelen,offsetaddress)

%
%
%sramrd, 
%


%
% Named states
%

idle = 0;

rdmode0 = 1;
rdmode1 = 2;
wrmode0=3;
wrmode1 = 4;
wrmode2 = 5;


%
% persistent registers
%
persistent state, state = xl_state(idle,{xlUnsigned, 3, 0});


persistent dramaddress, dramaddress = xl_state(0,{xlUnsigned, 32, 0});


persistent togglecounter, togglecounter = xl_state(0,{xlUnsigned, 4, 0});

persistent bramaddress, bramaddress = xl_state(0,{xlUnsigned, 9, 0});





%
% get bits crom control register
%





%
%
%

stateout = state;

dramaddressout = dramaddress;
bramaddressout = bramaddress;

sramrd =false;
syncout = false;
sramwr=false;
      
 
 
%
%
%



        

if fsmreset==true
  state=idle;    

  dramaddress = 0;
  togglecounter=0;
  sramwr=false;
  sramrd =false;
  syncout = false;
  
else

switch state
 
     
        
%wait for trigger to start reading the fifos, dumpFifo <=1
%rst addr and blk cnt
 
  case idle
        
       
       bramaddress = 0;
       dramaddress = 0;
 
      sramrd = false;
      syncout = true;
      sramwr = false;
      
      if startdac == true
          state = rdmode0;
   
      elseif startwrite==true
         state = wrmode0;
         
      else
          state = idle;

      end

          %
          % dram readout states
          %
      
    %1st part of read cycle that repeats over and over. 2 clkcs or more for a command     
    case rdmode0
        
        
      %set cmd to read
      sramrd = true;
      %cmdval 1;
      sramwr = false;
      
     togglecounter=rdtoggle;
   
     if dramaddress <lutsize
       
	dramaddress = dramaddress + 1;
	syncout = false;
     else
	dramaddress = 0;
	syncout = true;
         
     end

     if togglecounter~=0
        state = rdmode1;
     elseif startdac==true
       state = rdmode0;
     else
       state = idle;
     end
        
     
    %2nd part of read command cuycle, where we inc the dram address
    case rdmode1
        
               
      %set cmd to read
      sramrd = false;
      %cmdval lo;
      syncout = false;
          sramwr = false;
  
      
      
     %toggle counter will add a wait between the commands
     if  togglecounter>0
     	togglecounter=togglecounter-1;
        
     end
     if  togglecounter>1
         state = rdmode1;
      
     else
         state = rdmode0;
    
     end    
         
     
      
      
      

          %
          % dram write states
          %
      
    %setup for write block      
    case wrmode0
        
        
      %set cmd to read
      sramrd = false;
      %cmdval 1;
       sramwr = true;
     syncout = false;
      
     togglecounter=wrtoggle;
   
    dramaddress = offsetaddress;
    bramaddress = 0;
     
     
        state = wrmode1;
       
        
        
        
        
     %   
     %wruite data from bram to sram
     %
    case wrmode1
        
     sramwr = true;
     sramrd = false;
     syncout = false;
     
     dramaddress = dramaddress + 1;
     bramaddress = bramaddress+1;
     
     if bramaddress~=writelen
         state = wrmode1;
     elseif togglecounter~=0
         state = wrmode2;
         
     else
         state = idle;
     end
        
     
     
     %
     %wait between writes
     %
    case wrmode2
        
             
     sramwr = false;
     sramrd = false;
     syncout = false;
     
    
     
     togglecounter= togglecounter-1;
     if togglecounter==0
         state = wrmode1;
     else
         state = wrmode2;
     end
       
  
end


end
