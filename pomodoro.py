import PySide6.QtCore
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from settings import *

class Pomodoro(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setParent(self.parent)

        self.start_icon = QIcon('./data/icons/start.png')
        self.pause_icon = QIcon('./data/icons/pause.png')
        #settings
        self.total_minutes = 25
        self.elapsed_seconds =  0 
        self.total_seconds = self.total_minutes * 60

        self.total_rounds = 4
        self.current_rounds = 0

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_clock_values)
        
        # Make and add the widgets
        self.container_widget = QWidget()
        self.container_widget_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_widget_layout)

        self.header_widget = QWidget()
        self.header_widget_layout = QHBoxLayout()
        self.header_widget.setLayout(self.header_widget_layout)

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
        
        self.header_widget_layout.addStretch()
        self.header_widget_layout.addWidget(self.get_task_name, alignment=Qt.AlignmentFlag.AlignCenter)
        self.header_widget_layout.addWidget(self.add_task_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.header_widget_layout.addStretch()

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

        self.container_widget_layout.addWidget(self.header_widget, alignment=Qt.AlignmentFlag.AlignTop)
        self.container_widget_layout.addWidget(self.body_widget)
        self.container_widget_layout.addWidget(self.footer_widget, alignment=Qt.AlignmentFlag.AlignJustify)

        self.set_button_style_sheet(self.add_task_button)
        self.set_button_style_sheet(self.start_pause_button)

        self.add_task_button.pressed.connect(self.on_add_task_button_clicked)
        self.start_pause_button.pressed.connect(self.start_pause_pomodoro)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.container_widget)
        self.setLayout(self.main_layout)

    def set_task(self):
        text = self.get_task_name.text()
        task_label = Custom_QLabel()
        task_label.setText(text)
        self.animate_get_task()
        self.body_widget_layout.insertWidget(0, task_label, alignment=Qt.AlignmentFlag.AlignHCenter)

    def on_add_task_button_clicked(self):
        self.animate_add_task_button()
    
    def animate_add_task_button(self):
        if self.add_task_button.width() > 0:
            self.animation_task_button = QPropertyAnimation(self.add_task_button, b'maximumWidth')
            self.animation_task_button.setStartValue(self.add_task_button.width())
            self.animation_task_button.setEndValue(0)
        else:
            self.animation_task_button = QPropertyAnimation(self.add_task_button, b'maximumWidth')
            self.animation_task_button.setStartValue(self.add_task_button.width())
            self.animation_task_button.setEndValue(50)
            
            
        self.animation_task_button.setEasingCurve(QEasingCurve.Type.InCubic)
        self.animation_task_button.finished.connect(self.animate_get_task)
        self.animation_task_button.start()


    def animate_get_task(self):
        if self.get_task_name.width() == 0:
            self.animation_get_task = QPropertyAnimation(self.get_task_name, b'minimumWidth')
            self.animation_get_task.setStartValue(self.get_task_name.width())
            self.animation_get_task.setEndValue(400)
            self.animation_get_task.setEasingCurve(QEasingCurve.Type.OutBack)
            self.get_task_name.setFocus()
        
        else:
            self.animation_get_task = QPropertyAnimation(self.get_task_name, b'minimumWidth')
            self.animation_get_task.setStartValue(self.get_task_name.width())
            self.animation_get_task.setEndValue(0)
            self.animation_get_task.setEasingCurve(QEasingCurve.Type.InBack)
            self.get_task_name.clearFocus()
        self.animation_get_task.setDuration(500)
        self.animation_get_task.start()

    def start_pause_pomodoro(self):
        if not self.timer.isActive():
            self.start_pause_button.setIcon(self.pause_icon)
            self.timer.start()
        else:
            self.start_pause_button.setIcon(self.start_icon)
            self.timer.stop()

    def update_clock_values(self):
        self.elapsed_seconds += 1 
        hour ,time = self.get_formatted_time()
        self.clock_widget.set_value(self.elapsed_seconds, self.total_seconds, hour, time, self.total_rounds, self.current_rounds)

    def get_formatted_time(self):
        minute, elapsed_seconds = divmod(self.elapsed_seconds, 60)
        hour, minute = divmod(minute, 60)
        return "{:02d}".format(hour) ,"{:02d}:{:02d}".format(minute, elapsed_seconds)
    
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
        self.hour = '00'
        self.time = '00:00'
        self.width = 350
        self.height = 350
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = priority_mid
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

    def set_value(self, elapsed_seconds, total_seconds, hour, time, total_rounds, current_rounds):
        self.value = (elapsed_seconds/total_seconds)*100 
        self.time = time
        self.hour = hour
        self.current_rounds = current_rounds
        self.total_rounds = total_rounds
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
        pen.setColor(QColor(255,255,255,100))
        pen.setWidth(2)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, 0, 360*16)
        
        pen.setColor(QColor(255,255,255,255))
        pen.setWidth(self.progress_width/2)
        
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
        paint.drawText(total_time_text_rect, Qt.AlignmentFlag.AlignCenter, f"{self.hour}:{self.time}")

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


class Custom_QLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.parent.animate_add_task_button()
        if event.key() == Qt.Key_Return:
            self.parent.set_task()

        super().keyPressEvent(event)

class Custom_QLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""QLabel {{
                           font-size: 30px;
                           font-weight: 50;              
        }}""")