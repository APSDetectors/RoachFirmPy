
is_plot_mem=true;
is_plot_ch=false;



if is_plot_mem
    
    nchans=64
    
    mag=outmem.signals(1).values;
    phs=outmem.signals(2).values;
    dvld=outmem.signals(3).values;
    
    ff=find(phs>1.9);
    
    
    ff=find(dvld>0);
    
    
    magv=mag(ff);
    phsv=phs(ff);
    
    
    
    
    figure(10);
    clf();
    plot(mag(ff),'r');
    hold on;
    plot(phs(ff));
    
    
    nevents = length(magv)/34.0;
   

    
    events_m=zeros(nchans,256);
    events_p=zeros(nchans,256);
    indx=zeros(1,nchans);
    
    for k = 0:(nevents-1)
    
 
        ev_ph = phsv( ((k*34)+1):((k*34)+34)  );
      
        ev_mg = magv( ((k*34)+1):((k*34)+34)  );
        
        channel =1+ (2^15)*ev_ph(3)
        
        events_m(channel, (indx(channel)+1):(indx(channel)+34) ) = ev_mg;
        events_p(channel, (indx(channel)+1):(indx(channel)+34) ) = ev_ph;
       
      
        indx(channel)=indx(channel)+34;
      
    end
    
    


end


%plot each ahennel


%cc=1;
if is_plot_ch
    figure(11);clf();plot(datai(cc:64:16384));hold on; plot(dataq(cc:64:16384),'r');cc=cc+2;
end
