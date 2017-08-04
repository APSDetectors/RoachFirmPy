function [fifo_rden, wr_coef_big_fifo,cur_chanout, ...
        stateout,datapath_enable,write_data_sel,done_event,start_event, ...
        read_time_stamp] = ...
    fifoFSMPh3(dumpFifo,fifo_empty,half_full,...
        rst,data_valid,last_channel,is_datapath_ready,...
        flush_fifo,req_block_size,sync_pulse,is_look_for_sync,calc_busy)

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

%is_datapath_ready - high if we are legal to read the fifo to someting...
%req_block_size- how much to read out of the fifo

%sync_pulse - bool bit that is high when we have a sync pulse from flux ramp.
%           this pulse is stored along w/ FFT coef and comes out of fifos as en extra bit.
%           We can read fifos and look for sync pulse
%is_look_for_sync - high if we want fsm to look for sync pulse. it reads fifo and deletes data until find sync
%           then it will continue reading for block size words, sending data to data sink.
%           if false, it will just send all data to data sync



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%named states
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

idle=0;             %do nothing
ckeck_halffull=1;   %check fifo half full flag, or whatever flag is conn.

inc_ram_addr=2;     %inc fifo read addr, that is, proceed to tryu next channel
wait_emptyflag=3;   %wait for empty flag in fifo.
wait_emptyflag2=11;   %wait for empty flag in fifo.

aaaa=4;             %write aaaa to the header of output data.
wr_addr=5;          %write address or channel num to out put data


read_chan_fifo=6;   %red out data from fifo to data stream

done_fifo_rd=7;     %done reaading data, read whole block

finish_event = 8;   %finish reading event
read_timestamp=9;

flush_wait_empty=10;
flush_to_sync=12;   %read fifo, delete output data, until we find sync pulse high




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Registers
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

persistent state, state = xl_state(idle,{xlUnsigned, 4, 0});


% current fifl or channel we are reading out. must be power of two num
% channels. currently 256. wa have a max channel input, if we want to read
%chan 0 to 3 for example. we set max ahennto to 3. for 16 chans,
%we set max chan to 15
persistent cur_channel, cur_channel = xl_state(0,{xlUnsigned, 8, 0});





% Counter to keep track of block size read from channel fifo
% block size uop to 256. 
persistent blk_count, blk_count = xl_state(0,{xlUnsigned, 8, 0});







cur_chanout=cur_channel;

stateout = state;

%
% Reset state
%


if rst==true
  state=idle;

  blk_count=0;
  fifo_reread_cnt=0;  
  datapath_enable = false;  
  fifo_rden=false;
  wr_coef_big_fifo=false; 
  cur_channel =0;
  write_data_sel=0;
  done_event=false;
  start_event=false;
  read_time_stamp=false;
  
  
else

  %
  %  run staet machine, switch statements
  %

  switch state
 
     
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    %wait for trigger to start reading the fifos, dumpFifo <=1
    %rst addr and blk cnt
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
    case idle
 
        cur_channel = 0;  
        fifo_rden=false;
        wr_coef_big_fifo=false;
        write_data_sel=0;
        datapath_enable = false;
        done_event=false;
        start_event=false;
        read_time_stamp=false;
        
	    if  flush_fifo==true || dumpFifo==true
	        %emty fifos and throw away data, clean up.
	        state = ckeck_halffull;
       
        else
	        %do notghing
            state=idle;
        end
	
	
	
	
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
    %see if fifo has data in it. look for 1/2 full fifo
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case ckeck_halffull
 
        blk_count = req_block_size;
       
        fifo_reread_cnt=1;
        fifo_rden=false;
        wr_coef_big_fifo=false;
	    datapath_enable = false;
        write_data_sel=0;
        done_event=false;
        start_event=false;
        read_time_stamp=false;
        
        if dumpFifo==true            
          if half_full==false
            state=inc_ram_addr;
            
          elseif is_datapath_ready==true
            state = read_timestamp;
          else
            state = idle;
            
          end
        elseif flush_fifo == true
            state = flush_wait_empty;
            
        else
            state=idle;
           
        end
	
  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
    %  we imr the channel, or fifo number, we are looking at
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case inc_ram_addr
 
       
        if cur_channel<last_channel         
            cur_channel = cur_channel + 1;
        else
            cur_channel=0;
           
            
        end
        done_event=false;
        start_event=false;
        datapath_enable = false;
        write_data_sel=0;
        fifo_rden=false;
        wr_coef_big_fifo=false;
        read_time_stamp=false;

        state = wait_emptyflag;
        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
    %  waut state, waiting for empty flag to be valid
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case wait_emptyflag
        fifo_rden=false;
        wr_coef_big_fifo=false; 
        datapath_enable = false;
        state = wait_emptyflag2;
        write_data_sel=0;
        done_event=false;
        start_event=false;
        read_time_stamp=false;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
    %  waut state, it takes an extra clock for empty flag to be valid.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    case wait_emptyflag2
        fifo_rden=false;
        wr_coef_big_fifo=false;
        datapath_enable = false;
        state = ckeck_halffull;
        write_data_sel=0;
        done_event=false;
        start_event=false;
        read_time_stamp=false;





      
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5  
    %  waut state, waiting for empty flag to be valid
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case read_timestamp
        fifo_rden=false;
        wr_coef_big_fifo=false; 
        datapath_enable = false;
        
        write_data_sel=0;
        done_event=false;
        
        if cur_channel==0
            read_time_stamp=true;
        else
            read_time_stamp=false;
        end

