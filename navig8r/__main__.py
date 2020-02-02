import server
import device


if __name__=='__main__':
    server = server.Server()
    device = device.DeviceProcess(server.serial_queue)
