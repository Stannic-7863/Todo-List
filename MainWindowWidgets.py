from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from settings import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from db_data_functions import *
from CustomWidgets import *
from stat_widgets import *
from TaskWidget import *

class TaskView(QScrollArea):
    """Window where tasks are displayed"""
    def __init__(self, parent) -> None:    
        super().__init__()    
        self.parent = parent
        self.createWidgets()
        self.createButtons()
        self.addAllWidgets()
        self.setScrollArea()
        
    def createWidgets(self) -> None:
        self.taskViewLayout = QVBoxLayout()
        self.taskView = QWidget()
        self.taskView.setLayout(self.taskViewLayout)
    
        self.buttonsContainerLayout = QHBoxLayout()
        self.buttonsContainer = QWidget()
    
    def createButtons(self) -> None:
        self.addTaskButton = QPushButton()
        self.addTaskButton.setIcon(QIcon('./data/icons/plus.png'))
        self.addTaskButton.setIconSize(QSize(50,50))
        self.addTaskButton.setFixedWidth(200)
        self.addTaskButton.clicked.connect(self.onAddTaskButtonClicked)
    
    def addAllWidgets(self) -> None:
        self.buttonsContainerLayout.addWidget(self.addTaskButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.buttonsContainer.setLayout(self.buttonsContainerLayout)
    
    def setScrollArea(self) -> None:
        self.taskViewLayout.addWidget(self.buttonsContainer, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskViewLayout.addStretch()

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.taskView)
        self.setVerticalScrollBar(ScrollBar())
        
    def addTask(self, taskCheckbox) -> None:
        """Add a task into the container layout"""
        self.taskViewLayout.insertWidget(1, taskCheckbox)
        
    def removeTask(self, taskCheckbox) -> None:
        """Remove a task from the container layout"""
        self.taskViewLayout.removeWidget(taskCheckbox)
        
    def onAddTaskButtonClicked(self) -> None:
        """TaskAddButton press event handler"""
        getTaskFromUser = GetTaskFromUser(self.parent)
        self.taskViewLayout.insertWidget(1 , getTaskFromUser) 
    
class DoneTaskView(QScrollArea):
    """Window where tasks marked as done are shown"""
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.createWidgets()
        self.addAllWidgets()
        self.setScrollArea()
        self.setStyleSheet()
            
    def createWidgets(self) -> None:
        self.doneLabel = QLabel('Completed Tasks')
        
        self.doneTaskLabelFrame = QFrame()
        self.doneTaskLabelFrame.setFrameShape(QFrame.Shape.HLine)
        
        self.doneTaskView = QWidget()
        self.doneTaskViewLayout = QVBoxLayout()
        
    def addAllWidgets(self) -> None:
        self.doneTaskViewLayout.addWidget(self.doneLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.doneTaskViewLayout.addWidget(self.doneTaskLabelFrame)
        self.doneTaskViewLayout.addStretch()
        
        self.doneTaskView.setLayout(self.doneTaskViewLayout)
        
    def setScrollArea(self) -> None:
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.doneTaskView)
        self.setVerticalScrollBar(ScrollBar())
    
    def addTask(self, taskCheckBox) -> None:
        """Add task into the taskdone window"""
        self.doneTaskViewLayout.insertWidget(2, taskCheckBox)

    def removeTask(self, taskCheckBox) -> None:
        """Remove task from the taskdone window"""
        self.doneTaskViewLayout.removeWidget(taskCheckBox)
        
    def setStyleSheet(self):
        self.doneLabel.setStyleSheet(f'font-size: 30px; padding: 20px 0px 20px 0px')
        self.doneTaskLabelFrame.setStyleSheet(f'background: white')
        
class StatsView(QScrollArea):
    def __init__(self, parent) -> None:
        super().__init__()
                
        self.parent = parent

        self.statWidgetLayout = QVBoxLayout()
        self.statswidget = QWidget()
        self.statswidget.setLayout(self.statWidgetLayout)
        
        self.createStats()
        self.setScrollArea()
    
    def createStats(self) -> None:   
        self.createBarGraph()
        self.createPieGraph()
        
    def createBarGraph(self) -> None:
        self.priorityBarGraphWidget = QWidget()
        self.priorityBarGraphLayout = QVBoxLayout()
        self.priorityBarGraphWidget.setLayout(self.priorityBarGraphLayout)
        self.priorityBarGraph = PriorityBarGraph()
        barGraphVeiw = QtCharts.QChartView(self.priorityBarGraph)
        barGraphVeiw.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.priorityBarGraphLayout.addWidget(barGraphVeiw)
        self.statWidgetLayout.addWidget(self.priorityBarGraphWidget)
        
    def createPieGraph(self) -> None:
        self.piegraphWidgetLayout = QVBoxLayout()
        self.TaskPieGraphWidget = QWidget()
        self.TaskPieGraphWidget.setLayout(self.piegraphWidgetLayout)
        self.piegraph = PieGraph(self.parent)
        pieGraphVeiw = QtCharts.QChartView(self.piegraph)
        pieGraphVeiw.setRenderHint(QPainter.Antialiasing)
        self.piegraphWidgetLayout.addWidget(pieGraphVeiw)
        self.statWidgetLayout.addWidget(self.TaskPieGraphWidget)
    
    def updateGraphs(self) -> None:
        self.priorityBarGraph.update()
        self.piegraph.update()
    
    def setScrollArea(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.statswidget)
        self.setVerticalScrollBar(ScrollBar())
        self.setMaximumWidth((QApplication.primaryScreen().size().width())/2.5)
    
    def toggle(self) -> None:
        self.animation = QPropertyAnimation(self.statScrollArea, b"maximumWidth")
        
        if self.toggleButton.isChecked():
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.animation.setEndValue(QApplication.primaryScreen().size().width()/2.5)
        else:
            self.animation.setEndValue(0)
            self.animation.setEasingCurve(QEasingCurve.Type.InCubic)

        self.animation.setDuration(400)
        self.animation.start()

class TaskInfoView(QScrollArea):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.createWidgets()
        self.addAllWidgets()
        self.setScrollArea()
        
    def createWidgets(self) -> None:
        self.taskInfoWidget = QWidget()
        self.taskInfoWidgetLayout = QVBoxLayout()
        self.taskInfoWidget.setLayout(self.taskInfoWidgetLayout)
        
        self.taskNameEdit = QPlainTextEdit()
        self.taskNameEdit.installEventFilter(self)
        self.taskNameEdit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.taskNameEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.taskNameEdit.clearFocus()
        self.taskNameEdit.textChanged.connect(self.adjustTaskNameEditHeight)
    
        self.sessionDataVeiwWidget = QWidget()
        self.sessionDataVeiwWidgetLayout = QVBoxLayout()
        self.sessionDataVeiwWidget.setLayout(self.sessionDataVeiwWidgetLayout)
    
    def addAllWidgets(self) -> None:    
        self.taskInfoWidgetLayout.addWidget(self.taskNameEdit, alignment=Qt.AlignmentFlag.AlignTop)
        self.taskInfoWidgetLayout.addWidget(self.sessionDataVeiwWidget, alignment=Qt.AlignmentFlag.AlignLeft)
        self.taskInfoWidgetLayout.addStretch()
    
    def setScrollArea(self) -> None:
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.taskInfoWidget)
        self.setMaximumWidth(0)
        self.setVerticalScrollBar(ScrollBar())
    
    def displayTaskInfo(self, taskId) -> None:
        """Display info of current selected task"""
        taskName = getTaskName(taskId)
        self.taskNameEdit.setPlainText(taskName)
        
        for index in reversed(range(self.sessionDataVeiwWidgetLayout.count())):
            self.sessionDataVeiwWidgetLayout.itemAt(index).widget().deleteLater()
            
        chart = SessionTimeBarGraph(self.taskId)
        
        self.sessionDataVeiwWidgetLayout.addWidget(chart)
    
    def adjustTaskNameEditHeight(self):
        textHeight = self.taskNameEdit.document().size().height()
        self.taskNameEdit.setFixedHeight((textHeight * fontSize) + fontSize)
        
    def toggle(self, checked: bool, taskId: int, task: TaskCheckBox):
        """Toggle task info on or off"""
        self.taskId = taskId
        self.task = task
        self.animation = QPropertyAnimation(self, b'maximumWidth')
        
        maxWidth = QApplication.primaryScreen().size().width()//3.5
        
        if checked is True: 
            self.animation.setEndValue(0)
            self.animation.setEndValue(maxWidth)
            self.displayTaskInfo(self.taskId)
        else :     
            self.animation.setEndValue(maxWidth)
            self.animation.setEndValue(0)
        
        self.animation.setDuration(500)
        self.animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)  
    
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if source == self.taskNameEdit and self.taskNameEdit.hasFocus() is True:
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier: 
                    self.taskNameEdit.insertPlainText("\n")
                    return True
                elif event.key() == Qt.Key.Key_Return:
                    newName = self.taskNameEdit.toPlainText().strip()
                    updateTaskName(self.taskId, newName)
                    self.task.updateTaskName(newName)
                    self.taskNameEdit.clearFocus()
                    return True

        return super().eventFilter(source, event)
        
