function [fifo_rden, wr_coef_big_fifo,  write_data_sel, cur_chanout,fifo_overrun_cnt_out,stateout,clear_pulse]=fifoFSM(dumpFifo,fifo_empty,half_full, quart_full, almost_full,rst,proc_busy,is_pulse,data_valid,last_channel,wr_raw_data)

% 
% staet machine for reading out fifos
% 0 idle, rst addr 0, next=0 unless trigger readfifos(1)
% 1      blkcntrst=1
%  if fifo empty=1,  goto 6
% if fifo nempty,  goto 2
% 
% 6 inc ram addr=1
% ram_addr_rst=channel_G_M
% goto 5
% 
% 5 if stateFiveDelay=1, goto 1
% 
% 2 wr AAAAAAAA to out ram goto3
% fifoRd=0, outWr=1
% 3 write ramdata to  out ram, goto 4
% fifoRd=0, outWr=1
% 4 if blockcnt>N goto6, else goto 4
%  if !fifo_empty blockcntinc = 1, else 0
% if !fifo_emoty fifoRd=1, else 0
% if !fifo_empty outWr=1. else 0
%
%outputs
%outputs
%addr rst
%blockcnt rst
%inc addr
%inc blockcnt
%writeWhat (aaa,fifo,addr)
%wr en

%
%inputs
%
%inputs, 
%mem addr- address if fifo lookupram
%blockcnt, size of data to read from one fifo
%trigger fifo read signal
%fifo empty
%channel>?
%blockcnt>?




%
%named states
%

idle=0;
ckeck_halffull=1;

inc_ram_addr=2;
wait_emptyflag=3;

aaaa=4;
wr_addr=5;


read_chan_fifo=6;
start_chan_fifo=7;
done_fifo_rd=8;

out_of_data=9;
wait_for_data = 10;


look_for_pulse=11;



read_chan_fifo_raw=12;

done_fifo_rd_raw=13;

aaaa_raw=14;
wr_addr_raw=15;

%fifo_length=64;

%max block we read from the channel fifo when fifos have no puilses
%if we have puilses, then we can read more...
max_block_size=48;
mid_block_size=32;
sm_block_size = 16;


%
% Registers
%

persistent state, state = xl_state(idle,{xlUnsigned, 4, 0});


% current fifl or channel we are reading out. must be power of two num
% channels. currently 256. wa have a max channel input, if we want to read
%chan 0 to 3 for example. we set max ahennto to 3. for 16 chans,
%we set max chan to 15
persistent cur_channel, cur_channel = xl_state(0,{xlUnsigned, 8, 0});





% Counter to keep track of block size read from channel fifo
% block size uop to 256. 
persistent blk_count, blk_count = xl_state(0,{xlUnsigned, 8, 0});

% counter that kccoe s track of how many times we overrun chan fifo 
% by reading too much
persistent fifo_overrun_cnt, fifo_overrun_cnt = xl_state(0,{xlUnsigned, 32, 0});


%counter that allows rereading of same channel when it runs out of data
%during a pulse, it will limit how long pulse can be, and allows reading of
%other channels of puse on channel is too long. here we set ot 1, so we can
%ouly read one extra block of dqata for long pulses. before checking other
%channels
persistent fifo_reread_cnt, fifo_reread_cnt= xl_state(0,{xlUnsigned, 8, 0});


cur_chanout=cur_channel;
fifo_overrun_cnt_out = fifo_overrun_cnt;

stateout = state;

%
% Reset state
%


if rst==true
  state=idle;

  
  blk_count=0;
  fifo_reread_cnt=0;
  
  clear_pulse=true;
  
  fifo_rden=false;
  wr_coef_big_fifo=false;
  
  write_data_sel=0;

   cur_channel =0;
  
  
else

%
%  run staet machine, switch statements
%
    
switch state
 
     
        
%wait for trigger to start reading the fifos, dumpFifo <=1
%rst addr and blk cnt
    case idle
        
   cur_channel = 0;

   clear_pulse=true;
  
  fifo_rden=false;
  wr_coef_big_fifo=false;
    write_data_sel=0;

        
        if dumpFifo==true
            state=ckeck_halffull;
        else
            state=idle;
        end
	
	
	
	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
