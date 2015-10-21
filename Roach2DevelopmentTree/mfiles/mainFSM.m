function [rstStartFreq,incFreq,wrUserMem1,wrUserMem,isSweeping,idleStby,clrDFT,dValidDFT,pop,push,pushdata,userMemStrt,userMemSel,nextstate]=mainFSM(userMemDone,dftDone,isEndFreq,trigSweepDFT,trigSweep,setConstFreq,popdata,state,rst)

%
%outputs
%
%rstStartFreq- boolean to set freq gen to st. freq.
%incFreq- boolean to increment the freq of gen
%wrUserMem1= boolean to wr a single val into user mem. need edge sense
%wrUserMem - hold high to write many values to mem- 1 per clock
%next state- 8but val to set next state reg
%isSweeping- bool high when sweep/dft is working
%idleStby - high when we are idle, waiting
%clrDFT- bool high to clear dft ckt
%dValidDFT- tell dft data is valid and compute dft. hold hi for compute
%push
%pushdata
%pop
% userMemStrt - bool high to start writing block to user mem. hi for 1 pulse or longer.
%userMemSel- 2bit source data sel.

%
%inputs
%
%dftDone - pulses high for 1 clk when dft is done.
%isEndFreq - boolean high if we pass end freq in freq gen
%state- 8bit val that is current state
%trigSweepDFT- bool to start freq sweep and dft
%trigSweep- bool to start freq sweep, no dft. 
%setConstFreq - user sig bool to set a const freq.- no dft
%popdata
%userMemDone- hi for 1 clk when userMem is full


%
%named states
%
init0=0
idle=1

dftsweep0=2
dftsweep01=3

dftsweep1=4
dftsweep2=5
dftsweep3=6
dftsweep4=7
dftsweep5 = 8
dftsweep6=9

incfreq0=10
incfreq1=11

sweepdone0=12
sweepdone1 = 13

clrmem0=14
clrmem1=15

wrmem1_0=16
wrmem1_1=17

popaddr0=18
popaddr1=19

wrdftmem0=20
wrdftmem1=21
wrdftmem2=22
wrdftmem3=23
wrdftmem4=24
wrdftmem5=25
wrdftmem6=26
wrdftmem7=27
wrdftmem8=28
wrdftmem9=29
wrdftmem10=30
wrdftmem11=31
wrdftmem12=32
wrdftmem13=33
wrdftmem14=34
wrdftmem15=35


%bunch of waits so we can wait for dft engine to pipeline...
nopstate0=36
nopstate1=37
nopstate2=38
nopstate3=39
nopstate4=40
nopstate5=41
nopstate6=42
nopstate7=43




if rst==true
  nextstate=init0

  rstStartFreq=true;
  incFreq=false;
  wrUserMem1=false;
  wrUserMem=false;
  isSweeping=false;
  idleStby=false;
  clrDFT=true
  dValidDFT=false

  push=false;
  pop=false;
  pushdata=init0

  userMemStrt=false
  userMemSel=0
	
else

