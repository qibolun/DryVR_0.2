function Diff = diffparaJacobian(J1,J2,V1,V2,Enable_Res,Enable_Cap)

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
Total_N = N + length(Enable_Res) + length(Enable_Cap);
Diff = zeros(Total_N,Total_N);

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


col = N+1;
for j = Enable_Res
    Diff(j,col) = abs(J1(j,col)-J2(j,col));
    %Jac(j,col) = 100;
    col = col+1;
end

for j = Enable_Cap
        g1 = g_syn./(1+exp(K*(V1'-V_eq)/V_Range)); 
        g2 = g_syn./(1+exp(K*(V2'-V_eq)/V_Range)); 
        Diff(j,col) = abs(V2(j)-V1(j))/Res(j) + g_gap*W_gap(j,:)*abs(V1'-V2')-abs(V1(j)-V2(j)) ...
            + W_syn(j,:)*(g1.*(E_syn-V2(j))-g2.*(E_syn-V1(j)));
        col = col+1;
end
