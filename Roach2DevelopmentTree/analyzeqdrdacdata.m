plot(pfboutput.signals(1).values)
plot(pfboutput.signals(9).values)




i0=pfboutput.signals(1).values;
i1=pfboutput.signals(3).values;
i2=pfboutput.signals(5).values;
i3=pfboutput.signals(7).values;
q0=pfboutput.signals(2).values;
q1=pfboutput.signals(4).values;
q2=pfboutput.signals(6).values;
q3=pfboutput.signals(8).values;

sync = pfboutput.signals(9).values;

%sync on 499

k=500

I = zeros(512,1);
Q=zeros(512,1);

I(1:4:512) = i0(k:(k+127));
I(2:4:512) = i1(k:(k+127));
I(3:4:512) = i2(k:(k+127));
I(4:4:512) = i3(k:(k+127));



Q(1:4:512) = q0(k:(k+127));
Q(2:4:512) = q1(k:(k+127));
Q(3:4:512) = q2(k:(k+127));
Q(4:4:512) = q3(k:(k+127));


IQ = I - j*Q;

IQF = abs(fft(IQ));

plot(IQF)




