
% Computes look-up table for faster 8bit CRC verification
% Do not need to run this if file crctable.mat has already been created

crctable=uint8(zeros(256,1));

for dividend=0:255

    currByte = uint8(dividend);

     for bit=0:7
        if (currByte>127)
            currByte=bitxor(bitshift(currByte,1),0x07);
        else
            currByte=bitshift(currByte,1);
        end
     end

    crctable(dividend+1) = currByte;
    
end