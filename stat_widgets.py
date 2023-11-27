from PySide6 import QtCharts
from PySide6.QtGui import QColor, QBrush, qRgb
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication
from functools import partial
from settings import *
from db_data_functions import get_priority_data_for_bar_chart
import sys


class PieGraph(QtCharts.QChart):
    def __init__(self, data):
        super().__init__()
        self._data = data 
        self.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        self.outer = QtCharts.QPieSeries()
        self.inner = QtCharts.QPieSeries()
        self.outer.setHoleSize(0.4)
        self.inner.setPieSize(0.4)
        self.inner.setHoleSize(0.3)

        self.setBackgroundBrush(QBrush(QColor(qRgb(qbackground[0], qbackground[1], qbackground[2]))))
    
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
        for data in self._data:
            slice_ = QtCharts.QPieSlice(data['name'], data['value'])
            slice_.setLabelVisible()
            slice_.setColor(data['primary_color'])
            slice_.setLabelBrush(data['primary_color'])

            slices.append(slice_)
            self.outer.append(slice_)

            slice_.hovered.connect(partial(self.explode, slice_, str(data['value']), data['name']))
    
    def set_inner_series(self):
        for data in self._data:
            slice_ = self.inner.append(data['name'], data['value'])
            slice_.setColor(data['secondary_color'])
            slice_.setBorderColor(data['secondary_color'])

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

    def update_data(self, new_data):
        self.clear_series()
        self._data = new_data
        self.set_inner_series()
        self.set_outer_series()

        legend = self.legend()
        for marker in legend.markers():
            if marker.series() == self.inner:
                marker.setVisible(False)
    
    def clear_series(self):
        self.outer.clear()
        self.inner.clear()

class PriorityBarChart(QtCharts.QChart):
    def __init__(self):
        super().__init__()
        self.days = 18
        self.barchart = QtCharts.QStackedBarSeries()
        self.barchart.setBarWidth(1)
        self.addSeries(self.barchart)
        self.update()
        
    def create_bars(self):
        for index ,item in enumerate(self.priority_data):
            value_index = [self.all_dates.index(item) for item in self.dates_done if item in self.all_dates]
            bar_lst = [0 for _ in range(len(self.all_dates))]

            for index, val in enumerate(value_index):
                bar_lst[val] = item['values'][index]

            barset = QtCharts.QBarSet(item['label'])
            barset.append(bar_lst)
            self.barchart.append(barset)
            barset.setColor(QColor(qRgb(item['color'][0],item['color'][1],item['color'][2])))
        
        self.addSeries(self.barchart)
        self.setTitle(f"Tasks done in the previous {self.limit} days")
        self.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)
        self.legend().setLabelBrush(QColor(qRgb(255,255,255)))
        self.setTitleBrush(QColor(qRgb(255,255,255)))
        self.setBackgroundBrush(QColor(qRgb(qbackground[0], qbackground[1], qbackground[2])))

    
    def update(self):
        self.get_variables()
        self.set_axis()
        self.create_bars()

    def get_variables(self):
        self.priority_data, self.dates_done, self.all_dates, self.limit = get_priority_data_for_bar_chart(self.days)
        self.removeSeries(self.barchart)
        self.barchart = QtCharts.QStackedBarSeries()
        self.barchart.setBarWidth(1)
    
    def set_axis(self):
        x = self.axisX()
        if x :
            self.removeAxis(x)

        self.dates = []
        for item in self.all_dates:
            self.dates.append(item.split("-")[2])

        self.addSeries(self.barchart)
        self.date_axis = QtCharts.QBarCategoryAxis()
        self.date_axis.append(self.dates)
        self.date_axis.setLabelsColor(QColor(qRgb(255,255,255)))
        self.setAxisX(self.date_axis)
        self.barchart.attachAxis(self.date_axis)
        self.removeSeries(self.barchart)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    widget = PriorityBarChart()
    widget_view = QtCharts.QChartView()
    widget_view.setChart(widget)
    window.setCentralWidget(widget_view)
    window.show()
    app.exec()

