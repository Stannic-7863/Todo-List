from PySide6 import QtCharts
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from functools import partial
from settings import *
from db_data_functions import *
import datetime

import matplotlib.pyplot as plt 
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Agg')
matplotlib.rcParams['path.simplify_threshold'] = 1.0
plt.rcParams["agg.path.chunksize"] = 10000
plt.style.use("rose-pine")
color = plt.rcParams['axes.prop_cycle'].by_key()['color']

class PieGraph(QtCharts.QChart):
    """
    PieGraph for comparing Undone and done task ratio
    """
    def __init__(self, parent) -> None:
        super().__init__()
        self.parent = parent
        self.setMinimumHeight(400)
        self.data = self.getData()
        self.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.outer = QtCharts.QPieSeries()
        self.inner = QtCharts.QPieSeries()
        self.outer.setHoleSize(0.4)
        self.inner.setPieSize(0.4)
        self.inner.setHoleSize(0.3)

        self.setBackgroundBrush(QBrush(QColor(backgroundColor)))
    
        self.set_outer_series()
        self.set_inner_series()

        self.addSeries(self.outer)
        self.addSeries(self.inner)

        legend = self.legend()
        legend.setAlignment(Qt.AlignmentFlag.AlignBottom)
        for marker in legend.markers():
            if marker.series() == self.inner:
                marker.setVisible(False)
    
    def set_outer_series(self) -> None:
        slices = list()
        for data in self.data:
            slice_ = QtCharts.QPieSlice(data['name'], data['value'])
            slice_.setLabelVisible()
            slice_.setColor(QColor(data['primary_color']))
            slice_.setLabelBrush(QColor(data['primary_color']))

            slices.append(slice_)
            self.outer.append(slice_)

            slice_.hovered.connect(partial(self.explode, slice_, str(data['value']), data['name']))
    
    def set_inner_series(self) -> None:
        for data in self.data:
            slice_ = self.inner.append(data['name'], data['value'])
            slice_.setColor(QColor(data['secondary_color']))
            slice_.setBorderColor(QColor(data['secondary_color']))

    def explode(self, slice_,count, name, is_hovered) -> None:
        """Event Handle for hover event. Explode the slice on hover"""
        if is_hovered:
            start = slice_.startAngle()
            end = slice_.startAngle()+slice_.angleSpan()
            self.inner.setPieStartAngle(end)
            self.inner.setPieEndAngle(start+360)
            slice_.setLabel(count)
            
        else:
            self.inner.setPieStartAngle(0)
            self.inner.setPieEndAngle(360)
            slice_.setLabel(name)
            
        slice_.setExplodeDistanceFactor(0.1)
        slice_.setExploded(is_hovered)

    def update(self) -> None:
        """
        Update the PieGraph with new values
        """
    
        self.clear_series()
        self.data = self.getData()
        self.set_inner_series()
        self.set_outer_series()

        legend = self.legend()
        for marker in legend.markers():
            if marker.series() == self.inner:
                marker.setVisible(False)

    def getData(self) -> list[dict[str, any]]:
        """
        Returns data in [{done}, {undone}] formate about Undone and done tasks
        """
        return fetchPiegraphData()
    
    def clear_series(self) -> None:
        self.outer.clear()
        self.inner.clear()

