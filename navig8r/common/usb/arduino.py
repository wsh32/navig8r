from .device import Device
import os
import subprocess


class Arduino(Device):
    """
    Generic communication with an Arduino
    """
    def __init__(self, autodetect='Serial', baudrate=115200, port=None):
        super().__init__(autodetect, baudrate, port=port)

    @staticmethod
    def _check_windows():
        if os.name == 'nt':
            raise Exception("arduino-mk not supported on Windows")

    def build(self, dir, main='main.ino', makefile='makefile'):
        """
        Build Arduino program
        :param dir: Arduino src directory
        :param main: Main ino file
        :param makefile: Make settings file
        """
        self._check_windows()

        with self.read_lock:
            old_dir = os.getcwd()

            if not os.path.isdir(dir):
                raise FileNotFoundError("Directory {} not found.".format(dir))
            else:
                os.chdir(dir)

            if not os.path.isfile(makefile):
                raise FileNotFoundError("Makefile {} not found.".format(makefile))

            if not os.path.isfile(main):
                raise FileNotFoundError("Arduino main file {} not found.".format(main))

            subprocess.check_call('make', stderr=subprocess.STDOUT)

            os.chdir(old_dir)

    def upload(self, dir, board=None):
        """
        Upload a built program to the Arduino
        :param dir: Arduino src directory
        :param board: Arduino board tag. Same as in the makefile
        """
        with self.read_lock:
            old_dir = os.getcwd()

            if not os.path.isdir(dir):
                raise FileNotFoundError("Directory {} not found".format(dir))

            os.chdir(dir)

            dirs = os.listdir()

            build_dir_exists = len([name for name in dirs if 'build-' in name]) != 0

            if not build_dir_exists:
                raise FileNotFoundError("Build directory not found. Compile the arduino code first.")

            if board:
                board_check = len([name for name in dirs if 'build-{}'.format(board) in name]) != 0
                if not board_check:
                    raise Exception("Code compiled for incorrect board.")

            subprocess.check_call(['make', 'upload'], stderr=subprocess.STDOUT)

            os.chdir(old_dir)
