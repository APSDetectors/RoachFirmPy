function [inc,addr,we]=phaseincprog(L,phase_rots)

    inc=zeros(1,L);
    addr = zeros(1,L);
    we = zeros(1,L);

    k=1;
    nchans=length(phase_rots);

    for a=0:(nchans-1)
        addr(k)=a;
        addr(k+1)=a;
        addr(k+2)=a;
        we(k)=2;
        we(k+1)=3;
        we(k+2)=2;
        inc(k)=(phase_rots(1+a)/(pi));
        inc(k+1)=inc(k);
        inc(k+2)=inc(k);
        k=k+3;
    end

   
    

end 
