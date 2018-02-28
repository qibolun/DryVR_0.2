function xdot = f(x)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Matlab Function  Author: Ricardo Sanfelice (Revised by BMAlladi)
%
% Project: Simulation of a hybrid system (Spacecraft R&D)
%
% Name: f.m
%
% Description: Flow map
%
% Version: 1.0
% Required files: - 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global K1 K3 K4 NOISE2p NOISE3p NOISE1 tnoise NOISEP

xsys = x(1:4);
h = x(5);
p = x(6);
q = x(7);
xhat = x(8:11);
tau = x(12);
PO1 = x(13:16);
PO2 = x(17:20);
PO3 = x(21:24);
PO4 = x(25:28);
ysys = x(29:32);
xhatdot = xhat;
ydot = ysys;
POdot = [PO1;PO2;PO3;PO4];

% sqrt(x(1)^2+x(2)^2)



%--------------System dynamics------------%
mu = 3.98600444*10^14; ro = 7100*1000; rdy = sqrt((ro+ysys(1))^2+ysys(2)^2);
n = sqrt(mu/ro^3);
A = [0     0    1 0;
     0     0    0 1;
     3*n^2 0    0 2*n;
     0     0 -2*n 0];
m = 1*500;  
B = [0  0; 0  0; 1/m  0;0  1/m];
m2 = 2500;  
B2 = [0  0; 0  0; 1/m2  0;0  1/m2];


%-------------------PHASE I-----------------------%
if p==1
    %------------Noise----------%
    tn = 0; %tau;
    tmp = 0; %abs(tnoise-tn);
    %[row col] = min(tmp);
    pnoise = 0; %NOISEP(col);  % process noise
    %------------Noise----------%
    up = -B*K1*(xhat);
    inp = up;
    if norm(inp) > 0.02
        inp = 0.02* (inp/norm(inp));
    end
    SOM =  (mu/ro^4)*[0;0;-3*x(1)^2+(3/2*x(2)^2);3*x(1)*x(2)];
    SOMhat =  (mu/ro^4)*[0;0;-3*xhat(1)^2+(3/2*xhat(2)^2);3*xhat(1)*xhat(2)];
    FNL =  [0;0;-2*n^2*ysys(1)+(mu/ro^2)-((mu/rdy^3)*(ro+ysys(1)));n^2*ysys(2)-(mu/rdy^3)*ysys(2)];
    Ad = (mu/ro^4)*[0 0 0 0;0 0 0 0;-6*xhat(1) 3*xhat(2) 0 0;3*xhat(2) 3*xhat(1) 0 0];
    Ft = [0 0 1 0;0 0 0 1;3*n^2 0 0 2*n;0 0 -2*n 0]+Ad;
    Pt = [PO1';PO2';PO3';PO4'];
    Ptdot = Ft*Pt+Pt*Ft'+10^-8*[0 0 0 0;0 0 0 0;0 0 1 0;0 0 0 1];
    POdot = reshape(Ptdot,[16,1]);

    xsysdot = A*xsys+inp+SOM+[0 0 pnoise pnoise]';
    xhatdot = A*xhat+inp+SOMhat;
    ydot = A*ysys+FNL+inp;
%-------------------PHASE II-----------------------%    
else if p==2
%------------Noise----------%
tn = 0; %tau;
tmp = 0; %abs(tnoise-tn);
%[row col] = min(tmp);
anoise = 0; %NOISE1(col)*0.05;  % 5% of measurement noise
rnoise1 = 0; %NOISE2p(col)*0.05; % 5% of measurement noise
rnoisev = 0; %NOISE2p(col)*0.0001;
pnoise = 0; %NOISEP(col);  % process noise
%------------------------------------% 
% position error %                
xi(1) = xsys(1)+rnoise1;
xi(2) = xsys(2)+rnoise1;
xi(3) = xsys(3)+0.05*rnoisev;  % 5% of 0.001 m/s
xi(4) = xsys(4)+0.05*rnoisev;  % 5% of 0.001 m/s
% angle error %
Th = (atan2(xsys(2),xsys(1)))+anoise;
%-------------- CONTROLLER Phase-II -------------%
r = sqrt(xi(1)^2+xi(2)^2);
w =n;
an = 179;

