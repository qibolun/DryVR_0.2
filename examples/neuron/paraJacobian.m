function Jac = paraJacobian(V,Enable_Res,Enable_Cap,t)

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
Total_N = N + length(Enable_Res) + length(Enable_Cap);
Jac = zeros(Total_N,Total_N);
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

col = N+1;
for j = Enable_Res
    Jac(j,col) = -(V_leak-V(j))/(Res(j)^2)/Cap(j);
    %Jac(j,col) = 100;
    col = col+1;
end

for j = Enable_Cap
        I_stim = IStim(j,round(t/dt)+1);
        I_leak = (V_leak-V(j))/Res(j);
        I_gap = g_gap*W_gap(j,:)*(V'-V(j));
        g = g_syn./(1+exp(K*(V'-V_eq)/V_Range)); 
        I_syn = W_syn(j,:)*(g.*(E_syn-V(j)));
        Jac(j,col) = (I_leak+I_gap+I_syn+I_stim);
        col = col+1;
end

