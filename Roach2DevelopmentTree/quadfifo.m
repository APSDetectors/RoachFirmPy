function [re,trigrd,muxout,we]=quadfifo(full,rst)




%
% Named states
%

idle = 0;

rd0=1;
rd1=2;
rd2=3;
rd3=4;


%
% persistent registers
%
persistent state, state = xl_state(idle,{xlUnsigned, 3, 0});


persistent rdcount, rdcount = xl_state(0,{xlUnsigned, 32, 0});

persistent muxx,muxx =  xl_state(0,{xlUnsigned, 2, 0});




%
% get bits crom control register
%





%
%
%




muxout = muxx;
        

if rst==true
  state=idle;    

rdcount=0;
  muxx = 0;
 
  re= false;
  trigrd = false;
  we=false;
  
else

switch state
 
    case idle
        rdcount = 0;
        muxx=0;
        re=false;
        we=true;
        
        if full==true
            state=rd0;
            trigrd = true;
            
        else
            state = idle; 
        end

  
       
        
        
    case rd0
        
        %for next state
        muxx=1;
        trigrd=false;
        re=true;
        rdcount = rdcount+1;
        we=false;
        state = rd1;
        
          
    case rd1
        
        %for next state
        muxx=2;
         trigrd=false;
       we=false;
        re=false;
        
        
        state = rd2;

        
             
    case rd2
        
        %for next state
        muxx=3;
        trigrd=false;
        we=false;
        re=false;
        
        
        state = rd3;
    
        
        
        
          
    case rd3
        
        %for next state
        muxx=0;
        trigrd=false;
        we=false;
        re=false;
        
        if rdcount==512
            state=idle;
        else
            
           state = rd0;
        end
        
    
        
              
end
end



end