%k1 = 80; k2 = .1;k3 = 25; k4 = .05;
%k1 = 33; k2 = .1;k3 = 25; k4 = .09;
%--------------New noise in the phase2 sim--------------%
k1 = 30; k2 = .1;k3 = 25; k4 = 0.059;
    %-------desired angle-----%
    Ths = h*an*2*pi/360;
    %-------------------------%
vth = (-xi(3)*sin(Th)+xi(4)*cos(Th)); %Theta original
Thd = vth/r;

cosThe = cos(Th)*cos(Ths) - sin(Th)*sin(Ths);
sinThe = sin(Th)*cos(Ths) - cos(Th)*sin(Ths);

Te = atan2(sinThe,cosThe);

vr = (xi(3)*cos(Th)+xi(4)*sin(Th));  %Rho Original
rd = vr;
ur = -k1*(rd-0)-k2*(r-145);
wr = -((3*w^2*xi(1))+xi(4)*(2*w+Thd))*cos(Th)+xi(3)*(2*w+Thd)*sin(Th);  % omegar original
ar = ur+wr;
% ut = -r*(k3*(Thd-0)+k4*(Th-Ths));
ut = -r*(k3*(Thd-0)+k4*(Te));
wt = ((3*w^2*xi(1))+xi(4)*(2*w+Thd))*sin(Th)+xi(3)*(2*w+Thd)*cos(Th)+vr*Thd;   %omegatheta original
at = ut+wt;
inp = B*[cos(Th) -sin(Th);sin(Th) cos(Th)]*m*[ar;at];    % original input
if norm(inp) > 0.02
    inp = 0.02* (inp/norm(inp));
end
xsysdot = A*xsys+inp+[0 0 pnoise pnoise]'; 

%-------------------PHASE III-----------------------% 
    else if p==3
            %------------Noise----------%
            tn = 0; %tau;
            tmp = 0; %abs(tnoise-tn);
            %[row col] = min(tmp);
            rnoise2 = 0; %NOISE3p(col)*0.05;
            pnoise = 0; %NOISEP(col);  % process noise
            rnoisev = 0; %NOISE2p(col)*0.0001;
            %------------------------------------%                
            xi(1) = xsys(1)+rnoise2;
            xi(2) = xsys(2)+rnoise2;
            xi(3) = xsys(3)+0.05*rnoisev;
            xi(4) = xsys(4)+0.05*rnoisev;
            xi = [xi(1) xi(2) xi(3) xi(4)]';
            %-------------------------------------%
            if q == 1
                up = -B*K3*(xi-[-25 0 0 0]');
                inp = up;
                            else if q == 2
                                    k_1 = -0.0007;k_2 = -0.15;k_3 = -0.006;k_4 = -0.22;
                                    ax = 3*n^2*xi(1)+k_1*xi(1) +k_2*(xi(3)-0);
                                    ay = k_3*xi(2) +k_4*xi(4);
                                    inp = [0 0 ax ay]';
                                end
            end
            xsysdot = A*xsys+inp+10^-2*[0 0 pnoise pnoise]';
            
%-------------------PHASE IV-----------------------% 

                    else if p ==4
                            %------------Noise----------%
                            tn = 0; %tau;
                            tmp = 0; %abs(tnoise-tn);
                            %[row col] = min(tmp);
                            rnoise4 = 0; %NOISE2p(col)*0.05;
                            pnoise = 0; %NOISEP(col);  % process noise
                            rnoisev = 0; %NOISE2p(col)*0.0001;
                            %------------------------------------%
                            xi(1) = xsys(1)+rnoise4;
                            xi(2) = xsys(2)+rnoise4;
                            xi(3) = xsys(3)+0.05*rnoisev;
                            xi(4) = xsys(4)+0.05*rnoisev;
                            xi = [xi(1) xi(2) xi(3) xi(4)]';
                            %-------------------------------------%
                            up = -B2*K4*(xi-[0;20000;0;0]);
                            inp = up;
            
                        end
                        xsysdot = A*xsys+inp+[0 0 pnoise pnoise]';
        end
    end
end

%xsysdot = A*xsys+inp;
xdot = [xsysdot;0;0;0;xhatdot;1;POdot;ydot];

