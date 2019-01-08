"""
Demonstrates some layout and customized mouse
interaction , and drawing a stock curve every 10 sec
that getting pricing and bidding data from  a provider.

"""

import numpy as np
import datetime
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import pickle
from realtimeline import RetrieveOnLine, DueTime, AtTransactionTime

# Below code should be observed if duetime past ,should executed immediately
now = datetime.datetime.now()
print(str(now))
stlist = ["sz300474","sz002049"]
test_re = RetrieveOnLine(stlist, 30)

## temparily store pickle the recieved data set
st_data = open("stdata.pkl",'wb')


#generate layout
app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: crosshair')
# label = pg.LabelItem(justify='right')
# win.addItem(label)
for i in range(1,4):
    c1 = win.addLabel("cl ",0,i)
    r1 = win.addLabel("r0 ",i,0)

# use c1 instead of label ,for place it up right
label = c1
p0 = win.addPlot(row=1, col=1,rowspan =2 ,colspan=1)
p1 = win.addPlot(row=1, col=2,rowspan =2 ,colspan=2)
p2 = win.addPlot(row=3, col=1, colspan=3)

region = pg.LinearRegionItem()
region.setZValue(10)   # wut the hell of this means ??
# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
# item when doing auto-range calculations.
p2.addItem(region, ignoreBounds=True)

#pg.dbg()
p1.setAutoVisible(y=True)
p1.showGrid(x=True, y=True, alpha=0.5)


#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
data0 = 10+ 15000 * pg.gaussianFilter(np.random.random(size=100), 10)\
            + 3000 * np.random.random(size=100)
#
data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

# define the stock_curve
#define the dynamic variable names
for i,stc in enumerate(stlist):
    exec('curve{}=p1.plot()'.format(i))
# stock_curve0 = p1.plot()
# stock_curve1 = p1.plot()

p0.plot(data0, pen="y")
# p1.plot(data1, pen="r")
# p1.plot(data2, pen="g")

p2.plot(data1, pen="w")

# initializing the
stockline0 = data1
stockline1 = data2

def update():
    global stock_curve1,  stock_curve2
    if AtTransactionTime() ==  "after":
        MarketClosed = True
        pickle.dump(test_re.datalines,st_data)
        time.sleep(300)
        print("Market Closed Alreedy!!!")
        return 0
    if AtTransactionTime() == "noon" :
        # sleep until 13:00,think recover Retrieving exactly on time
        time.sleep(180)
        print("HeartBeat 3 minutes,expected the Market @pm")
        return 0

    # print(test_re.datalines)
    for i,line_data in enumerate(test_re.datalines):
        test_re.getStockData(line_data["name"])
        print(line_data["name"])
        print(line_data["price"])
        exec("curve{}.setData(line_data['price'])".format(i))
        #stockline 1 ,2 save the data set
        exec("stockline{} = line_data['price']".format(i))
        # stock_curve0.setData(line_data["price"])
        # stock_curve1.setData(old_line["price"])
        # old_line = line_data

timer = QtCore.QTimer()
timer.timeout.connect(update)
# interval 29 sec to update the plotting
timer.start(29000)


# region.sigRegionChanged.connect(update)
#
def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)

p1.sigRangeChanged.connect(updateRegion)

region.setRegion([1000, 2000])

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)

vb = p1.vb

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if index > 0 and index < len(data1):
            label.setText("<span style='font-size: 12pt'>x=%0.1f, \
                          <span style='color: red'>y1=%0.1f</span>, \
                          <span style='color: green'>y2=%0.1f</span>"\
                          % (mousePoint.x(), stockline0[index], stockline1[index]))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())



proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
    pickle.dump(test_re.datalines,st_data)
    # test_re.realtimeDataTracking()
    # print(test_re.datalines)
