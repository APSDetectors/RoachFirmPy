function [cnten,cntrst,nextstate] = viewmemcontrol(start,endcnt,state)
init = 0;


%default vals
switch state
    case 0
        cnten=false;
        cntrst=true;
        
       
        nextstate=1;
      
        
    case 1
        cntrst=false;
        cnten=true;
        
        
        if start == true
            nextstate = 0
        elseif endcnt==false
            nextstate=1;
        else
            nextstate=2;
        end
        
    case 2
        
        cnten=false;
        cntrst=false;
        
        if start == true
            nextstate = 0
        else
            nextstate=2;
        end
        
    case 3
        
        cnten=false;
        cntrst=false;
       
        nextstate=0;
       
        
    otherwise
        cnten=false;
        cntrst=false;
        nextstate=0;
end        
        


end