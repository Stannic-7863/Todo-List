import typing
from settings import *
from custom_widgets_for_main import *
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QScrollArea,
                             QPushButton
                             )

    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_init()

    def ui_init(self):

        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        self.setFont(QFont(fontfamily))

        self.setWindowTitle('Todo List')
        self.setMinimumHeight(600)
        self.setMinimumWidth(400)

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
        addtask_shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        addtask_shortcut.activated.connect(self.addtask_dialog_show)
       
        self.addtask.setFixedWidth(200)
        self.taskwidget_layout.addWidget(self.addtask, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskwidget_layout.addStretch()


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
        add_task_no_dailog_widget = Add_Task_No_dialog(self, self.taskwidget_layout)
        self.taskwidget_layout.insertWidget(1 , add_task_no_dailog_widget)        

    def addtask_dialog_show(self):
        dialog = Add_task_dialog(self, self.taskwidget_layout)

        dialog.exec()





if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()