%see if fifo has data in it. look for 1/2 full fifo
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case ckeck_halffull
      
 
     if almost_full==true 
	     blk_count = max_block_size;
     else
         blk_count = mid_block_size;
     end
     
fifo_reread_cnt=1;

 clear_pulse=true;

  
  fifo_rden=false;
  wr_coef_big_fifo=false;
  
  write_data_sel=0;
	
    
        if dumpFifo==true
            
          if half_full==false
            state=inc_ram_addr;
          else
            %if data in fifo, read a block
           
            %for just writing coef, and not pulse detecting
            if wr_raw_data
                state=aaaa_raw;
            else
                state = start_chan_fifo;
            end
            
          end
        else
            state=idle;
        end
	
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
%  we imr the channel, or fifo number, we are looking at
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case inc_ram_addr
      
        
    if    cur_channel<last_channel  
        
        cur_channel = cur_channel + 1;
    else
        cur_channel=0;
    end
    
 
 clear_pulse=false;
 
 
  fifo_rden=false;
  wr_coef_big_fifo=false;
 
	  write_data_sel=0;

  state = wait_emptyflag;
        

   
 
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
%  waut state, waiting for empty flag to be valid
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case wait_emptyflag
      
 
 
   clear_pulse=false;
  
  fifo_rden=false;
  wr_coef_big_fifo=false;
 
	  write_data_sel=0;

  state = ckeck_halffull;
   
  
  
  
  
  
  
  
  
 %%%%%%%%%%%%%%%%%%%%%5
 %write header and block of fifo data
 %%%%%%%%%%%%%555555555555555
 
 
 
        
    case aaaa
        
        
        clear_pulse=false; 
        
    if blk_count>0
      blk_count = blk_count - 1;
    end 
  
   %here we haave dounf taht the fifo has a pulse coming, so stiop
   %reading the fifo, write the header
      fifo_rden=false; 
       
  %write to output mem.
  wr_coef_big_fifo=true;

  %1 to write header 123456789 decimal to out put mem
    write_data_sel=1;

  
 
	state=wr_addr;
    
   

	
	
	
	

    case wr_addr
