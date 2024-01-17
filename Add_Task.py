import datetime
from sqlite3.dbapi2 import SQLITE_DBCONFIG_ENABLE_FKEY
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import *
from settings import *
from db_data_functions import *
import datetime

class QLineEdit(QLineEdit):
    def __init__(self, parent, color):
        super().__init__()
        self.parent = parent
        self.setStyleSheet(f"""background-color: rgb{color};
                                border: none; 
                                border-bottom: 1px solid white; 
                                padding: 10px 0px 10px 0px; 
                                font-size: 20px""")
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.parent.set_edit_task()
        super().keyPressEvent(event)

class TaskCheckBox(QCheckBox):
    
    activeInstance = None
    
    def __init__(self, text, parent, priority_str, mainwindowlayout, status,taskId, loadingData):
        super().__init__()
        self.mainLayout = QHBoxLayout()
        self.loadingData = loadingData
        self.parent = parent
        self.setParent(self.parent)
        self.text = text
        self.priority_str = priority_str
        self.mainwindowlayout = mainwindowlayout
        self.status = status
        self.taskId = taskId
        
        self.color = get_color(self.priority_str)
        change_color(self, f"rgb{str(self.color)}")
        self.stateChanged.connect(lambda value: self.on_state_changed(value, self.color, self.parent))
        
        self.get_edit = QLineEdit(self, self.color) 

        self.taskNameLabel = QLabel()
        self.taskNameLabel.setText(self.text)
        self.taskNameLabel.setWordWrap(True)
        self.optionMenu = self.createOptionMenu()
        self.infoButton = QToolButton()
        self.isInfoToggled = False
        self.infoButton.setText('Info button')
        self.infoButton.clicked.connect(self.checkOtherToggled)
        
        self.mainLayout.addWidget(self.taskNameLabel)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.infoButton, alignment=Qt.AlignmentFlag.AlignRight)
        self.mainLayout.addWidget(self.optionMenu, alignment= Qt.AlignmentFlag.AlignRight)

        self.setLayout(self.mainLayout)
        self.mouse_inside = False
        
        self.setMainStyleSheet()
        
    def checkOtherToggled(self):
        self.isInfoToggled = not self.isInfoToggled
        if self.isInfoToggled:
            if TaskCheckBox.activeInstance and TaskCheckBox.activeInstance != self : 
                TaskCheckBox.activeInstance.isInfoToggled = False
                
            TaskCheckBox.activeInstance = self
        else: 
            TaskCheckBox.activeInstance = None
        
        self.parent.toggleTaskInfo(self.isInfoToggled, self.taskId)

        
    def createOptionMenu(self):
        self.options = QToolButton()
        self.options.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.options.setIcon(QIcon('./data/icons/menu.png'))
        self.options.setIconSize(QSize(30, 30))
        self.options.setMenu(self.createMenu()) 
        return self.options
    
    def createMenu(self):
        self.menu = QMenu(self)    
        self.create_sub_menu_priority()
        
        edit = QAction('Edit', self)
        edit.triggered.connect(self.get_edit_task)
        self.menu.addAction(edit)
        
        pomodoro = QAction('Pomdoro', self)
        pomodoro.triggered.connect(lambda : self.parent.pomodoro_widget.get_task(self.text, self.taskId))
        self.menu.addAction(pomodoro)
        
        delete = QAction('Delete', self)
        delete.triggered.connect(lambda : self.delete_task(self))
        self.menu.addAction(delete)

        return self.menu
    
    def get_edit_task(self):
        self.taskNameLabel.setFixedWidth(0)
        self.get_edit.show()
        self.get_edit.setFocus()
        self.mainLayout.insertWidget(1, self.get_edit)
        
        edit_height = self.get_edit.height()
        margin = 30
        self.setMaximumHeight(edit_height+30)
        
    def set_edit_task(self):
        set_new_task_name(self.taskId, self.get_edit.text().strip())
        self.mainLayout.removeWidget(self.get_edit)
        self.taskNameLabel.setText(self.get_edit.text().strip())
        self.get_edit.clear()
        self.get_edit.hide()
        self.get_edit.clearFocus()
        self.taskNameLabel.setMaximumWidth(1000)
        text_height = self.taskNameLabel.height()
        height = self.height()
        self.setMaximumHeight(text_height+height)
    
    def create_sub_menu_priority(self):
        priority_menu = QMenu('Set Priority', parent=self.parent)
        priority_menu.setStyleSheet(f"QMenu::item:selected {{ background-color : {primary}}}")
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
        self.menu.addMenu(priority_menu)
        
    def change_prio(self, prio):
        previous_prio = self.priority_str
        current_color = self.color
        self.priority_str = prio
        self.color = get_color(prio)
        if self.isChecked() == False:
            start_animation(self, current_color , self.color)

        change_priority_db(previous_prio, self.priority_str, self.taskId)
        if not self.loadingData:    
            self.update_graphs()

    def on_state_changed(self, value, color, parent):
        state = Qt.CheckState(value)
        current_color = self.status

        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        
        text_height = self.taskNameLabel.height()
        height = self.height()
        self.setMaximumHeight(text_height+height)
        
        if state == Qt.CheckState.Unchecked:
            start_animation(self, task_done, color)
            self.status = 'not done'
            self.parent.doneTasksWidgetLayout.removeWidget(self)
            self.mainwindowlayout.insertWidget(1, self)
            if not self.loadingData: 
                change_status_db(current_color, self.status, self.taskId, formatted_date) 
        
        if state == Qt.CheckState.Checked:
            start_animation(self, color, task_done)
            self.status = 'done'
            self.mainwindowlayout.removeWidget(self)
            self.parent.doneTasksWidgetLayout.insertWidget(2, self)
            if not self.loadingData:
                change_status_db(current_color, self.status, self.taskId, formatted_date)

        if not self.loadingData:  
            self.update_graphs() 
        
    def update_graphs(self):
        self.parent.priorityBarChart.update()
        new_data = self.parent.get_task_status_data()
        self.parent.piegraph.update_data(new_data)
    
    def delete_task(self, widget: QCheckBox):
        delete_task_db(self.taskId)
        widget.deleteLater()
        self.update_graphs()
    
    def enterEvent(self, event):
        self.mouse_inside = True    
    def leaveEvent(self, event):
        self.mouse_inside = True
    def mousePressEvent(self, event):
        if self.mouse_inside:
            if event.button() == Qt.MouseButton.LeftButton:
                self.setChecked(not self.isChecked())
                
    def setMainStyleSheet(self):
        self.options.setStyleSheet(f"""
                                    QToolButton {{
                                    background-color : transparent;
                                    }}
                                    
                                    QToolButton::menu-indicator {{
                                    image: none;
                                    }}
                                    
                                    QMenu::item:selected {{
                                    background-color : {primary}
                                    }}
                                    """)
        
        self.menu.setStyleSheet(f"""
                                QMenu::item:selected {{
                                    background-color : {primary}
                                }}
                                """)

        self.taskNameLabel.setStyleSheet(f"font-size: 18px")

