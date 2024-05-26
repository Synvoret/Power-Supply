import time
from tango.server import run
from tango.server import Device
from tango.server import attribute, command


class Clock(Device):

    time = attribute()

    def read_time(self):
        return time.time()

    @command(dtype_in=str, dtype_out=str)
    def strftime(self, format):
        return time.strftime(format)


if __name__ == "__main__":
    run((Clock,))