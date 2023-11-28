from settings import *
from custom_widgets import *
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QPainter
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint,QRect, QEasingCurve
from PySide6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QScrollArea,
                             QPushButton
                             )
from PySide6 import QtCharts
from db_data_functions import fetch_data, get_task_status_count, main
from stat_widgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main()
        self.piegraph = PieGraph([])
        self.priority_bar_chart = PriorityBarChart()

        self.font_init()
        self.ui_init()

    def font_init(self):
        path = './data/fonts/bfont.TTF'

        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        self.setFont(QFont(fontfamily))
    def ui_init(self):
        self.getting_task = False

        self.setWindowTitle('Yarikata')
        self.setMinimumHeight(800)
        self.setMinimumWidth(700)

        self.central_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)

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
        self.show_hide_stats.clicked.connect(self.animate_stat_hide_show)

        self.addtask.setFixedWidth(200)
        self.buttons_container = QWidget()
        self.buttons_container_layout = QHBoxLayout()
        self.buttons_container_layout.addWidget(self.addtask, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.buttons_container_layout.addWidget(self.show_hide_stats, Qt.AlignmentFlag.AlignRight)
        self.buttons_container.setLayout(self.buttons_container_layout)
        self.taskwidget_layout.addWidget(self.buttons_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.taskwidget_layout.addStretch()

        data = fetch_data()
        for items in data:
            task_name, prio, status, category, task_id = items
            add_task = Add_Task(self, self.taskwidget_layout, task_name, prio, status, task_id, loading_data=True)
            add_task.add()

        self.pie_chart_widget = QWidget()
        self.pie_chart_widget_layout = QVBoxLayout()
        self.pie_chart_widget.setLayout(self.pie_chart_widget_layout)
        
        task_status_data = self.get_task_status_data()
        self.piegraph = PieGraph(task_status_data)
        piegraph_veiw = QtCharts.QChartView(self.piegraph)
        piegraph_veiw.setRenderHint(QPainter.Antialiasing)
        self.pie_chart_widget_layout.addWidget(piegraph_veiw)

        self.priority_bar_chart_widget = QWidget()
        self.priority_bar_chart_widget_layout = QVBoxLayout()
        self.priority_bar_chart_widget.setLayout(self.priority_bar_chart_widget_layout)
        self.priority_bar_chart = PriorityBarChart()
        barchart_veiw = QtCharts.QChartView(self.priority_bar_chart)
        barchart_veiw.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.priority_bar_chart_widget_layout.addWidget(barchart_veiw)

        self.statswidget_layout.addWidget(self.priority_bar_chart_widget)
        self.statswidget_layout.addWidget(self.pie_chart_widget)

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
        
        self.central_layout.addWidget(self.task_scroll)
        self.central_layout.addWidget(self.stat_scroll)
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
                                   max-width: 1200;
                                   }}
                                   QPushButton:hover {{
                                   background-color: {primary}
                                   }}
                                   """)
        self.stat_scroll.setStyleSheet(f"""
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
        self.task_scroll.setStyleSheet(f"""
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

    def animate_stat_hide_show(self):
        current_width = self.stat_scroll.width()
        self.animation = QPropertyAnimation(self.stat_scroll, b"maximumWidth")
        
        if current_width == 0:
            newwidth = QApplication.primaryScreen().size().width()/2.5
            self.animation.setEasingCurve(QEasingCurve.Type.OutBack)
        else:
            newwidth = 0
            self.animation.setEasingCurve(QEasingCurve.Type.InBack)

        self.animation.setDuration(500)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(newwidth)
        self.animation.start()


    def on_addtask_clicked(self):
        if not self.getting_task:
            self.getting_task = True
            layout = QHBoxLayout()    
            self.placeholder_widget = QWidget()
            self.placeholder_widget.setLayout(layout)
            add_task_no_dailog_widget = Add_Task_No_dialog(self, self.taskwidget_layout)
            layout.addWidget(add_task_no_dailog_widget)
            self.taskwidget_layout.insertWidget(1 , self.placeholder_widget) 

            self.placeholder_widget.setStyleSheet(f"""background : {primary}; max-width: 1200; border-radius: 5px""")

    def get_task_status_data(self):
        not_done, done = get_task_status_count()
        
        undone_task = {'name' : 'Not Completed', 'value': not_done, 'primary_color': QColor("#82d3e5"), 'secondary_color': QColor("#cfeef5")}
        done_task = {'name' : 'Completed', 'value': done, 'primary_color': QColor("#fd635c"), 'secondary_color': QColor("#fdc4c1")}
        data = [undone_task, done_task]

        return data
 
    def on_task_added(self):
        self.getting_task = False
        data = self.get_task_status_data()
        self.piegraph.update_data(data)


if __name__ == '__main__':
    app = QApplication([])
    windows = MainWindow()
    app.exec()