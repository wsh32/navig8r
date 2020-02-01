from universe.usb.arduino import Arduino


source_dir = '/home/wsh32/PycharmProjects/Byte/src/arduino/tests/imu'

arduino = Arduino(autodetect='')
arduino.build(source_dir)
arduino.upload(source_dir)

while True:
    print(arduino.read_line(timeout=2).decode().strip('\r\n'))
