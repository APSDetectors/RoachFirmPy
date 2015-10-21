function [eventfifo_rd,outfifo_wr]=eventsaveFSM(save_event,delete_event,event_length,rst)




%
%named states
%

idle=0;

save_data=1;
delete_data=2;





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
  
  
else

switch state
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case idle
        eventfifo_rd=false;
  outfifo_wr=false;
  
  blk_count=event_length;
  
  
  
  if save_event==true 
      state=save_data;
  elseif delete_event == true
      state = delete_data;
  else
      state= idle;
  end
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case save_data
          eventfifo_rd=true;
  outfifo_wr=true;
  
  blk_count=blk_count-1;
  
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
   
  
  if blk_count==0
      state=idle;
  else
      state = delete_data;
  end
  
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



     otherwise
          eventfifo_rd=false;
  outfifo_wr=false;
          
 

end
end
