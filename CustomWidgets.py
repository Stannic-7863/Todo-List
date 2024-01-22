from settings import *
from TaskWidget import *
from PySide6.QtGui import QColor, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QSize, QVariantAnimation, QAbstractAnimation
from PySide6.QtWidgets import (QWidget,
                            QVBoxLayout,
                            QHBoxLayout,
                            QPushButton,
                            QPlainTextEdit,
                            QLabel,
                            QRadioButton,
                            QButtonGroup,
                            QScrollBar,
                            )

import datetime
from db_data_functions import commit_new_task_data

class NavMenuItemLabels(QLabel):
    
    activeInstance = None
    
    def __init__(self, name, parent, assigned):
        super().__init__()
        self.setText(name)
        self.is_hovering = False
        self.selected = False
        self.parent = parent
        self.assigned = assigned
        
        self.setStyleSheet(f"""
            QLabel {{
                font-size: 15px;
                border-radius: 3px;
                padding: 5px 2px 5px 2px;
            }}
            QLabel::hover {{
                background-color : {accentdarkColor}
            }}
            """)
    
    def enterEvent(self, event):
        self.is_hovering = True

    def leaveEvent(self, event):
        self.is_hovering = False

    def mousePressEvent(self, event):
        if self.is_hovering:
            self.switch_widget()

    def switch_widget(self):
        if NavMenuItemLabels.activeInstance and NavMenuItemLabels.activeInstance != self:
            NavMenuItemLabels.activeInstance.selected = False
            NavMenuItemLabels.activeInstance = self
        else:
            NavMenuItemLabels.activeInstance = None
            
        self.selected = True

        self.parent.stackedContainerLayout.setCurrentWidget(self.assigned)

class ScrollBar(QScrollBar):
    def __init__(self) -> QScrollBar:
        """
        A customized QScrollBar
        """
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
        
    def enterEvent(self, event) -> bool:
        start_animation(self, primaryColor, priorityMidColor)
        return True
    def leaveEvent(self, event) -> bool:
        start_animation(self, priorityMidColor, primaryColor)
        return True
    
class GetTaskFromUser(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.parent = parent
        self.limit = 300
        
        self.containerLayout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.containerLayout)
        
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.addWidget(self.container)
        
        self.getTaskName = QPlainTextEdit()
        self.getTaskName.setStyleSheet("max-height: 70")
        self.getTaskName.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.getTaskName.textChanged.connect(self.LimitWordCount)
        self.getTaskName.setPlaceholderText('Enter Task Name')

        self.WordCountLabel = QLabel()
        self.WordCountLabel.setText(f'{len(self.getTaskName.toPlainText())}/{self.limit}')
        self.WordCountLabel.setStyleSheet(f"""QLabel {{
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
        self.save_button.setFixedSize(QSize(70, 35))
        
        cancel_shortcut = QShortcut(QKeySequence('escape'), self)
        cancel_shortcut.activated.connect(self.on_cancel)
        
        priority_button_container_layout.addWidget(priority_label, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addWidget(self.p_high, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addWidget(self.p_mid, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addWidget(self.p_low, alignment=Qt.AlignmentFlag.AlignLeft)
        priority_button_container_layout.addStretch()
        priority_button_container_layout.addWidget(self.WordCountLabel, alignment=Qt.AlignmentFlag.AlignRight)
        self.containerLayout.addWidget(self.getTaskName)
        self.containerLayout.addWidget(priority_button_container)   
        self.containerLayout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.save_button.clicked.connect(self.on_save)

        self.setStyleSheet(f"""
                        QWidget {{
                            background: {primaryColor};
                            border-radius: 5px;
                            max-width : 2000;
                        }}
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

    def on_save(self):
        priority = 'none'
        if self.p_high.isChecked():
            priority = 'high'
        if self.p_mid.isChecked():
            priority = 'mid'
        if self.p_low.isChecked():
            priority = 'low'
        
        taskName = self.getTaskName.toPlainText().strip()
        currentDatetime = datetime.datetime.now()
        formattedDate = currentDatetime.strftime('%Y-%m-%d')
        task_id = commit_new_task_data(taskName, str(formattedDate), priority, 'not done', None)
        TaskCheckBox(self.parent ,taskName, priority, 'not done', task_id, False)

        self.deleteLater()

    def on_cancel(self):
        self.deleteLater()
        
    def LimitWordCount(self):
        self.getTaskName.blockSignals(True)
        current_text = self.getTaskName.toPlainText()
        if len(current_text) > self.limit:
            cursor = self.getTaskName.cursor()
            turnacatedText = current_text[:self.limit]
            self.getTaskName.setPlainText(turnacatedText)
            self.getTaskName.setCursor(cursor)
            
        currentWordCount = len(current_text)
        self.WordCountLabel.setStyleSheet(f"""QLabel {{
                                                color : {backgroundColor};
                                                font-weight: bold;
                                                }}""")
        if currentWordCount >= 300:
            currentWordCount = 300   
            self.WordCountLabel.setStyleSheet(f"""QLabel {{
                                                    color : {priorityMidColor};
                                                    font-weight: bold;
                                                    }}""")

        self.WordCountLabel.setText(f'{currentWordCount}/{self.limit}')

        self.getTaskName.blockSignals(False)

    def set_radio_style_sheet(self, widget, color):
        widget.setStyleSheet(f"""QRadioButton
                                {{
                                    background-color: {color};
                                    padding: 5px 10px 5px 1px;
                                    text-align: center;
                                    width: 60px;
                                    height: 20px;
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