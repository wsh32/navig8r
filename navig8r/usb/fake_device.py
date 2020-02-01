class FakeDevice:
    """
    Serial input/output operations. Raises SerialException if errors occur
    """
    def __init__(self, autodetect, baudrate, port=None, encoding='utf-8'):
        self.encoding = encoding
        pass

    def write(self, data):
        print(data.decode(self.encoding))

    def read(self, buffer=1, timeout=None):
        return ''.join(['a' for i in range(buffer)]).encode(self.encoding)

    def read_line(self, timeout=None):
        return "Test\n".encode(self.encoding)

    def write_string(self, data):
        self.write(data.encode(self.encoding))

    def close(self):
        pass

    def open(self):
        pass

    def flush_input(self):
        pass

    def flush_output(self):
        pass

    def flush_all(self):
        pass

    def in_waiting(self):
        pass
