



save('../projcts/simresults.mat','fsmdata','fsmdata3','fsmdata5','fsmdata4','fsmdata1','fsmdata2','fsmdata6','fsmdata7','fsmdata8','fsmdata9','fsmdata10','fsmdata11');


p_times_=fsmdata4.time';

p_stfft_=fsmdata4.signals(5).values';
p_we_=fsmdata4.signals(6).values';
p_mag_=fsmdata4.signals(7).values';

p_phase_=fsmdata4.signals(8).values';

ff=find(p_we_>0);
    
    
magv=p_mag_(ff);

phsv=p_phase_(ff);





save('../projcts/m2py.mat','p_times_','p_stfft_','p_we_','p_mag_','p_phase_','magv','phsv');

