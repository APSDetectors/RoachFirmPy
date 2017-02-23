function xyb = transTable(xtr,ytr)




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%set up translator bin vars


xtrb = round(abs(xtr) * 2^14);
if xtr<0
    xtrb = 2^16 - xtrb ;
end

ytrb = round(abs(ytr) * 2^14);
if ytr<0
    ytrb =2^16 - ytrb ;
end

xtrb = typecast(uint16(xtrb),'uint16');
ytrb = typecast(uint16(ytrb),'uint16');

xtrb = double(xtrb);
ytrb=double(ytrb);


%comment out to NOT set trans table, leave 0
%transtable(1) = 65536.0 * xtrb + ytrb;


xyb=65536.0 * xtrb + ytrb;

end
