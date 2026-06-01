from __future__ import print_function
import time
import ftd2xx 
import math

##################### Set up connection to FTDI chip on ADC ###################
def init():   
    dev = ftd2xx.openEx(b'NLAI72OTA')   # Mimas board serial (port A) is needed for opening connection
  
    dev.setTimeouts(5000, 5000)   #   dev.setTimeouts(5000, 5000) 
    dev.setBitMode(0xff, 0x00)
    dev.setBitMode(0xff, 0x40)
    # dev.setUSBParameters(0x10000, 0x10000)
    dev.setLatencyTimer(2)    #  dev.setLatencyTimer(2)
    dev.setFlowControl(ftd2xx.defines.FLOW_RTS_CTS, 0, 0)
    dev.purge(ftd2xx.defines.PURGE_RX|ftd2xx.defines.PURGE_TX)      
    return dev

##################### Setting up number of read requests #####################
Fs=50000; # [Hz] Sampling frequency (not set here, must know from instrument FW)
recTime=5; #[s]  - Specify here recording time in seconds

nSamples=Fs*recTime # Total number of data frame that will be read
dataFrameSize=102           # Each data frame is 102 bytes
nFramesSingleRead=5000      # Read chunks of 5000 dataFrames i.e. a "BLOCK"
BLOCK_LEN =  dataFrameSize*nFramesSingleRead  # Read this many bytes in single block read
REPEATS = math.ceil(nSamples/nFramesSingleRead) # Number of block reads

############# MAIN - OPEN INSTRUMENT AND FILE AND START RECORDING ############# 

deviceList=ftd2xx.listDevices()
print(deviceList)
dev = init()    
print("\nDevice Details :")
print(dev.getDeviceInfo())

start_time = time.time()

# Main recording loop
newFile = open("data.txt", "wb")

dev.write(bytes([0x55]))  # INSTRUMENT START CMD
for x in range(REPEATS):  #Read from ADC and write to file in chunks 
    rx_data = dev.read(BLOCK_LEN)  # COMMAND WHICH GIVES ISSUE!!
    newFile.write(rx_data)    
    if (x%10==0):
        print("%2.2f %% done" % round(x/REPEATS*100))  # Useful for long reads
dev.write(bytes([0x33]))  # INSTRUMENT STOP CMD

# Close instrument and file
newFile.close()
dev.setBitMode(0xff, 0x00) #Go back to non-sync mode for easier reprogramming
dev.close()

# Elapsed time
print("Elapsed time: %5.2f seconds" % (time.time() - start_time))


