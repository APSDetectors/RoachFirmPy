function [fifo_rden, wr_coef_big_fifo,  write_data_sel,cur_chanout,fifo_overrun_cnt_out,stateout,clear_pulse,datapath_enable,save_event,delete_event,save_pulse_state,calc_mean,store_mean]=fifoFSM(dumpFifo,fifo_empty,half_full,quart_full, almost_full,rst,proc_busy,is_pulse,data_valid,last_channel,wr_raw_data,ram_pulse_state,is_calc_mean, flush_fifo)

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
%save_event- tell output evt fifo to save into out mem.
%delete_event- tell out evt fifo, to flush to bit bucket

%calc_mean tells pulse finder to measure noise and find exp val for phwse
%and amp
%store man stores the calc'ed mean in ram on a per channel basis

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

%is_calc_mean input, if high we will calc mean of noise and store it.




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

done_fifo_rd=7;

finish_event = 8;


flush_zero_addr=9;
flush_wait_empty=10;
flush_inc_addr=11;



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



% set to 1 if we saw a pulse during a fifo read of some channel.
persistent is_found_pulse, is_found_pulse= xl_state(0,{xlUnsigned, 1, 0});



cur_chanout=cur_channel;
fifo_overrun_cnt_out = fifo_overrun_cnt;

stateout = state;

%
% Reset state
%


if rst==true
  state=idle;

  
  calc_mean=false;
  store_mean = false;
  
  save_pulse_state=false;
  
  
  save_event = false;
  delete_event= false;
  
  is_found_pulse=0;
  
  blk_count=0;
  fifo_reread_cnt=0;
  
  clear_pulse=true;
  datapath_enable = false;
  
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
  
  save_pulse_state=false;
  
  
  calc_mean=false;
  store_mean = false;
  

  save_event = false;
  delete_event= false;
  
        is_found_pulse=0;
        
   cur_channel = 0;

   clear_pulse=true;
  
  fifo_rden=false;
  wr_coef_big_fifo=false;
    write_data_sel=0;
datapath_enable = false;true
        
	if  flush_fifo==true
	    %emty fifos and throw away data, clean up.
	    state = flush_zero_addr;
        elseif dumpFifo==true
	    %read data from fifos and store to outpit, read chuncks per channel
            state=ckeck_halffull;
        else
	   %do notghing
            state=idle;
        end
	
	
	
	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
%see if fifo has data in it. look for 1/2 full fifo
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case ckeck_halffull
        
  calc_mean=false;
  store_mean = false;
  

  
  save_pulse_state=false;
  

  save_event = false;
  delete_event= false;
  
 
    % if almost_full==true 
	%     blk_count = max_block_size;
     %else
         blk_count = mid_block_size;
    % end
     
     is_found_pulse=0;
     
fifo_reread_cnt=1;

 clear_pulse=true;

  
  fifo_rden=false;
  wr_coef_big_fifo=false;
  
  write_data_sel=0;
	datapath_enable = false;
    
        if dumpFifo==true
            
          if half_full==false
            state=inc_ram_addr;
          else
            %if data in fifo, read a block
           
          
                state = aaaa;
         
            
          end
        else
            state=idle;
        end
	
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
%  we imr the channel, or fifo number, we are looking at
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case inc_ram_addr
        
  save_pulse_state=false;
    
  calc_mean=false;
  store_mean = false;
  


  
  save_event = false;
  delete_event= false;
  
      
    if    cur_channel<last_channel  
        
        cur_channel = cur_channel + 1;
    else
        cur_channel=0;
    end
    
 
 clear_pulse=false;
 datapath_enable = false;
 
  fifo_rden=false;
  wr_coef_big_fifo=false;
 
	  write_data_sel=0;

  state = wait_emptyflag;
        

   
 
  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
%  waut state, waiting for empty flag to be valid
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case wait_emptyflag
      
   
  save_pulse_state=false;
  
  
  calc_mean=false;
  store_mean = false;
  

  
  save_event = false;
  delete_event= false;
  

 
   clear_pulse=false;
  
  fifo_rden=false;
  wr_coef_big_fifo=false;
 
	  write_data_sel=0;
datapath_enable = false;


  state = ckeck_halffull;
   
  
  
  
  
  
  
  
  
 %%%%%%%%%%%%%%%%%%%%%5
 %write header and block of fifo data
 %%%%%%%%%%%%%555555555555555
 
 
 
        
    case aaaa
        
    
  save_pulse_state=false;
  
  
  calc_mean=false;
  store_mean = false;
  

  save_event = false;
  delete_event= false;
  
      
        clear_pulse=false; 
        
 
  
   %here we haave dounf taht the fifo has a pulse coming, so stiop
   %reading the fifo, write the header
      fifo_rden=false; 
       datapath_enable = false;
  %write to output mem.
  wr_coef_big_fifo=true;

  %1 to write header 123456789 decimal to out put mem
    write_data_sel=1;

  
 
	state=wr_addr;
    
   

	
	
	
	

    case wr_addr
        
   
  save_pulse_state=false;
  
  
  
  store_mean = false;
  calc_mean = false;
  
 

  save_event = false;
  delete_event= false;
  
       
 
   
        
