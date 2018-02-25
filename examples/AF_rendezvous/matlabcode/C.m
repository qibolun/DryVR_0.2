function v  = C(x) 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Matlab Function  Author: Ricardo Sanfelice (Revised by BMAlladi)
%
% Project: Simulation of a hybrid system (Spacecraft R&D)
%
% Name: C.m
%
% Description: Flow set
%
% Version: 1.0
% Required files: - 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

xsys = x(1:4);
h = x(5);
p = x(6);
Th = (atan2(x(2),x(1)));
r = sqrt(xsys(1)^2+xsys(2)^2);
rho = 10*pi/180;
v=0;
% 
if (abs(r-700)>=.1 && p == 1) || (abs(r-700)<= .1 && p == 2)||(abs(r-150)>=.1 && p == 3) 
    v=1;
end

if (Th <=rho && h==-1) || (Th >=-rho && h==1)
    v = 1;
end

% if (Th<= 0+0.1745 && h==-1) || (Th >=0-0.1745 && h==1)
%     v=1;
% end
if (abs(r-10e-2)>=0) && p==4
    v = 1;
end