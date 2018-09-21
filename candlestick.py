
"""
Demonstrate creation of a custom graphic (a candlestick plot)

"""
###TODO 1 : modify and fit the pandas dataframe and  tushare daily data
## TODO 2 : Grid and include, integrated in the realtime graphics

import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui
import tushare as ts

## Create a subclass of GraphicsObject.
## The only required methods are paint() and boundingRect()
## (see QGraphicsItem documentation)
class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()

    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly,
        ## rather than re-drawing the shapes every time.
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        # p.showGrid(x=True, y=True, alpha=0.7)
        w = (self.data[1][0] - self.data[0][0]) / 3.
        print(self.data[1][0])
        print(self.data[0][0])
        for (t, open, close, min, max) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())

data = [  ## fields are (time, open, close, min, max).
    (1., 10, 13, 5, 15),
    (2., 13, 17, 9, 20),
    (3., 17, 14, 11, 23),
    (4., 14, 15, 5, 19),
    (5., 15, 9, 8, 22),
    (6., 9, 15, 8, 16),
]
# read the sh index from the tushare module
# shdata = ts.get_hist_data('sh',start = '2018-07-15',end='2018-08-11').sort_index()
# oclh = shdata[]


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    item = CandlestickItem(data)
    plt = pg.plot()
    plt.addItem(item)
    plt.setWindowTitle('pyqtgraph example: customGraphicsItem')
    import sys
    QtGui.QApplication.instance().exec_()

