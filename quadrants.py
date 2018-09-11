
# -*- coding: utf-8 -*-
"""
This example demonstrates quadrants plotting pricing/vol line capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

## TODO in each quadrants draw both pricing and volumn
## if possible ,try to plotting the bidding distribution along the
## Y axis/pricing axis
import numpy as np
import datetime
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import pickle
from realtimeline import RetrieveOnLine, DueTime, AtTransactionTime

def minMaxRange(x,range_values):
    """scale data list to fit the range values"""
    return [round( ((xx-min(x))/(max(x)-min(x)))*\
                    (range_values[1] - range_values[0])+\
            range_values[0],2) for xx in x]

# Below code should be observed if duetime past ,should executed immediately
now = datetime.datetime.now()
print(str(now))
stlist = ["sz300474","sz002049","sz000977","sz002642"]
test_re = RetrieveOnLine(stlist, 30)

### pickle save /load the previous data
pkl_file = open('stdata1.pkl', 'rb')
pre_data = pickle.load(pkl_file)
pkl_file.close()

stdatafile = open("stdata1.pkl",'wb')


app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="stock pricing plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p0 = win.addPlot(title="jjw300474" )
p0.setTitle
# curve0 = p0.plot(pre_data[0]["price"] ,pen= "r")
p0.showGrid(x=True, y=True, alpha=0.7)
p1 = win.addPlot(title="zggw002049")
# curve1 = p1.plot(pre_data[1]["price"],pen = "g")
p1.showGrid(x=True, y=True, alpha=0.7)

win.nextRow()
p2 = win.addPlot(title="lcxx000977")
p2.showGrid(x=True, y=True, alpha=0.8)
curve2 = p2.plot(pen = "y")

p3 = win.addPlot(title="rzl002642")
p3.showGrid(x=True, y=True, alpha=0.9)
curve3 = p3.plot(pen = "b")

#define the dynamic variable names
print(list(enumerate(stlist)))
# define the downwards size
down = 0.4

#merge the pickle load data to the datalines
test_re.datalines = pre_data
for i,pdata in enumerate(test_re.datalines):
    # print(pdata['vol'][:30])
    if len(pdata['vol'])>2:
        voldata = list(np.array(pdata['vol'][1:])-np.array(pdata['vol'][:-1]))
        print(voldata[:20])
        mi, mx = min(pdata['price']),max(pdata['price'])
        # voldata = minMaxRange(pdata['vol'], (mi-down,mx-down))
        voldata = minMaxRange(voldata, (mi-down,mx-down))
        print(voldata[:20])
    # exec("vol_curve{0}=p{0}.plot(voldata,pen='y',brush=(200,200,233),\
         # fillLevel=0)".format(i))
        exec("vol_curve{0}=p{0}.plot(voldata,pen='y')".format(i))
    exec("curve{0}=p{0}.plot(pdata['price'],pen='r',)".format(i))


def update():
    if AtTransactionTime() ==  "after":
        MarketClosed = True
        pickle.dump(test_re.datalines,stdatafile)
        time.sleep(300)
        print("Market Closed Alreedy!!!")
        # stdatafile.close()
        return 0
    if AtTransactionTime() == "noon" :
        # sleep until 13:00,think recover Retrieving exactly on time
        time.sleep(180)
        print("HeartBeat 3 minutes,expected the Market @pm")
        return 0

    # print(test_re.datalines)
    for i,line_data in enumerate(test_re.datalines):
        test_re.getStockData(line_data["name"])
        print(line_data["name"],line_data["price"])
        exec("curve{}.setData(line_data['price'])".format(i))
        exec("vol_curve{}.setData(line_data['vol'])".format(i))
        now_price = line_data["price"][-1]
        exec("p{0}.setTitle('{1}@price ={2}')".\
             .format(i,line_data["name"],now_price))

timer = QtCore.QTimer()
timer.timeout.connect(update)
# interval 29 sec to update the plotting
timer.start(23000)
# timer.start(999000)  ## not updating the plotting ,for the trial


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
    pickle.dump(test_re.datalines,stdatafile)
    stdatafile.close()

