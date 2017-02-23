function [datain_muxsw, eventfifo_rd,outfifo_wr ,event_done,clr_evt_rdy,stout]=combinefftdataFSM(event_rdy,event_length,rst,clr_fifos,fifo_empty)




%
%named states
%

idle=0;
clr_in_evt=1;
read_fifo_data1=2;
read_fifo_data2=3;
read_fifo_data3=4;
read_fifo_data4=5;


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
 event_done=false;
 clr_evt_rdy=false;
 datain_muxsw=false;
 state = idle;
 
  
else

switch state
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case idle
   
 eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
  datain_muxsw=false;

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
 event_done=false;
 clr_evt_rdy=true;
 
 datain_muxsw=false;

    
    
    
    %header is 2, so we have evt len + headlen 
    blk_count = event_length;
    
 
    state = read_fifo_data1;
   
    
        

    
  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % read aaaa and 1/2 of timestamp
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data1
        
        
  eventfifo_rd=true;
 outfifo_wr =true;
 event_done=false;
 clr_evt_rdy=false;
  datain_muxsw=false;

 
  
 
   % blk_count = blk_count - 1;
    
  state = read_fifo_data2;
  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % read chan, is puilse, and 1/s of timestamp
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data2
        
            
  eventfifo_rd=true;
 outfifo_wr =true;
 
 event_done=false;
 clr_evt_rdy=false;
  datain_muxsw=false;

          
  
  % blk_count = blk_count - 1;
    
  state = read_fifo_data3;
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % read and wrie z-128 coeff, the earlier tin time fft data
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data3
        
   blk_count = blk_count - 1;
            
  eventfifo_rd=false;
 outfifo_wr =true;
 
 event_done=false;
 clr_evt_rdy=false;
  datain_muxsw=false;

          
  
  
     
    
  
       state =read_fifo_data4;
      
    
    
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % write z coef, the later in time fft dqata
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case read_fifo_data4
        
             
            
  eventfifo_rd=true;
 outfifo_wr =true;
 event_done=false;
 clr_evt_rdy=false;
  datain_muxsw=true;

          
  
  
    
    
    if blk_count==0
       state = finish_event;      
    else
       state =read_fifo_data3;          
    end    
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  
    case finish_event
        
             
            
  eventfifo_rd=false;
 outfifo_wr =false;
 event_done=true;
 clr_evt_rdy=false;
  datain_muxsw=false;

            
  
  
    
   
       state =idle;
      
   
  
  
  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  

    case clear_fifo
   
           
  eventfifo_rd=true;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=true;
   datain_muxsw=false;

   
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
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;

  
 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un2
             
 
 
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;

 state = idle;

 
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un3
             
 
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;

 
   
 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un4
             
 
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;

 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un5
             
  
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;

 
 state = idle;

 
   
    
      
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un6
     
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;
        
 
 state = idle;

 
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un7
             
 
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;

 

 state = idle;

  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case un8
             
 
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;

 

 state = idle;

 
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    otherwise
               
 
 
    eventfifo_rd=false;
 outfifo_wr =false;
 event_done=false;
 clr_evt_rdy=false;
   datain_muxsw=false;


 state = idle;
 

end
end
