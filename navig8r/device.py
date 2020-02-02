from multiprocessing import Process, Queue
import serial
import time

class DeviceProcess:
    def __init__(self, serial_queue, port='/dev/ttyUSB0', baudrate=9600, send_rate_s=0.25):
        self._ser = serial.Serial(port, baudrate)
        # self._ser = FakeSerialConsole()
        self.serial_queue = serial_queue
        self.direction = 0
        self.flash_enable = 0
        self.distance = 0
        self.send_rate_s = send_rate_s
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        while True:
            if not self.serial_queue.empty():
                n_direction, n_flash_enable, n_distance = self.serial_queue.get()
                self.direction = n_direction if n_direction is not None else self.direction
                self.flash_enable = n_flash_enable if n_flash_enable is not None else self.flash_enable
                self.distance = n_distance if n_distance is not None else self.distance

            data = self.format_serial(self.direction, self.flash_enable, self.distance)
            self._ser.write(data.encode('utf-8'))

            time.sleep(self.send_rate_s)

    def format_serial(self, direction, flash_enable, distance):
        formatted = "${}{}{}\n".format(
            "L" if direction == 1 else ("R" if direction == 2 else "Z"),
            "F" if flash_enable == 1 else "Z",
            "N" if distance == 1 else ("F" if distance == 2 else "Z")
        )
        return formatted

class FakeSerialConsole:
    def __init__(self):
        pass

    def write(self, data):
        print(data)

