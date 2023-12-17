import datetime
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from settings import *
from db_data_functions import change_priority_db, change_status_db, delete_task_db
import datetime

class custom_checkbox(QCheckBox):
    def __init__(self, text, parent, priority_str, mainwindowlayout, status, task_id, loading_data):
        super().__init__()

        layout = QHBoxLayout()
        self.loading_data = loading_data
        self.parent = parent
        self.setParent(self.parent)
        self.text = text
        self.priority_str = priority_str
        self.mainwindowlayout = mainwindowlayout
        self.status = status
        self.task_id = task_id

        self.text_label = QLabel()
        self.text_label.setText(self.text)
        self.text_label.setWordWrap(True)
        
        option_menu = self.create_task_options()
        
        layout.addWidget(self.text_label)
        layout.addWidget(option_menu, alignment= Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.mouse_inside = False
        
        self.color = get_color(self.priority_str)
        change_color(self, f"rgb{str(self.color)}")
        self.stateChanged.connect(lambda value: self.on_state_changed(value, self.color, self.parent))
        
        self.set_style_sheet()
        
    def create_task_options(self):
        self.options = QToolButton()
        self.options.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.options.setIcon(QIcon('./data/icons/menu.png'))
        self.options.setIconSize(QSize(30, 30))
        self.options.setMenu(self.create_menu())

        return self.options
    
    def create_menu(self):
        self.menu = QMenu(parent=self.parent)
        
        self.create_sub_menu_priority()
        
        edit = QAction('Edit', parent=self.parent)
        self.menu.addAction(edit)
        
        pomodoro = QAction('Pomdoro', parent=self.parent)
        pomodoro.triggered.connect(lambda : self.parent.pomodoro_widget.get_task(self.text, self.task_id))
        self.menu.addAction(pomodoro)
        
        delete = QAction('Delete', parent=self.parent)
        delete.triggered.connect(lambda : self.delete_task(self))
        self.menu.addAction(delete)

        return self.menu

    def create_sub_menu_priority(self):
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
        self.menu.addMenu(priority_menu)
        
    def change_prio(self, prio):
        previous_prio = self.priority_str
        current_color = self.color
        self.priority_str = prio
        self.color = get_color(prio)
        if self.isChecked() == False:
            start_animation(self, current_color , self.color)

        change_priority_db(previous_prio, self.priority_str, self.task_id)
        if not self.loading_data:    
            self.update_graphs()

    def on_state_changed(self, value, color, parent):
        state = Qt.CheckState(value)
        current_color = self.status

        current_datetime = datetime.datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        
        text_height = self.text_label.height()
        height = self.height()
        self.setMaximumHeight(text_height+height)
        
        if state == Qt.CheckState.Unchecked:
            start_animation(self, task_done, color)
            self.status = 'not done'
            self.parent.done_tasks_widget_layout.removeWidget(self)
            self.mainwindowlayout.insertWidget(1, self)
            if not self.loading_data: 
                change_status_db(current_color, self.status, self.task_id, formatted_date) 
        
        if state == Qt.CheckState.Checked:
            start_animation(self, color, task_done)
            self.status = 'done'
            self.mainwindowlayout.removeWidget(self)
            self.parent.done_tasks_widget_layout.insertWidget(2, self)
            if not self.loading_data:
                change_status_db(current_color, self.status, self.task_id, formatted_date)

        if not self.loading_data:  
            self.update_graphs() 
        
    def update_graphs(self):
        self.parent.priority_bar_chart.update()
        new_data = self.parent.get_task_status_data()
        self.parent.piegraph.update_data(new_data)
    
    def delete_task(self, widget: QCheckBox):
        delete_task_db(self.task_id)
        widget.deleteLater()
        self.update_graphs()
    
    def enterEvent(self, event):
        self.mouse_inside = True    
    def leaveEvent(self, event):
        self.mouse_inside = True
    def mousePressEvent(self, event):
        if self.mouse_inside:
            if event.button() == Qt.MouseButton.LeftButton:
                self.setChecked(not self.isChecked())
                
    def set_style_sheet(self):
        self.options.setStyleSheet(f"""
                                    QToolButton {{
                                    background-color : transparent;
                                    }}
                                    
                                    QToolButton::menu-indicator {{
                                    image: none;
                                    }}
                                    """)

        self.text_label.setStyleSheet(f"font-size: 18px")

class Add_Task:
    def __init__(self, parent, mainlayout, task_name, prio, status, task_id, loading_data=False):
        self.set_font()
        
        self.loading_data = loading_data
        self.text = task_name
        self.status = status
        self.mainwindowlayout = mainlayout
        self.parent = parent
        self.text = self.text.strip()

        if self.text:
            self.check_box = custom_checkbox(self.text, self.parent, prio, self.mainwindowlayout, self.status, task_id, self.loading_data)

            if self.status == 'done':
                self.check_box.setChecked(True)
                self.parent.done_tasks_widget_layout.insertWidget(2, self.check_box) 
            if self.status == 'not done':
                self.check_box.setChecked(False) 
                self.mainwindowlayout.insertWidget(1, self.check_box, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.loading_data = False
            
    def set_font(self):
        path = './data/fonts/bfont.TTF'
        fontinfo = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont(path))
        fontfamily = fontinfo[0] if fontinfo else 'Areil'
        QApplication.setFont(QFont(fontfamily))

def start_animation(widget, color_from, color_to):
    animation = QVariantAnimation(widget)
    animation.setDuration(400)
    animation.setStartValue(QColor(qRgb(color_from[0], color_from[1], color_from[2])))
    animation.setEndValue(QColor(qRgb(color_to[0], color_to[1], color_to[2])))
    animation.valueChanged.connect(lambda value: change_color(widget, value.name()))
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

def change_color(widget, color):
    widget.setStyleSheet(f"""
                            QCheckBox {{
                            background-color: {color};
                            color: white;
                            padding: 30px;
                            border-radius: 5px;
                            border : none
                            }}  
                            QCheckBox::indicator {{
                            image: none;
                            }}
                            QCheckBox::indicator:checked {{
                            image: none;
                            }}
                            QLabel {{
                            background-color : {color};
                            padding: 20px;
                            font-size: px
                            }}
                            """)
    
def get_color(prio):
    color = priority_none
    if prio == 'high':
        color = priority_high
    elif prio == 'mid':
        color = priority_mid
    elif prio == 'low':
        color = priority_low
        
    return color