class NavMenu(QWidget):
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.isOpen = False
        self.setMaximumWidth(0)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(f"background-color: {backgroundDarkColor}")
        
        self.createNavItems()
        
    def createNavItems(self) -> None:
        """Creates all the required widgets"""
        titleLabel = NavMenuItemLabels('YARIKATA', self, self.parent.homeWidget)
        titleLabel.setStyleSheet("""font-size: 30px;""")
        seperation_frame = QFrame()
        seperation_frame.setFrameShape(QFrame.Shape.HLine)
        seperation_frame.setStyleSheet(f"background: white")
        seperation_frame.setFrameShadow(QFrame.Shadow.Sunken)
        
        self.layout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(seperation_frame)
        
        homeTab = NavMenuItemLabels('Home', parent=self.parent, assigned=self.parent.homeWidget)
        doneTaskTab = NavMenuItemLabels('Task Done', parent=self.parent, assigned=self.parent.doneTaskView)
        pomodoroTab = NavMenuItemLabels('Pomodoro', parent=self.parent, assigned=self.parent.pomodoroWidget)
        
        self.layout.addWidget(homeTab)
        self.layout.addWidget(doneTaskTab)
        self.layout.addWidget(pomodoroTab)
        self.layout.addStretch()
    
    def toggle(self) -> None:
        """Toggle the Navigation Menu on or off"""
        
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        
        if self.isOpen is True:
            self.animation.setEndValue(300)
            self.animation.setEasingCurve(QEasingCurve.Type.OutBack)
        else:
            self.animation.setEndValue(0)
            self.animation.setEasingCurve(QEasingCurve.Type.InBack)

        self.animation.setDuration(400)
        self.animation.start() 