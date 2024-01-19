from settings import *
from custom_widgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6 import QtCharts
from db_data_functions import *
from stat_widgets import *
from pomodoro import Pomodoro

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        setupDatabase()
        self.font_init()
        self.gettingTask = False
        self.isTabMenuOpen = False
        self.ui_init()
        self.setMouseTracking(True)

    def font_init(self):
        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        self.setFont(QFont(fontfamily))
        QApplication.setFont(QFont(fontfamily))

    def ui_init(self):
        self.setWindowTitle('Yarikata')
        self.setMinimumHeight(800)
        self.setMinimumWidth(400)

        self.centralLayout = QHBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralLayout)
        self.centralWidget.setMouseTracking(True)

        self.homeWidget = QWidget()
        self.homeWidget.setLayout(QHBoxLayout())

        self.taskwidget = QWidget()
        self.taskwidgetLayout = QVBoxLayout()
        self.taskwidget.setLayout(self.taskwidgetLayout)

        self.statswidget = QWidget()
        self.statWidgetLayout = QVBoxLayout()
        self.statswidget.setLayout(self.statWidgetLayout)
        
        self.addTaskButton = QPushButton()
        self.addTaskButton.setIcon(QIcon('./data/icons/plus.png'))
        self.addTaskButton.setIconSize(QSize(50,50))
        self.addTaskButton.setContentsMargins(0,0,0,0)
        self.addTaskButton.clicked.connect(self.onAddtaskClicked)

        self.toggleStatsButton = QRadioButton()

        self.toggleStatsButton.setChecked(True)
        self.toggleStatsButton.toggled.connect(self.toggleStats)
        self.addTaskButton.setFixedWidth(200)
        self.buttonsContainerLayout = QHBoxLayout()
        self.buttonsContainer = QWidget()
        self.buttonsContainerLayout.addWidget(self.addTaskButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.buttonsContainerLayout.addWidget(self.toggleStatsButton, Qt.AlignmentFlag.AlignRight)
        self.buttonsContainer.setLayout(self.buttonsContainerLayout)
        self.taskwidgetLayout.addWidget(self.buttonsContainer, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskwidgetLayout.addStretch()
    
        self.TaskPieGraphWidget = QWidget()
        self.piegraphWidgetLayout = QVBoxLayout()
        self.TaskPieGraphWidget.setLayout(self.piegraphWidgetLayout)
        
        self.piegraph = PieGraph(self)
        pieChartVeiw = QtCharts.QChartView(self.piegraph)
        pieChartVeiw.setRenderHint(QPainter.Antialiasing)
        self.piegraphWidgetLayout.addWidget(pieChartVeiw)

        self.priorityBarChartWidget = QWidget()
        self.priorityBarChartLayout = QVBoxLayout()
        self.priorityBarChartWidget.setLayout(self.priorityBarChartLayout)
        self.priorityBarChart = PriorityBarChart()
        barChartVeiw = QtCharts.QChartView(self.priorityBarChart)
        barChartVeiw.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.priorityBarChartLayout.addWidget(barChartVeiw)

        self.statWidgetLayout.addWidget(self.priorityBarChartWidget)
        self.statWidgetLayout.addWidget(self.TaskPieGraphWidget)

        self.taskScroll = QScrollArea()
        self.taskScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.taskScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.taskScroll.setWidgetResizable(True)
        self.taskScroll.setWidget(self.taskwidget)
        customScrollTask = Custom_Scroll_Bar()
        self.taskScroll.setVerticalScrollBar(customScrollTask)

        self.statScroll = QScrollArea()
        self.statScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.statScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.statScroll.setWidgetResizable(True)
        self.statScroll.setWidget(self.statswidget)
        customScrollStat = Custom_Scroll_Bar()
        self.statScroll.setVerticalScrollBar(customScrollStat)
        self.statScroll.setMaximumWidth((QApplication.primaryScreen().size().width())/2.5)

        self.stackedContainerWidget = QWidget()
        self.stackedContainerLayout = QStackedLayout()
        self.stackedContainerWidget.setLayout(self.stackedContainerLayout)
        
        self.navMenuWidget = QWidget()
        self.navMenuWidget.setMaximumWidth(0)
        self.navMenuWidgetLayout = QVBoxLayout()
        self.navMenuWidget.raise_()
        self.navMenuWidget.setLayout(self.navMenuWidgetLayout)
        self.navMenuWidget.setStyleSheet(f"background-color: {backgroundDarkColor}; border-radius: 7px")
        titleLabel = ItemLable('YARIKATA', self.stackedContainerLayout, self.homeWidget)
        titleLabel.setStyleSheet("""
                                font-size: 30px;
                                """)
        seperation_frame = QFrame()
        seperation_frame.setFrameShape(QFrame.Shape.HLine)
        seperation_frame.setStyleSheet(f"background: white")
        seperation_frame.setFrameShadow(QFrame.Shadow.Sunken)


        self.doneTaskWidget = QWidget()
        doneLabel = QLabel('Completed Tasks')
        doneLabel.setStyleSheet(f'font-size: 30px; padding: 20px 0px 20px 0px')
        doneTaskLabelFrame = QFrame()
        doneTaskLabelFrame.setFrameShape(QFrame.Shape.HLine)
        doneTaskLabelFrame.setStyleSheet(f'background: white')
        
        self.doneTasksWidgetLayout = QVBoxLayout()
        self.doneTasksWidgetLayout.addWidget(doneLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.doneTasksWidgetLayout.addWidget(doneTaskLabelFrame)
        self.doneTasksWidgetLayout.addStretch()
        self.doneTaskWidget.setLayout(self.doneTasksWidgetLayout)

        self.taskInfoWidget = QWidget()
        self.taskInfoWidgetLayout = QVBoxLayout()
        self.taskInfoWidget.setLayout(self.taskInfoWidgetLayout)
        
        self.taskInfoScrollArea = QScrollArea()
        self.taskInfoScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.taskInfoScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.taskInfoScrollArea.setWidgetResizable(True)
        self.taskInfoScrollArea.setWidget(self.taskInfoWidget)
        self.taskInfoScrollArea.setMaximumWidth(0)
        
        self.taskNameEdit = QPlainTextEdit()
        self.taskNameEdit.installEventFilter(self)
        self.taskNameEdit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.taskNameEdit.textChanged.connect(self.adjustTaskNameEditHeight)
        self.taskNameEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.taskNameEdit.clearFocus()
        self.taskStatsWidgetLayout = QVBoxLayout()
        self.taskStatsWidget = QWidget()
        self.taskStatsWidget.setLayout(self.taskStatsWidgetLayout)

        self.taskInfoWidgetLayout.addWidget(self.taskNameEdit, alignment=Qt.AlignmentFlag.AlignTop)
        self.taskInfoWidgetLayout.addWidget(self.taskStatsWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        doneTaskScrollArea = QScrollArea()
        doneTaskScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        doneTaskScrollArea.setWidgetResizable(True)
        doneTaskScrollArea.setWidget(self.doneTaskWidget)
        doneTaskScrollBar = Custom_Scroll_Bar()
        doneTaskScrollArea.setVerticalScrollBar(doneTaskScrollBar)

        self.pomodoroWidget = Pomodoro(self)
        homeTabLabel = ItemLable('Home', self.stackedContainerLayout, self.homeWidget)
        tasksDoneTabLabel = ItemLable('Task Done', self.stackedContainerLayout, doneTaskScrollArea)
        pomodoroTabLabel = ItemLable('Pomodoro', self.stackedContainerLayout, self.pomodoroWidget)

        self.setNavTabStyleSheet(homeTabLabel)
        self.setNavTabStyleSheet(tasksDoneTabLabel)
        self.setNavTabStyleSheet(pomodoroTabLabel)

        self.navMenuWidgetLayout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.navMenuWidgetLayout.addWidget(seperation_frame)
        self.navMenuWidgetLayout.addWidget(homeTabLabel)
        self.navMenuWidgetLayout.addWidget(tasksDoneTabLabel)
        self.navMenuWidgetLayout.addWidget(pomodoroTabLabel)
        self.navMenuWidgetLayout.addStretch()

        self.stackedContainerLayout.addWidget(self.homeWidget)
        self.stackedContainerLayout.addWidget(doneTaskScrollArea)
        self.stackedContainerLayout.addWidget(self.pomodoroWidget)
        self.stackedContainerLayout.setCurrentWidget(self.homeWidget) 

        self.homeWidget.layout().addWidget(self.taskScroll)
        self.homeWidget.layout().addWidget(self.statScroll)
        self.homeWidget.layout().addWidget(self.taskInfoScrollArea)
        self.centralLayout.addWidget(self.navMenuWidget, Qt.AlignmentFlag.AlignTop)
        self.centralLayout.addWidget(self.stackedContainerWidget)
        self.setCentralWidget(self.centralWidget)
        
        data = fetch_data()
        for items in data:
            taskName, prio, status, category, taskId = items
            Add_Task(self, self.taskwidgetLayout, taskName, prio, status, taskId, True)

        self.showMaximized()
        
        self.setStyleSheet(f"""
                        QWidget {{
                            background-color: {backgroundColor}; 
                            color: white;
                        }}
                        QPlainTextEdit {{
                            border : none;
                            font : {fontSize}px;
                            padding-top : 8px;
                        }}
                        QPlainTextEdit:focus {{
                            border : 1px solid white;
                            border-radius : 10px
                        }}
                        """)
        
        self.toggleStatsButton.setStyleSheet(f"""
                                        QRadioButton::indicator {{
                                            background: {primaryColor};
                                            border-radius: 2px;
                                        }}
                                        QRadioButton::indicator:checked {{
                                            background: {priorityMidColor}; 
                                        }}""")
        
        self.statswidget.setStyleSheet("""
                                    QWidget {{
                                        border-radius : 5px;
                                    }}
                                    """)
        
        self.addTaskButton.setStyleSheet(f"""
                                QPushButton {{
                                    color: white;
                                    background-color: none;
                                    padding: 10px;
                                    border: 2px solid white;
                                    border-radius: 12px;
                                }}
                                QPushButton:hover {{
                                    background-color: {primaryColor}
                                }}
                                """)
    
    def setNavTabStyleSheet(self, widget):
        widget.setStyleSheet(f"""
                            QLabel {{
                                font-size: 15px;
                                border-radius: 3px;
                                padding: 5px 2px 5px 2px;
                            }}
                            QLabel::hover {{
                                background-color : {accentdarkColor}
                            }}
                            """)
    
    def displayTaskInfo(self, taskId):
        taskName = getTaskName(taskId)
        self.taskNameEdit.setPlainText(taskName)

    def onAddtaskClicked(self):
        if not self.gettingTask:
            self.gettingTask = True
            layout = QHBoxLayout()    
            self.placeholder_widget = QWidget()
            self.placeholder_widget.setLayout(layout)
            TaskWidget = GetTaskFromUser(self, self.taskwidgetLayout)
            layout.addWidget(TaskWidget)
            self.taskwidgetLayout.insertWidget(1 , self.placeholder_widget) 

            self.placeholder_widget.setStyleSheet(f"""
                                                background : {primaryColor}; 
                                                max-width: 2000; 
                                                border-radius: 5px
                                                """)
            
    def onTaskAdded(self):
        self.gettingTask = False
        self.piegraph.update_data()

    def adjustTaskNameEditHeight(self):
        textHeight = self.taskNameEdit.document().size().height()
        self.taskNameEdit.setFixedHeight((textHeight * fontSize) + fontSize)
    
    def toggleStats(self):
        currentWidth = self.statScroll.width()
        self.animation = QPropertyAnimation(self.statScroll, b"maximumWidth")
        
        if currentWidth == 0:
            newWidth = QApplication.primaryScreen().size().width()/2.5
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        else:
            newWidth = 0
            self.animation.setEasingCurve(QEasingCurve.Type.InCubic)

        self.animation.setDuration(400)
        self.animation.setStartValue(currentWidth)
        self.animation.setEndValue(newWidth)
        self.statWidgetLayout.removeWidget(self.priorityBarChartWidget)
        self.statWidgetLayout.removeWidget(self.TaskPieGraphWidget)
        self.animation.start()
        self.statWidgetLayout.addWidget(self.priorityBarChartWidget)
        self.statWidgetLayout.addWidget(self.TaskPieGraphWidget)
        
    def toggleTaskInfo(self, checked, taskId):
        if self.toggleStatsButton.isChecked():
            self.toggleStatsButton.setChecked(False)
        
        self.currentEditingTaskId = taskId
        
        self.showStateAnimation = QPropertyAnimation(self.taskInfoScrollArea, b'maximumWidth')
        self.showStateAnimation.setStartValue(self.taskInfoScrollArea.width())
        
        if checked is True : 
            self.showStateAnimation.setEndValue(0)
            self.showStateAnimation.setEndValue(400)
            self.displayTaskInfo(self.currentEditingTaskId)
        else :     
            self.showStateAnimation.setEndValue(400)
            self.showStateAnimation.setEndValue(0)
        
        self.showStateAnimation.setDuration(500)
        self.showStateAnimation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)  
    
    def toggleNavMenu(self):
        self.animation = QPropertyAnimation(self.navMenuWidget, b"maximumWidth")
        currentWidth = self.navMenuWidget.width()
        
        if self.isTabMenuOpen is True:
            newWidth = 300
            self.animation.setEasingCurve(QEasingCurve.Type.OutBack)
        else:
            self.animation.setEasingCurve(QEasingCurve.Type.InBack)
            newWidth = 0

        self.animation.setDuration(400)
        self.animation.setStartValue(currentWidth)
        self.animation.setEndValue(newWidth)
        self.animation.start()     
    
    def resizeEvent(self, event: QResizeEvent):
        if event.size().width() <= 600:
            self.toggleStatsButton.setChecked(False)
        if event.size().width() >= 600:
            self.toggleStatsButton.setChecked(True)

    def mousePressEvent(self, event):
        if QRect(0, 0, 60, 40).contains(event.pos()):
            self.isTabMenuOpen = not self.isTabMenuOpen
            self.toggleNavMenu()

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if source == self.taskNameEdit and self.taskNameEdit.hasFocus() is True:
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier: 
                    self.taskNameEdit.insertPlainText("\n")
                    return True
                elif event.key() == Qt.Key.Key_Return:
                    updateTaskName(self.currentEditingTaskId, self.taskNameEdit.toPlainText().strip())
                    self.taskNameEdit.clearFocus()
                    return True

        return super().eventFilter(source, event)
    
if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()
