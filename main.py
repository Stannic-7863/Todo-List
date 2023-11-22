import typing
from settings import *
from custom_widgets import *
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QScrollArea,
                             QPushButton
                             )
from db_data_functions import fetch_data
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.font_init()
        self.ui_init()

    def font_init(self):
        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        self.setFont(QFont(fontfamily))
    def ui_init(self):
        self.getting_task = False

        self.setWindowTitle('Todo List')
        self.setMinimumHeight(800)
        self.setMinimumWidth(700)

        self.central_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)

        taskwidget = QWidget()
        self.taskwidget_layout = QVBoxLayout()
        taskwidget.setLayout(self.taskwidget_layout)

        self.statswidget = QWidget()
        self.statswidget_layout = QVBoxLayout()
        self.statswidget.setLayout(self.taskwidget_layout)
        self.central_layout.addWidget(self.statswidget)
        self.central_layout.addWidget(taskwidget)
        
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(central_widget)
        custom_scroll = Custom_Scroll_Bar()
        scroll.setVerticalScrollBar(custom_scroll)
        
        self.setCentralWidget(scroll)
        
        self.addtask = QPushButton()
        self.addtask.setIcon(QIcon('./data/icons/plus.png'))
        self.addtask.setIconSize(QSize(50,50))
        self.addtask.setContentsMargins(0,0,0,0)
        self.addtask.clicked.connect(self.on_addtask_clicked)
       
        self.addtask.setFixedWidth(200)
        self.taskwidget_layout.addWidget(self.addtask, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskwidget_layout.addStretch()

        data = fetch_data()
        for items in data:
            task_name, prio, status, category, task_id = items
            add_task = Add_Task(self, self.taskwidget_layout, task_name, prio, status, task_id)
            add_task.add()


        self.setStyleSheet(f"""
                           QWidget {{
                           background-color: {background}; 
                           color: white;
                           }}
                           """)
        self.statswidget.setStyleSheet(f"""
                                       QWidget {{
                                       border-radius : 5px;
                                       }}
                                       """)
        self.addtask.setStyleSheet(f"""QPushButton {{
                                   color: white;
                                   background-color: none;
                                   padding: 10px;
                                   border: 2px solid white;
                                   border-radius: 12px;
                                   max-width: 1200;
                                   }}
                                   QPushButton:hover {{
                                   background-color: {primary}
                                   }}
                                   """)
        scroll.setStyleSheet(f"""
                             QScrollBar:vertical {{
                             background: {background};
                             width: 20px;
                             border: 0px solid black;
                             margin: 15px 10px 15px 0px
                             }}

                             QScrollBar::handle:vertical {{
                             border: 0px solid black;
                             border-radius : 5px;
                             background-color : {primary}; 
                             }}

                             QScrollBar::sub-line:vertical {{
                             background: {background};
                             }}
                             
                             QScrollBar::add-line:vertical {{
                             background: {background}; 
                             }}

                             QScrollBar::sub-page:vertical {{
                             background: {background};
                             }}

                             QScrollBar::add-page:vertical {{
                             background: {background};
                             }}
                            """)
        self.showMaximized()
    def on_addtask_clicked(self):
        if not self.getting_task:
            self.getting_task = True
            layout = QHBoxLayout()    
            self.placeholder_widget = QWidget()
            self.placeholder_widget.setLayout(layout)
            add_task_no_dailog_widget = Add_Task_No_dialog(self, self.taskwidget_layout)
            layout.addWidget(add_task_no_dailog_widget)
            self.taskwidget_layout.insertWidget(1 , self.placeholder_widget) 

            self.placeholder_widget.setStyleSheet(f"""background : {primary}; max-width: 1200;""")
          
    def on_task_added(self):
        self.getting_task = False


if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()