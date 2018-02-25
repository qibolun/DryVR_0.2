function v  = D(x) 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Matlab Function  Author: Ricardo Sanfelice (Revised by BMAlladi)
%
% Project: Simulation of a hybrid system (Spacecraft R&D)
%
% Name: D.m
%
% Description: Jump set
%
% Version: 1.0
% Required files: - 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global er xd Ts

xsys = x(1:4);
h = x(5);
p = x(6);
q = x(7);
tau = x(12);
Th = (atan2(x(2),x(1)));
r = sqrt(x(1)^2+x(2)^2);
r3 = norm([xsys(1)-xd(1) xsys(2)-xd(2)]);
rho = 10*pi/180;

v=0;

if (abs(r-700)<=.1 && p==1) || (abs(r-150)<=.1 && p==2) 
     v=1;
 end

% if (Th >=(0+0.1745) && h==-1) || (Th <= 0-0.1745 && h==1)
%     v=1;
% end

if (Th >= rho && h ==-1) || (Th <= -rho && h ==1)
    v=1;
end

 if p ==3 && (q ==1 && r3 <er)
         v =1;
 end
if p ==3 && r<= 1e-2
    v = 1;
end
if p==1 && tau > Ts
    v=1;
end



    