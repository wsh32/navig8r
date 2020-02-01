from common.usb.device import Device

import time

if __name__=='__main__':
    d = Device(autodetect='', baudrate=9600, encoding='utf-8')

    while True:
        d.write('test')
        print(d.read_line(timeout=1))
