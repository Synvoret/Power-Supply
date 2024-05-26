import sys
from PyTango import DeviceProxy
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout
)


class MyWidget:

    def __init__(self):
        try:
            self.dev = DeviceProxy("sound/sound/1")
        except:
            print("Error")
    
    def on_clicked(self):
        try:
            self.dev.Mute = not self.dev.Mute
        except:
            print("Cannot Mute, setting volume to max")
            self.dev.Volume = 1
            self.dev.Mute = not self.dev.Mute

    def get_volume(self):
        return str(round(self.dev.Volume, 2))
    
    def show(self):
        app = QApplication([])

        window = QWidget()
        window.setWindowTitle("Pulse Audio System")

        btn = QPushButton("Mute")
        btn.clicked.connect(self.on_clicked)

        label1 = QLabel("Volume")
        label2 = QLabel(self.get_volume())

        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(btn)
        window.setLayout(layout)

        window.show()
        sys.exit(app.exec_())



def main():
    app = MyWidget()
    app.show()
    


if __name__ == '__main__':
    main()