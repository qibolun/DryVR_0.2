function Simulation = HyRendezvous_Simulate(~,initCond,simTime)
    % Single mode, so disregard input arg 'mode'
    % Expecting 'initCond' to be a [x0,y0,vx0,vy0]; edit if time is
    % included
    % simTime is originally 20000 in Ricardo's example

    %Simulate the system
%%%%%%%%%%%%%% COPIED FROM run_switch.m %%%%%%%%%%%%%%
global K1 K3 er xd K4 Ts NOISE1 tnoise NOISE2p NOISE3p NOISEP
    er = 1;
    xd = [-25;0];
    Ts = 10;

    %-----------------NOISE-----------%
    N= 0; %150000;
    Fs = 0; % 1000;
    tnoise = 0; % (0:N-1)/Fs;
    sigma = 0; % 1;
    NOISE1 =0; % (0.001)*sigma*randn(size(tnoise));
    NOISE2p =0; % (10)*sigma*randn(size(tnoise));
    NOISE3p =0; % (1/100)*sigma*randn(size(tnoise));
    NOISEP =0; % (10^-4)*sigma*randn(size(t4noise));
    %---------------------------------------
    mu = 3.98600444*10^14; ro = 7100*1000;
    n = sqrt(mu/ro^3); 
    A = [0     0    1 0;
         0     0    0 1;
         3*n^2 0    0 2*n;
         0     0 -2*n 0];
    m = 0.5*1000;  
    B = [0  0; 0  0; 1/m  0;0  1/m];
    m2 = 2500;  
    B2 = [0  0; 0  0; 1/m2  0;0  1/m2];
    %-----------------------% Phase-I
    Q1 = 1.5e-1*eye(4);
    R1 = 18e5*eye(2); 
    [K1,~,~] = lqr(A,B,Q1,R1);
    %-------------------------- Estimation
    po = [1*10^5 0 0 0;
          0 1*10^5 0 0;
          0 0 1*10^1 0;
          0 0 0 1*10^1];

    poi = reshape(po,[1,16]);
    %-----------------------------% Phase - III
    Q3 = 38.4*eye(4);
    R3 = 9.7e3*eye(2);
    [K3,~,~] = lqr(A,B,Q3,R3);
    %---------------------------% Phase -IV
      Q4 = 6e-1*eye(4);
      R4 = 11e4*eye(2);
    [K4,~,~] = lqr(A,B2,Q4,R4);
    %-------------------------
    hint = -1;
    pint = 1;
    qint = 1;
    xhati = initCond + [1000 1000 0 0];
    tau = 0;
    yint = initCond;
    xint = [initCond hint pint qint xhati tau poi yint]; 
    
    % Initialize the augmented "state" vector
    x0 = xint;

    % simulation horizon
    T = [0,simTime];                                                                
    J = [0 10000];

    % rule for jumps
    % rule = 1 -> priority for jumps
    % rule = 2 -> priority for flows
    rule = 1;

    %options = odeset('RelTol',1e-6,'MaxStep',100, 'InitialStep', 10);
    options = odeset('RelTol',1e-6,'MaxStep',.1);

    % simulate
    [t,~,x] = HyEQsolver( @f,@g,@C,@D,x0',T,J,rule,options);

    %size(x)
    %x(1:5,1)
    
    % Return simulated trajectory
    Simulation = [t,x(:,1),x(:,2),x(:,3),x(:,4)];

    %{
    sim_copy = Simulation;
    i = 1;
    compact_factor = 100;
    rows = size(sim_copy, 1);
    new_sim = zeros(0,5);
    while i < rows
        new_sim = [new_sim; sim_copy(i,:)];
        i = i + compact_factor;
    end
    Simulation = new_sim;
    %}
    
end