%write which fifo addr or channel we are reading out        
	 clear_pulse=false;
   
     %here we haave dounf taht the fifo has a pulse coming, so stiop
   %reading the fifo, write the header
  fifo_rden=false;
  
  datapath_enable = false;
  
  %write to output mem
  wr_coef_big_fifo=true;
  %write the chan number and fifo addresss. whihc fifo
  write_data_sel=2;
  

	state=read_chan_fifo;
	
     
    

   
 
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
  
  save_pulse_state=false;
    
  
  store_mean = false;
  
 if is_calc_mean == true
       calc_mean = true;
 else
     calc_mean = false;
 end
 

  save_event = false;
  delete_event= false;
  

      clear_pulse=false;

	  %counds reads from chan fifo
    if blk_count>0
      blk_count = blk_count - 1;
       fifo_rden=true;
    else
        fifo_rden=false;
    end
    
 
 
  
  datapath_enable = true;
  
  %onluy write out the fifodata if there is a pulse
  if data_valid ==true
  wr_coef_big_fifo=true;
  else
      wr_coef_big_fifo=false;
  end
  
  %write the fifo data
 write_data_sel=3;
	
    if is_pulse==true || ram_pulse_state==true
        is_found_pulse = 1;
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
   	
  
   if blk_count ==0;
       state = done_fifo_rd;
   
   else
       state = read_chan_fifo;
   end

   
  
	
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % waitand do nothing after reading a block from chan fifo
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case done_fifo_rd
     
  save_pulse_state=false;
  
  
  calc_mean=false;
  store_mean = false;
  

  save_event = false;
  delete_event= false;
  
  
     
         clear_pulse=false;
	
 
    if is_pulse==true
        is_found_pulse = 1;
    end
 
  %stop reading out channfl fifo, but we must wait until all the data
  %has perculated through pulse processor.
  fifo_rden=false;
 
  datapath_enable = true;
  %onluy write out the fifodata if there is a pulse


  
   if data_valid ==true
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
    state=finish_event;
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

  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 % waitand do nothing after reading a block from chan fifo
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case finish_event
    
          
  calc_mean=false;
 
  

  if is_calc_mean == true
      store_mean= true;
  else
      store_mean = false;
  end
  
  
  
  
  save_pulse_state=true;
  

  if is_found_pulse == 1 ||wr_raw_data==true 
      save_event = true;
      delete_event = false;
  else
      save_event = false;
      delete_event = true;
  end
  
  
  
     
         clear_pulse=false;
	
 
 
  %stop reading out channfl fifo, but we must wait until all the data
  %has perculated through pulse processor.
  fifo_rden=false;
 
  datapath_enable = true;
  %onluy write out the fifodata if there is a pulse


  
      wr_coef_big_fifo=false;
 
  
  
  %write the fifo data
 write_data_sel=0;
	
	

    state=inc_ram_addr;

   

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% beginning of flush fifo, to clear it. we zero current channel and move on
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	case flush_zero_addr
    
        %read a block of data from one channel fifo, write to outptu fifo   
  
  	save_pulse_state=false; 
  	store_mean = false;
     	calc_mean = false;
 
  	save_event = false;
  	delete_event= false;
        clear_pulse=false;

	  %counds reads from chan fifo
  
       fifo_rden=false;
  
  datapath_enable = false;
  
 
  wr_coef_big_fifo=false;

  
  %write the fifo data
 write_data_sel=0;
	
    %register
        is_found_pulse = 0;
   %register
   cur_channel=0
  
       state = flush_wait_empty;
  
   
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% on this channel, read fifo until empty, do not store data. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	case flush_wait_empty
    
        %read a block of data from one channel fifo, write to outptu fifo   
  
  	save_pulse_state=false; 
  	store_mean = false;
     	calc_mean = false;
 
  	save_event = false;
  	delete_event= false;
        clear_pulse=false;

	  %counds reads from chan fifo
  
       fifo_rden=true;
   
 
 
  
  	datapath_enable = false;
  
 
 	 wr_coef_big_fifo=false;

  
 	 %write the fifo data
 	write_data_sel=0;
 
 	if fifo_empty==false
   	    state = flush_wait_empty;
	else
	    state = flush_inc_addr;
	end
	
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% if not at last chan, inc chan, and fluch that channel. else goto idle
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	case flush_inc_addr
	
 
        %read a block of data from one channel fifo, write to outptu fifo   
  
  	save_pulse_state=false; 
  	store_mean = false;
     	calc_mean = false;
 
  	save_event = false;
  	delete_event= false;
        clear_pulse=false;

	  %counds reads from chan fifo
  
       fifo_rden=false;
   
 
 
  
  	datapath_enable = false;
  
 
 	 wr_coef_big_fifo=false;

  
 	 %write the fifo data
 	write_data_sel=0;
 
 	if cur_channel<255
            cur_channel=cur_channel+1;
 
   	     state = flush_wait_empty;
	else
	   cur_channel=0;
	   state=idle;
        end

 
 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
         
    otherwise
          
  save_pulse_state=false;
  
  
  calc_mean=false;
  store_mean = false;
  

  save_event = false;
  delete_event= false;
  
   
   clear_pulse=true;

  datapath_enable = false;
  
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
