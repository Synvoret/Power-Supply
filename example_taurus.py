import sys
from PyTango import DeviceProxy

from taurus.qt.qtgui.container import TaurusWidget
from taurus.qt.qtgui.application import TaurusApplication
from taurus.qt.qtgui.display import TaurusLabel
from taurus.external.qt import QtGui
from taurus.qt.qtgui.input import TaurusValueLineEdit
from taurus.qt.qtgui.button import TaurusCommandButton
from taurus.external.qt.QtGui import (
    QMessageBox,
    QComboBox,
    QPushButton,
    QInputDialog,
    QSizePolicy,
    QWidget
)


class MyWidget(TaurusWidget):

    def __init__(self, parent=None, args=None):
        super(MyWidget, self).__init__(parent, args)
        try:
            self.dev = DeviceProxy("sound/sound/1")
        except:
            print("Error")

        self.resize(400, 200)
        self.setup_ui()

    def on_clicked(self):
        try:
            # self.dev.Mute = not self.dev.Mute
            self.dev.Toggle()
        except:
            print("Cannot mute, setting volume to max")
            self.dev.Volume = 1
            # self.dev.Mute = not self.dev.Mute
            self.on_clicked()
    
    def get_volume(self):
        return str(round(self.dev.Volume, 2))
    
    def setup_ui(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2
        )
        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        window = QWidget()
        window.setWindowTitle("Pulse Audio Sink")

        mute_btn = QPushButton("Mute")
        mute_btn.clicked.connect(self.on_clicked)

        layout.addWidget(mute_btn, 0, 0)

        button = TaurusCommandButton(
            command='Toggle', icon="logos:taurus.png", text="Mute"
        )

        button.setModel("sound/sound/1")
        layout.addWidget(button, 0, 3)
        label1 = TaurusLabel("Volume")

        label1.setModel("sound/sound/1/Volume")
        layout.addWidget(label1, 0, 1)

        input_spin = TaurusValueLineEdit()
        input_spin.setModel("sound/sound/1/Volume")
        layout.addWidget(input_spin, 0, 2)


def main():
    app_ = TaurusApplication()
    win = MyWidget()
    win.show()
    sys.exit(app_.exec_())


if __name__ == '__main__':
    main()
