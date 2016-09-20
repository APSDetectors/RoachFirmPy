function [eventfifo_rd,outfifo_wr,write_sel]=eventsaveFSM(save_event,delete_event,event_length,rst,clr_fifos)




%
%named states
%

idle=0;
write_header = 1;
save_data=2;
delete_data=3;
clear_fifo = 4;




%
% Registers
%

persistent state, state = xl_state(idle,{xlUnsigned, 4, 0});





% Counter to keep track of block size read from channel fifo
% block size uop to 256. 
persistent blk_count, blk_count = xl_state(0,{xlUnsigned, 8, 0});

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if rst==true
  state=idle;
  eventfifo_rd=false;
  outfifo_wr=false;
  blk_count=0;
  write_sel=false;
  
else

switch state
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case idle
        eventfifo_rd=false;
  outfifo_wr=false;
  write_sel=false;
  blk_count=event_length;
  
  
  
  if save_event==true 
      state=write_header;
  elseif delete_event == true
      state = delete_data;
  elseif clr_fifos==true
      state = clear_fifo;
  else
      state= idle;
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case write_header
        eventfifo_rd=false;
        outfifo_wr=true;
        write_sel=false;
        state = save_data;
        
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case save_data
          eventfifo_rd=true;
  
  write_sel=true;
  blk_count=blk_count-1;
  outfifo_wr=true;
  if blk_count==0
      state=idle;
     
  else
      state = save_data;
     
  end
  
  
  
  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  

    case delete_data
          eventfifo_rd=true;
  outfifo_wr=false;
   blk_count=blk_count-1;
   write_sel=false;
  
  if blk_count==0
      state=idle;
  else
      state = delete_data;
  end
  
  
  
  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  

    case clear_fifo
          eventfifo_rd=true;
  outfifo_wr=false;
   
   write_sel=false;
  
  if clr_fifos==true
      state=clear_fifo;
  else
      state = idle;
  end
  
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



     otherwise
          eventfifo_rd=false;
  outfifo_wr=false;
          write_sel=false;
 

end
end
