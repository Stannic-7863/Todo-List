from settings import *
from custom_widgets import *
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QPainter, QResizeEvent
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import (QApplication,
                            QMainWindow,
                            QWidget,
                            QVBoxLayout,
                            QHBoxLayout,
                            QScrollArea,
                            QPushButton,
                            QFrame,
                            QStackedLayout
                            )
from PySide6 import QtCharts
from db_data_functions import fetch_data, get_task_status_count, setupDatabase
from stat_widgets import *
from pomodoro import Pomodoro

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        setupDatabase()
        self.font_init()
        self.getting_task = False
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
        self.toggleStatsButton.setStyleSheet(f"""QRadioButton::indicator {{
                                        background: {primary};
                                        border-radius: 2px;
        }}
                                            QRadioButton::indicator:checked {{
                                            background: rgb{priority_mid};
                                            }}
""")
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
    
        self.DoneUndoneTaskPieChartWidget = QWidget()
        self.piegraph_widget_layout = QVBoxLayout()
        self.DoneUndoneTaskPieChartWidget.setLayout(self.piegraph_widget_layout)
        
        task_status_data = self.getTaskStatusData()
        self.piegraph = PieGraph(task_status_data)
        pieChartVeiw = QtCharts.QChartView(self.piegraph)
        pieChartVeiw.setRenderHint(QPainter.Antialiasing)
        self.piegraph_widget_layout.addWidget(pieChartVeiw)

        self.priorityBarChartWidget = QWidget()
        self.priorityBarChartLayout = QVBoxLayout()
        self.priorityBarChartWidget.setLayout(self.priorityBarChartLayout)
        self.priorityBarChart = PriorityBarChart()
        barChartVeiw = QtCharts.QChartView(self.priorityBarChart)
        barChartVeiw.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.priorityBarChartLayout.addWidget(barChartVeiw)

        self.statWidgetLayout.addWidget(self.priorityBarChartWidget)
        self.statWidgetLayout.addWidget(self.DoneUndoneTaskPieChartWidget)

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

        self.stacked_display = QWidget()
        self.stackedLayout = QStackedLayout()
        self.stacked_display.setLayout(self.stackedLayout)
        
        self.navMenuWidget = QWidget()
        self.navMenuWidget.setMaximumWidth(0)
        self.navMenuWidgetLayout = QVBoxLayout()
        self.navMenuWidget.raise_()
        self.navMenuWidget.setLayout(self.navMenuWidgetLayout)
        self.navMenuWidget.setStyleSheet(f"background-color: {background_dark}; border-radius: 7px")
        titleLabel = ItemLable('YARIKATA', self.stackedLayout, self.homeWidget)
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
        
        self.taskInfoScroll = QScrollArea()
        self.taskInfoScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.taskInfoScroll.setWidgetResizable(True)
        self.taskInfoScroll.setWidget(self.taskInfoWidget)
        self.taskInfoScroll.setMaximumWidth(0)
        
        doneTaskScroll = QScrollArea()
        doneTaskScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        doneTaskScroll.setWidgetResizable(True)
        doneTaskScroll.setWidget(self.doneTaskWidget)
        custom_done_scroll = Custom_Scroll_Bar()
        doneTaskScroll.setVerticalScrollBar(custom_done_scroll)

        self.pomodoroWidget = Pomodoro(self)
        homeTabLabel = ItemLable('Home', self.stackedLayout, self.homeWidget)
        tasksDoneTabLabel = ItemLable('Task Done', self.stackedLayout, doneTaskScroll)
        pomodoroTabLabel = ItemLable('Pomodoro', self.stackedLayout, self.pomodoroWidget)

        self.set_tab_style_sheet(homeTabLabel)
        self.set_tab_style_sheet(tasksDoneTabLabel)
        self.set_tab_style_sheet(pomodoroTabLabel)

        self.navMenuWidgetLayout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.navMenuWidgetLayout.addWidget(seperation_frame)
        self.navMenuWidgetLayout.addWidget(homeTabLabel)
        self.navMenuWidgetLayout.addWidget(tasksDoneTabLabel)
        self.navMenuWidgetLayout.addWidget(pomodoroTabLabel)
        self.navMenuWidgetLayout.addStretch()

        self.stackedLayout.addWidget(self.homeWidget)
        self.stackedLayout.addWidget(doneTaskScroll)
        self.stackedLayout.addWidget(self.pomodoroWidget)
        self.stackedLayout.setCurrentWidget(self.homeWidget) 

        self.homeWidget.layout().addWidget(self.taskScroll)
        self.homeWidget.layout().addWidget(self.statScroll)
        self.homeWidget.layout().addWidget(self.taskInfoScroll)
        self.centralLayout.addWidget(self.navMenuWidget, Qt.AlignmentFlag.AlignTop)
        self.centralLayout.addWidget(self.stacked_display)
        
        self.setCentralWidget(self.centralWidget)
        self.setStyleSheet(f"""
                        QWidget {{
                        background-color: {background}; 
                        color: white;
                        }}
                        """)
        self.statswidget.setStyleSheet("""
                                    QWidget {{
                                    border-radius : 5px;
                                    }}
                                    """)
        self.addTaskButton.setStyleSheet(f"""QPushButton {{
                                color: white;
                                background-color: none;
                                padding: 10px;
                                border: 2px solid white;
                                border-radius: 12px;
                                }}
                                QPushButton:hover {{
                                background-color: {primary}
                                }}
                                """)
        
        data = fetch_data()
        for items in data:
            taskName, prio, status, category, taskId = items
            Add_Task(self, self.taskwidgetLayout, taskName, prio, status, taskId, True)

        self.showMaximized()
        
    def toggleTaskInfo(self, checked, taskId):
        if self.toggleStatsButton.isChecked():
            self.toggleStatsButton.setChecked(False)
        
        self.showStateAnimation = QPropertyAnimation(self.taskInfoScroll, b'maximumWidth')
        self.showStateAnimation.setStartValue(self.taskInfoScroll.width())
        
        if checked is True : 
            self.showStateAnimation.setEndValue(0)
            self.showStateAnimation.setEndValue(400)
            self.displayTaskInfo(taskId)
        else :     
            self.showStateAnimation.setEndValue(400)
            self.showStateAnimation.setEndValue(0)
        
        self.showStateAnimation.setDuration(500)
        self.showStateAnimation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)     
        
    def displayTaskInfo(self, taskId):
        pass

    def set_tab_style_sheet(self, widget):
        widget.setStyleSheet(f"""QLabel {{
                            font-size: 15px;
                            border-radius: 3px;
                            padding: 5px 2px 5px 2px;
                            }}
                            QLabel::hover {{
                            background-color : {accent_dark}
                            }}
                            """)
    
    def onAddtaskClicked(self):
        if not self.getting_task:
            self.getting_task = True
            layout = QHBoxLayout()    
            self.placeholder_widget = QWidget()
            self.placeholder_widget.setLayout(layout)
            TaskWidget = GetTaskFromUser(self, self.taskwidgetLayout)
            layout.addWidget(TaskWidget)
            self.taskwidgetLayout.insertWidget(1 , self.placeholder_widget) 

            self.placeholder_widget.setStyleSheet(f"""
                                                background : {primary}; 
                                                max-width: 2000; 
                                                border-radius: 5px
                                                """)

    def getTaskStatusData(self):
        not_done, done = get_task_status_count()
        
        undone_task = {'name' : 'Not Completed', 
                    'value': not_done, 
                    'primary_color': QColor(piegraph_primary_hex_undone), 
                    'secondary_color': QColor(piegraph_secondary_hex_undone)}
        
        done_task = {'name' : 'Completed', 
                    'value': done, 
                    'primary_color': QColor(piegraph_primary_hex_done), 
                    'secondary_color': QColor(piegraph_secondary_hex_done)}
        
        data = [undone_task, done_task]

        return data
    
    def onTaskAdded(self):
        self.getting_task = False
        self.piegraph.update_data(self.getTaskStatusData())

    
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
        self.statWidgetLayout.removeWidget(self.DoneUndoneTaskPieChartWidget)
        self.animation.start()
        self.statWidgetLayout.addWidget(self.priorityBarChartWidget)
        self.statWidgetLayout.addWidget(self.DoneUndoneTaskPieChartWidget)
    
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

if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()
