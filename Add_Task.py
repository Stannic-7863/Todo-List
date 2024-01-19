import datetime
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
    
    def __init__(self, text, parent, currentPriority, mainwindowlayout, status,taskId, loadingData):
        super().__init__()
        self.mainLayout = QHBoxLayout()
        self.loadingData = loadingData
        self.parent = parent
        self.setParent(self.parent)
        self.text = text
        self.currentPriority = currentPriority
        self.mainwindowlayout = mainwindowlayout
        self.status = status
        self.taskId = taskId
        
        self.color = get_color(self.currentPriority)
        changeColor(self, self.color)
        self.stateChanged.connect(self.onStateChange)
        
        self.taskNameEdit = QLineEdit(self, self.color) 

        self.taskNameLabel = QLabel()
        self.taskNameLabel.setText(self.text)
        self.taskNameLabel.setWordWrap(True)
        
        self.buttonsLayout = QHBoxLayout()
        self.buttonsWidget = QWidget()
        self.buttonsWidget.setLayout(self.buttonsLayout)
        
        self.optionMenu = self.createOptionMenu()
        self.infoButton = QToolButton()
        self.isInfoToggled = False
        self.infoButton.setText('Info button')
        self.infoButton.clicked.connect(self.checkOtherToggled)
        
        self.mainLayout.addWidget(self.taskNameLabel)
        self.buttonsLayout.addWidget(self.infoButton, alignment=Qt.AlignmentFlag.AlignRight)
        self.buttonsLayout.addWidget(self.optionMenu, alignment= Qt.AlignmentFlag.AlignRight)
        self.mainLayout.addWidget(self.buttonsWidget, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.mainLayout)
        self.mouse_inside = False
        
        self.updateMainStyleSheet(self.color)
        
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
        pomodoro.triggered.connect(lambda : self.parent.pomodoroWidget.getTask(self.text, self.taskId))
        self.menu.addAction(pomodoro)
        
        delete = QAction('Delete', self)
        delete.triggered.connect(lambda : self.delete_task(self))
        self.menu.addAction(delete)

        return self.menu
    
    def get_edit_task(self):
        self.taskNameLabel.setFixedWidth(0)
        self.taskNameEdit.show()
        self.taskNameEdit.setFocus()
        self.mainLayout.insertWidget(1, self.taskNameEdit)
        
        edit_height = self.taskNameEdit.height()
        self.setMaximumHeight(edit_height+30)
        
    def set_edit_task(self):
        updateTaskName(self.taskId, self.taskNameEdit.text().strip())
        self.mainLayout.removeWidget(self.taskNameEdit)
        self.taskNameLabel.setText(self.taskNameEdit.text().strip())
        self.taskNameEdit.clear()
        self.taskNameEdit.hide()
        self.taskNameEdit.clearFocus()
        self.taskNameLabel.setMaximumWidth(1000)
        text_height = self.taskNameLabel.height()
        height = self.height()
        self.setMaximumHeight(text_height+height)
    
    def create_sub_menu_priority(self):
        priority_menu = QMenu('Set Priority', parent=self.parent)
        priority_menu.setStyleSheet(f"QMenu::item:selected {{ background-color : {primaryColor}}}")
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
        previous_prio = self.currentPriority
        current_color = self.color
        self.currentPriority = prio
        self.color = get_color(prio)
        if self.isChecked() == False:
            colorChangeAnimation(self, current_color , self.color)

        change_priority_db(previous_prio, self.currentPriority, self.taskId)
        if not self.loadingData:    
            self.update_graphs()

    def onStateChange(self, value):
        state = Qt.CheckState(value)
        prevStatus = self.status

        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        
        text_height = self.taskNameLabel.height()
        height = self.height()
        self.setMaximumHeight(text_height+height)
        
        if state == Qt.CheckState.Unchecked:
            self.updateMainStyleSheet(self.color)
            self.status = 'not done'
            self.parent.doneTasksWidgetLayout.removeWidget(self)
            self.mainwindowlayout.insertWidget(1, self)
            if not self.loadingData: 
                change_status_db(prevStatus, self.status, self.taskId, formatted_date) 
        
        if state == Qt.CheckState.Checked:
            self.updateMainStyleSheet(taskDoneColor)
            self.status = 'done'
            self.mainwindowlayout.removeWidget(self)
            self.parent.doneTasksWidgetLayout.insertWidget(2, self)
            if not self.loadingData:
                change_status_db(prevStatus, self.status, self.taskId, formatted_date)

        if not self.loadingData:  
            self.updateGraphs() 
        
    def updateGraphs(self):
        self.parent.priorityBarChart.update()
        self.parent.piegraph.update()    
    
    def delete_task(self, widget: QCheckBox):
        delete_task_db(self.taskId)
        widget.deleteLater()
        self.update_graphs()

    def updateMainStyleSheet(self, color):     
        self.setStyleSheet(f"""
                        QWidget {{
                            background : {color}
                        }}
                        
                        QMenu {{
                            background : {backgroundColor} 
                        }}
                        
                        QToolButton {{
                            background-color : transparent;
                        }}
                                    
                        QToolButton::menu-indicator {{
                            image: none;
                        }}
                                    
                        QMenu::item:selected {{
                            background-color : {primaryColor}
                        }}
                        QMenu::item:selected {{
                            background-color : {primaryColor}
                        }}
                        QCheckBox::indicator {{
                            image: none;
                        }}
                        QCheckBox::indicator:checked {{
                            image: none;
                        }}
                        QCheckBox {{
                            background-color: {color};
                            color: white;
                            padding: 30px;
                            border-radius: 5px;
                            border : none
                            }}
                        QLabel {{
                            font-size : 18px
                        }}
                        
                        QLineEdit {{
                            background-color : {color};
                            border-radius : 5px
                        }}
                        """)
    
    def enterEvent(self, event):
        self.mouse_inside = True    
    def leaveEvent(self, event):
        self.mouse_inside = True
    def mousePressEvent(self, event):
        if self.mouse_inside:
            if event.button() == Qt.MouseButton.LeftButton:
                self.setChecked(not self.isChecked())

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
            self.taskCheckBox = TaskCheckBox(self.text, self.parent, prio, self.mainwindowlayout, self.status, taskId, self.loadingData)

            if self.status == 'done':
                self.taskCheckBox.setChecked(True)
                self.parent.doneTasksWidgetLayout.insertWidget(2, self.taskCheckBox) 
            if self.status == 'not done':
                self.taskCheckBox.setChecked(False) 
                self.mainwindowlayout.insertWidget(1, self.taskCheckBox, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.loadingData = False
        self.taskCheckBox.loadingData = False
            
    def set_font(self):
        path = './data/fonts/bfont.TTF'
        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        QApplication.setFont(QFont(fontfamily))

def colorChangeAnimation(widget, color_from, color_to):
    animation = QVariantAnimation(widget)
    animation.setDuration(1000)
    animation.setStartValue(QColor(color_from))
    animation.setEndValue(QColor(color_to))
    animation.valueChanged.connect(lambda value: changeColor(widget, value.name()))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

def changeColor(widget, color):
    widget.updateMainStyleSheet(color)
    
def get_color(prio):
    color = priorityNoneColor
    if prio == 'high':
        color = priorityHighColor
    elif prio == 'mid':
        color = priorityMidColor
    elif prio == 'low':
        color = priorityLowColor
        
    return color
