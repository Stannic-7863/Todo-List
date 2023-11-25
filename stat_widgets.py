from PySide6 import QtCharts
from PySide6.QtGui import QPainter, QColor, QBrush, qRgb
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QSize, Qt
import sys
from functools import partial
from settings import *


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


        slice_.setExplodeDistanceFactor(0.2)
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


        