switch state
    case init0
        
        rstStartFreq=true;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=false;
        idleStby=false;
        clrDFT=true
        dValidDFT=false
	
	push=false;
	pop=false;
	pushdata=init0
	
	userMemStrt=false
        userMemSel=0
	
        nextstate=idle
        

    case idle
        
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=false;
        idleStby=true;
        clrDFT=false;
        dValidDFT=false;

	%set where subroutines return to.. it is idle, right here.
	push=true;
	pop=false;
	pushdata=idle;
	
	userMemStrt=false
        userMemSel=0
	

        
        if trigSweepDFT==true
            nextstate=dftsweep0
        else
            nextstate=idle
        end
	
	
	
	
   %%%%%%%%%%%%%%%%%%%%%
   % clear user memory
   %pop statck to return
   %%%%%%%%%%%%%%%%%%%%%%%
	

    case clrmem0
        
	%start user mem writing- reset addr, and hold WE
	
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=false;
        idleStby=false;
        clrDFT=false;
        dValidDFT=false;

	%set where subroutines return to.. it is idle, right here.
	push=false;
	pop=false;
	pushdata=idle;
	
	
	userMemStrt=true
        userMemSel=0
	
	nextstate=clrmem1
	
	
    case clrmem1
        
	%wait for mem to be done.
	
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=true;
        isSweeping=false;
        idleStby=false;
        clrDFT=false;
        dValidDFT=false;

	%set where subroutines return to.. it is idle, right here.
	push=false;
	pop=false;
	pushdata=idle;
	
	userMemStrt=false
        userMemSel=0
	
	
	
	
       
   	if userMemDone==false
        	nextstate=clrmem1
	else
		nextstate = popaddr0
        end

	
	
	
	
		

	
	
   %%%%%%%%%%%%%%%%%%%%%
   % clear user memory- write mem- sel=1
   %pop statck to return
   %%%%%%%%%%%%%%%%%%%%%%%
	

    case wrmem1_0
        
	%start user mem writing- reset addr, and hold WE
	
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=false;
        idleStby=false;
        clrDFT=false;
        dValidDFT=false;

	%set where subroutines return to.. it is idle, right here.
	push=false;
	pop=false;
	pushdata=idle;
	
	
	userMemStrt=true
        userMemSel=1
	
	nextstate=wrmem1_1
	
	
    case wrmem1_1
        
	%wait for mem to be done.
	
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=true;
        isSweeping=false;
        idleStby=false;
        clrDFT=false;
        dValidDFT=false;

	%set where subroutines return to.. it is idle, right here.
	push=false;
	pop=false;
	pushdata=idle;
	
	userMemStrt=false
        userMemSel=1
	
	
	
	
       
   	if userMemDone==false
        	nextstate=wrmem1_1
	else
		nextstate = popaddr0
        end

	
	
	
	


	
	
    %%%%%%%%%%%%%%%%%%%%%%%%%%%	
    % do dft sweep, and pop stack to return
    %%%%%%%%%%%%%%%%%%%%%   
    
    case  dftsweep0

           %rst freq to start, 
        rstStartFreq=true;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false;
        dValidDFT=false;

	push=true;
	pop=false;
	pushdata=dftsweep2

	
	userMemStrt=false
        userMemSel=0
	

        %do a wait,, then return to dftsweep2	  
        nextstate=nopstate0
        
    
        
    case dftsweep2
        
 
           % rst  wr mem addr
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false

	push=true;
	pop=false;
	pushdata=dftsweep01
	
	userMemStrt=true
        userMemSel=0
	
	    %do a wait...
	nextstate=nopstate0
    
    case  dftsweep01

           % rst dft
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=true
        dValidDFT=false

	push=true;
	pop=false;
	pushdata=dftsweep1
	
	userMemStrt=false
        userMemSel=0
	
	%subroutine to nopstate to wait for clear dft to finish
	%then resume at dftsweep1    
	nextstate=nopstate0
 
        
    case  dftsweep1

        %start compute dft- this computes ONE SUM
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=true
 
	push=false;
	pop=false;
	pushdata=init0
        
  	
	userMemStrt=false
        userMemSel=2
	
     
        nextstate=dftsweep3
        
          
         
        
    case  dftsweep3

        %wait for  compute dft sum to finish
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=true
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
        userMemSel=2
	
     
        if dftDone==false
            nextstate=dftsweep3
        else
            nextstate=dftsweep4
        end
        
	
	
%
% done w/ dft. call thestates to wr dft to ram.
%	
          
       
    case  dftsweep4

        %dft is done, write dft to user mem
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
 	% we will return to dftsweep 5
	push=true;
	pop=false;
	pushdata=dftsweep5
        
 	
	userMemStrt=false
	
        userMemSel=0
	
     
       
   	%this is a subroutine to wr dft mem.
	% wepop back to dftsweep5
        nextstate=wrdftmem0
        
 
 
    case  dftsweep5

        %nop state, do nothong...
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
       
   
        nextstate=dftsweep6
        

