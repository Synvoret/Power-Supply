import sys
import time
from PyTango import AttrWriteType, DevState, DispLevel, DeviceProxy, DevBoolean, DevEncoded, DevString
from PyTango.server import Device, attribute, command, run


class Camera(Device):

    def init_device(self):
        Device.init_device(self)
        self.image_width = 640
        self.image_height = 480
        self.image_data = b''
    
    @attribute(dtype=DevString)
    def CameraModel(self):
        return "Sample Camera Model"
    
    @attribute(dtype=DevBoolean)
    def Acquisition(self):
        return False
    
    @command(dtype_out=DevEncoded)
    def AcquireImage(self):
        time.sleep(1)
        self.image_data = b'SampleImageData'
        return self.image_data
    

if __name__ == '__main__':
    run([Camera])