from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import datetime
from settings import *
from db_data_functions import *

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
        self.total_long_break_interval = 4
        self.current_long_break_interval = 0
        
        self.total_seconds = self.total_minutes * 60
        self.short_break_seconds = self.short_break_minute * 60
        self.long_break_seconds = self.long_break_minutes * 60
        
        self.display_time = 0
        self.display_time_total = self.total_seconds
        self.total_rounds = 4
        self.current_rounds = 0
        
        self.sessionId = None
        self.taskId = None

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
        
        self.clock_widget = CircularProgressBar()
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
        remove.triggered.connect(self.remove_task_label)
        
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
    
    def remove_task_label(self):
        pass
            
    def onAddTaskButtonClicked(self):
        self.animate_add_task_button(animate_open=False, animate_open_get_task=True)
    
    def setTask(self):
        text = self.get_task_name.text()
        dateCreated = datetime.now()
        dateCreated = dateCreated.strftime('%Y-%m-%d')
        self.taskNameLabel.setText(text)
        self.taskId = commit_new_task_data(text, dateCreated, 'none', 'not done', None)
        self.pomodoroId = fetchPomodoroId(self.taskId)
        self.sessionId = insertNewSessionData(self.pomodoroId)
        self.totalFocusTime = 0
        
        self.animate_add_task_button(animate_open=False, animate_open_get_task=False)
        self.animate_set_task(animate_open=True)
        
    def getTask(self, text, taskId):
        self.taskNameLabel.setText(text)
        self.taskId = taskId
        self.pomodoroId = fetchPomodoroId(self.taskId)
        self.sessionId = insertNewSessionData(self.pomodoroId)
        self.totalFocusTime = fetchTaskTotalFocusTime(self.pomodoroId)
        self.parent.stackedContainerLayout.setCurrentWidget(self.parent.pomodoroWidget) 
        
        self.animate_add_task_button(animate_open=False, animate_open_get_task=False)
        self.animate_set_task(animate_open=True)
        
    def animate_set_task(self, animate_open=True):
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
            if self.taskNameLabel.text():
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


class CircularProgressBar(QWidget):
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
