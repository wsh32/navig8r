from universe.usb.arduino import Arduino


source_dir = '/home/wsh32/PycharmProjects/Byte/src/arduino/tests/comm'

arduino = Arduino(autodetect='')
arduino.build(source_dir)
arduino.upload(source_dir)

while True:
    cmd = input('> ')
    arduino.write(bytes([int(cmd)]))
    print(arduino.read_line())