%here we start reading the fifo, which will be one event starting
        %w/ aaaa in the outout data                
        if is_look_for_sync==true
           if sync_pulse==false
                %read fifo and delete data until we find sync.
                state = flush_to_sync;
                start_event=false;
           else
            %read out data to data sink.
                state = aaaa;
                start_event=true;
           end
        else
            %read out data to data sink.
            state = aaaa;
            start_event=true;
        end


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Read fifo, but do nto store data. stay in this state until we ahve
    %high sync pulse. then goto to aaaa, for read data readout.
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case flush_to_sync


        %red out the fifo
        fifo_rden=true;
        wr_coef_big_fifo=false; 
	    write_data_sel=0;
        %false for datapath mean data is deleted, and read to no where.
        datapath_enable = false;
        done_event=false;
        read_time_stamp=false;
        
        
        if sync_pulse == false
            state = flush_to_sync;
            start_event=false;
        else
            state = aaaa;
            start_event=true;
        end


  
    %%%%%%%%%%%%%%%%%%%%%5
    %write header and block of fifo data
    %%%%%%%%%%%%%555555555555555
    case aaaa

        %here we haave dounf taht the fifo has a pulse coming, so stiop
        %reading the fifo, write the header
        fifo_rden=false; 
        datapath_enable = false;
        %write to output mem.
        wr_coef_big_fifo=true;
        %1 to write header 123456789 decimal to out put mem
        write_data_sel=1;
	    done_event=false;
        state=wr_addr;
        read_time_stamp=false;
        start_event=false;
        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case wr_addr
        
        %here we haave dounf taht the fifo has a pulse coming, so stiop
        %reading the fifo, write the header
        fifo_rden=false;
  
        datapath_enable = false;
  
        %write to output mem
        wr_coef_big_fifo=true;
        %write the chan number and fifo addresss. whihc fifo
        write_data_sel=2;
        done_event=false;
	    state=read_chan_fifo;
        read_time_stamp=false;
        start_event=false;
        
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % read current channel fifo, write data to out mem.
    % state 6
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		
    case read_chan_fifo
        %read a block of data from one channel fifo, write to outptu fifo   
	    %counds reads from chan fifo
        if blk_count>0
            blk_count = blk_count - 1;
            fifo_rden=true;
        else
            fifo_rden=false;
        end
    
        datapath_enable = true;
        read_time_stamp=false;
        start_event=false;
        
        %onluy write out the fifodata if there is a pulse
        if data_valid ==true
            wr_coef_big_fifo=true;
        else
            wr_coef_big_fifo=false;
        end

        %write the fifo data
        write_data_sel=3;
        done_event=false;
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

        %stop reading out channfl fifo, but we must wait until all the data
        %has perculated through pulse processor.
        fifo_rden=false; 
        datapath_enable = true;
        %onluy write out the fifodata if there is a pulse
        read_time_stamp=false;
        
        if data_valid ==true
            wr_coef_big_fifo=true;
        else
            wr_coef_big_fifo=false;
        end
  
  
        %write the fifo data
        write_data_sel=3;
	    done_event=false;
        start_event=false;
        
	    %goto next channel fifo
        if data_valid ==true || calc_busy == true
            state= done_fifo_rd;
        else   
            state=finish_event;
        end


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % waitand do nothing after reading a block from chan fifo
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    case finish_event
  
        read_time_stamp=false;
        %stop reading out channfl fifo, but we must wait until all the data
        %has perculated through pulse processor.
        fifo_rden=false;
        datapath_enable = true;
        %onluy write out the fifodata if there is a pulse
        wr_coef_big_fifo=false;
        %write the fifo data
        write_data_sel=0;
        done_event=true;
        state=inc_ram_addr;
        start_event=false;

    
   
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % on this channel, read fifo until empty, do not store data. 
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	case flush_wait_empty
        %counds reads from chan fifo
        fifo_rden=true;
  	    datapath_enable = false;
 	    wr_coef_big_fifo=false;
 	    write_data_sel=0;
        done_event=false;
        read_time_stamp=true;
        start_event=false;
        
 	    if fifo_empty==false
   	        state = flush_wait_empty;
	    else
	        state = inc_ram_addr;
	    end
	
 

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

         
    otherwise
 
        datapath_enable = false;  
        fifo_rden=false;
        wr_coef_big_fifo=false;
        write_data_sel=0;
        done_event=false;     
        state=idle;
        read_time_stamp=false;
        start_event=false;
     

    %end switch
    end        
%end if rst
end        

%end function
end
