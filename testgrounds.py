import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QCheckBox, QSizePolicy, QVBoxLayout, QApplication, QWidget, QMainWindow, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QResizeEvent

support = 'rgb(255, 255, 255)'
background = 'rgb(34, 40, 49)'
primary = 'rgb(57, 62, 70)'
secondary = 'rgb(0, 173, 181)'
accent = '(237,76,76)'

qsupport = (255, 255, 255)
qbackground = (34, 40, 49)
qprimary = (57, 62, 70)
qsecondary = (0, 173, 181)
qaccent = (237,76,76)

priority_low = (0, 173, 181)
priority_mid = (255,167,0)
priority_high = (237,76,76)
priority_none = (57, 62, 70)
task_done = (11, 219, 123)

class Custom(QCheckBox):
    def __init__(self, text):
        super().__init__()

        layout = QHBoxLayout(self)
        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)

        self.mouse_inside = True

        self.setMouseTracking(True)

        self.setStyleSheet(f"""
                                QCheckBox {{
                                background-color: rgb{str(task_done)};
                                color: white;
                                padding: 30px;
                                border-radius: 5px;
                                }}  
                                QCheckBox::indicator {{
                                subcontrol-position:left;
                                background-color: {background};
                                border-radius: 4px;
                                }}
                                QCheckBox::indicator:checked {{
                                background-color: {support};
                                }}
                                QLabel {{
                                padding-left: 40px;
                                }}
                                """)
    def enterEvent(self, event):
        self.mouse_inside = True
    def leaveEvent(self, event):
        self.mouse_inside = True
    def mousePressEvent(self, event):
        if self.mouse_inside:
            self.setChecked(not self.isChecked())


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Word Wrap')

        check_box = Custom('hmmmm hhmmm hm hmmhm hhm hm hm m')
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        layout.addWidget(check_box)
        self.setCentralWidget(widget)
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    main = Main()
    app.exec()