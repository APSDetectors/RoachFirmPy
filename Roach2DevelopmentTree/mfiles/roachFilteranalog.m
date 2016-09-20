




s=1.0

C = 100e-12
L = 50e-6
R1 = 100
R2 = 50


x = 1
y = 0

decade = log10(1:0.1:10)


freqabs = 2*pi*[ 1e3.*decade , 1e4.*decade ,1e5.*decade ,1e6.*decade ,1e7.*decade ];
freqs = [ -fliplr(freqabs), freqabs]

lenx = length(freqs);

sre = ones(lenx,lenx);


sim = ones(lenx,lenx);

for row = 1:lenx
    sre(row,:) = freqs;    
end

for col = 1:lenx
    sim(:,col) = j * freqs';    
end

s = sre + sim;

        



Zc = 1 ./(s .* C); 

Zl = s.*L;

ZcPR2 = (Zc.*R2) ./ (Zc+R2);

Z_2 = ZcPR2 ./ (Zl + ZcPR2);

Ztop = (Zc.*(L + ZcPR2) ) ./ ( (Zc + L + ZcPR2  ));

Zbot = Ztop + R1;
Z_1 = Ztop./ Zbot;

Ztot = Z_1 .* Z_2;


mesh(log10(abs(Ztot)))

