#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""Demo power supply tango device server."""

import time
import datetime
import numpy
from time import sleep

from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState
from PyTango.server import Device, attribute, command, pipe, device_property


class PowerSupply(Device):

    voltage = attribute(
        label='Voltage',
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ_WRITE,
        unit="V",
        format="8.0f",
        min_value=0.0,
        max_value=30.0,
        fget="get_voltage",
        fset="set_voltage",
        doc="the power supply voltage",
    )

    current = attribute(
        label="Current",
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ_WRITE,
        unit="A",
        format="8.0f",
        min_value=0.0,
        max_value=16.0,
        max_alarm=15.5,
        max_warning=15.0,
        fget="get_current",
        fset="set_current",
        doc="the power supply current",
    )

    power = attribute(
        label="Power",
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ,
        unit="W",
        format="8.0f",
        doc="the power generation from power supply"
    )

    noise = attribute(
        label="Noise",
        dtype=((int, ), ),
        max_dim_x=1024,
        max_dim_y=1024,
    )

    time = attribute(
        label="Time",
        dtype=float,
        display_level=DispLevel.OPERATOR,
        access=AttrWriteType.READ
    )

    info = pipe(label="Info")

    host = device_property(dtype=str)
    port = device_property(dtype=int, default_value=9788)

    def init_device(self):
        Device.init_device(self)
        self.__current = 0.0
        self.__voltage = 0.0
        self.set_state(DevState.STANDBY)
    
    def read_voltage(self):
        self.info_stream("read_voltage(%s, %d)", self.host, self.port)
        return str(self.get_voltage()), time.time(), AttrQuality.ATTR_WARNING

    def read_current(self, attr):
        # attr.set_valve(self.__current, 1)
        return str(self.get_current())

    def read_power(self):
        return round(self.get_voltage() * self.get_current(), 2)

    def get_voltage(self):
        return round(self.__voltage, 2)

    def set_voltage(self, voltage):
        # if self.set_state(DevState.ON):
        if self.check_state():
            self.__voltage = voltage

    def get_current(self):
        return round(self.__current, 2)
    
    def set_current(self, current):
        # should set power supply current
        if current > self.current:
            self.set_state(DevState.ALARM)
        else:
            if self.check_state():
                self.__current = current
    
    def read_info(self):
        return "Information", dict(
            manufacturer="Tango", model="PS2000", version_number=123
        )
    
    def read_time(self):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H.%M")
        return float(formatted_time)

    @DebugIt()
    def read_noise(self):
        return numpy.random.random_integers(1000, size=(100, 100))
    
    @command
    def TurnOn(self):
        # turn on the actual power supply here
        self.set_state(DevState.ON)
    
    @command
    def TurnOff(self):
        # turn off the actual power supply here
        self.set_state(DevState.OFF)
    
    @command(
        dtype_in=float,
        doc_in="Ramp target current",
        dtype_out=bool,
        doc_out="True if ramping went well, False otherwise",
    )
    def Ramp(self, target_current):
        # should do the ramping

        # ramp step
        ramp_step = 1

        # get actual current value
        initial_current = self.get_current()

        # determining direction of ramp (up or down)
        if target_current > initial_current:
            step = ramp_step
        else:
            step = -ramp_step
        
        # ramp loop
        while abs(self.get_current() - target_current) >= 0.01:
            new_current = self.get_current() + step
            self.set_current(new_current)
        
        return True
    
    def set_values(self):
        pass

    def check_state(self):
        state = str(self.get_state())
        if state == "STANDBY" or state == "OFF":
            return False
        return True


if __name__ == "__main__":
    PowerSupply.run_server()
