from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from settings import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from db_data_functions import *
from CustomWidgets import *
from stat_widgets import *

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
        self.setMinimumWidth(70)
        self.setMaximumWidth(70)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(f"background-color: {backgroundDarkColor}")
        
        self.createNavItems()
        
    def createNavItems(self) -> None:
        """Creates all the required widgets"""

        homeTab = NavMenuItemLabels('Home', parent=self.parent, assigned=self.parent.homeWidget)
        doneTaskTab = NavMenuItemLabels('Task Done', parent=self.parent, assigned=self.parent.doneTaskView)
        pomodoroTab = NavMenuItemLabels('Pomodoro', parent=self.parent, assigned=self.parent.pomodoroWidget)
        
        self.layout.addStretch()
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
        
# Still to be refactored 


class Pomodoro(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setParent(self.parent)

        self.start_icon = QIcon('./data/icons/start.png')
        self.pause_icon = QIcon('./data/icons/pause.png')

        self.total_minutes = 1
        self.short_break_minute = 5
        self.long_break_minutes = 15
        self.elapsed_seconds =  0 
        self.currentSessionFocusTime = 0
        self.totalFocusTime = 0
        self.break_status = False
        self.current_long_break_interval = 0
        self.total_long_break_interval = 4
        
        self.total_seconds = self.total_minutes * 60
        self.short_break_seconds = self.short_break_minute * 60
        self.long_break_seconds = self.long_break_minutes * 60
        
        self.display_time = 0
        self.display_time_total = self.total_seconds
        self.total_rounds = 4
        self.current_rounds = 0
        
        self.sessionId = None
        self.taskId = None
        self.isSessionActive = False

        self.display_timer = QTimer()
        self.display_timer.setInterval(1000)
        self.display_timer.timeout.connect(self.update_clock_values)
        
        self.timer = QTimer()
        self.timer.setInterval(self.total_seconds*1000)
        self.timer.timeout.connect(self.break_time)
        
        self.short_break_timer = QTimer()
        self.short_break_timer.setInterval(self.short_break_seconds*1000)
        self.short_break_timer.timeout.connect(self.break_over)
        
        self.long_break_timer = QTimer()
        self.long_break_timer.setInterval(self.long_break_seconds*1000)
        self.long_break_timer.timeout.connect(self.break_over)
        
        self.quote = 'Focus'
        self.status = 'focus'


        self.container_widget = QWidget()
        self.container_widget_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_widget_layout)

        self.headerWidget = QWidget()
        self.headerWidgetLayout = QHBoxLayout()
        self.headerWidget.setLayout(self.headerWidgetLayout)

        self.add_task_button = QPushButton()
        self.add_task_button.setIcon(QIcon('./data/icons/plus.png'))
        self.add_task_button.setIconSize(QSize(50,50))

        self.get_task_name = Custom_QLineEdit(self)
        self.get_task_name.setMaximumWidth(0)
        self.get_task_name.clearFocus()
        self.get_task_name.setPlaceholderText('What are you working on today?')
        self.get_task_name.setStyleSheet(f"""QLineEdit {{
                                        padding: 8px 8px 8px 8px;
                                        border: none;
                                        border-bottom: 1px solid white;
                                        font-size: 20px;
                                        }}
                                        """)  
        
        self.taskNameLabel = Custom_QLabel(self.createTaskMenu())
        self.taskNameLabel.setMaximumWidth(0)
        
        self.headerWidgetLayout.addStretch()
        self.headerWidgetLayout.addWidget(self.get_task_name, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerWidgetLayout.addWidget(self.add_task_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerWidgetLayout.addWidget(self.taskNameLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.headerWidgetLayout.addStretch()

        self.body_widget = QWidget()
        self.body_widget_layout = QVBoxLayout()
        self.body_widget.setLayout(self.body_widget_layout)
        
        self.clock_widget = PomodoroClock()
        self.clock_widget.total_rounds = self.total_rounds

        self.body_widget_layout.addStretch()
        self.body_widget_layout.addWidget(self.clock_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.body_widget_layout.addStretch()

        self.start_pause_button = QPushButton()
        self.start_pause_button.setIcon(self.start_icon)
        self.start_pause_button.setIconSize(QSize(40,40))

        self.footer_widget = QWidget()
        self.footer_widget_layout = QHBoxLayout()
        self.footer_widget.setLayout(self.footer_widget_layout)

        self.footer_widget_layout.addWidget(self.start_pause_button)

        self.container_widget_layout.addWidget(self.headerWidget, alignment=Qt.AlignmentFlag.AlignTop)
        self.container_widget_layout.addWidget(self.body_widget)
        self.container_widget_layout.addWidget(self.footer_widget, alignment=Qt.AlignmentFlag.AlignJustify)

        self.set_button_style_sheet(self.add_task_button)
        self.set_button_style_sheet(self.start_pause_button)

        self.add_task_button.pressed.connect(self.onAddTaskButtonClicked)
        self.start_pause_button.pressed.connect(self.start_pause_pomodoro)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.container_widget)
        self.setLayout(self.main_layout)
        
    def createTaskMenu(self):
        self.task_menu = QToolButton()
        self.task_menu.setIcon(QIcon('./data/icons/menu.png'))
        self.task_menu.setIconSize(QSize(50, 50))
        self.task_menu.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        menu = QMenu(self.parent)
        
        edit = QAction('Edit', self.parent)
        edit.triggered.connect(self.editTaskName)
        remove = QAction('Remove', self.parent)
        remove.triggered.connect(self.endCurrentPomodoro)
        
        menu.addAction(edit)
        menu.addAction(remove)
        
        self.task_menu.setMenu(menu)
        
        return self.task_menu
        
    def editTaskName(self):
        self.get_task_name.clear()
        self.get_task_name.setText(self.taskNameLabel.text())
        
        self.animate_set_task(animate_open=False)
        self.animate_get_task(animate_open=True)
        self.get_task_name.editing = True
    
    def updateTaskName(self):
        task_name = self.get_task_name.text()
        updateTaskName(self.taskId, task_name)
        self.taskNameLabel.setText(task_name)
        self.animate_get_task(animate_open=False)
        self.animate_set_task(animate_open=True)
    
    def endCurrentPomodoro(self):
        self.elapsed_seconds =  0 
        self.currentSessionFocusTime = 0
        self.totalFocusTime = 0
        self.break_status = False
        self.current_long_break_interval = 0
        
        self.display_time = 0
        self.display_time_total = self.total_seconds
        self.total_rounds = 4
        self.current_rounds = 0
        
        self.sessionId = None
        self.taskId = None
        self.isSessionActive = False
        
        if self.display_timer.isActive() == True:
            self.start_pause_pomodoro()
        
        self.taskNameLabel.setText("")
        
        self.animate_add_task_button(True, False)
        self.animate_get_task(False)
        
        self.clock_widget.repaint()
        
    def onAddTaskButtonClicked(self):
        self.animate_add_task_button(animate_open=False, animate_open_get_task=True)
    
    def setTask(self):
        text = self.get_task_name.text()
        dateCreated = datetime.datetime.now()
        dateCreated = dateCreated.strftime('%Y-%m-%d')
        self.taskNameLabel.setText(text)
        self.taskId = commit_new_task_data(text, dateCreated, 'none', 'not done', None)
        self.totalFocusTime = 0
        
        self.animate_add_task_button(animate_open=False, animate_open_get_task=False)
        self.animate_set_task(animate_open=True)
        
    def getTask(self, text, taskId):
        self.taskNameLabel.setText(text)
        self.taskId = taskId
        self.pomodoroId = fetchPomodoroId(self.taskId)
        self.parent.stackedContainerLayout.setCurrentWidget(self.parent.pomodoroWidget) 
        
        self.animate_add_task_button(animate_open=False, animate_open_get_task=False)
        self.animate_set_task(animate_open=True)
        
    def animate_set_task(self, animate_open):
        self.set_task_animation = QPropertyAnimation(self.taskNameLabel, b"maximumWidth")
        self.set_task_animation.setStartValue(self.taskNameLabel.width())
        if animate_open == True:
            self.set_task_animation.setEndValue(600)
        else:
            self.set_task_animation.setEndValue(0)
        self.set_task_animation.setEasingCurve(QEasingCurve.Type.InExpo)
        self.set_task_animation.setDuration(1500)
        self.set_task_animation.start()
    
    def animate_add_task_button(self, animate_open, animate_open_get_task):
        self.animation_task_button = QPropertyAnimation(self.add_task_button, b'maximumWidth')
        self.animation_task_button.setStartValue(self.add_task_button.width())
        
        if animate_open == True:
            self.animation_task_button.setEndValue(50)
        else:
            self.animation_task_button.setEndValue(0)
            
        self.animation_task_button.setEasingCurve(QEasingCurve.Type.InCubic)
        self.animation_task_button.finished.connect(lambda : self.animate_get_task(animate_open=animate_open_get_task))
        self.animation_task_button.start()

    def animate_get_task(self, animate_open):
        self.animation_get_task = QPropertyAnimation(self.get_task_name, b'minimumWidth')
        self.animation_get_task.setStartValue(self.get_task_name.width())
        
        if animate_open == True:
            self.animation_get_task.setEndValue(400)
            self.animation_get_task.setEasingCurve(QEasingCurve.Type.OutBack)
            self.get_task_name.setFocus()
        
        else:
            self.animation_get_task.setEndValue(0)
            self.animation_get_task.setEasingCurve(QEasingCurve.Type.InBack)
            self.get_task_name.clearFocus()
        
        self.animation_get_task.setDuration(500)
        self.animation_get_task.start()
    
    def break_time(self):
        self.timer.stop()
        if self.current_long_break_interval >= self.total_long_break_interval:
            self.long_break_timer.start()
            self.display_time_total = self.long_break_seconds
            self.quote = 'Long Break'
            self.status = 'long break'
            self.clock_widget.get_change_color(taskColor, longBreakColor)
            self.current_long_break_interval = 0
        else: 
            self.short_break_timer.start()
            self.display_time_total = self.short_break_seconds
            self.quote = 'Short Break'
            self.status = 'short break'
            self.clock_widget.get_change_color(taskColor, shortBreakColor)
        self.break_status = True
        self.display_time = 0
    
    def break_over(self):
        if self.long_break_timer.isActive():
            self.long_break_timer.stop()
            self.clock_widget.get_change_color(longBreakColor, taskColor)
        if self.short_break_timer.isActive():
            self.long_break_timer.stop()
            self.clock_widget.get_change_color(shortBreakColor, taskColor)
        self.timer.start()
        self.current_rounds += 1
        self.current_long_break_interval += 1

        if self.current_rounds >= self.total_rounds:
            self.total_rounds = self.current_rounds
        self.break_status = False
        self.display_time = 0 
        self.display_time_total = self.total_seconds
        self.quote = 'Focus'
        self.status = 'focus'

    def start_pause_pomodoro(self):
        if self.sessionId:
            if self.isSessionActive == False: 
                self.sessionId = insertNewSessionData(self.pomodoroId)
                self.totalFocusTime = fetchTaskTotalFocusTime(self.pomodoroId)
                self.isSessionActive = True
        
        if self.display_timer.isActive() == False:
            self.start_pause_button.setIcon(self.pause_icon)
            self.display_timer.start()
            if self.status == 'focus':
                self.timer.start()
            if self.status == 'long break':
                self.long_break_timer.start()
            if self.status == 'short break':
                self.short_break_timer.start()
        else:
            self.start_pause_button.setIcon(self.start_icon)
            self.display_timer.stop()
            self.timer.stop()
            self.long_break_timer.stop()
            self.short_break_timer.stop()
        
    def update_clock_values(self):
        self.elapsed_seconds += 1
        self.display_time += 1
        if self.break_status == False:
            self.currentSessionFocusTime += 1
            self.totalFocusTime += 1
            if self.taskId:
                update_pomodoro_data(self.pomodoroId, self.current_rounds, self.totalFocusTime)
        
        if self.sessionId:
            updateSessionData(self.sessionId, self.elapsed_seconds, self.currentSessionFocusTime)

        total_time, time = self.get_formatted_time()
        self.clock_widget.set_value(self.display_time, self.display_time_total, time, total_time, self.total_rounds, self.current_rounds, self.quote)
        
    def get_formatted_time(self):
        display_minute, display_elapsed_seconds = divmod(self.display_time, 60)
        total_minutes, total_seconds = divmod(self.elapsed_seconds, 60)
        total_hour, total_minutes = divmod(total_minutes, 60)
        
        return "{:02d}:{:02d}:{:02d}".format(total_hour, total_minutes, total_seconds) ,"{:02d}:{:02d}".format(display_minute, display_elapsed_seconds)
    
    def set_button_style_sheet(self, widget):
        widget.setStyleSheet(f"""QPushButton {{
                            border-radius: 5px;
                            border: none; 
        }}""")
        
class Custom_QLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.editing = False

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.parent.animate_add_task_button(animate_open=True, animate_open_get_task=False)
        if event.key() == Qt.Key_Return and self.editing == False:
            self.parent.setTask()
        if event.key() == Qt.Key_Return and self.editing == True:
            self.parent.updateTaskName()
            self.editing = False

        super().keyPressEvent(event)
        
class Custom_QLabel(QWidget):
    def __init__(self, options):
        super().__init__() 
        self.label = QLabel()
        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(options)
        
        self.setStyleSheet(f"""QLabel {{
                        font-size: 30px;
                        font-weight: 50; 
                        }}
                        QToolButton {{
                            border: none
                        }}
                        QToolButton:menu-indicator {{
                            image:none
                        }}
                        """)

    def setText(self, text):
        self.label.setText(text)
        
    def text(self):
        return self.label.text()


# Additional Classes used by the Classes above

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
        
class GetTaskFromUser(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.setMaximumHeight(200)
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
        TaskCheckBox(self.parent ,taskName, priority, 'not done', task_id)

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
