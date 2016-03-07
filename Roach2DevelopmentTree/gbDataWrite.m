function [fifo_rd_a, fifo_rd_b, mux_a, mux_b, tx_vld, tx_eof,stateout]=gbDataWrite(almost_empty_a, almost_empty_b,rst,clr_fifos)




%
%named states
%

idle=0;

%write zzz's to the gb frame to denote start of data
start_gb_frame=1;

%write frame number as uint32's
write_packet_number = 2;

%write just fifo a, write yyyy's for fifo b
write_fifo_a=3;

%write just fifo b, wrhite yyy's in place of fifo a
write_fifo_b = 4;

%write data from both fifos
write_fifo_ab = 5;

%write xxxx's for end of frame
write_end_frame=6;


%write xxxx's for end of frame
write_end_frame_b=7;

%do nothing, but wait for interframe time
gb_wait = 8;


clear_fifos=9;
nop10=10;
nop11=11;
nop12=12;
nop13=13;
nop14=14;
nop15=15;


%
% Registers
%

persistent state, state = xl_state(idle,{xlUnsigned, 4, 0});





% counter that keeps track of num words to gb ente
persistent word_count, word_count  = xl_state(0,{xlUnsigned, 12, 0});




% counter that keeps track of num words to gb ente
persistent wait_count, wait_count  = xl_state(0,{xlUnsigned, 32, 0});



stateout = state;


%n_almost_empty_a = not(almost_empty_a);
%n_almost_empty_b = not(almost_empty_b);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if rst==true
  state=idle;
  
  fifo_rd_a=false;
  fifo_rd_b=false;
  mux_a=0; 
  mux_b=0;
  tx_vld=false;
  tx_eof=false;
  
else

switch state
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case idle
    
    word_count=0;
    wait_count=0;
    
    fifo_rd_a=false;
  fifo_rd_b=false;
  mux_a=0; 
  mux_b=0;
  tx_vld=false;
  tx_eof=false;
  
 % almost_empty_a, almost_empty_b
  if  almost_empty_a || almost_empty_b
      state = start_gb_frame;
  
  elseif clr_fifos
      state = clear_fifos
  else
      state= idle;
  end
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%write zzzzz's
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
    case start_gb_frame
        
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write zzzz s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=true;
  tx_eof=false;
        
 state=write_packet_number;
  
  
  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%wrate packet counter
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case write_packet_number
        
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write zzzz s
  mux_a=1; 
  mux_b=1;
  
  tx_vld=true;
  tx_eof=false;
        
  if almost_empty_a && almost_empty_b
      state = write_fifo_ab;

  elseif almost_empty_a
      state=write_fifo_a;
      
    elseif almost_empty_b
      state=write_fifo_b;    
  else
      state = write_end_frame;
  end
  


 
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  
        
    case write_fifo_ab
        
       
     
   fifo_rd_a=true;
  fifo_rd_b=true;
  %write data s
  mux_a=2; 
  mux_b=2;
  
  tx_vld=true;
  tx_eof=false; 
         
   word_count = word_count + 1;
  
  if word_count ==180
      state=write_end_frame;
  else
      state = write_fifo_ab;
  end

  
  
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  
        
    case write_fifo_a
        
       
     
   fifo_rd_a=true;
  fifo_rd_b=false;
  %write data s
  mux_a=2; 
  mux_b=3;
  
  tx_vld=true;
  tx_eof=false; 
         
   word_count = word_count + 1;
  
  if word_count ==180
      state=write_end_frame;
  else
      state = write_fifo_a;
  end
  
  
  
  
    
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  
        
    case write_fifo_b
        
       
     
   fifo_rd_a=false;
  fifo_rd_b=true;
  %write data s
  mux_a=3; 
  mux_b=2;
  
  tx_vld=true;
  tx_eof=false; 
         
   word_count = word_count + 1;
  
  if word_count ==180
      state=write_end_frame;
  else
      state = write_fifo_b;
  end
  
  
  

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  
        
    case write_end_frame
        
       
     
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=true;
  tx_eof=false; 
         
   word_count = 0;
  
  
      state=write_end_frame_b;
  
    
  
  
  
  

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
  
        
    case write_end_frame_b
        
       
     
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=true;
  tx_eof=true; 
         
   word_count = 0;
  
  
      state=gb_wait;
  
    
  
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  
  
        
    case gb_wait
        
       
     
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
   wait_count = wait_count + 1;
  
  if wait_count < 8
      state=gb_wait;
  else
      state = idle;
  end
  
  
  
 %%%%%%%%%%%%%%%%%%%%%%%%%
 %
 %%%%%%%%%%%%%%%%%%%%%%%%%
  
      case clear_fifos 
    
 
    
    fifo_rd_a=true;
  fifo_rd_b=true;
  mux_a=0; 
  mux_b=0;
  tx_vld=false;
  tx_eof=false;
  

 
  
  if clr_fifos
      state = clear_fifos
  else
      state= idle;
  end
  
  
  
  
 
 %%%%%%%%%%%%%%%%%%%%%%%%%
 %
 %%%%%%%%%%%%%%%%%%%%%%%%%
    
    case nop10
         
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
  state = idle;
 
 %%%%%%%%%%%%%%%%%%%%%%%%%
 %
 %%%%%%%%%%%%%%%%%%%%%%%%%
  
    case nop11
         
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
  state = idle;
  
 %%%%%%%%%%%%%%%%%%%%%%%%%
 %
 %%%%%%%%%%%%%%%%%%%%%%%%%
 
    case nop12
         
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
  state = idle;
  
 %%%%%%%%%%%%%%%%%%%%%%%%%
 %
 %%%%%%%%%%%%%%%%%%%%%%%%%
 
    case nop13
         
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
  state = idle;
  
 %%%%%%%%%%%%%%%%%%%%%%%%%
 %
 %%%%%%%%%%%%%%%%%%%%%%%%%
 
    case nop14
         
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
  state = idle;
  
 %%%%%%%%%%%%%%%%%%%%%%%%%
 %
 %%%%%%%%%%%%%%%%%%%%%%%%%
 
    case nop15
        
  
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
  state = idle;
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

     otherwise
  
   fifo_rd_a=false;
  fifo_rd_b=false;
  %write data s
  mux_a=0; 
  mux_b=0;
  
  tx_vld=false;
  tx_eof=false; 
         
  state = idle;
 
 

end
end
