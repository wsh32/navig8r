from serial import Serial, SerialException
from serial.tools import list_ports
from threading import Lock


class Device:
    """
    Serial input/output operations. Raises SerialException if errors occur
    """
    def __init__(self, autodetect, baudrate, port=None, encoding='utf-8'):
        self.read_lock = Lock()
        self.write_lock = Lock()
        self._ser = Serial()
        self._ser.baudrate = baudrate
        self.encoding = encoding
        if not port:
            ports = list(list_ports.grep(r'.*{}.*'.format(autodetect)))
            if len(ports) == 0:
                raise SerialException('Could not locate USB device with name {}. Devices connected: {}'
                                      .format(autodetect, list_ports.comports()))
            self._ser.port = list(ports[0])[0]
        else:
            self._ser.port = port

        self._ser.open()

    def write(self, data):
        """
        Write data to the serial bus
        Serial ports are full duplex, so reading/writing can happen at the same time (thus, a different lock is used)
        :param data: The data to be written
        """
        with self.write_lock:
            self._ser.write(data)

    def read(self, buffer=1, timeout=None):
        """
        Read a series of bytes from the serial bus
        :param buffer: The number of bytes to be read
        :param timeout: The amount of time to wait before a timeout exception occurs
        :return: The packet of bytes
        """
        with self.read_lock:
            self._ser.timeout = timeout
            response = self._ser.read(buffer)
            return response

    def read_line(self, timeout=None):
        """
        Read bytes up to the newline character
        :param timeout: The amount of time to wait before a timeout exception occurs
        :return: The packet of bytes
        """
        with self.read_lock:
            self._ser.timeout = timeout
            response = self._ser.readline()
            return response

    def write_string(self, data):
        self.write(data.encode(self.encoding))

    def close(self):
        self._ser.close()

    def open(self):
        self._ser.open()

    def flush_input(self):
        self._ser.flushInput()

    def flush_output(self):
        self._ser.flushOutput()

    def flush_all(self):
        self._ser.flush()

    def in_waiting(self):
        return self._ser.in_waiting()
