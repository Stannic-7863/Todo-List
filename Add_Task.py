import csv
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QCheckBox,
                             QHBoxLayout,
                             QToolButton,
                             QMenu
                             )
from settings import *

class Add_Task:
    def __init__(self, parent, mainlayout, task_name, prio):
        self.parent = parent
        self.text = task_name
        self.priority_str = prio
        self.mainwindowlayout = mainlayout
    
    def change_prio(self, prio):
        self.priority_str = prio
        self.color = self.get_color(prio)
        if self.check_box.isChecked() == False:
            self.change_style_sheet()

    def save(self):
        self.text = self.text.strip()
        if self.text.strip():
            self.color = priority_none
            self.color = self.get_color(self.priority_str)
           
            self.options = QToolButton()
            self.options.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            self.options.setText('...')
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
            
            checkbox_layout = QHBoxLayout()
            self.check_box = QCheckBox(self.text, self.parent)
            self.check_box.setLayout(checkbox_layout)
            checkbox_layout.addStretch()
            checkbox_layout.addWidget(self.options)
            
            self.mainwindowlayout.insertWidget(1,self.check_box, alignment=Qt.AlignmentFlag.AlignTop)
            self.change_style_sheet()
            self.check_box.stateChanged.connect(lambda value: self.parent.on_state_changed(value, self.color))
            widget_data = {
                'Name' : self.text,
                'Current_status' : False,
                'Priority' : self.priority_str
            }
            file_path = './data/task_data/data.csv'
        
            with open(file_path, 'a', newline='')as data_csv:
                writer = csv.writer(data_csv)
                writer.writerow(widget_data.values())

    def create_menu(self):
        menu = QMenu(parent=self.parent)

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

        return menu

    def change_style_sheet(self):
        self.check_box.setStyleSheet(f"""QCheckBox {{
                                    background-color: rgb{str(self.color)};
                                    color: white;
                                    padding: 30px;
                                    border-radius: 5px;
                                    }}  
                                    QCheckBox::indicator {{
                                    background-color: {background};
                                    border-radius: 4px;
                                    }}
                                    QCheckBox::indicator:checked {{
                                    background-color: {support};
                                    }}
                                    """)

    def get_color(self, prio):
        self.color = priority_none
        if prio == 'high':
            self.color = priority_high
        elif prio == 'mid':
            self.color = priority_mid
        elif prio == 'low':
            self.color = priority_low
        
        return self.color