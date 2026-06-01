from __future__ import print_function
import time
import ftd2xx 

print(ftd2xx.listDevices())

# This scripts turns of SYNC-FIFO mode in the FT2232H USB present on the mimas boards
# Resetting chip mode may be necessary if readout script is run and get stuck for any reason

def init():
  dev = ftd2xx.openEx(b'NLAI72OTA')  # Mimas board serial (port A) is needed for opening connection
    
  time.sleep(0.1)
  dev.setTimeouts(5000, 5000)
  time.sleep(0.1)
  dev.setBitMode(0xff, 0x00)
  time.sleep(0.1)
  # dev.setBitMode(0xff, 0x40)
  # time.sleep(0.1)
  dev.setLatencyTimer(2)
  time.sleep(0.1)
  dev.setFlowControl(ftd2xx.defines.FLOW_RTS_CTS, 0, 0)
  time.sleep(0.1)
  dev.purge(ftd2xx.defines.PURGE_RX)
  time.sleep(0.1)
  dev.purge(ftd2xx.defines.PURGE_TX)
  time.sleep(0.1)
  return dev


############# OPEN AND CLOSE INSTRUMENT TO SET LOW SPEED MODE ############# 
dev = init()
print("\nDevice Details :")
print("Serial : " , dev.getDeviceInfo()['serial'])
print("Type : " , dev.getDeviceInfo()['type'])
print("ID : " , dev.getDeviceInfo()['id']) 
dev.close()     # CLOSE FILE
