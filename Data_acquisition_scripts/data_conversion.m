
clc;
close all;
clear all;

filename=['data.txt'];

%% Indicate here the sampling rate and voltage/level ADC gain
Fs=50e3;
gain=(0.625/2^23);

% Do not modify
frameSize=102; % Each data frame is 102 bytes
fileSize = dir(filename).bytes;

%% Find start of first data frame

fileID = fopen(filename); % ID=3 or higher, open succeeded
[byteData,~]=fread(fileID, 52*102, '*uint8');
fclose(fileID);     % Returns 0 if close succeeded

if (byteData(1)==uint8(85) && byteData(2)==uint8(170) && byteData(101)==uint8(51) && byteData(102)==uint8(204) )
    idxStart=1;
else
    idx=[ 51 204 85 170];   %New firmware
    idxStart=strfind(byteData',idx);
    idxStart=idxStart(1)+2;
end

%% Read file through memorymap and reshape intro array of frames

tic

%%%% Need to develop version for large files which reads in chunks
m = memmapfile(filename,'Format','uint8','Writable',false,'Offset',idxStart(end)-1);
numFrames=floor(length(m.Data)/frameSize);

x=reshape(m.Data(1:numFrames*frameSize),102,numFrames)'; 
clear m;

%% Perform check on Flags and CRC

if (all(x(:,1)==uint8(85)) || all(x(:,2)==uint8(170)) || all(x(:,101)==uint8(51)) || all(x(:,102)==uint8(204)))
    disp('Flags ok');
end

% Remove flags
x=x(:,3:end-2);

% CRC test

load('crctable.mat');

data_size = size(x, 2);

crc=uint8(zeros(numFrames,1));

for iFrame=1:numFrames

    tempcrc = uint8(0x00);
    for iByte = 1:data_size
        tempcrc = bitxor(tempcrc,x(iFrame,iByte));
        tempcrc = crctable(double(tempcrc)+1);
    end
    crc(iFrame)=tempcrc;

end

if all(crc==0)
    disp('CRC ok');
end

x=x(:,1:end-1);

%% Convert to real data 
 
data=int32(zeros(numFrames,32));
trigs=uint8(zeros(numFrames,8));

%%%%%%%%%%%%%%%%%%%%%%%% Get byte with trigger data %%%%%%%%%%%%%%%%%%%%%%%
mask = 0b00000001;
tempTrig=x(:,97);                           
for iBit=0:7
    trigs(:,iBit+1)=bitshift(bitand(tempTrig, bitshift(mask,iBit)),-iBit);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%% Get actual ADC data %%%%%%%%%%%%%%%%%%%%%%%%%%%
x=x(:,1:96);

for iCh=1:32
    
    iCh

    idxCh=[1 2 3]+(iCh-1)*3;
    binval=[dec2bin(x(:,idxCh(1)),8) dec2bin(x(:,idxCh(2)),8) dec2bin(x(:,idxCh(3)),8)];
    binval= [repmat(binval(:,1),1,8) binval ];
    data(:,iCh)=typecast(uint32(bin2dec(binval)),'int32');
end

toc

clear x m binval byteData tempTrig

%% Save data

data=double(data);
save(filename(1:end-4),'filename', 'data', 'Fs',  'trigs', 'gain','-v7.3');










