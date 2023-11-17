import functools, csv
from PyQt6.QtGui import QFont, QFontDatabase, QIcon, QColor, qRgb, QAction, QActionGroup
from PyQt6.QtCore import Qt, QSize, QVariantAnimation, QAbstractAnimation
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QCheckBox,
                             QVBoxLayout,
                             QHBoxLayout,
                             QScrollArea,
                             QPushButton,
                             QDialog,
                             QDialogButtonBox,
                             QPlainTextEdit,
                             QLabel,
                             QRadioButton,
                             QButtonGroup,
                             QToolButton,
                             QMenu
                             )
support = 'rgb(255, 255, 255)'
background = 'rgb(34, 40, 49)'
primary = 'rgb(57, 62, 70)'
secondary = 'rgb(0, 173, 181)'
accent = '(237,76,76)'

qsupport = (255, 255, 255)
qbackground = (34, 40, 49)
qprimary = (57, 62, 70)
qsecondary = (0, 173, 181)
qaccent = (237,76,76)

priority_low = (0, 173, 181)
priority_mid = (255,167,0)
priority_high = (237,76,76)
priority_none = (57, 62, 70)
task_done = (11, 219, 123)

class Add_task_dialog(QDialog):
    def __init__(self, parent, mainwindowlayout):
        super().__init__(parent)
        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        QApplication.setFont(QFont(fontfamily))

        self.parent = parent
        self.mainwindowlayout = mainwindowlayout
        self.setWindowTitle('Add a new task')
        self.setGeometry(100, 100, 500, 400)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        label = QLabel("New task")
        self.buttonbox = QDialogButtonBox(buttons)
        self.buttonbox.clicked.connect(self.save)
        self.buttonbox.rejected.connect(self.reject)

        self.get_task_text = QPlainTextEdit()
        self.get_task_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        self.p_high = QRadioButton('Priority : High')
        self.p_mid = QRadioButton('Priority : Mid')
        self.p_low = QRadioButton('Priority : Low')

        
        self.buttongroup = QButtonGroup()
        self.buttongroup.addButton(self.p_high)
        self.buttongroup.addButton(self.p_mid)
        self.buttongroup.addButton(self.p_low)


        self.layout = QVBoxLayout()
        self.layout.addWidget(label, alignment= Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.get_task_text, alignment= Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.p_high)
        self.layout.addWidget(self.p_mid)
        self.layout.addWidget(self.p_low)
        self.layout.addStretch()
        self.layout.addWidget(self.buttonbox, alignment= Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.layout)

    def save(self):
        prio = None
        if self.p_high.isChecked():
            prio = 'high'
        elif self.p_mid.isChecked():
            prio = 'mid'
        elif self.p_low.isChecked():
            prio = 'low'

        text = self.get_task_text.toPlainText()

        add_task = Add_Task(self.parent, self.mainwindowlayout ,text, prio)
        add_task.save()

        self.accept()

class Add_Task:
    def __init__(self, parent, mainlayout, task_name, prio):
        self.parent = parent
        self.text = task_name
        self.priority_str = prio
        self.mainwindowlayout = mainlayout
    
    def change_prio(self, prio):
        self.priority_str = prio
        self.color = self.get_color(prio)
        if self.check_box.isChecked() == False:
            self.change_style_sheet()

    def save(self):
        self.text = self.text.strip()
        if self.text.strip():
            self.color = priority_none
            self.color = self.get_color(self.priority_str)
           
            self.options = QToolButton()
            self.options.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            self.options.setText('...')
            self.options.setIcon(QIcon('./data/icons/menu.png'))
            self.options.setIconSize(QSize(30, 30))
            self.options.setMenu(self.create_menu())
            self.options.setStyleSheet(f"""
                                       QToolButton {{
                                       background-color : transparent;
                                       }}

                                       QToolButton::menu-indicator {{
                                       image: none;
                                       }}
                                       """)
            
            checkbox_layout = QHBoxLayout()
            self.check_box = QCheckBox(self.text, self.parent)
            self.check_box.setLayout(checkbox_layout)
            checkbox_layout.addStretch()
            checkbox_layout.addWidget(self.options)
            
            self.mainwindowlayout.insertWidget(1,self.check_box, alignment=Qt.AlignmentFlag.AlignTop)
            self.change_style_sheet()
            self.check_box.stateChanged.connect(lambda value: self.parent.on_state_changed(value, self.color))
            widget_data = {
                'Name' : self.text,
                'Current_status' : False,
                'Priority' : self.priority_str
            }
            file_path = './data/task_data/data.csv'
        
            with open(file_path, 'a', newline='')as data_csv:
                writer = csv.writer(data_csv)
                writer.writerow(widget_data.values())

    def create_menu(self):
        menu = QMenu(parent=self.parent)

        priority_menu = QMenu('Set Priority', parent=self.parent)

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

        menu.addMenu(priority_menu)

        return menu

    def change_style_sheet(self):
        self.check_box.setStyleSheet(f"""QCheckBox {{
                                    background-color: rgb{str(self.color)};
                                    color: white;
                                    padding: 30px;
                                    border-radius: 5px;
                                    }}  
                                    QCheckBox::indicator {{
                                    background-color: {background};
                                    border-radius: 4px;
                                    }}
                                    QCheckBox::indicator:checked {{
                                    background-color: {support};
                                    }}
                                    """)

    def get_color(self, prio):
        self.color = priority_none
        if prio == 'high':
            self.color = priority_high
        elif prio == 'mid':
            self.color = priority_mid
        elif prio == 'low':
            self.color = priority_low
        
        return self.color
         
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
        
        self.setCentralWidget(scroll)
        
        self.addtask = QPushButton()
        self.addtask.setIcon(QIcon('./data/icons/plus.png'))
        self.addtask.setIconSize(QSize(50,50))
        self.addtask.setContentsMargins(0,0,0,0)
        self.addtask.clicked.connect(self.on_addtask_clicked)
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
                             margin: 10px 10px 10px 0px
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
        dialog = Add_task_dialog(self, self.taskwidget_layout)

        dialog.exec()

    def on_state_changed(self, value, color):
        state = Qt.CheckState(value)
        checkbox = self.sender()

        if state == Qt.CheckState.Unchecked:
            start_animation(checkbox, task_done, color)
        if state == Qt.CheckState.Checked:
            start_animation(checkbox, color, task_done)

def start_animation(checkbox, qprimary, qaccent):
    animation = QVariantAnimation(checkbox)
    animation.setDuration(400)
    animation.setStartValue(QColor(qRgb(qprimary[0], qprimary[1], qprimary[2])))
    animation.setEndValue(QColor(qRgb(qaccent[0], qaccent[1], qaccent[2])))
    animation.valueChanged.connect(functools.partial(change_color, checkbox))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

def change_color(widget, color):
    widget.setStyleSheet(f"""
                            QCheckBox {{
                            background-color: {color.name()};
                            color: white;
                            padding: 30px;
                            border-radius: 5px;
                            }}  
                            QCheckBox::indicator {{
                            background-color: {background};
                            border-radius: 4px;
                            }}
                            QCheckBox::indicator:checked {{
                            background-color: {support};
                            }}
                            """)


if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()