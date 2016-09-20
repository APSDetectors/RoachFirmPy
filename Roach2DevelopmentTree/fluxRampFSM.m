function [eventfifo_rd,outfifo_wr ,demod_wr,event_done,clr_evt_rdy,stout,chanwr]=fluxRampFSM(event_rdy,event_length,rst,clr_fifos,fifo_empty,is_fluxrampdemod)




%
%named states
%

idle=0;
clr_in_evt=1;
read_fifo_data=2;
read_fifo_data_flux=3;
read_fifo_data_flux2=4;
read_fifo_data_flux3=5;


finish_event=6;

clear_fifo = 7;

un1 = 8;
un2 =9;
un3 =10;
un4=11;
un5=12;
un6=13;
un7=14;
un8=15;




%
% Registers
%

persistent state, state = xl_state(idle,{xlUnsigned, 4, 0});





% Counter to keep track of block size read from channel fifo
% block size uop to 256. 
persistent blk_count, blk_count = xl_state(0,{xlUnsigned, 8, 0});


stout = state;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if rst==true
 eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
 chanwr = false;
 
 state = idle;
 
  
else

switch state
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case idle
   
 eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
 chanwr = false;
 
    if clr_fifos==true
    state = clear_fifo;
    elseif event_rdy==true
       state = clr_in_evt;
    else
        state = idle;
    end
    
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case clr_in_evt 
  
    
    eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=true;
  chanwr = false;
 

    
    
    
    %header is 2, so we have evt len + headlen 
    blk_count = event_length+2;
    
    if is_fluxrampdemod==true
        state = read_fifo_data_flux;
    else
        state = read_fifo_data;
    end
    
        
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data
          
    eventfifo_rd=true;
 outfifo_wr =true;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
  chanwr = false;
 

     
  
  blk_count = blk_count - 1;
    
    if blk_count==0
       state = finish_event; 
    else
       state =read_fifo_data;
      
    end
    
  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data_flux
        
        
  eventfifo_rd=true;
 outfifo_wr =true;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
        chanwr = false;
 
 
  
 
    blk_count = blk_count - 1;
    
  state = read_fifo_data_flux2;
  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data_flux2
        
            
  eventfifo_rd=true;
 outfifo_wr =true;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
 chanwr = true;
 
          
  
   blk_count = blk_count - 1;
    
  state = read_fifo_data_flux3;
    
    
       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data_flux3
        
             
            
  eventfifo_rd=true;
 outfifo_wr =true;
 demod_wr=true;
 event_done=false;
 clr_evt_rdy=false;
 chanwr = false;
 
          
  
  
     blk_count = blk_count - 1;
    
    if blk_count==0
       state = finish_event; 
    else
       state =read_fifo_data_flux3;
      
    end
    
    
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  
    case finish_event
        
             
            
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=true;
 clr_evt_rdy=false;
 chanwr = false;
 
            
  
  
    
   
       state =idle;
      
   
  
  
  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  

    case clear_fifo
   
           
  eventfifo_rd=true;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=true;
 chanwr = false;
 
   
    if fifo_empty==false
        
      state=clear_fifo;
    elseif event_rdy
         state=clear_fifo;
    else
      state = idle;
    end
  
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un1
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
  chanwr = false;
 
  
 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un2
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
 chanwr = false;
 
   
 state = idle;

 
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un3
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
 chanwr = false;
 
   
 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un4
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
   chanwr = false;
 
 
 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un5
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
   chanwr = false;
 
 
 state = idle;

 
   
    
      
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un6
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
    chanwr = false;
 

 state = idle;

 
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un7
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
    chanwr = false;
 

 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un8
             
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
    chanwr = false;
 

 state = idle;

 
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    otherwise
               
  eventfifo_rd=false;
 outfifo_wr =false;
 demod_wr=false;
 event_done=false;
 clr_evt_rdy=false;
    chanwr = false;
 

 state = idle;
 

end
end