class PriorityBarGraph(QtCharts.QChart):
    """
    Bargraph to display info about tasks done on a specific day
    """
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(500)
        self.tool_tip = QToolTip()
        self.days = 14
        self.barGraph = QtCharts.QStackedBarSeries()
        self.barGraph.setBarWidth(0.8)
        self.addSeries(self.barGraph)
        self.update()
    
    def create_bars(self) -> None:
        """Create bars for the barGraph"""
        for idx ,item in enumerate(self.priority_data):
            value_index = [self.all_dates.index(item) for item in self.dates_done if item in self.all_dates]
            bar_lst = [0 for _ in range(len(self.all_dates))]

            for index, val in enumerate(value_index):
                bar_lst[val] = item['values'][index]

            barset = QtCharts.QBarSet(item['label'])
            barset.append(bar_lst)
            self.barGraph.append(barset)
            barset.setColor(QColor(item['color']))
            barset.hovered.connect(partial(self.showInfoOnHover, item['label'], bar_lst, self.all_dates))
        

        self.setTitle(f"Tasks done in the previous {self.limit} days")
        self.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)
        self.legend().setLabelBrush(QColor(qRgb(255,255,255)))
        self.setTitleBrush(QColor(qRgb(255,255,255)))
        self.setBackgroundBrush(QColor(backgroundColor))

    
    def update(self) -> None:
        """Update the barGraph with new values"""
        self.get_variables()
        self.create_bars()
        self.set_axis()

    def get_variables(self) -> None:
        """Get new values and reset the barGraph"""
        self.priority_data, self.dates_done, self.all_dates, self.limit = fetchBarGraphPriorityData(self.days)
        self.removeSeries(self.barGraph)
        self.barGraph = QtCharts.QStackedBarSeries()
        self.barGraph.setBarWidth(0.8)

    def set_axis(self) -> None:
        """
        Give an axis to the BarGraph
        """
        
        x = self.axisX()
        if x:
            self.removeAxis(x)

        self.dates = []
        for item in self.all_dates:
            self.dates.append(item.split("-")[2])

        self.addSeries(self.barGraph)
        self.date_axis = QtCharts.QBarCategoryAxis()
        self.date_axis.append(self.dates)
        self.date_axis.setLabelsColor(QColor(qRgb(255,255,255)))
        self.y_axis = QtCharts.QValueAxis()
        self.y_axis.setLabelsColor(QColor(qRgb(255,255,255)))
        max_val = 0
        try :
            max_val = sum([max(item['values']) for item in self.priority_data])+3
        except :
            max_val = 1
        self.y_axis.setRange(0 ,max_val)
        self.y_axis.setLabelFormat("%0.0f") 
        self.setAxisX(self.date_axis)
        self.setAxisY(self.y_axis)
        self.barGraph.attachAxis(self.date_axis)
        self.barGraph.attachAxis(self.y_axis)
        self.axisX().setGridLineVisible(False)
        self.axisY().setGridLineVisible(False)

    def showInfoOnHover(self, label, value, all_dates, status, barindex):
        """Event handler for hover events. Shows info on hover"""
        
        self.tool_tip.showText(QCursor().pos(), f"Priority: {label} \n Tasks Done: {value[barindex]} \n At Day: {datetime.datetime.strptime(all_dates[barindex], '%Y-%m-%d').strftime('%A')} ,{all_dates[barindex]}")
        
        if not status:
            self.tool_tip.hideText()

class SessionTimeBarGraph(QWidget):
    def __init__(self, taskId):
        super().__init__()
        self.setMaximumWidth(900)
        self.setMinimumHeight(500)
        self.layout = QHBoxLayout(self)    
        self.taskId = taskId
        
        self.canvas = FigureCanvas(Figure(figsize=(9,1), dpi=100))
        self.layout.addWidget(self.canvas)
        
        self.ax = self.canvas.figure.add_subplot(111)
        self.dpi = self.canvas.figure.get_dpi()

        self.createBars()
        
        self.tooltip = QToolTip()
        self.tooltip.hideText()
        
    def createBars(self):
        self.data = fetchPomodoroAllSessionDataForSingleTask(taskId=self.taskId)
        self.xData = []
        self.yData = []
        for index, sessionInfo in enumerate(self.data):
            self.xData.append(index)
            self.yData.append(round(sessionInfo[2]/60, 2))
        
        self.graph = self.ax.bar(self.xData, self.yData, color=color)
        self.canvas.mpl_connect("motion_notify_event", self.hover)
        self.ax.set_ylabel("Time Spent (Minutes)")
        self.ax.set_xlabel("Session")
        self.canvas.draw()
    
    def updateTooltip(self, index) -> None:  
        sessionInfo = self.data[index]
        text = f"Start : {sessionInfo[0]} \nEnd : {sessionInfo[1]} \nDuration : {round(sessionInfo[3]/60, 2)} Minutes \nFocus : {round(sessionInfo[2]/60, 2)} Minutes"
        
        self.tooltip.showText(QCursor().pos(), text)

    def hover(self, event) -> None:
        """Handle hover event over the bars"""
        if event.inaxes == self.ax:
            for index, bar in enumerate(self.graph):
                contains, _ = bar.contains(event)
                if contains:
                    self.updateTooltip(index)
        else:
            self.tooltip.hideText()