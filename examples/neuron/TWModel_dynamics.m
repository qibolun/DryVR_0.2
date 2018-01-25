function [Vprime] = TWModel_dynamics(t, V)

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

for i=1:length(V)
        % External/stimulus current
        I_stim = IStim(i,round(t/dt)+1);
        % Leak current
        I_leak = (V_leak-V(i))/Res(i);
        % Gap junction current
        I_gap = g_gap*W_gap(i,:)*(V-V(i));
        % Synaptic current
        g = g_syn./(1+exp(K*(V-V_eq)/V_Range)); 
        I_syn = W_syn(i,:)*(g.*(E_syn-V(i)));
        % f function
        Vprime(i,1) = (I_leak+I_gap+I_syn+I_stim)/Cap(i);  
end