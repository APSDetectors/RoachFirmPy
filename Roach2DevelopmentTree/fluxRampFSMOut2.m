function [eventfifo_rd,fluxfifo_rd,outfifo_wr ,wr_select,event_done,clr_evt_rdy,stout,cirtranfiford]=fluxRampFSMOut2(event_rdy,event_length,rst,clr_fifos,rawevt_fifo_empty,fluxrmp_fifo_empy,is_fluxrampdemod,is_savefluxraw,is_save_fluxtran,cirtranfifoempty)




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
writetran=14;
header_fluxtran=15;
header_fluxtran2=16;

unused0 =  17;
unused1 =  18;
unused2 =  19;
unused3 =  20;

unused4 =  21;
unused5 =  22;
unused6 =  23;
unused7 =  24;
unused8 =  25;
unused9 =  26;
unused10 =  27;
unused11 =  28;
unused12 =  29;
unused13 =  30;
unused14 =  31;





%
% Registers
%

persistent state, state = xl_state(idle,{xlUnsigned, 5, 0});





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
  cirtranfiford=false;
  
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
  cirtranfiford=false;
        
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
  cirtranfiford=false;
        
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
  cirtranfiford=false;
  
    if  fluxrmp_fifo_empy==true
        state = wait_flux_calc;
        
    elseif is_savefluxraw ==true
          state =  header_fluxraw;
          
    elseif is_save_fluxtran ==true
        state = header_fluxtran;
    else
          state = header_flux;
    end
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_fluxraw
        
        %write 0x5555, len of raw data+2word header+1 (flux ramp val)
        %header for flux ramp and raw data
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
   cirtranfiford=false;
       
  state = header_fluxraw2;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case header_fluxraw2
    
    %write flux ramp calc- one word
    %flux ramp calc data written here
       eventfifo_rd=false;
  fluxfifo_rd=true;
  outfifo_wr =true;
  wr_select=3;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;
        
  %goto writtin g raw data, including the aaaa and chan
  state = writeraw;
    
    
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_fluxtran
        
        %write 0x5555, len of raw data+2word header+1 (flux ramp val)
        
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=5;
  event_done=false;
  clr_evt_rdy=false;
   cirtranfiford=false;
       
  state = header_fluxtran2;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case header_fluxtran2
    
    %write flux ramp calc- one word
       eventfifo_rd=false;
  fluxfifo_rd=true;
  outfifo_wr =true;
  wr_select=3;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;
        %goto writing the aaaa data and chan
  state = header_flux3;
    
    
    
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case header_flux
    
        
        %write 0x5555, 1 (flux ramp val)+aaa/can (2) 
        %head for only flux data
        
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=2;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;
        
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
  cirtranfiford=false;
        
  state = header_flux3;
    
    
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_flux3
        
            %write aaaa
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=4;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;
  
        blk_count =blk_count-1;
  state = header_flux4;
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case header_flux4
        
            %write chan
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=4;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;
  
        blk_count =blk_count-1;
        
        %if we only want flux ramp data, then delete reaw of raw data
        %if we want flux and trans, then add on the translated data
  if is_save_fluxtran == true
      state = writetran;
  else
      state = deleteraw;
  end
    
        
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case header_raw
           %write 0x5555, len of raw data+2word header
            %header for onluy raw data
      eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=1;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;
        
  state = writeraw;
  
    
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case writeraw
    
    %read raw data fifo. may or may not have the aaaa there.
    % in flux-raw mode, the aaaas are already read out.
    %in raw only m ode, we read aaas out here. the blk_count determines it
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=4;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;
        
  blk_count =blk_count-1;
 
  if blk_count==0
  state = finish_event;
  
  else
      state = writeraw;
  end
  
  
  
      
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
case writetran
    
   %write translated data
   %read trans data fifo, and raw data fifo
   %raw data fifo data is cleared out and discarded
       eventfifo_rd=true;
  fluxfifo_rd=false;
  outfifo_wr =true;
  wr_select=6;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=true;
        
  blk_count =blk_count-1;
 
  if blk_count==0
  state = finish_event;
  
  else
      state = writetran;
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
  cirtranfiford=false;

  
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
    cirtranfiford=false;

    
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
  cirtranfiford=true;

  
     if event_rdy==true
         state = clear_fifo;
     elseif rawevt_fifo_empty==false
        state = clear_fifo ;
         
     elseif fluxrmp_fifo_empy==false
       state = clear_fifo;
       
     elseif cirtranfifoempty ==false
       state = clear_fifo;
       
       
     else
         state = idle;
     end
     

  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%unused1
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case unused0
   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  

    case unused1

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  


    case unused2

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
  
  
    case unused3

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
  
    case unused4

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
    case unused5

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
  
  
    case unused6

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
    case unused7

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
    case unused8

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
    case unused9

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
    case unused10

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
    case unused11

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
    case unused12

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
    case unused13

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
    case unused14

   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
  
  
  
  
     otherwise
   
   eventfifo_rd=false;
  fluxfifo_rd=false;
  outfifo_wr =false;
  wr_select=0;
  event_done=false;
  clr_evt_rdy=false;
  cirtranfiford=false;

  
  state = idle;
  
  
  
  
end
end
