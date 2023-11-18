import csv, datetime, functools
from PyQt6.QtGui import QIcon, QAction, QActionGroup,  QColor, qRgb
from PyQt6.QtCore import Qt, QSize, QVariantAnimation, QAbstractAnimation
from PyQt6.QtWidgets import (QCheckBox,
                             QHBoxLayout,
                             QToolButton,
                             QMenu,
                             QLabel
                             )
from settings import *

class custom_checkbox(QCheckBox):
    def __init__(self, text, option_menu):
        super().__init__()

        layout = QHBoxLayout()

        text_label = QLabel()
        text_label.setText(text)
        text_label.setWordWrap(True)
        
        layout.addWidget(text_label)
        layout.addStretch()
        layout.addWidget(option_menu)

        self.setLayout(layout)

        self.mouse_inside = False
    def enterEvent(self, event):
        self.mouse_inside = True
    def leaveEvent(self, event):
        self.mouse_inside = True
    def mousePressEvent(self, event):
        if self.mouse_inside:
            self.setChecked(not self.isChecked())

class Add_Task:
    def __init__(self, parent, mainlayout, task_name, prio):
        self.parent = parent
        self.text = task_name
        self.priority_str = prio
        self.mainwindowlayout = mainlayout

    def add(self):
        self.text = self.text.strip()
        if self.text.strip():
            self.create_task_widgets()
        
    def create_task_widgets(self):
        self.color = priority_none
        self.color = self.get_color(self.priority_str)
        
        self.create_task_check_box()

    def create_task_check_box(self):
        self.options = self.create_task_options()
        self.check_box = custom_checkbox(self.text, self.options)
        self.mainwindowlayout.insertWidget(1, self.check_box, alignment=Qt.AlignmentFlag.AlignTop)
        self.check_box.stateChanged.connect(lambda value: self.on_state_changed(value, self.color))
        change_color(self.check_box, f"rgb{str(self.color)}")
    
    def create_task_options(self):
        self.options = QToolButton()
        self.options.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.options.setIcon(QIcon('./data/icons/menu.png'))
        self.options.setIconSize(QSize(30, 30))
        self.options.setMenu(self.create_menu())
        self.options.setStyleSheet(f"""
                                    QToolButton {{
                                    background-color : transparent;
                                    }}

                                    QToolButton::menu-indicator {{
                                    image: none;
                                    }}
                                    """)
        return self.options
    
    def create_menu(self):
        menu = QMenu(parent=self.parent)

        self.create_sub_menu_priority(menu)

        delete = QAction('Delete', parent=self.parent)
        delete.triggered.connect(lambda : self.delete_task(self.check_box))
        menu.addAction(delete)

        return menu

    def create_sub_menu_priority(self, menu):
        priority_menu = QMenu('Set Priority', parent=self.parent)
        action_group = QActionGroup(self.parent)
        m_high = QAction('High', parent=self.parent, checkable=True)
        m_mid = QAction('Mid', parent=self.parent, checkable=True)
        m_low = QAction('Low', parent=self.parent, checkable=True)
        action_group.addAction(m_high)
        action_group.addAction(m_mid)
        action_group.addAction(m_low)
        m_high.toggled.connect(lambda : self.change_prio('high'))
        m_mid.toggled.connect(lambda : self.change_prio('mid'))
        m_low.toggled.connect(lambda : self.change_prio('low'))
        priority_menu.addAction(m_high)
        priority_menu.addAction(m_mid)
        priority_menu.addAction(m_low)
        menu.addMenu(priority_menu)
    
    def delete_task(self, widget: QCheckBox):
        widget.deleteLater()
    
    def change_prio(self, prio):
        current = self.color
        self.priority_str = prio
        self.color = self.get_color(prio)
        if self.check_box.isChecked() == False:
            start_animation(self.check_box, current , self.color)

    def get_color(self, prio):
        self.color = priority_none
        if prio == 'high':
            self.color = priority_high
        elif prio == 'mid':
            self.color = priority_mid
        elif prio == 'low':
            self.color = priority_low
        
        return self.color
    

    def on_state_changed(self, value, color):
        state = Qt.CheckState(value)

        if state == Qt.CheckState.Unchecked:
            start_animation(self.check_box, task_done, color)
        if state == Qt.CheckState.Checked:
            start_animation(self.check_box, color, task_done)

def start_animation(checkbox, qprimary, qaccent):
    animation = QVariantAnimation(checkbox)
    animation.setDuration(400)
    animation.setStartValue(QColor(qRgb(qprimary[0], qprimary[1], qprimary[2])))
    animation.setEndValue(QColor(qRgb(qaccent[0], qaccent[1], qaccent[2])))
    animation.valueChanged.connect(lambda value: change_color(checkbox, value.name()))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

def change_color(widget, color):
    widget.setStyleSheet(f"""
                            QCheckBox {{
                            background-color: {color};
                            color: white;
                            padding: 30px;
                            border-radius: 5px;
                            border : none
                            }}  
                            QCheckBox::indicator {{
                            image: none;
                            }}
                            QCheckBox::indicator:checked {{
                            image: none;
                            }}
                            QLabel {{
                            background-color : {color};
                            padding: 20px;
                            font-size: 20px
                            }}
                            """)