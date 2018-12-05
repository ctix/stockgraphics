
# -*- coding: utf-8 -*-
"""
In this example we draw two different kinds of histogram.
the vertical shows the vol distribution
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

## the usage of the pyqtgraph , steps
win = pg.GraphicsWindow()       # 1, create the root windows
# win.resize(800,350)             # 2, resize the windows, and set Title
win.setWindowTitle('pyqtgraph example: Histogram')
plt1 = win.addPlot()            #3, add a plot area inside the root win
plt2 = win.addPlot()            # 4, more plot ,will in a stack order

## make interesting distribution of values
vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])
print("vals", vals)

## compute standard histogram
#y,x = np.histogram(vals, bins=np.linspace(-3, 8, 40))
x,y = np.histogram(vals, bins=np.linspace(-3, 8, 40))
y = y[:-1]
print("y",y,y.shape)
print("x===<",x,x.shape)

## Using stepMode=True causes the plot to draw two lines for each sample.
## notice that len(x) == len(y)+1
#plt1.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,150))
plt1.plot(x,y,fillLevel=0, brush=(0,0,255,150))

y,x = np.histogram(vals, bins=np.linspace(-3, 8, 40))
# plt2.plot(x,y,fillLevel=0, brush=(0,0,255,150))
plt2.plot(x, y, stepMode=True, fillLevel=0, brush=(134,0,0,150))
## Now draw all points as a nicely-spaced scatter plot
y = pg.pseudoScatter(vals, spacing=0.15)
# plt2.plot(vals, y, pen=None, symbol='o', symbolSize=5)
plt2.plot(vals, y, pen=None, symbol='o', symbolSize=5, \
          symbolPen=(255,255,255,200), symbolBrush=(133,133,33,150))

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
