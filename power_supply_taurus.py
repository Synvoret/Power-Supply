import sys
from PyTango import DeviceProxy

from taurus.qt.qtgui.container import TaurusWidget
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel, TaurusLCD, TaurusLed
from taurus.external.qt import QtGui, QtCore
from taurus.external.qt.QtGui import (
    QPushButton,
    QSizePolicy,
    QWidget,
    QSpacerItem,
    QDial,
    )


class MyWidget(TaurusWidget):

    def __init__(self, parent=None, args=None):
        super(MyWidget, self).__init__(parent, args)
        try:
            self.device = DeviceProxy("test/power_supply/1")
        except:
            print("Error!!")
        
        # self.resize(400, 400)
        self.setup_ui()
    
    def setup_ui(self):
        # screen = QtGui.QDesktopWidget().screenGeometry()
        # size = self.geometry
        # self.move(
        #     (screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2
        # )
        self.grid_widget = QWidget()

        layout = QtGui.QGridLayout(self.grid_widget)
        self.setLayout(layout)
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)       

        # LCDs
        size_lcd = 100, 35
        self.voltage_LCD = TaurusLCD()
        # self.voltage_LCD.setMaximumSize(size_lcd[0], size_lcd[1])
        self.voltage_LCD.setModel("test/power_supply/1/voltage")
        # self.voltage_LCD.setMaximumSize(QtCore.QSize(50, 30))
        self.voltage = self.device.voltage
        self.voltage_LCD.setProperty("value", self.voltage)
        self.current_LCD = TaurusLCD()
        # self.current_LCD.setMaximumSize(size_lcd[0], size_lcd[1])
        self.current_LCD.setModel("test/power_supply/1/current")
        current = self.device.current
        self.current_LCD.setProperty("value", current)
        self.power_LCD = TaurusLCD()
        # power_LCD.setMaximumSize(size_lcd[0], size_lcd[1])
        self.power_LCD.setModel("test/power_supply/1/power")
        power = self.device.power
        self.power_LCD.setProperty("value", power)

        
        # LABELs
        font = QtGui.QFont()
        font.setPointSize(16)
        # sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        size_unit = 20
        self.title_label = TaurusLabel("Power Supply - PS500")
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        voltage_unit = self.device.get_attribute_config("voltage")
        self.voltage_unit_label = TaurusLabel(voltage_unit.unit)
        self.voltage_unit_label.setFont(font)
        self.voltage_unit_label.setFixedWidth(size_unit)
        self.voltage_unit_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.voltage_unit_label.setSizePolicy(sizePolicy)
        # self.voltage_unit_label.adjustSize()
        current_unit = self.device.get_attribute_config("current")
        self.current_unit_label = TaurusLabel(current_unit.unit)
        self.current_unit_label.setFixedWidth(size_unit)
        self.current_unit_label.setFont(font)
        power_unit = self.device.get_attribute_config("power")
        self.power_unit_label = TaurusLabel(power_unit.unit)
        self.power_unit_label.setFixedWidth(size_unit)
        self.power_unit_label.setFont(font)

        # DIALs
        max_size_dial = 75, 75
        self.voltage_dial = QDial()
        self.voltage_dial.setMaximumSize(max_size_dial[0], max_size_dial[1])
        self.voltage_dial.setEnabled(True)
        self.voltage_dial.setAutoFillBackground(False)
        self.voltage_dial.setMinimum(0.0)
        self.voltage_dial.setMaximum(30.0)
        self.voltage_dial.setSingleStep(1)
        self.voltage_dial.setWrapping(False)
        self.voltage_dial.setNotchesVisible(True)
        self.voltage_dial.setObjectName("voltage_dial")
        actual_voltage = self.device.voltage
        self.voltage_dial.setValue(actual_voltage)
        self.voltage_dial.valueChanged.connect(self.voltage_change)
        self.current_dial = QDial()
        self.current_dial.setMaximumSize(max_size_dial[0], max_size_dial[1])
        self.current_dial.setEnabled(True)
        self.current_dial.setAutoFillBackground(False)
        self.current_dial.setMinimum(0.0)
        self.current_dial.setMaximum(16.0)
        self.current_dial.setSingleStep(1)
        self.current_dial.setWrapping(False)
        self.current_dial.setNotchesVisible(True)
        self.current_dial.setObjectName("current_dial")
        actual_current = self.device.current
        self.current_dial.setValue(actual_current)
        self.current_dial.valueChanged.connect(self.current_change)

        # MAIN PANEL
        self.device_state = TaurusLed()
        # self.device_state.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
        self.device_state.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.device_state.setAlignment(QtCore.Qt.AlignCenter)
        self.device_state_actual()
        self.on_off_button = QPushButton(text="Power On/Off")
        self.on_off_button.clicked.connect(self.on_off_device)

        # layout.addItem(spacer_item, 0, 1, 1, 1)
        # layout.addItem(spacer_item, 0, 2, 1, 1)
        layout.addWidget(self.title_label, 1, 1, 1, 3)
        # layout.addItem(spacer_item, 1, 0, 1, 1)
        # layout.addItem(spacer_item, 1, 3, 1, 1)
        layout.addWidget(self.voltage_LCD, 4, 1)
        layout.addWidget(self.voltage_unit_label, 4, 2)
        layout.addWidget(self.voltage_dial, 4, 3)
        layout.addWidget(self.current_LCD, 5, 1)
        layout.addWidget(self.current_unit_label, 5, 2)
        layout.addWidget(self.current_dial, 5, 3)
        layout.addWidget(self.power_LCD, 6, 1)
        layout.addWidget(self.power_unit_label, 6, 2)
        layout.addWidget(self.device_state, 7, 1)
        layout.addWidget(self.on_off_button, 7, 2, 1, 2)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        # layout.addItem(spacer_item, 10, 1, 1, 1)
        # layout.addItem(spacer_item, 10, 2, 1, 1)
    
    def open(self):
        print("XXX")
        print(self.device.status())
        print("---")
        print(self.device.state())
        print("XXX")

    def on_off_device(self):
        actual_state = str(self.device.state())
        if actual_state == "ON":
            self.device.command_inout("TurnOff")
            self.device_state_actual()
        if actual_state == "OFF" or actual_state == "STANDBY":
            self.device.command_inout("TurnOn")
            self.device_state_actual()

    def device_state_actual(self):
        # states: STANDBY ALARM ON OFF
        actual_state = str(self.device.state())
        if actual_state == 'ON':
            self.device_state.setLedColor("GREEN")
            self.voltage_dial.setDisabled(False)
            self.current_dial.setDisabled(False)
            self.voltage_LCD.show()
            self.current_LCD.show()
            self.power_LCD.show()
        elif actual_state == "STANDBY":
            self.device_state.setLedColor("YELLOW")
            self.voltage_LCD.hide()
            self.current_LCD.hide()
            self.power_LCD.hide()
        elif actual_state == 'OFF':        
            self.device_state.setLedColor("RED")
            self.voltage_LCD.hide()
            self.current_LCD.hide()
            self.power_LCD.hide()
            self.voltage_dial.setDisabled(True)
            self.current_dial.setDisabled(True)
        elif actual_state == "ALARM":
            self.device_state.setLedColor("ORANGE")

    def voltage_change(self, val):
        self.device.write_attribute("voltage", val)
        self.voltage_LCD.setProperty("value", val)
        self.device_state_actual()
    
    def current_change(self, val):
        self.device.write_attribute("current", val)
        self.current_LCD.setProperty("value", val)
        self.device_state_actual()


def main():
    app_ = TaurusApplication()
    window = MyWidget()
    with open("power_supply_taurus_css.css", 'r') as file:
        style_sheet = file.read()
    app_.setStyleSheet(style_sheet)
    window.show()
    sys.exit(app_.exec_())


if __name__ == '__main__':
    main()
