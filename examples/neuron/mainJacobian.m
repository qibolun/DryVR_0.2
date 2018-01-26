function Jac = mainJacobian(V)

% Declare global variable
global IStim;
global W_gap;
global W_syn;
global Cap;
global E_syn;
global Res;
global V_eq;
global dt;
% Parameter
% Leakage voltage
V_leak = -0.035;
% Gap-junction parameter
g_gap = 5e-9;
%Synaptic Parameters
g_syn = 6e-10; 
V_Range = 0.035;
K=-4.3944;

N = length(V);
Jac = zeros(N,N);
for i = 1:N
    for j = 1:N
        if j==i
            dI_leakdVi = -1/Res(i);
            dI_gapdVi = g_gap*W_gap(i,i)-g_gap*W_gap(i,:)*ones(N,1);
            g = g_syn./(1+exp(K*(V'-V_eq)/V_Range)); 
            dI_syndVi = -W_syn(i,:)*g;
            Jac(i,j) = (dI_leakdVi+dI_gapdVi+dI_syndVi)/Cap(i);
        else
            dI_gapdVj = g_gap * W_gap(i,j);
            dI_syndVj = g_syn * W_syn(i,j) * (E_syn(j)-V(i)) * ...
            -(exp(K*(V(j)-V_eq(j))/V_Range)*K/V_Range)...
            /((1+exp(K*(V(j)-V_eq(j))/V_Range))^2);
            Jac(i,j) = (dI_gapdVj +dI_syndVj)/Cap(i);
        end
    end
end

