from multiprocessing import Process, Queue
import serial
import time

class DeviceProcess:
    def __init__(self, serial_queue, port='/dev/ttyUSB0', baudrate=9600, send_rate_s=0.25):
        self.serial_queue = serial_queue
        self.ser_data = (0, 0, 0)
        self._ser = serial.Serial(port, baudrate)
        # self._ser = FakeSerialConsole()
        self.send_rate_s = send_rate_s
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        while True:
            if not self.serial_queue.empty():
                self.ser_data = self.serial_queue.get()
            data = self.format_serial(self.ser_data)
            self._ser.write(data.encode('utf-8'))

            time.sleep(self.send_rate_s)

    def format_serial(self, ser_data):
        direction, flash_enable, distance = ser_data
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

