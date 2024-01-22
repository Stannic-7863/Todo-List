from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from settings import *
from db_data_functions import *
import datetime

class TaskCheckBox(QCheckBox):    
    activeInstance = None
    
    def __init__(self, parent: QMainWindow, taskName: str, priority: str, status: str, taskId: int, loadingData: bool) -> QCheckBox:
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.status = status
        self.taskId = taskId
        self.taskName = taskName
        self.loadingData = loadingData
        self.currentPriority = priority
        
        self.taskNameLabel = QLabel()
        self.taskNameLabel.setText(self.taskName)
        self.taskNameLabel.setWordWrap(True)
        
        self.buttonsLayout = QHBoxLayout()
        self.buttonsWidget = QWidget()
        self.buttonsWidget.setLayout(self.buttonsLayout)
        
        self.optionMenu = self.createOptionMenu()
        self.infoButton = QToolButton()
        self.isInfoToggled = False
        self.infoButton.setText('Info button')
        self.infoButton.clicked.connect(self.checkOtherToggled)
        
        self.layout.addWidget(self.taskNameLabel)
        self.buttonsLayout.addWidget(self.infoButton, alignment=Qt.AlignmentFlag.AlignRight)
        self.buttonsLayout.addWidget(self.optionMenu, alignment= Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.buttonsWidget, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)
        self.mouse_inside = False
        
        self.color = get_color(self.currentPriority)
        self.stateChanged.connect(self.onStateChange)
        changeColor(self, self.color)

        self.updateMainStyleSheet(self.color)
        
        if self.taskName:       
            if self.status == 'done':
                self.setChecked(True)
                self.parent.doneTaskView.addTask(self) 
            if self.status == 'not done':
                self.setChecked(False) 
                self.parent.taskView.addTask(self)
    
        
    def checkOtherToggled(self) -> None:
        self.isInfoToggled = not self.isInfoToggled
        if self.isInfoToggled:
            if TaskCheckBox.activeInstance and TaskCheckBox.activeInstance != self : 
                TaskCheckBox.activeInstance.isInfoToggled = False
                
            TaskCheckBox.activeInstance = self
        else: 
            TaskCheckBox.activeInstance = None
        
        self.parent.taskInfoView.toggle(self.isInfoToggled, self.taskId, self)

        
    def createOptionMenu(self) -> QToolButton:
        """Create the options Button to hold the option menu"""

        self.options = QToolButton()
        self.options.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.options.setIcon(QIcon('./data/icons/menu.png'))
        self.options.setIconSize(QSize(30, 30))
        self.options.setMenu(self.createMenu()) 
        
        return self.options
    
    def createMenu(self) -> QMenu:
        """Create menu"""
        self.menu = QMenu(self)    
        delete = QAction('Delete', self)
        pomodoro = QAction('Pomdoro', self)
        
        self.menu.addAction(pomodoro)
        self.menu.addAction(delete)
        
        delete.triggered.connect(self.delete_task)
        pomodoro.triggered.connect(lambda : self.parent.pomodoroWidget.getTask(self.taskName, self.taskId))

        self.create_sub_menu_priority()

        return self.menu
    
    def create_sub_menu_priority(self) -> None:
        """Create the menu to change priority and add it to the options menu"""
        priority_menu = QMenu('Set Priority', parent=self.parent)
        priority_menu.setStyleSheet(f"QMenu::item:selected {{ background-color : {primaryColor}}}")
        action_group = QActionGroup(self.parent)
        m_high = QAction('High', parent=self.parent, checkable=True)
        m_mid = QAction('Mid', parent=self.parent, checkable=True)
        m_low = QAction('Low', parent=self.parent, checkable=True)
        action_group.addAction(m_high)
        action_group.addAction(m_mid)
        action_group.addAction(m_low)
        m_high.toggled.connect(lambda : self.changePrio('high'))
        m_mid.toggled.connect(lambda : self.changePrio('mid'))
        m_low.toggled.connect(lambda : self.changePrio('low'))
        priority_menu.addAction(m_high)
        priority_menu.addAction(m_mid)
        priority_menu.addAction(m_low)
        self.menu.addMenu(priority_menu)
        
    def changePrio(self, prio):
        previous_prio = self.currentPriority
        current_color = self.color
        self.currentPriority = prio
        self.color = get_color(prio)
        if self.isChecked() == False:
            colorChangeAnimation(self, current_color , self.color)

        change_priority_db(previous_prio, self.currentPriority, self.taskId)
        if not self.loadingData:    
            self.updateGraphs()

    def onStateChange(self, value):
        state = Qt.CheckState(value)
        prevStatus = self.status

        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        
        self.updateHeight()
        
        if state == Qt.CheckState.Unchecked:
            self.updateMainStyleSheet(self.color)
            self.status = 'not done'
            self.parent.taskView.addTask(self)
            self.parent.doneTaskView.removeTask(self)
            
            if not self.loadingData: 
                change_status_db(prevStatus, self.status, self.taskId, formatted_date) 
        
        if state == Qt.CheckState.Checked:
            self.updateMainStyleSheet(taskDoneColor)
            self.status = 'done'
            self.parent.taskView.removeTask(self)
            self.parent.doneTaskView.addTask(self)
            
            if not self.loadingData:
                change_status_db(prevStatus, self.status, self.taskId, formatted_date)
    
        self.parent.statsView.update() 

        self.loadingData = False

    def updateTaskName(self, newName) -> None:
        """Update the task Name and write changes to the database"""
        self.taskNameLabel.setText(newName)
        self.updateHeight()

    def updateHeight(self)-> None:
        """Update height of the widget to correct height"""
        labelHeight = self.taskNameLabel.height()
        height = self.height()
        self.setMaximumHeight(labelHeight+height)   

    def delete_task(self, widget: QCheckBox):
        delete_task_db(self.taskId)
        self.updateGraphs()
        self.deleteLater()

    def enterEvent(self, event) -> bool:
        self.mouse_inside = True
        return self.mouse_inside    
    def leaveEvent(self, event) -> bool:
        self.mouse_inside = False
        return self.mouse_inside
    def mousePressEvent(self, event):
        if self.mouse_inside:
            if event.button() == Qt.MouseButton.LeftButton:
                self.setChecked(not self.isChecked())
                
    def updateMainStyleSheet(self, color) -> None:
        """Set main Style Sheet and update it if needed"""

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
                        """)

def colorChangeAnimation(widget, color_from, color_to):
    animation = QVariantAnimation(widget)
    animation.setDuration(1000)
    animation.setStartValue(QColor(color_from))
    animation.setEndValue(QColor(color_to))
    animation.valueChanged.connect(lambda value: changeColor(widget, value.name()))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

def changeColor(widget, color):
    widget.updateMainStyleSheet(color)
    
def get_color(prio) -> str:
    """
    Get the color depending on the Priority of the task
    """
    color = priorityNoneColor
    if prio == 'high':
        color = priorityHighColor
    elif prio == 'mid':
        color = priorityMidColor
    elif prio == 'low':
        color = priorityLowColor
        
    return color
