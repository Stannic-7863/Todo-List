from settings import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from db_data_functions import *
from datetime import datetime

class PomodoroClock(QWidget):
    def __init__(self):
        super().__init__()
        font_path = "./data/fonts/clockfont.ttf" 
        QFontDatabase.addApplicationFont(font_path)
        self.clock_font = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(font_path))[0]
        self.setFont(self.clock_font)

        self.value = 0
        self.elapsed_seconds = 0
        self.time = '00:00'
        self.total_time = '00:00:00'
        self.width = 350
        self.height = 350
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = QColor(255,255,255)
        self.max_value = 100
        self.font_size = 30
        self.font_size_small = 16
        self.enable_shadow = True
        self.total_rounds = 0
        self.current_rounds = 0
        self.quote = 'Focus'

        self.resize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        
        self.setStyleSheet(f"font-size: {self.font_size}px")

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,120))
        self.setGraphicsEffect(self.shadow)

    def set_value(self, elapsed_seconds, total_seconds, time, total_time, total_rounds, current_rounds, quote):
        self.value = (elapsed_seconds/total_seconds)*100 
        self.time = time
        self.total_time = total_time
        self.current_rounds = current_rounds
        self.total_rounds = total_rounds
        self.quote = quote 
        self.repaint()

    def paintEvent(self, event):
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value

        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.PenStyle.NoPen)
        paint.drawRect(rect)

        pen = QPen()
        pen.setColor(QColor(255,255,255,120))
        pen.setWidth(2)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, 0, 360*16)
        
        pen.setWidth(self.progress_width/2)
        pen.setColor(self.progress_color)
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90*16, -value*16)

        pen.setColor(QColor(255,255,255,120))
        paint.setPen(pen)
        font = QFont()
        font.setPointSize(self.font_size_small)
        paint.setFont(font)
        total_time_text_rect = QRect(margin, margin, width, height-self.font_size-self.progress_width-10-self.font_size_small)
        paint.drawText(total_time_text_rect, Qt.AlignmentFlag.AlignCenter, f"{self.total_time}")

        pen.setColor(QColor(qRgb(255,255,255)))
        font = QFont()
        font.setPointSize(self.font_size)
        paint.setFont(font)
        paint.setPen(pen)
        paint.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.time}")

        pen.setColor(QColor(255,255,255,120))
        paint.setPen(pen)
        font = QFont()
        font.setPointSize(self.font_size_small)
        paint.setFont(font)
        percent_rounds_text_rect = QRect(margin, margin, width, height+self.font_size+self.progress_width+10+self.font_size_small)
        paint.drawText(percent_rounds_text_rect, Qt.AlignmentFlag.AlignCenter, f"{int(self.value)}%    {self.current_rounds}/{self.total_rounds}")
        
        pen.setColor(QColor(255,255,255,255))
        paint.setPen(pen)
        quote_rect = QRect(margin, margin, width, height+height/2)
        paint.drawText(quote_rect, Qt.AlignmentFlag.AlignCenter, f"{self.quote}")
        
        paint.end() 

    def get_change_color(self, color_from, color_to):
        animation = QVariantAnimation(self)
        animation.setDuration(2000)
        animation.setStartValue(QColor(qRgb(color_from[0], color_from[1], color_from[2])))
        animation.setEndValue(QColor(qRgb(color_to[0], color_to[1], color_to[2])))
        animation.valueChanged.connect(lambda value: self.set_change_color(value))
        animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
    
    def set_change_color(self, color):
        self.progress_color = color
        self.update()

class TaskCheckBox(QCheckBox):    
    activeInstance = None
    
    def __init__(self, parent: QMainWindow, taskName: str, priority: str, status: str, taskId: int) -> None:
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.status = status
        self.taskId = taskId
        self.taskName = taskName
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

        if self.taskName:       
            if self.status == 'done':
                self.setChecked(True)
                self.parent.doneTaskView.addTask(self) 
            if self.status == 'not done':
                self.setChecked(False) 
                self.parent.taskView.addTask(self)
    
        self.color = self.get_color(self.currentPriority)
        self.stateChanged.connect(self.onStateChange)
        self.updateMainStyleSheet(self.color)

        self.updateMainStyleSheet(self.color)
        
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
        prevPriority = self.currentPriority
        prevColor = self.color
        
        self.currentPriority = prio
        self.color = self.get_color(prio)
        
        if self.isChecked() == False:
            colorChangeAnimation(self, prevColor , self.color)

        change_priority_db(prevPriority, self.currentPriority, self.taskId)
        self.updateGraphs()

    def onStateChange(self, value):
        state = Qt.CheckState(value)
        prevStatus = self.status

        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        
        if state == Qt.CheckState.Unchecked:
            self.updateMainStyleSheet(self.color)
            self.status = 'not done'
            self.parent.taskView.addTask(self)
            self.parent.doneTaskView.removeTask(self)
            change_status_db(prevStatus, self.status, self.taskId, formatted_date) 
        
        if state == Qt.CheckState.Checked:
            self.updateMainStyleSheet(taskDoneColor)
            self.status = 'done'
            self.parent.taskView.removeTask(self)
            self.parent.doneTaskView.addTask(self)
            change_status_db(prevStatus, self.status, self.taskId, formatted_date)
    
        self.updateHeight()
        self.parent.statsView.update()

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
    
    def get_color(self, prio) -> str:
        """Get the color depending on the Priority of the task"""
        color = priorityNoneColor
        if prio == 'high':
            color = priorityHighColor
        elif prio == 'mid':
            color = priorityMidColor
        elif prio == 'low':
            color = priorityLowColor
            
        return color

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
                            border-radius: 1px;
                            border : 3px black;
                            }}
                        QLabel {{
                            font-size : 18px
                        }}
                        """)
        
class ScrollBar(QScrollBar):
    def __init__(self) -> QScrollBar:
        """A customized QScrollBar"""
        super().__init__()
        self.updateMainStyleSheet(primaryColor)
    
    def updateMainStyleSheet(self, color):
        self.setStyleSheet(f"""
            QScrollBar:vertical {{
            background: {backgroundColor};
            width: 20px;
            border: 0px solid black;
            margin: 15px 10px 15px 0px
            }}

            QScrollBar::handle:vertical {{
            border: 0px solid black;
            border-radius : 5px;
            background-color : {color}; 
            }}

            QScrollBar::sub-line:vertical {{
            background: {backgroundColor};
            }}
            
            QScrollBar::add-line:vertical {{
            background: {backgroundColor}; 
            }}

            QScrollBar::sub-page:vertical {{
            background: {backgroundColor};
            }}

            QScrollBar::add-page:vertical {{
            background: {backgroundColor};
            }}
        """)
        
    def enterEvent(self, event) -> bool:
        colorChangeAnimation(self, primaryColor, priorityMidColor)
        return True
    def leaveEvent(self, event) -> bool:
        colorChangeAnimation(self, priorityMidColor, primaryColor)
        return True


def colorChangeAnimation(widget, color_from, color_to):
    animation = QVariantAnimation(widget)
    animation.setDuration(1000)
    animation.setStartValue(QColor(color_from))
    animation.setEndValue(QColor(color_to))
    animation.valueChanged.connect(lambda value: (widget.updateMainStyleSheet(value.name())))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
    

