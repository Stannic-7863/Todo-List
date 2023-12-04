from settings import *
from custom_widgets import *
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QPainter
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QScrollArea,
                             QPushButton,
                             QFrame,
                             QTabWidget,
                             QStackedLayout
                             )
from PySide6 import QtCharts
from db_data_functions import fetch_data, get_task_status_count, main
from stat_widgets import *
from pomodoro import Pomodoro

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.font_init()
        main()
        self.piegraph = PieGraph([])
        self.priority_bar_chart = PriorityBarChart()
        self.ui_init()
        self.setMouseTracking(True)
    def font_init(self):
        
        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        self.setFont(QFont(fontfamily))
        QApplication.setFont(QFont(fontfamily))

    def ui_init(self):
        self.is_tab_menu_open = False
        self.getting_task = False

        self.setWindowTitle('Yarikata')
        self.setMinimumHeight(800)
        self.setMinimumWidth(700)

        self.central_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)
        central_widget.setMouseTracking(True)

        self.home_widget = QWidget()
        self.home_widget.setLayout(QHBoxLayout())

        self.taskwidget = QWidget()
        self.taskwidget_layout = QVBoxLayout()
        self.taskwidget.setLayout(self.taskwidget_layout)

        self.statswidget = QWidget()
        self.statswidget_layout = QVBoxLayout()
        self.statswidget.setLayout(self.statswidget_layout)
        
        self.addtask = QPushButton()
        self.addtask.setIcon(QIcon('./data/icons/plus.png'))
        self.addtask.setIconSize(QSize(50,50))
        self.addtask.setContentsMargins(0,0,0,0)
        self.addtask.clicked.connect(self.on_addtask_clicked)

        self.show_hide_stats = QRadioButton()
        self.show_hide_stats.setStyleSheet(f"""QRadioButton::indicator {{
                                           background: {primary};
                                           border-radius: 2px;
        }}
                                            QRadioButton::indicator:checked {{
                                            background: rgb{priority_mid};
                                            }}
""")
        self.show_hide_stats.setChecked(True)
        self.show_hide_stats.clicked.connect(self.animate_stat_hide_show)
        self.addtask.setFixedWidth(200)
        self.buttons_container_layout = QHBoxLayout()
        self.buttons_container = QWidget()
        self.buttons_container_layout.addWidget(self.addtask, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.buttons_container_layout.addWidget(self.show_hide_stats, Qt.AlignmentFlag.AlignRight)
        self.buttons_container.setLayout(self.buttons_container_layout)
        self.taskwidget_layout.addWidget(self.buttons_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskwidget_layout.addStretch()
       
        self.piegraph_widget = QWidget()
        self.piegraph_widget_layout = QVBoxLayout()
        self.piegraph_widget.setLayout(self.piegraph_widget_layout)
        
        task_status_data = self.get_task_status_data()
        self.piegraph = PieGraph(task_status_data)
        piegraph_veiw = QtCharts.QChartView(self.piegraph)
        piegraph_veiw.setRenderHint(QPainter.Antialiasing)
        self.piegraph_widget_layout.addWidget(piegraph_veiw)

        self.priority_bar_chart_widget = QWidget()
        self.priority_bar_chart_widget_layout = QVBoxLayout()
        self.priority_bar_chart_widget.setLayout(self.priority_bar_chart_widget_layout)
        self.priority_bar_chart = PriorityBarChart()
        barchart_veiw = QtCharts.QChartView(self.priority_bar_chart)
        barchart_veiw.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.priority_bar_chart_widget_layout.addWidget(barchart_veiw)

        self.statswidget_layout.addWidget(self.priority_bar_chart_widget)
        self.statswidget_layout.addWidget(self.piegraph_widget)

        self.task_scroll = QScrollArea()
        self.task_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.task_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.task_scroll.setWidgetResizable(True)
        self.task_scroll.setWidget(self.taskwidget)
        custom_scroll_task = Custom_Scroll_Bar()
        self.task_scroll.setVerticalScrollBar(custom_scroll_task)

        self.stat_scroll = QScrollArea()
        self.stat_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.stat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.stat_scroll.setWidgetResizable(True)
        self.stat_scroll.setWidget(self.statswidget)
        custom_scroll_stat = Custom_Scroll_Bar()
        self.stat_scroll.setVerticalScrollBar(custom_scroll_stat)
        self.stat_scroll.setMaximumWidth((QApplication.primaryScreen().size().width())/2.5)

        self.stacked_display = QWidget()
        self.stacked_display_layout = QStackedLayout()
        self.stacked_display.setLayout(self.stacked_display_layout)
        
        self.nav_menu_bar_widget = QWidget()
        self.nav_menu_bar_widget.setMaximumWidth(0)
        self.nav_menu_bar_widget_layout = QVBoxLayout()
        self.nav_menu_bar_widget.raise_()
        self.nav_menu_bar_widget.setLayout(self.nav_menu_bar_widget_layout)
        self.nav_menu_bar_widget.setStyleSheet(f"background-color: {background_dark}; border-radius: 7px")
        title_label = ItemLable('YARIKATA', self.stacked_display_layout, self.home_widget)
        title_label.setStyleSheet(f"""
                                  font-size: 30px;
                                """)
        seperation_frame = QFrame()
        seperation_frame.setFrameShape(QFrame.Shape.HLine)
        seperation_frame.setStyleSheet(f"background: white")
        seperation_frame.setFrameShadow(QFrame.Shadow.Sunken)


        self.done_tasks_widget = QWidget()
        done_label = QLabel('Completed Tasks')
        done_label.setStyleSheet(f'font-size: 30px; padding: 20px 0px 20px 0px')
        done_frame = QFrame()
        done_frame.setFrameShape(QFrame.Shape.HLine)
        done_frame.setStyleSheet(f'background: white')
        self.done_tasks_widget_layout = QVBoxLayout()
        self.done_tasks_widget_layout.addWidget(done_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.done_tasks_widget_layout.addWidget(done_frame)
        self.done_tasks_widget_layout.addStretch()
        self.done_tasks_widget.setLayout(self.done_tasks_widget_layout)

        donetask_scroll = QScrollArea()
        donetask_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        donetask_scroll.setWidgetResizable(True)
        donetask_scroll.setWidget(self.done_tasks_widget)
        custom_done_scroll = Custom_Scroll_Bar()
        donetask_scroll.setVerticalScrollBar(custom_done_scroll)

        self.pomodoro_widget = Pomodoro(self)
          
        home_tab_label = ItemLable('Home', self.stacked_display_layout, self.home_widget)
        tasks_done_tab_label = ItemLable('Task Done', self.stacked_display_layout, donetask_scroll)
        pomodoro_tab_label = ItemLable('Pomodoro', self.stacked_display_layout, self.pomodoro_widget)

        self.set_tab_style_sheet(home_tab_label)
        self.set_tab_style_sheet(tasks_done_tab_label)
        self.set_tab_style_sheet(pomodoro_tab_label)

        self.nav_menu_bar_widget_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.nav_menu_bar_widget_layout.addWidget(seperation_frame)
        self.nav_menu_bar_widget_layout.addWidget(home_tab_label)
        self.nav_menu_bar_widget_layout.addWidget(tasks_done_tab_label)
        self.nav_menu_bar_widget_layout.addWidget(pomodoro_tab_label)
        self.nav_menu_bar_widget_layout.addStretch()

        self.stacked_display_layout.addWidget(self.home_widget)
        self.stacked_display_layout.addWidget(donetask_scroll)
        self.stacked_display_layout.addWidget(self.pomodoro_widget)
        self.stacked_display_layout.setCurrentWidget(self.home_widget) 

        self.home_widget.layout().addWidget(self.task_scroll)
        self.home_widget.layout().addWidget(self.stat_scroll)
        self.central_layout.addWidget(self.nav_menu_bar_widget, Qt.AlignmentFlag.AlignTop)
        self.central_layout.addWidget(self.stacked_display)
        
        self.setCentralWidget(central_widget)
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
        
        data = fetch_data()
        for items in data:
            task_name, prio, status, category, task_id = items
            add_task = Add_Task(self, self.taskwidget_layout, task_name, prio, status, task_id, loading_data=True)
            add_task.add()

        self.showMaximized()

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
    
    def on_addtask_clicked(self):
        if not self.getting_task:
            self.getting_task = True
            layout = QHBoxLayout()    
            self.placeholder_widget = QWidget()
            self.placeholder_widget.setLayout(layout)
            add_task_no_dailog_widget = Add_Task_No_dialog(self, self.taskwidget_layout)
            layout.addWidget(add_task_no_dailog_widget)
            self.taskwidget_layout.insertWidget(1 , self.placeholder_widget) 

            self.placeholder_widget.setStyleSheet(f"""background : {primary}; max-width: 2000; border-radius: 5px""")

    def get_task_status_data(self):
        not_done, done = get_task_status_count()
        
        undone_task = {'name' : 'Not Completed', 'value': not_done, 'primary_color': QColor(piegraph_primary_hex_undone), 'secondary_color': QColor(piegraph_secondary_hex_undone)}
        done_task = {'name' : 'Completed', 'value': done, 'primary_color': QColor(piegraph_primary_hex_done), 'secondary_color': QColor(piegraph_secondary_hex_done)}
        data = [undone_task, done_task]

        return data
 
    def on_task_added(self):
        self.getting_task = False
        data = self.get_task_status_data()
        self.piegraph.update_data(data)

    def mousePressEvent(self, event):
        if QRect(0, 0, 60, 40).contains(event.pos()):
            self.is_tab_menu_open = not self.is_tab_menu_open

            self.handle_tab_menu()
    
    def animate_stat_hide_show(self):
        current_width = self.stat_scroll.width()
        self.animation = QPropertyAnimation(self.stat_scroll, b"maximumWidth")
        
        if current_width == 0:
            newwidth = QApplication.primaryScreen().size().width()/2.5
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        else:
            newwidth = 0
            self.animation.setEasingCurve(QEasingCurve.Type.InCubic)

        self.animation.setDuration(400)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(newwidth)
        self.statswidget_layout.removeWidget(self.priority_bar_chart_widget)
        self.statswidget_layout.removeWidget(self.piegraph_widget)
        self.animation.start()
        self.statswidget_layout.addWidget(self.priority_bar_chart_widget)
        self.statswidget_layout.addWidget(self.piegraph_widget)
    
    def handle_tab_menu(self):
        self.animation = QPropertyAnimation(self.nav_menu_bar_widget, b"maximumWidth")
        current_width = self.nav_menu_bar_widget.width()
        
        if self.is_tab_menu_open == True:
            newwidth = 300
            self.animation.setEasingCurve(QEasingCurve.Type.OutBack)
        else:
            self.animation.setEasingCurve(QEasingCurve.Type.InBack)
            newwidth = 0

        self.animation.setDuration(400)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(newwidth)
        self.animation.start()

if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()