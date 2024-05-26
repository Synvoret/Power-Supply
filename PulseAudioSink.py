import pulsectl
import tango
from tango.server import Device, attribute, command, device_property, run

__all__ = ["PulseAudioSink", "main"]


class PulseAudioSink(Device):
    SinkName = device_property(
        dtype=str,
        default_value='@DEFAULT_SINK@'
    )

    Volume = attribute(
        dtype=float,
        access=tango.AttrWriteType.READ_WRITE,
        min_value=0,
        max_value=1
    )

    Mute = attribute(
        dtype=bool,
        access=tango.AttrWriteType.READ_WRITE
    )

    ChannelCount = attribute(
        dtype=bool,
        access=tango.AttrWriteType.READ
    )

    def init_device(self):
        super(PulseAudioSink, self).init_device()
        self.pulse = pulsectl.Pulse(self.get_name())
        self.extended_status = ""
    
    def delete_device(self):
        self.pulse.close()
        super(PulseAudioSink, self).delete_device()
    
    def dev_status(self):
        base_status = super(PulseAudioSink, self).dev_status()
        if self.extended_status:
            return "{}\n{}".format(base_status, self.extended_status)
        else:
            return base_status
    
    def always_executed_hook(self):
        try:
            sink = self.get_sink()
        except Exception as e:
            self.set_state(tango.DevState.FAULT)
            self.extended_status = "Failed to access sink: {!r}".format(e)
        else:
            mute = bool(sink.mute)
            if mute == True:
                self.set_state(tango.DevState.DISABLE)
                self.extended_status = "The device is muted."
            else:
                self.set_state(tango.DevState.ON)
                self.extended_status = "The device is not muted."
    
    def get_sink(self):
        return self.pulse.get_sink_by_name(self.SinkName)
    
    def read_Volume(self):
        return self.pulse.volume_get_all_chans(self.get_sink())
    
    def read_ChannelCount(self):
        return self.get_sink().channel_count
    
    def write_Volume(self, value):
        self.pulse.volume_set_all_chans(self.get_sink(), value)
    
    def read_Mute(self):
        return self.get_sink().mute
    
    def write_Mute(self, value):
        self.pulse.sink_mute(self.get_sink().index, value)
    
    @attribute(dtype=str)
    def Description(self):
        return self.get_sink().description
    
    @attribute(dtype=str)
    def Name(self):
        return self.get_sink().name
    
    @attribute(dtype=str)
    def Driver(self):
        return self.get_sink().driver
    
    @command
    def Toggle(self):
        sink = self.get_sink()
        mute = bool(sink.mute)
        self.pulse.sink_mute(self.get_sink().index, not mute)
    
    def is_Toggle_allowed(self):
        return self.get_state() != tango.DevState.FAULT
    
    def is_Volume_allowed(self, attr):
        return self.get_state() != tango.DevState.FAULT
    
    def is_Mute_allowed(self, attr):
        return self.read_Volume() > 0.5
    
    def is_Description_allowed(self, attr):
        return self.get_state() != tango.DevState.FAULT
    
    def is_ChannelCount_allowed(self, attr):
        return self.get_state() != tango.DevState.FAULT
    
    def is_Name_allowed(self, attr):
        return self.get_state() != tango.DevState.FAULT
    
    def is_Driver_allowed(self, attr):
        return self.get_state() != tango.DevState.FAULT


def main():
    run((PulseAudioSink, ))


if __name__ == '__main__':
    main()
