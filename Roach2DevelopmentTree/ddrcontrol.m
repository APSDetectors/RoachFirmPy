
function [bramaddressout, dramaddressout, dramrst, dramrwn, dramcmdvld,dramrdack,dramoutmuxsel, stateout,syncout] =ddrcontrolb(...
    syncin,startdac,startwrite,fsmreset, rdtoggle,wrtoggle,  lutsize, offsetaddress,bramwritesize)

%
%
%
%
%
%


%
% Named states
%

idle = 0;

rdmode0 = 1;
rdmode1 = 2;
rdmode2 = 3;
rdmode3 = 4; 
wrmode0 = 5;
wrmode1 = 6;
wrmode2 = 7;
wrmode3 = 8;
wrmode4 = 9;
sync0 = 10;

unused0=11;
unused1=12;
unused2=13;
unused3=14;
unused4=15;


%
% persistent registers
%
persistent state, state = xl_state(idle,{xlUnsigned, 4, 0});


persistent dramaddress, dramaddress = xl_state(0,{xlUnsigned, 32, 0});

persistent bramaddress, bramaddress = xl_state(0,{xlUnsigned, 7, 0});

persistent togglecounter, togglecounter = xl_state(0,{xlUnsigned, 4, 0});




%
% get bits crom control register
%





%
%
%

stateout = state;
bramaddressout = bramaddress;
dramaddressout = dramaddress;
 
      
dramrst = false;
  dramrwn = true;
  dramcmdvld = false;
  dramrdack = false;
  dramoutmuxsel = false;
  syncout = false;
%
%
%



        

if fsmreset==true
  state=idle;    

  dramaddress = 0;
  bramaddress=0;
  togglecounter=0;
  
  dramrst = false;
  dramrwn = true;
  dramcmdvld = false;
  dramrdack = false;
  dramoutmuxsel = false;
  syncout = false;
  
else

switch state
 
     
        
%wait for trigger to start reading the fifos, dumpFifo <=1
%rst addr and blk cnt
 
  case idle
        
       
        
 
      dramrst = false;
      dramrwn = true;
      dramcmdvld = false;
      dramrdack = true;
      dramoutmuxsel = false;
      syncout = true;
      
      if startwrite == true
          state = wrmode0;
      elseif startdac == true
          state = rdmode0;
      elseif syncin ==true
          state = sync0;
      else
          state = idle;
      end

    
    case sync0
        
          dramaddress = 0;
          bramaddress=0;
          togglecounter=0;

          dramrst = false;
          dramrwn = true;
          dramcmdvld = false;
          dramrdack = false;
          dramoutmuxsel = false;
          syncout = false;
          
          state = idle;
          

          %
          % dram readout states
          %
      
    %1st part of read cycle that repeats over and over. 2 clkcs or more for a command     
    case rdmode0
        
        
      dramrst = false;
      %set cmd to read
      dramrwn = true;
      %cmdval 1;
      dramcmdvld = true;
      dramrdack = true;
      dramoutmuxsel = false;
      syncout = false;
      
     togglecounter=rdtoggle;
   
     if dramaddress <lutsize
        state = rdmode1;
     else
         state = rdmode2;
     end
     
    %2nd part of read command cuycle, where we inc the dram address
    case rdmode1
        
               
      dramrst = false;
      %set cmd to read
      dramrwn = true;
      %cmdval lo;
      dramcmdvld = false;
      dramrdack = true;
      dramoutmuxsel = true;
      syncout = false;
      
      dramaddress = dramaddress + 8;
      
     %toggle counter will add a wait between the commands
     if  togglecounter>0
     
      state = rdmode3;
     elseif startdac ==true
         state = rdmode0;
     else
         state = idle;
     end    
         
      
    
    
      
      %2nd part of read command cuycle, where we rst dramaddr
    case rdmode2
        
               
      dramrst = false;
      %set cmd to read
      dramrwn = true;
      %cmdval lo;
      dramcmdvld = false;
      dramrdack = true;
      dramoutmuxsel = true;
     syncout = true;
      
      dramaddress = 0;
      
     
      %toggle counter will add a wait between the commands
     if  togglecounter>0
     
      state = rdmode3;
     elseif startdac ==true
         state = rdmode0;
     else
         state = idle;
     end   
        
      
  
    case rdmode3
        
      dramrst = false;
      %set cmd to read
      dramrwn = true;
      %cmdval lo;
      dramcmdvld = false;
      dramrdack = false;
      dramoutmuxsel = false;
     syncout = false;
     
      togglecounter = togglecounter-1;
      
      if togglecounter==0
          state = rdmode0;
      else
          state = rdmode3;
          
      end
      
       
	  
	  
     %
   % writing dram states
   %
   
   %rst bram address 0, load dram offs address
   
     
    case wrmode0
        
      dramrst = false;
      %set cmd to write
      dramrwn = false;
      %cmdval lo;
      dramcmdvld = false;
      dramrdack = false;
      dramoutmuxsel = false;
     syncout = false;
     
     
     dramaddress = offsetaddress;
     bramaddress = 0;
     
      state = wrmode1;
         
      
    %1st part of wr dram command  that loops
    %
    case wrmode1
        
      dramrst = false;
      %set cmd to write
      dramrwn = false;
      %cmdval hi;
      dramcmdvld = true;
      dramrdack = false;
      dramoutmuxsel = false;
     syncout = false;
     
     
    
     togglecounter=wrtoggle;
     
     
     
     if bramaddress <bramwritesize
      state = wrmode2;
        %we inc the bram address in middle of the cucle becayse the
        %data out has a one clk delay. we are inc the address 1 clk early
       bramaddress = bramaddress + 1;
     else 
         state = wrmode3;
         
     end
     
        %2st part of wr dram command, when we inc addresses
    case wrmode2
        
      dramrst = false;
      %set cmd to write
      dramrwn = false;
      %cmdval hi;
      dramcmdvld = true;
      dramrdack = false;
      dramoutmuxsel = false;
     syncout = false;
     
     
      
    %bramaddress = bramaddress + 1;
    dramaddress = dramaddress + 8;
    
   if togglecounter==0
      state = wrmode1;
   else
       state =wrmode4;
   end
   
    
   %2nd part of wr command, when we are done inc addresses
    case wrmode3
        
      dramrst = false;
      %set cmd to write
      dramrwn = false;
      %cmdval hi;
      dramcmdvld = true;
      dramrdack = false;
      dramoutmuxsel = false;
     syncout = false;
     
     
      
   
      %inc dramaddress to make sure we do nto write to it twice in idle
      %mode
      dramaddress = dramaddress + 8;
    %goto uidle after last address is written
  
      state = idle;
 
   
      %this is wait state between wr commands
    case wrmode4 
        
      dramrst = false;
      %set cmd to write
      dramrwn = false;
      %cmdval hi;
      dramcmdvld = false;
      dramrdack = false;
      dramoutmuxsel = false;
     syncout = false;
     
     
      togglecounter = togglecounter -1;
      if togglecounter == 0
          state = wrmode1;
      else
          state = wrmode4;         
      end
      
      
      
      
      
      
      
      
   
     
end


end
