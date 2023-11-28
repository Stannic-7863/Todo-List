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

        self.ui_init()

    def ui_init(self):
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
        self.current_word_count_label.setStyleSheet(f"""QLabel {{
                            color : {background};
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
                           QWidget {{border-radius: 5px}}
                           QPlainTextEdit {{
                           background: {background};
                           border-radius: 5px
                           }}
                           QPushButton {{
                           background: {background};
                           border-radius: 5px;
                           }}
                           QRadioButton::indicator {{
                           image : none;
                           }}""")

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
                                                color : {background};
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
        prio = 'none'
        if self.p_high.isChecked():
            prio = 'high'
        if self.p_mid.isChecked():
            prio = 'mid'
        if self.p_low.isChecked():
            prio = 'low'
        
        text = self.get_task_text.toPlainText().strip()
        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        task_id = commit_new_task_data(text, str(formatted_date), prio, 'not done', None)
        add_task = Add_Task(self.parent, self.mainwindowlayout ,text, prio, 'not done', task_id, loading_data=False)
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
