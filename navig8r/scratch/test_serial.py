from usb.device import Device

import time

if __name__=='__main__':
    d = Device(autodetect="", port='/dev/ttyUSB0', baudrate=9600, encoding='utf-8')

    print(d._ser)

    left = True
    right = False
    enable_flash = True
    distance = 1

    send_bytes = "$" + ("L" if left else ("R" if right else "Z")) + ("F" if enable_flash else "Z") + ("N" if distance==1 else ("A" if distance==2 else "Z")) + "\n"

    d.write(send_bytes.encode())
    print(send_bytes)

    while True:
        pass

