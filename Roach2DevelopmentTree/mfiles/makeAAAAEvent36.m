function event = makeAAAAEvent36(mag,phase,chan,timestamp,ispulse)

    evtlen = length(phase)+2;
    event = zeros(1,evtlen);
    
    event(1) = uint64(hex2dec('aaaa'))*2^2 + bitand(uint64(timestamp), uint64(hex2dec('ffff0000'))) * 2^4;
    event(2) =  uint64(chan +ispulse*2^8 + bitand(uint64(timestamp),uint64(bin2dec('1111111'))))*2^2 + 
            bitand( uint32(timestamp),uint32( hex2dec('ffff'))*2^9  + ispulse*2^8);
    magb=uint64(toTwoComp(mag,18,18));
    phsb = uint64(toTwoComp(phase,18,15));
    magb =uint32(magb * 2^18);
    
    magphs = uint32(magb + bitand(uint32(phsb),uint32(hex2dec('ffff'))));
    event(3:evtlen) = magphs;
    

end
