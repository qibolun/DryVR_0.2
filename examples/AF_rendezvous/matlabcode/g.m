function xplus = g(x)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Matlab Function  Author: Ricardo Sanfelice (Revised by BMAlladi)
%
% Project: Simulation of a hybrid system (Spacecraft R&D)
%
% Name: g.m
%
% Description: Jump map
%
% Version: 1.0
% Required files: - 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global er xd Ts NOISE1 tnoise

xsys = x(1:4);
h = x(5);
p = x(6);
qp = x(7);
Th = (atan2(x(2),x(1)));
xhat = x(8:11);
tau = x(12);
PO1 = x(13:16);
PO2 = x(17:20);
PO3 = x(21:24);
PO4 = x(25:28);
ysys = x(29:32);
Ptk = [PO1;PO2;PO3;PO4];
xhatp = xhat;
%----------------------------------%
%xhatp = xhat;
r = sqrt(x(1)^2+x(2)^2);
r3 = norm([xsys(1)-xd(1) xsys(2)-xd(2)]);
hp = h;
pp = p;

%------------Noise----------%
tn = 0; %tau;
tmp = 0; %abs(tnoise-tn);
%[row col] = min(tmp);
Ynoise = 0; %NOISE1(col);
%---------------------------%

if abs(r-700)<=.1 && p==1
    pp = 2;
else if abs(r-150)<=.1 && p==2
        pp = 3;
            else if r<= 10e-2 && p==3
                    pp =4;
                end
    end
end

%-----------Phase-II jump codition-------%

rho = 10*pi/180;

if (Th >= rho && h ==-1) || (Th <= -rho && h ==1)
    hp = -h;
end

%----------------------------------------%

% if Th >= 0+0.1745 && h==-1
%     hp = 1;
% else if Th <= 0-0.1745 && h==1
%         hp = -1;
%     end
% end


%-----------Phase-III jump codition-------%
if p==3
    if r3<=er && qp==1
    qp = 3-qp;
    end
end
%----------------------------------------%

%-------------KALMAN ESTIMATION------------%

if p==1 && tau >=Ts
    Pkm = [PO1';PO2';PO3';PO4'];
rho = [xhat(1);xhat(2)];
nrho = norm(rho);
H1 = 1/nrho *eye(2)-rho*rho'/nrho^3;
H2 = zeros(2,2);
Hkm = [H1 H2];
ys = [ysys(1)/sqrt(ysys(1)^2+ysys(2)^2); ysys(2)/sqrt(ysys(1)^2+ysys(2)^2)]+[(Ynoise); (Ynoise)];
yhat = [xhat(1)/sqrt(xhat(1)^2+xhat(2)^2); xhat(2)/sqrt(xhat(1)^2+xhat(2)^2)];   

Rk  = [((0.001))^2 0;0 ((0.001))^2];    
%     Hkm = [-xhat(2)/(xhat(1)^2+xhat(2)^2) xhat(1)/(xhat(1)^2+xhat(2)^2) 0 0];
%     Rk  = (0.001*pi/180)^2;
    Kk  = Pkm*Hkm'/(Hkm*Pkm*Hkm'+Rk);
%    ys = atan2(xsys(2),xsys(1))+Ynoise;
%    yhat = atan2(xhat(2),xhat(1));
    xhatp = xhat+Kk*(ys-yhat);
    Ptp   = (eye(4)-Kk*Hkm)*Pkm;
    Ptk = reshape(Ptp,[16,1]);
    tau = 0;
end
%--------------------------------------------------------%


xplus =[xsys;hp;pp;qp;xhatp;tau;Ptk;ysys];

end

