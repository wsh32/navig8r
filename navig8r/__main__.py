import server
import device


if __name__=='__main__':
    server = server.Server()
    try:
        device = device.DeviceProcess(server.serial_queue, port='/dev/ttyUSB0')
    except FileNotFoundError:
        device = device.DeviceProcess(server.serial_queue, port='/dev/ttyUSB1')
