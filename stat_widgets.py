from PySide6 import QtCharts
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from functools import partial
from settings import *
from db_data_functions import fetchBarChartPriorityData, fetchPiegraphData
import datetime


class PieGraph(QtCharts.QChart):
    def __init__(self, parent):
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
    
    def set_outer_series(self):
        slices = list()
        for data in self.data:
            slice_ = QtCharts.QPieSlice(data['name'], data['value'])
            slice_.setLabelVisible()
            slice_.setColor(QColor(data['primary_color']))
            slice_.setLabelBrush(QColor(data['primary_color']))

            slices.append(slice_)
            self.outer.append(slice_)

            slice_.hovered.connect(partial(self.explode, slice_, str(data['value']), data['name']))
    
    def set_inner_series(self):
        for data in self.data:
            slice_ = self.inner.append(data['name'], data['value'])
            slice_.setColor(QColor(data['secondary_color']))
            slice_.setBorderColor(QColor(data['secondary_color']))

    def explode(self, slice_,count, name, is_hovered):
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

    def update(self):
        self.clear_series()
        self.data = self.getData()
        self.set_inner_series()
        self.set_outer_series()

        legend = self.legend()
        for marker in legend.markers():
            if marker.series() == self.inner:
                marker.setVisible(False)

    def getData(self):
        return fetchPiegraphData()
    
    def clear_series(self):
        self.outer.clear()
        self.inner.clear()

class PriorityBarChart(QtCharts.QChart):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(500)
        self.days = 14
        self.barchart = QtCharts.QStackedBarSeries()
        self.barchart.setBarWidth(1)
        self.addSeries(self.barchart)
        self.update()
    
    def create_bars(self):
        for idx ,item in enumerate(self.priority_data):
            value_index = [self.all_dates.index(item) for item in self.dates_done if item in self.all_dates]
            bar_lst = [0 for _ in range(len(self.all_dates))]

            for index, val in enumerate(value_index):
                bar_lst[val] = item['values'][index]

            barset = QtCharts.QBarSet(item['label'])
            barset.append(bar_lst)
            self.barchart.append(barset)
            barset.setColor(QColor(item['color']))
            barset.hovered.connect(partial(self.showInfoOnHover, item['label'], bar_lst, self.all_dates))
        

        self.setTitle(f"Tasks done in the previous {self.limit} days")
        self.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)
        self.legend().setLabelBrush(QColor(qRgb(255,255,255)))
        self.setTitleBrush(QColor(qRgb(255,255,255)))
        self.setBackgroundBrush(QColor(backgroundColor))

    
    def update(self):
        self.get_variables()
        self.create_bars()
        self.set_axis()

    def get_variables(self):
        self.priority_data, self.dates_done, self.all_dates, self.limit = fetchBarChartPriorityData(self.days)
        self.removeSeries(self.barchart)
        self.barchart = QtCharts.QStackedBarSeries()
        self.barchart.setBarWidth(0.8)

    def set_axis(self):
        x = self.axisX()
        if x:
            self.removeAxis(x)

        self.dates = []
        for item in self.all_dates:
            self.dates.append(item.split("-")[2])

        self.addSeries(self.barchart)
        self.date_axis = QtCharts.QBarCategoryAxis()
        self.date_axis.append(self.dates)
        self.date_axis.setLabelsColor(QColor(qRgb(255,255,255)))
        self.y_axis = QtCharts.QValueAxis()
        self.y_axis.setLabelsColor(QColor(qRgb(255,255,255)))
        try:  
            max_val = sum([max(item['values']) for item in self.priority_data])+3
        except:
            max_val = 1
        self.y_axis.setRange(0 ,max_val)
        self.y_axis.setLabelFormat("%0.0f") 
        self.setAxisX(self.date_axis)
        self.setAxisY(self.y_axis)
        self.barchart.attachAxis(self.date_axis)
        self.barchart.attachAxis(self.y_axis)
        self.axisX().setGridLineVisible(False)
        self.axisY().setGridLineVisible(False)

    def showInfoOnHover(self, label, value, all_dates, status, barindex):
        tool_tip = QToolTip()
        tool_tip.showText(QCursor().pos(), f"Priority: {label} \n Tasks Done: {value[barindex]} \n At Day: {datetime.datetime.strptime(all_dates[barindex], '%Y-%m-%d').strftime('%A')} ,{all_dates[barindex]}")
        
        if not status:
            tool_tip.hideText()
