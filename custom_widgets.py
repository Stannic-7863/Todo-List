from settings import *
from Add_Task import Add_Task
from PySide6.QtGui import QFont, QFontDatabase, QColor, qRgb, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QSize, QVariantAnimation, QAbstractAnimation
from PySide6.QtWidgets import (QApplication,
                            QWidget,
                            QVBoxLayout,
                            QHBoxLayout,
                            QPushButton,
                            QPlainTextEdit,
                            QLabel,
                            QRadioButton,
                            QButtonGroup,
                            QScrollBar,
                            QSizePolicy
                            )

import datetime
from db_data_functions import commit_new_task_data

class ItemLable(QLabel):
    instances = []
    def __init__(self, text, central, assigned):
        super().__init__()
        self.instances.append(self)
        self.setText(text)
        self.is_hovering = False
        self.selected = False
        self.central = central
        self.assigned = assigned
    
    def enterEvent(self, event):
        self.is_hovering = True

    def leaveEvent(self, event):
        self.is_hovering = False

    def mousePressEvent(self, event):
        if self.is_hovering:
            self.switch_widget()

    def switch_widget(self):
        for instance in self.instances:
                instance.selected = False
        self.selected = True

        self.central.setCurrentWidget(self.assigned)

class Custom_Scroll_Bar(QScrollBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
                            QScrollBar:vertical {{
                            background: {backgroundColor};
                            width: 20px;
                            border: 0px solid black;
                            margin: 15px 10px 15px 0px
                            }}

                            QScrollBar::handle:vertical {{
                            border: 0px solid black;
                            border-radius : 5px;
                            background-color : {primaryColor}; 
                            }}

                            QScrollBar::sub-line:vertical {{
                            background: {backgroundColor};
                            }}
                            
                            QScrollBar::add-line:vertical {{
                            background: {backgroundColor}; 
                            }}

                            QScrollBar::sub-page:vertical {{
                            background: {backgroundColor};
                            }}

                            QScrollBar::add-page:vertical {{
                            background: {backgroundColor};
                            }}
                        """)
        

    def enterEvent(self, event):
        start_animation(self, primaryColor, priorityMidColor)

    def leaveEvent(self, event):
        start_animation(self, priorityMidColor, primaryColor)

class GetTaskFromUser(QWidget):
    def __init__(self, parent, mainwindowlayout):
        super().__init__(parent)
        self.setMinimumWidth(200)
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
        self.getTaskName = QPlainTextEdit()
        self.get_task_text_widget_layout.addWidget(self.getTaskName)
        self.getTaskName.setStyleSheet("max-height: 70")
        self.getTaskName.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.getTaskName.textChanged.connect(self.word_limit)
        self.getTaskName.setPlaceholderText('Enter Task Name and description')

        self.currentWordCountLabel = QLabel()
        self.currentWordCountLabel.setText(f'{len(self.getTaskName.toPlainText())}/{self.limit}')
        self.currentWordCountLabel.setStyleSheet(f"""QLabel {{
                            color : {backgroundColor};
                            font-weight: bold;}}
                        """)

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

        self.set_radio_style_sheet(self.p_high, priorityHighColor)
        self.set_radio_style_sheet(self.p_mid, priorityMidColor)
        self.set_radio_style_sheet(self.p_low, priorityLowColor)
        
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
        priority_button_container_layout.addWidget(self.currentWordCountLabel, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(priority_button_container)   
        self.main_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.main_layout)

        self.save_button.clicked.connect(self.on_save)
        

        self.setStyleSheet(f"""
                        QWidget {{border-radius: 5px}}
                        QPlainTextEdit {{
                        background: {backgroundColor};
                        border-radius: 5px
                        }}
                        QPushButton {{
                        background: {backgroundColor};
                        border-radius: 5px;
                        }}
                        QRadioButton::indicator {{
                        image : none;
                        }}
                        QLabel {{
                        color : {fontColor}
                        }}
                        """)

    def word_limit(self):
        self.getTaskName.blockSignals(True)
        current_text = self.getTaskName.toPlainText()
        if len(current_text) > self.limit:
            cursor = self.getTaskName.cursor()
            turnacatedText = current_text[:self.limit]
            self.getTaskName.setPlainText(turnacatedText)
            self.getTaskName.setCursor(cursor)
            
        currentWordCount = len(current_text)
        self.currentWordCountLabel.setStyleSheet(f"""QLabel {{
                                                color : {backgroundColor};
                                                font-weight: bold;
                                                }}""")
        if currentWordCount >= 300:
            currentWordCount = 300   
            self.currentWordCountLabel.setStyleSheet(f"""QLabel {{
                                                    color : rgb{str(priorityMidColor)};
                                                    font-weight: bold;
                                                    }}""")

        self.currentWordCountLabel.setText(f'{currentWordCount}/{self.limit}')

        self.getTaskName.blockSignals(False)

    def on_save(self):
        prio = 'none'
        if self.p_high.isChecked():
            prio = 'high'
        if self.p_mid.isChecked():
            prio = 'mid'
        if self.p_low.isChecked():
            prio = 'low'
        
        text = self.getTaskName.toPlainText().strip()
        currentDatetime = datetime.datetime.now()
        formattedDate = currentDatetime.strftime('%Y-%m-%d')
        task_id = commit_new_task_data(text, str(formattedDate), prio, 'not done', None)
        Add_Task(self.parent, self.mainwindowlayout ,text, prio, 'not done', task_id)

        self.parent.on_task_added()
        self.parent.placeholder_widget.deleteLater()
        self.deleteLater()

    def on_cancel(self):
        self.parent.on_task_added()
        self.parent.placeholder_widget.deleteLater()
        self.deleteLater()

    def set_radio_style_sheet(self, widget, color):
        widget.setStyleSheet(f"""QRadioButton
                                {{
                                    background-color: rgb{color};
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

def start_animation(widget, color_from, color_to):
    animation = QVariantAnimation(widget)
    animation.setDuration(400)
    animation.setStartValue(QColor(color_from))
    animation.setEndValue(QColor(color_to))
    animation.valueChanged.connect(lambda value: change(widget, value.name()))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

def change(widget, color):
    widget.setStyleSheet(f"""
                        QScrollBar:vertical {{
                        background: {backgroundColor};
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
                        background: {backgroundColor};
                        }}
                        
                        QScrollBar::add-line:vertical {{
                        background: {backgroundColor}; 
                        }}

                        QScrollBar::sub-page:vertical {{
                        background: {backgroundColor};
                        }}

                        QScrollBar::add-page:vertical {{
                        background: {backgroundColor};
                        }}
                    """)