function bdata=toTwoComp(data,nbits,dpoint)


bdata=floor(abs(data) *2^dpoint);

for k =1:length(data)
    if data(k)<0
        bdata(k)=2^nbits - bdata(k);
    end
end
bdata = uint32(bdata);
end
