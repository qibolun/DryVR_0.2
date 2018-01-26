function [AVA_ID, AVB_ID] = newNeuronID(knockedOut)
% Determine ID of AVA and AVB (may change for knockout)
AVA_ID = 5; AVB_ID = 7;
if knockedOut == 0
    return;
end
for i=1:length(knockedOut)
    
    if knockedOut(i) < 5
        AVA_ID = AVA_ID -1;
    end
    if knockedOut(i) < 7
        AVB_ID = AVB_ID - 1;
    end
end