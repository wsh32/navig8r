import serial

import time

if __name__=='__main__':
    s = serial.Serial('/dev/ttyUSB0')
    while True:
        s.write('$LFN\n'.encode('utf-8'))
        print('hi')
        time.sleep(1)

