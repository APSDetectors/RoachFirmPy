function [ Circle ] = fit_circle2( x,y )
%Calculate center and radius of a circle given x,y
%   Uses circle fitting routine from Gao dissertation
%From publication Chernov and Lesort, Journal of Mathematical Imaging and
%Vision 23: 239-252, 2005. Springer Science
% Updated: 01-09-2012 - alterted to work with 'Resonator' IQ data structure



n = length(x);
w =(x.^2+y.^2);

%create moment matrix
M(1,1) = sum(w.*w);
M(2,1) = sum(x.*w);
M(3,1) = sum(y.*w);
M(4,1) = sum(w);
M(1,2) = sum(x.*w);
M(2,2) = sum(x.*x);
M(3,2) = sum(x.*y);
M(4,2) = sum(x);
M(1,3) = sum(y.*w);
M(2,3) = sum(x.*y);
M(3,3) = sum(y.*y);
M(4,3) = sum(y);
M(1,4) = sum(w);
M(2,4) = sum(x);
M(3,4) = sum(y);
M(4,4) = n;

%constraint matrix
B = [0,0,0,-2;0,1,0,0;0,0,1,0;-2,0,0,0];
%Calculate eigenvalues and functions

[V,D] = eig(M,B); %calculate eigens
X = diag(D);  %creates column array of eigenvalues
[C,IX] = sort(X); %sorts iegen values into Y, places index in IX 
Values = V(:,IX(2)); % we want eigenfunction of first positive eigenvalue (IX(2)) becuase IX(1) is neg
% Column vector Values is then [A,B,C,D] from Gao dissertaion
xc = -Values(2)/(2*Values(1));
yc = -Values(3)/(2*Values(1));
R = (xc^2+yc^2-Values(4)/Values(1))^0.5;

Circle.xc = xc;
Circle.yc = yc;
Circle.R = R;

end

