import typing
from PyQt6 import QtCore, QtGui
from settings import *
from Add_Task import Add_Task
from PyQt6.QtGui import QFont, QFontDatabase, QColor, qRgb, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QSize, QVariantAnimation, QAbstractAnimation
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QDialog,
                             QDialogButtonBox,
                             QPlainTextEdit,
                             QLabel,
                             QRadioButton,
                             QButtonGroup,
                             QScrollBar,
                             QSizePolicy
                             )
import datetime
from load_save_data import commit_new_task_data


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
        self.current_word_count_label = QLabel()
        self.current_word_count_label.setText(f'{len(self.get_task_text.toPlainText())}/{self.limit}')
        self.current_word_count_label.setStyleSheet(f"""QLabel {{
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
        self.layout.addWidget(self.current_word_count_label, alignment= Qt.AlignmentFlag.AlignRight)
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
        commit_new_task_data(text, str(datetime.datetime.now()), prio, 'Not Done', None)
        add_task.add()
        self.parent.on_task_added()
        self.accept()
    
    def reject(self):
        self.parent.on_task_added()
        self.close()

    def word_limit(self):
        self.get_task_text.blockSignals(True)
        current_text = self.get_task_text.toPlainText()
        if len(current_text) > self.limit:
            cursor = self.get_task_text.cursor()
            turnacated_text = current_text[:self.limit]
            self.get_task_text.setPlainText(turnacated_text)
            self.get_task_text.setCursor(cursor)
            
        display_text = len(current_text)
        self.current_word_count_label.setStyleSheet(f"""QLabel {{
                                                    color : {primary};
                                                    font-weight: bold;
                                                    }}""")
        if display_text >= 300:
            display_text = 300   
            self.current_word_count_label.setStyleSheet(f"""QLabel {{
                                                    color : rgb{str(priority_mid)};
                                                    font-weight: bold;
                                                    }}""")
        

        self.current_word_count_label.setText(f'{display_text}/{self.limit}')

        self.get_task_text.blockSignals(False)

 
class Custom_Scroll_Bar(QScrollBar):
    def __init__(self):
        super().__init__()

    def enterEvent(self, event):
        start_animation(self, qprimary, priority_mid)

    def leaveEvent(self, event):
        start_animation(self, priority_mid, qprimary)

class Add_Task_No_dialog(QWidget):
    def __init__(self, parent, mainwindowlayout):
        super().__init__(parent)
        self.parent = parent
        self.mainwindowlayout = mainwindowlayout
        self.limit = 300
        self.main_layout = QVBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        path = './data/fonts/bfont.TTF' 

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        QApplication.setFont(QFont(fontfamily))

        self.get_task_text_widget_layout = QVBoxLayout()
        self.get_task_text_widget = QWidget()
        self.get_task_text_widget.setLayout(self.get_task_text_widget_layout)
        self.get_task_text = QPlainTextEdit()
        self.get_task_text_widget_layout.addWidget(self.get_task_text)
        self.get_task_text.setStyleSheet("max-height: 70")
        self.get_task_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
   
        self.get_task_text.textChanged.connect(self.word_limit)
        self.get_task_text.setPlaceholderText('Enter Task Name and description')

        self.current_word_count_label = QLabel()
        self.current_word_count_label.setText(f'{len(self.get_task_text.toPlainText())}/{self.limit}')

        priority_button_container = QWidget()
        priority_button_container_layout = QHBoxLayout()
        priority_button_container.setLayout(priority_button_container_layout)
        priority_button_group = QButtonGroup()
        priority_label = QLabel()
        priority_label.setText('Priority [Optional]:')
        self.p_high = QRadioButton("High")
        self.p_mid = QRadioButton("Mid")
        self.p_low = QRadioButton("Low")
        priority_button_group.addButton(self.p_high)
        priority_button_group.addButton(self.p_mid)
        priority_button_group.addButton(self.p_low)

        self.save_button = QPushButton('Save')
        cancel_shortcut = QShortcut(QKeySequence('escape'), self)
        cancel_shortcut.activated.connect(self.on_cancel)
        
        self.save_button.setFixedSize(QSize(70, 35))
    
        self.main_layout.addWidget(self.get_task_text_widget)
        priority_button_container_layout.addWidget(priority_label, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addWidget(self.p_high, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addWidget(self.p_mid, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addWidget(self.p_low, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addStretch()
        priority_button_container_layout.addWidget(self.current_word_count_label, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(priority_button_container)   
        self.main_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.main_layout)

        self.save_button.clicked.connect(self.on_save)
        

        self.setStyleSheet(f"""
                           QPlainTextEdit {{
                           background: {primary};
                           }}
                           QPushButton {{
                           background: {primary};
                           border-radius: 5px;
                           }}
                           QRadioButton::indicator {{
                           image : none;
                           }}
                           
                           
                           """)
        self.p_high.setStyleSheet(f"""QRadioButton
                                {{
                                    background-color: rgb{priority_high};
                                    padding: 5px 10px 5px 0px;
                                    text-align: center;
                                    width: 60px;
                                    height: 15px;
                                }}
                                QRadioButton:checked
                                {{
                                    border:2px solid white;
                                }}
                                """)

        self.p_mid.setStyleSheet(f"""QRadioButton
                                {{
                                    background-color: rgb{priority_mid};
                                    padding: 5px 10px 5px 0px;
                                    text-align: center;
                                    width: 60px;
                                    height: 15px;
                                }}
                                QRadioButton:checked
                                {{
                                    border:2px solid white;
                                }}
                                """)

        self.p_low.setStyleSheet(f"""QRadioButton
                                {{
                                    background-color: rgb{priority_low};
                                    padding: 5px 10px 5px 0px;
                                    text-align: center;
                                    width: 60px;
                                    height: 15px;
                                }}
                                QRadioButton:checked
                                {{
                                    border:2px solid white;
                                }}
                                """)


    def word_limit(self):
        self.get_task_text.blockSignals(True)
        current_text = self.get_task_text.toPlainText()
        if len(current_text) > self.limit:
            cursor = self.get_task_text.cursor()
            turnacated_text = current_text[:self.limit]
            self.get_task_text.setPlainText(turnacated_text)
            self.get_task_text.setCursor(cursor)
            
        display_text = len(current_text)
        self.current_word_count_label.setStyleSheet(f"""QLabel {{
                                                color : {primary};
                                                font-weight: bold;
                                                }}""")
        if display_text >= 300:
            display_text = 300   
            self.current_word_count_label.setStyleSheet(f"""QLabel {{
                                                    color : rgb{str(priority_mid)};
                                                    font-weight: bold;
                                                    }}""")

        self.current_word_count_label.setText(f'{display_text}/{self.limit}')

        self.get_task_text.blockSignals(False)
    
    def on_save(self):
        prio = 'None'
        if self.p_high.isChecked():
            prio = 'high'
        if self.p_mid.isChecked():
            prio = 'mid'
        if self.p_low.isChecked():
            prio = 'low'
        
        text = self.get_task_text.toPlainText().strip()
        add_task = Add_Task(self.parent, self.mainwindowlayout ,text, prio)
        commit_new_task_data(text, str(datetime.datetime.now()), prio, 'Not Done', None)
        add_task.add()

        self.parent.on_task_added()
        self.parent.placeholder_widget.deleteLater()
        self.deleteLater()

    def on_cancel(self):
        self.parent.on_task_added()
        self.parent.placeholder_widget.deleteLater()
        self.deleteLater()

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
