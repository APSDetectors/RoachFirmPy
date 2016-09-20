function [eventfifo_rd,fluxfifo_rd,outfifo_wr ,wr_select,event_done,clr_evt_rdy,stout]=fluxRampFSMOut(event_rdy,event_length,rst,clr_fifos,rawevt_fifo_empty,fluxrmp_fifo_empy,is_fluxrampdemod,is_savefluxraw)




%
%named states
%

idle=0;
clr_in_evt=1;
wait_flux_calc = 2;
header_fluxraw=3;
header_fluxraw2=4;
header_flux=5;
header_flux2=6;
header_flux3=7;
header_flux4=8;
header_raw=9;
writeraw=10;
deleteraw = 11;
finish_event=12;
clear_fifo = 13;
unused1=14;
unused2=15;



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
  state=idle;
  
  blk_count=0;
 
  eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  
  
else

switch state
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case idle
    
   
  
  eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
        
     %   event_rdy,event_length,rst,clr_fifos,rawevt_fifo_empty,fluxrmp_fifo_empy,is_fluxrampdemod
  
  blk_count = 0;
  
  if clr_fifos ==true 
      state=clear_fifo;
  elseif event_rdy == true
      state = clr_in_evt;
 
  else
      state= idle;
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case clr_in_evt
        
         eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=true;
        
  blk_count =event_length +2;
  
    %   event_rdy,event_length,rst,clr_fifos,rawevt_fifo_empty,fluxrmp_fifo_empy,is_fluxrampdemod,is_savefluxraw
  
   if is_fluxrampdemod==true
       state = wait_flux_calc;
       
       
       
   else
       
       state =  header_raw;
  
   end
   
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case wait_flux_calc
     
        eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  
    if  fluxrmp_fifo_empy==true
        state = wait_flux_calc;
        
    elseif is_savefluxraw ==true
          state =  header_fluxraw;
    else
          state = header_flux;
    end
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_fluxraw
        
        %write 0x5555, len of raw data+2word header+1 (flux ramp val)
        
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
        
  state = header_fluxraw2;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case header_fluxraw2
    
    %write flux ramp calc- one word
       eventfifo_rd=false;
  fluxfifo_rd=true;
  outfifo_wr =true;
  wr_select=3;
  event_done=false;
  clr_evt_rdy=false;
        
  state = writeraw;
    
    
    
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case header_flux
    
        
        %write 0x5555, 1 (flux ramp val)+aaa/can (2) 
        
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=2;
  event_done=false;
  clr_evt_rdy=false;
        
  state = header_flux2;
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_flux2
        
            %write flux ramp calc- one word
       eventfifo_rd=false;
  fluxfifo_rd=true;
  outfifo_wr =true;
  wr_select=3;
  event_done=false;
  clr_evt_rdy=false;
        
  state = header_flux3;
    
    
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_flux3
        
            %write flux ramp calc- one word
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=4;
  event_done=false;
  clr_evt_rdy=false;
        blk_count =blk_count-1;
  state = header_flux4;
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_flux4
        
            %write flux ramp calc- one word
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=4;
  event_done=false;
  clr_evt_rdy=false;
        blk_count =blk_count-1;
  state = deleteraw;
  
    
        
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case header_raw
           %write 0x5555, len of raw data+2word header
        
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=1;
  event_done=false;
  clr_evt_rdy=false;
        
  state = writeraw;
  
    
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case writeraw
    
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=4;
  event_done=false;
  clr_evt_rdy=false;
        
  blk_count =blk_count-1;
 
  if blk_count==0
  state = finish_event;
  
  else
      state = writeraw;
  end
  
  
      
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case deleteraw
    
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=4;
  event_done=false;
  clr_evt_rdy=false;
        
  blk_count =blk_count-1;
 
  if blk_count==0
  state = finish_event;
  
  else
      state = deleteraw;
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case finish_event
  
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=true;
  clr_evt_rdy=false;
  
       state = idle; 
  
 
  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 

    case clear_fifo
        %event_rdy,event_length,rst,clr_fifos,rawevt_fifo_empty,fluxrmp_fifo_empy,is_fluxrampdemod,is_savefluxraw)

   eventfifo_rd=true;
  fluxfifo_rd=true;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=true;
  
     if event_rdy==true
         state = clear_fifo;
     elseif rawevt_fifo_empty==false
        state = clear_fifo ;
         
     elseif fluxrmp_fifo_empy==false
       state = clear_fifo;
     else
         state = idle;
     end
     

  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%unused1
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case unused1
   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;

  state = idle;
  
  

    case unused2

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;

  state = idle;
  
  

     otherwise
   
   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;

  state = idle;
  
  
  
  
end
end