class Add_Task:
    def __init__(self, parent, mainlayout, task_name, prio, status,taskId, loadingData=False):
        self.set_font()
        
        self.loadingData = loadingData
        self.text = task_name
        self.status = status
        self.mainwindowlayout = mainlayout
        self.parent = parent
        self.text = self.text.strip()

        if self.text:
            self.check_box = TaskCheckBox(self.text, self.parent, prio, self.mainwindowlayout, self.status, taskId, self.loadingData)

            if self.status == 'done':
                self.check_box.setChecked(True)
                self.parent.doneTasksWidgetLayout.insertWidget(2, self.check_box) 
            if self.status == 'not done':
                self.check_box.setChecked(False) 
                self.mainwindowlayout.insertWidget(1, self.check_box, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.loadingData = False
        self.check_box.loadingData = False
            
    def set_font(self):
        path = './data/fonts/bfont.TTF'
        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        QApplication.setFont(QFont(fontfamily))

def start_animation(widget, color_from, color_to):
    animation = QVariantAnimation(widget)
    animation.setDuration(400)
    animation.setStartValue(QColor(qRgb(color_from[0], color_from[1], color_from[2])))
    animation.setEndValue(QColor(qRgb(color_to[0], color_to[1], color_to[2])))
    animation.valueChanged.connect(lambda value: change_color(widget, value.name()))
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
                            font-size: px
                            }}
                            """)
    
def get_color(prio):
    color = priority_none
    if prio == 'high':
        color = priority_high
    elif prio == 'mid':
        color = priority_mid
    elif prio == 'low':
        color = priority_low
        
    return color
