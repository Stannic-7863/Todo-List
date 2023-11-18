from settings import *
from Add_Task import Add_Task
import functools, csv
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QScrollArea,
                             QPushButton,
                             QDialog,
                             QDialogButtonBox,
                             QPlainTextEdit,
                             QLabel,
                             QRadioButton,
                             QButtonGroup
                             )

class Add_task_dialog(QDialog):
    def __init__(self, parent, mainwindowlayout):
        super().__init__(parent)
        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        QApplication.setFont(QFont(fontfamily))

        self.parent = parent
        self.mainwindowlayout = mainwindowlayout
        self.setWindowTitle('Add a new task')
        self.setGeometry(100, 100, 500, 400)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        label = QLabel("New task")
        self.buttonbox = QDialogButtonBox(buttons)
        self.buttonbox.clicked.connect(self.save)
        self.buttonbox.rejected.connect(self.reject)

        self.get_task_text = QPlainTextEdit()
        self.get_task_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        self.p_high = QRadioButton('Priority : High')
        self.p_mid = QRadioButton('Priority : Mid')
        self.p_low = QRadioButton('Priority : Low')

        
        self.buttongroup = QButtonGroup()
        self.buttongroup.addButton(self.p_high)
        self.buttongroup.addButton(self.p_mid)
        self.buttongroup.addButton(self.p_low)


        self.layout = QVBoxLayout()
        self.layout.addWidget(label, alignment= Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.get_task_text, alignment= Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.p_high)
        self.layout.addWidget(self.p_mid)
        self.layout.addWidget(self.p_low)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonbox, alignment= Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.layout)

    def save(self):
        prio = 'none'
        if self.p_high.isChecked():
            prio = 'high'
        elif self.p_mid.isChecked():
            prio = 'mid'
        elif self.p_low.isChecked():
            prio = 'low'

        text = self.get_task_text.toPlainText()

        add_task = Add_Task(self.parent, self.mainwindowlayout ,text, prio)
        add_task.add()

        self.accept()

         
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_init()

    def ui_init(self):

        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        self.setFont(QFont(fontfamily))

        self.setWindowTitle('Todo List')
        self.setMinimumHeight(600)
        self.setMinimumWidth(400)

        self.central_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)

        taskwidget = QWidget()
        self.taskwidget_layout = QVBoxLayout()
        taskwidget.setLayout(self.taskwidget_layout)

        self.statswidget = QWidget()
        self.statswidget_layout = QVBoxLayout()
        self.statswidget.setLayout(self.taskwidget_layout)
        self.central_layout.addWidget(self.statswidget)
        self.central_layout.addWidget(taskwidget)
        
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(central_widget)
        
        self.setCentralWidget(scroll)
        
        self.addtask = QPushButton()
        self.addtask.setIcon(QIcon('./data/icons/plus.png'))
        self.addtask.setIconSize(QSize(50,50))
        self.addtask.setContentsMargins(0,0,0,0)
        self.addtask.clicked.connect(self.on_addtask_clicked)
        self.addtask.setFixedWidth(200)
        self.taskwidget_layout.addWidget(self.addtask, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskwidget_layout.addStretch()


        self.setStyleSheet(f"""
                           QWidget {{
                           background-color: {background}; 
                           color: white;
                           }}
                           """)
        self.statswidget.setStyleSheet(f"""
                                       QWidget {{
                                       border-radius : 5px;
                                       }}
                                       """)
        self.addtask.setStyleSheet(f"""QPushButton {{
                                   color: white;
                                   background-color: none;
                                   padding: 10px;
                                   border: 2px solid white;
                                   border-radius: 12px;
                                   }}
                                   QPushButton:hover {{
                                   background-color: {primary}
                                   }}
                                   """)
        scroll.setStyleSheet(f"""
                             QScrollBar:vertical {{
                             background: {background};
                             width: 20px;
                             border: 0px solid black;
                             margin: 10px 10px 10px 0px
                             }}

                             QScrollBar::handle:vertical {{
                             border: 0px solid black;
                             border-radius : 5px;
                             background-color : {primary}; 
                             }}

                             QScrollBar::sub-line:vertical {{
                             background: {background};
                             }}
                             
                             QScrollBar::add-line:vertical {{
                             background: {background}; 
                             }}

                             QScrollBar::sub-page:vertical {{
                             background: {background};
                             }}

                             QScrollBar::add-page:vertical {{
                             background: {background};
                             }}
                            """)

        self.showMaximized()

    def on_addtask_clicked(self):
        dialog = Add_task_dialog(self, self.taskwidget_layout)

        dialog.exec()




if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()