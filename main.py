from settings import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6 import QtCharts
from db_data_functions import *
from CustomWidgets import *
from stat_widgets import *
from TaskWidget import *
from pomodoro import Pomodoro
from MainWindowWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        setupDatabase()
        self.font_init()
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

        self.taskView = TaskView(parent=self)
        self.doneTaskView = DoneTaskView(parent=self)
        self.pomodoroWidget = Pomodoro(parent=self)
        self.statsView = StatsView(parent=self)
        self.taskInfoView = TaskInfoView(parent=self)
        self.navMenu = NavMenu(parent=self)
        
        self.stackedContainerWidget = QWidget()
        self.stackedContainerLayout = QStackedLayout()
        self.stackedContainerWidget.setLayout(self.stackedContainerLayout)

        self.stackedContainerLayout.addWidget(self.homeWidget)
        self.stackedContainerLayout.addWidget(self.doneTaskView)
        self.stackedContainerLayout.addWidget(self.pomodoroWidget)
        self.stackedContainerLayout.setCurrentWidget(self.homeWidget) 

        self.homeWidget.layout().addWidget(self.taskView)
        self.homeWidget.layout().addWidget(self.statsView)
        self.homeWidget.layout().addWidget(self.taskInfoView)
        self.centralLayout.addWidget(self.navMenu, Qt.AlignmentFlag.AlignTop)
        self.centralLayout.addWidget(self.stackedContainerWidget)
        self.setCentralWidget(self.centralWidget)
        
        data = fetch_data()
        for items in data:
            taskName, priority, status, category, taskId = items
            TaskCheckBox(self, taskName, priority, status, taskId, True)

        self.showMaximized()
        self.setMainStyleSheet()    

    def mousePressEvent(self, event) -> bool:
        if QRect(0, 0, 60, 40).contains(event.pos()):
            self.navMenu.isOpen = not self.navMenu.isOpen
            self.navMenu.toggle()
        
        return super().mousePressEvent(event)

    def setMainStyleSheet(self):
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
                        QPushButton {{
                            color: white;
                            background-color: none;
                            padding: 10px;
                            border: 2px solid white;
                            border-radius: 12px;
                        }}
                        QPushButton:hover {{
                            background-color: {primaryColor}
                        }}""")
        
if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()
