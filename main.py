import typing
from PyQt6 import QtCore, QtGui
from settings import *
from Add_Task import Add_Task
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QColor, qRgb
from PyQt6.QtCore import Qt, QSize, QVariantAnimation, QAbstractAnimation
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
                             QButtonGroup,
                             QScrollBar
                             )


class Add_task_dialog(QDialog):
    def __init__(self, parent, mainwindowlayout):
        super().__init__(parent)
        path = './data/fonts/bfont.TTF'

        self.limit = 300

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
        self.buttonbox.accepted.connect(self.save)
        self.buttonbox.rejected.connect(self.reject)

        self.get_task_text = QPlainTextEdit()
        self.get_task_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.get_task_text.textChanged.connect(self.word_limit)
        self.current_word_count_labet = QLabel()
        self.current_word_count_labet.setText(f'{len(self.get_task_text.toPlainText())}/{self.limit}')
        self.current_word_count_labet.setStyleSheet(f"""QLabel {{
                                                    color : {primary};
                                                    font-weight: bold;
        }}""")

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
        self.layout.addWidget(self.current_word_count_labet, alignment= Qt.AlignmentFlag.AlignRight)
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
    
    def word_limit(self):
        self.get_task_text.textChanged.disconnect(self.word_limit)
        current_text = self.get_task_text.toPlainText()
        if len(current_text) > self.limit:
            cursor = self.get_task_text.textCursor()
            cursor.deletePreviousChar()
            self.get_task_text.setTextCursor(cursor)
            
        display_text = len(current_text)
        if display_text >= 300:
            display_text = 300   
            self.current_word_count_labet.setStyleSheet(f"""QLabel {{
                                                    color : rgb{str(priority_mid)};
                                                    font-weight: bold;
                                                    }}""")
        else : 
            self.current_word_count_labet.setStyleSheet(f"""QLabel {{
                                                    color : {primary};
                                                    font-weight: bold;
                                                    }}""")

        self.current_word_count_labet.setText(f'{display_text}/{self.limit}')

        self.get_task_text.textChanged.connect(self.word_limit)
    
 
class Custom_Scroll_Bar(QScrollBar):
    def __init__(self):
        super().__init__()

    def enterEvent(self, event):
        start_animation(self, qprimary, priority_mid)

    def leaveEvent(self, event):
        start_animation(self, priority_mid, qprimary)
    
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
        custom_scroll = Custom_Scroll_Bar()
        scroll.setVerticalScrollBar(custom_scroll)
        
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
                             margin: 15px 10px 15px 0px
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

def start_animation(widget, color_from, color_to):
    animation = QVariantAnimation(widget)
    animation.setDuration(400)
    animation.setStartValue(QColor(qRgb(color_from[0], color_from[1], color_from[2])))
    animation.setEndValue(QColor(qRgb(color_to[0], color_to[1], color_to[2])))
    animation.valueChanged.connect(lambda value: change(widget, value.name()))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)


def change(widget, color):
    widget.setStyleSheet(f"""
                        QScrollBar:vertical {{
                        background: {background};
                        width: 20px;
                        border: 0px solid black;
                        margin: 15px 10px 15px 0px
                        }}

                        QScrollBar::handle:vertical {{
                        border: 0px solid black;
                        border-radius : 5px;
                        background-color : {color}; 
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




if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()