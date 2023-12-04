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
        self.total_minutes = 0.5
        self.seconds =  0 
        self.total_seconds = self.total_minutes * 60

        self.rounds = 4

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_clock_values)
        
        self.container_widget = QWidget()
        self.container_widget_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_widget_layout)

        self.header_widget = QWidget()
        self.header_widget_layout = QHBoxLayout()
        self.header_widget.setLayout(self.header_widget_layout)

        self.options_button = QPushButton()
        self.options_button.setIcon(QIcon('./data/icons/menu.png'))
        self.options_button.setIconSize(QSize(50, 50))

        self.add_task_button = QPushButton()
        self.add_task_button.setIcon(QIcon('./data/icons/plus.png'))
        self.add_task_button.setIconSize(QSize(50,50))

        self.header_widget_layout.addWidget(self.options_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.header_widget_layout.addStretch()
        self.header_widget_layout.addWidget(self.add_task_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.header_widget_layout.addStretch()

        self.body_widget = QWidget()
        self.body_widget_layout = QVBoxLayout()
        self.body_widget.setLayout(self.body_widget_layout)
        
        self.clock_widget = CircularProgressBar()

        self.body_widget_layout.addWidget(self.clock_widget, alignment=Qt.AlignmentFlag.AlignCenter)

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

        self.set_button_style_sheet(self.options_button)
        self.set_button_style_sheet(self.add_task_button)
        self.set_button_style_sheet(self.start_pause_button)
        self.start_pause_button.pressed.connect(self.start_pause_pomodoro)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.container_widget)
        self.setLayout(self.main_layout)

    def start_pause_pomodoro(self):
        if not self.timer.isActive():
            self.start_pause_button.setIcon(self.pause_icon)
            self.timer.start()
        else:
            self.start_pause_button.setIcon(self.start_icon)
            self.timer.stop()

    def update_clock_values(self):
        self.seconds += 1 
        time = self.get_formatted_time()
        self.clock_widget.set_value(self.seconds, self.total_seconds, time)

    def get_formatted_time(self):
        minute, seconds = divmod(self.seconds, 60)
        hour, minute = divmod(minute, 60)
        return "{:02d}:{:02d}".format(minute, seconds)
    
    def set_button_style_sheet(self, widget):
        widget.setStyleSheet(f"""QPushButton {{
                             border-radius: 5px;
                             border: none; 
        }}""")


class CircularProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.seconds = 0
        self.time = '00:00'
        self.width = 300
        self.height = 300
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.progress_color = priority_mid
        self.max_value = 100
        self.font_size = 30
        self.enable_shadow = True

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

    def set_value(self, current_seconds, total_seconds, time):
        self.value = (current_seconds/total_seconds)*100 
        self.time = time
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
        pen.setColor(QColor(qRgb(255,255,255)))
        pen.setWidth(2)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, 0, 360*16)
        
        pen.setColor(QColor(qRgb(self.progress_color[0], self.progress_color[1], self.progress_color[2])))
        pen.setWidth(self.progress_width)
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90*16, -value*16)


        pen.setColor(QColor(qRgb(255,255,255)))
        paint.setPen(pen)
        paint.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.time}")
        paint.end() 