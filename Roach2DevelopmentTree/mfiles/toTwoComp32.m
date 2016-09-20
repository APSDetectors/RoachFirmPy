function bdata=toTwoComp32(data,nbits,dpoint)

    bdata = zeros(1,length(data));
    
    for k = 1:length(data)
        bdata(k)=floor(abs(data(k)) * (2^dpoint));
        if data(k)<0
            bdata(k)=2^nbits - bdata(k);
        end
        
        bdata(k) = int32(bdata(k));     
    end
   
end
