from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process, Queue, Event

class Server:
    def __init__(self):
        self.serial_queue = Queue()
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        self.http_server = HTTPServer(('0.0.0.0', 8000), make_nav_handler(self.serial_queue))
        self.http_server.serve_forever()


def make_nav_handler(serial_queue):
    class NavRequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.queue = serial_queue
            super(NavRequestHandler, self).__init__(*args, **kwargs)
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            processed = self.process_path(self.path)
            if processed:
                self.queue.put(processed)
        def process_path(self, path):
            path_data = path.split('/')
            if len(path_data) != 4:
                return None
            try:
                direction = int(path_data[1])
            except ValueError:
                direction = None
            try:
                flash_enable = int(path_data[2])
            except ValueError:
                flash_enable = None
            try:
                distance = int(path_data[3])
            except ValueError:
                distance = None
            if direction or flash_enable or distance:
                return (direction, flash_enable, distance)
            else:
                return None
    return NavRequestHandler


if __name__=='__main__':
    s = Server()