%
% enbd writing dft data
%





    case  dftsweep6

        %noop state
	
	
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
        userMemSel=3
	
     
       
   
        nextstate=incfreq0
        
 
    %%%%%%%%%%%%%%%%%%%%%%%%%
    %Increment sin gen freq if we are not at end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
       
    case  incfreq0

        %inc the frequency to next step
        rstStartFreq=false;
        incFreq=true;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
       

	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
        userMemSel=2
	
      
   
        nextstate=incfreq1
                 
       
       
    case  incfreq1

        %if we have passed last freq, we quit and idle, else we do new dft
        %also, if we run out of mem, we quit and idle.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
  	
	userMemStrt=false
        userMemSel=2
	
      
      
       
   	if isEndFreq==true
        	nextstate=popaddr0
    elseif userMemDone==true
            nextstate=popaddr0
	else
		nextstate = dftsweep01
        end

    %%%%%%%%%%%%%%%%%%
    %
    % pop address- pop stack and set state to that.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%
    
    
              
       
       
    case  popaddr0

        %if we have passed last freq, we quit and idle, else we do new dft
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=true;
	pushdata=init0
        
	
	userMemStrt=false
        userMemSel=0
	
      
       
        	nextstate=popaddr1
	
    
     
        
       
    case  popaddr1

        %if we have passed last freq, we quit and idle, else we do new dft
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false;
        dValidDFT=false;
 
	push=false;
	pop=false;
	pushdata=init0;
        
 	
	userMemStrt=false
        userMemSel=0
	
     
       
       	nextstate=popdata;







%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Write DFT data to memory
% this is a subroutine...
% it writes 8 valuies by setting sel.
% Is uses wrUserMem1, that wires one mem word
%on rising edge. So we have to push wrUserMem1 Lo than
%high. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	
          
 
 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem0

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%sel real part
        userMemSel=0
	
     
       
   
        nextstate=wrdftmem1
        
 
 
    case  wrdftmem1

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
       
   
        nextstate=wrdftmem2




 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem2

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	
        userMemSel=1
	
     
       
   
        nextstate=wrdftmem3
        
 
 
    case  wrdftmem3

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=1
	
     
       
   
        nextstate=wrdftmem4


 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem4

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	
        userMemSel=2
	
     
       
   
        nextstate=wrdftmem5
        
 
 
    case  wrdftmem5

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=2
	
     
       
   
        nextstate=wrdftmem6


 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem6

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	
        userMemSel=3
	
     
       
   
        nextstate=wrdftmem7
        
 
 
    case  wrdftmem7

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=3
	
     
       
   
        nextstate=wrdftmem8


 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem8

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	
        userMemSel=4
	
     
       
   
        nextstate=wrdftmem9
        
 
 
    case  wrdftmem9

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=4
	
     
       
   
        nextstate=wrdftmem10


 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem10

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=5
	
     
       
   
        nextstate=wrdftmem11
        
 
 
    case  wrdftmem11

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=5
	
     
       
   
        nextstate=wrdftmem12


 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem12

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=6
	
     
       
   
        nextstate=wrdftmem13
        
 
 
    case  wrdftmem13

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=6
	
     
       
   
        nextstate=wrdftmem14


 
%
% Two states to set userMemSel, and wrUserMem1 from low to high
%   Writes data to RAM
%
    
    case  wrdftmem14

        %set mem sel. 
	% wrUserMem1=low so we can flag it high.
        rstStartFreq=false;
        incFreq=false;
	
	
        wrUserMem1=false;
        
	wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=7
	
     
       
   
        nextstate=wrdftmem15
        
 
 
    case  wrdftmem15

        %set wrUserMem1 high. 
	%data is written here.
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=true;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=7
	
     
   
        nextstate=popaddr0






%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%wait 8 cycles and pop address
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    case  nopstate0

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
	nextstate=nopstate1
     


    case  nopstate1

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
	nextstate=nopstate2
     
    

    case  nopstate2

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
	nextstate=nopstate3
     
    

    case  nopstate3

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
	nextstate=nopstate4
     
    

    case  nopstate4

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
	nextstate=nopstate5
     
    

    case  nopstate5

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
	nextstate=nopstate6
     
    

    case  nopstate6

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
	nextstate=nopstate7
     
    

    case  nopstate7

      
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=true;
        idleStby=false;
        clrDFT=false
        dValidDFT=false
 
	push=false;
	pop=false;
	pushdata=init0
        
 	
	userMemStrt=false
	%
        userMemSel=0
	
     
     
	 nextstate=popaddr0




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
         
    otherwise
    
        rstStartFreq=false;
        incFreq=false;
        wrUserMem1=false;
        wrUserMem=false;
        isSweeping=false;
        idleStby=false;
        clrDFT=false;
        dValidDFT=false;
 
	push=false;
	pop=false;
	pushdata=init0
        
        
    
  	
	userMemStrt=false
        userMemSel=0
	
   
        nextstate=init0;

%end switch
end        
%end if rst
end        

%end function
end
