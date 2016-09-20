function event = makeAAAAEvent(mag,phase,chan,timestamp,ispulse)

    evtlen = length(phase)+2;
    event = zeros(1,evtlen);
    
    event(1) = uint32(hex2dec('aaaa') + bitand(uint32(timestamp), uint32(hex2dec('ffff0000'))));
    event(2) = uint32( chan + bitand( uint32(timestamp),uint32( hex2dec('ffff'))*2^9  + ispulse*2^8));
    magb=toTwoComp(mag,16,16);
    phsb = toTwoComp(phase,16,13);
    magb =uint32(magb * 2^16);
    
    magphs = uint32(magb + bitand(uint32(phsb),uint32(hex2dec('ffff'))));
    event(3:evtlen) = magphs;
    

end