%write which fifo addr or channel we are reading out        
	 clear_pulse=false;
     
    if blk_count>0
      blk_count = blk_count - 1;
    end 
     %here we haave dounf taht the fifo has a pulse coming, so stiop
   %reading the fifo, write the header
  fifo_rden=false;
  %write to output mem
  wr_coef_big_fifo=true;
  %write the chan number and fifo addresss. whihc fifo
  write_data_sel=2;
  

	state=read_chan_fifo;
	
     
    

 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % start reading fifo data from chan fifo.
 % wait until it p[ercolates through the pulse
 %detectir 
 %state 7
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	 
    case start_chan_fifo
        
        clear_pulse=false; 
        
        
        %couns reads from chan fifo
       blk_count = blk_count - 1;
       
  fifo_rden=true;
  %write to output mem
  wr_coef_big_fifo=false;
  %write the chan number and fifo addresss. whihc fifo
  write_data_sel=0;
  
  %when data is perculated thru pulse detector, it is valid, we can now
  %save it
 if proc_busy==false
	state=start_chan_fifo;
 else
     state = look_for_pulse;
 end
 
 
 
   

 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % readhing channel fifo, look for a pulse, before writin event header
 % 
 %state 11
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	  
 
    case look_for_pulse
        
        
        clear_pulse=false; 
        
        %couns reads from chan fifo
     
     if blk_count>0
      blk_count = blk_count - 1;
    end      
  fifo_rden=true;
  %write to output mem
  wr_coef_big_fifo=false;
  %write the chan number and fifo addresss. whihc fifo
  write_data_sel=0;
  
 
 
 
 
   if is_pulse==true
       state = aaaa;
   elseif blk_count ==0;
       state = done_fifo_rd;
   else
       state = look_for_pulse;
   end
 
 
 
%     
%     
% read_chan_fifo=6;
% start_chan_fifo=7;
% done_fifo_rd=8;
% 
% out_of_data=9;
% wait_for_data = 10;

 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % read current channel fifo, write data to out mem.
 % state 6
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		
    case read_chan_fifo
     %read a block of data from one channel fifo, write to outptu fifo   

      clear_pulse=false;

	  %counds reads from chan fifo
    if blk_count>0
      blk_count = blk_count - 1;
    end
  
 %readout channel fifo data
  fifo_rden=true;
  %onluy write out the fifodata if there is a pulse
  if is_pulse == true && data_valid ==true
  wr_coef_big_fifo=true;
  else
      wr_coef_big_fifo=false;
  end
  
  %write the fifo data
 write_data_sel=3;
	
	if fifo_empty==true
        fifo_overrun_cnt=fifo_overrun_cnt+1;
       
    end
    
	
       %see if we are in the muiddle of a pulse. if so keep reading it out
       %until puise is done. we must check for empty fifo... if empty fifo
       %we will wait for data. 
       %therefure block size must be less than the length of a pulse, and
       %less than what is in fifo, less than 1/2 full fifo.
       %known to be infifo. if we trigger read channel fifo at say 32 wirds
       %or 1/2 full, then block size should be 24 or something... perhaps
       %16. fifo length should be about 4 times the length of pulse.
       %trigger when fifo is 1/2 full. then we have two blocks. block size
       %should be 1 pulse length, or 1/4 fifo size.
   	
   if fifo_empty==true
      %ran out of data...    
        if fifo_reread_cnt>0
          state = out_of_data;
          fifo_reread_cnt=fifo_reread_cnt-1;
      else
          state = done_fifo_rd;
      end
   elseif is_pulse==true
       state = read_chan_fifo;
   elseif blk_count ==0;
       state = done_fifo_rd;
   elseif is_pulse == false
       state = done_fifo_rd;
   else
       state = read_chan_fifo;
   end

   
%%%%%%%%%%%%%%%%%%%%%%%%%%%5
% case where fifo empties out before we are done with it...
% we stio readuibg channel fifo.
%we wait here until all valid data trickes thru
%pulse detector
%state 9
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case out_of_data
        
	  clear_pulse=false;
  
 %stop readout channel fifo data
  fifo_rden=false;
  %we still have valid data cuycling through the pulse detector, so write
  %it to output
  %onluy write out the fifodata if there is a pulse
 
    if is_pulse == true && data_valid ==true
  wr_coef_big_fifo=true;
  else
      wr_coef_big_fifo=false;
    end

  %write the fifo data
 write_data_sel=3;
	
  %when rd-_delay goes low we are out of data.
  %proc_data will be jhigh if there is apulse... so we 
  %is_pulse is high if we are in muiddle of pulse
        
   if data_valid==true  
       %still have data perculating thru pulse detector
       state= out_of_data;
   elseif is_pulse==false
       %out of data from pulse det. no pulse present, we are done
       state = done_fifo_rd;
   else
       %we are in the middle of a pulse, and we ran out of fifo data
       % we must wait until we have some data in fifo
       state = wait_for_data;
  end
   
   
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 %wait until fifo has data in it.
 % then we go cak to reading same channel to finish pulse
 %wait for data
 %sate 10
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
    case wait_for_data
        
         clear_pulse=false;
  blk_count = sm_block_size;
  
 %stop readout channel fifo data
  fifo_rden=false;
  %we still have valid data cuycling through the pulse detector, so write
  %it to output
  %onluy write out the fifodata if there is a pulse
  wr_coef_big_fifo=false;
  
  %write the fifo data
 write_data_sel=3;
	
  %when rd-_delay goes low we are out of data.
  %proc_data will be jhigh if there is apulse... so we 
  %is_pulse is high if we are in muiddle of pulse
        
   if quart_full==true 
       state= read_chan_fifo;
  
   else
       state = wait_for_data;
   end
 
 
	
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % waitand do nothing after reading a block from chan fifo
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case done_fifo_rd
        
         clear_pulse=false;
	
 blk_count =0;
 
  %stop reading out channfl fifo, but we must wait until all the data
  %has perculated through pulse processor.
  fifo_rden=false;
 
  
  %onluy write out the fifodata if there is a pulse


  
   if is_pulse == true && data_valid ==true
  wr_coef_big_fifo=true;
  else
      wr_coef_big_fifo=false;
  end
  
  
  %write the fifo data
 write_data_sel=3;
	
	
	%goto next channel fifo
   if data_valid ==true
       state= done_fifo_rd;
   else   
    state=inc_ram_addr;
   end
   

        
 
 
%    
%    
% 
% read_chan_fifo_raw=12;
% 
% done_fifo_rd_raw=13;
% 
% aaaa_raw=14;
% wr_addr_raw=15;
%    

  
  
 %%%%%%%%%%%%%%%%%%%%%5
 %write header and block of fifo data
 %%%%%%%%%%%%%555555555555555
 
 
 
        
    case aaaa_raw
        
        
        clear_pulse=true; 
        
       
  
   %here we haave dounf taht the fifo has a pulse coming, so stiop
   %reading the fifo, write the header
      fifo_rden=false; 
       
  %write to output mem.
  wr_coef_big_fifo=true;

  %1 to write header 123456789 decimal to out put mem
    write_data_sel=1;

  
 
	state=wr_addr_raw;
    
   

	
	
	
	

    case wr_addr_raw
%write which fifo addr or channel we are reading out        
	 clear_pulse=false;
 
     %here we haave dounf taht the fifo has a pulse coming, so stiop
   %reading the fifo, write the header
  fifo_rden=false;
  %write to output mem
  wr_coef_big_fifo=true;
  %write the chan number and fifo addresss. whihc fifo
  write_data_sel=2;
  

	state=read_chan_fifo_raw;
	
 
 
     
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % read current channel fifo, write data to out mem.
 % state 6
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		
    case read_chan_fifo_raw
     %read a block of data from one channel fifo, write to outptu fifo   

      clear_pulse=false;
  

      fifo_rden=true;
  
  
  
	  %counds reads from chan fifo
    if blk_count>0
      blk_count = blk_count - 1;
      
    end
  

  %onluy write out the fifodata if there is a pulse
  if data_valid ==true
  wr_coef_big_fifo=true;
  else
      wr_coef_big_fifo=false;
  end
  
  %write the fifo data
 write_data_sel=3;
    
	
       %see if we are in the muiddle of a pulse. if so keep reading it out
       %until puise is done. we must check for empty fifo... if empty fifo
       %we will wait for data. 
       %therefure block size must be less than the length of a pulse, and
       %less than what is in fifo, less than 1/2 full fifo.
       %known to be infifo. if we trigger read channel fifo at say 32 wirds
       %or 1/2 full, then block size should be 24 or something... perhaps
       %16. fifo length should be about 4 times the length of pulse.
       %trigger when fifo is 1/2 full. then we have two blocks. block size
       %should be 1 pulse length, or 1/4 fifo size.
   	
 if blk_count ==0;
       state = done_fifo_rd_raw;
 else
       state = read_chan_fifo_raw;
   end

    
    
 
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % waitand do nothing after reading a block from chan fifo
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case done_fifo_rd_raw
        
         clear_pulse=false;
	
 blk_count =0;
 
  %stop reading out channfl fifo, but we must wait until all the data
  %has perculated through pulse processor.
  fifo_rden=false;
 
  
  %onluy write out the fifodata if there is a pulse


  
   if  data_valid ==true
  wr_coef_big_fifo=true;
  else
      wr_coef_big_fifo=false;
  end
  
  
  %write the fifo data
 write_data_sel=3;
	
	
	%goto next channel fifo
   if data_valid ==true
       state= done_fifo_rd_raw;
   else   
    state=inc_ram_addr;
   end
   

           
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
         
    otherwise
           
   clear_pulse=true;

  
  
  fifo_rden=false;
  wr_coef_big_fifo=false;
    write_data_sel=0;

      
            state=idle;
     

%end switch
end        
%end if rst
end        

%end function
end
