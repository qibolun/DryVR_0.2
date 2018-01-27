function Diff = diffJacobian(J1,J2,V1,V2)

% Declare global variable
global W_gap;
global W_syn;
global Cap;
global E_syn;
global Res;
global V_eq;
% Parameter
% Leakage voltage
V_leak = -0.035;
% Gap-junction parameter
g_gap = 5e-9;
%Synaptic Parameters
g_syn = 6e-10; 
V_Range = 0.035;
K=-4.3944;

%Calculating the difference of the two Jacobian matrix
N = length(V1);
Diff = zeros(size(J1));
for i = 1:N
    for j = 1:N
        if j==i
            Diff(i,j) = abs(J1(i,j)-J2(i,j));
        else
            deno_min = min(exp(K*(V1(j)-V_eq(j))/V_Range),exp(K*(V2(j)-V_eq(j))/V_Range));
            deno_max = max(exp(K*(V1(j)-V_eq(j))/V_Range),exp(K*(V2(j)-V_eq(j))/V_Range));
            Diff(i,j) = g_syn * W_syn(i,j) * (E_syn(j)-min(V1(i),V2(i)))/Cap(i)...
                *((exp(K*(V2(j)-V_eq(j))/V_Range)*K/V_Range)/(1+deno_min)^2)...
                -g_syn * W_syn(i,j) * (E_syn(j)-max(V1(i),V2(i)))/Cap(i)...
                *((exp(K*(V2(j)-V_eq(j))/V_Range)*K/V_Range)/(1+deno_max)^2);
        end
    end
end

