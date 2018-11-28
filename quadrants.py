# -*- coding: utf-8 -*-
"""
This example demonstrates quadrants plotting pricing/vol line capabilities
in pyqtgraph.  Now the demo can show 4 stocks in quadrants with pricing and
volume, act as a stock pricing client in linux
"""

## TODO 0  in each quadrants draw both pricing and volumn [done]
## if possible ,try to plotting the bidding distribution along the
## Y axis/pricing axis [not yet]
## TODO 1 , simulating the retrieving and displaying process , by
## using the dataset pickle dumped before [done], in quadrants_vol
import numpy as np
import datetime
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import pickle
import json
from utilities import minMaxRange, getCurrentDate

from urllib.request import urlopen

# Below code should be observed if duetime past ,should executed immediately
now = datetime.datetime.now()
print(str(now))
stlist = ["sh600460","sz002389","sz300059","sz300474"]
test_re = RetrieveOnLine(stlist, 30)

rest_config_file = "pw/rest.ini"

ip_port = "http://172.16.6.55:8000/"
day_all_="today/"
sanic_day_rest_api = ip_port + day_all_

def get_rest_api(stock_name):
    #sanic_rest_api = "http://172.16.6.55/hq"
    pass


def get_rest_pre_all(stock_name):
    """retrieving all day biddings thru this api
    return a list of all transactions of this stock"""
    detail_all = urlopen(sanic_day_rest_api + stock_name).read()
    return jason.loads(detail_all)

def get_minute_datum(stock_name):
    #read_rest_config(rest.ini)
    pass


def parse_per_stock(stock_name, datum):

    for i,pdata in enumerate(test_re.datalines):
        print("the Length of the vol list==>",len(pdata['vol']))
        if len(pdata['vol'])>2:
            voldata = list(np.array(pdata['vol'][1:])-np.array(pdata['vol'][:-1]))
            # print(voldata[:20])
            mi, mx = min(pdata['price']),max(pdata['price'])
            # voldata = minMaxRange(pdata['vol'], (mi-down,mx-down))
            voldata = minMaxRange(voldata, (mi-down,mx-down))
            # print(voldata[:20])
        # exec("vol_curve{0}=p{0}.plot(voldata,pen='y',brush=(200,200,233),\
             # fillLevel=0)".format(i))
        exec("vol_curve{0}=p{0}.plot(voldata,pen='y')".format(i))
        mypen = pg.mkPen(color='r',width=3)
        exec("curve{0}=p{0}.plot(pdata['price'],pen=mypen)".format(i))

## save the datfile named by the date created!!
#pkl_file_name = "stkpkl" + getCurrentDate()
#print("The pickled stock data will be saved in file ==> {}".format(pkl_file_name))

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="stock pricing plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p0 = win.addPlot(title="jjw300474" )
p0.showGrid(x=True, y=True, alpha=0.7)
p1 = win.addPlot(title="zggw002049")
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

def plot_price_vol__curve(pdata, voldata, pos):
    mypen = pg.mkPen(color='r',width=3)
    exec("curve{0}=p{0}.plot(pdata['price'],pen=mypen)".format(pos))
    exec("vol_curve{0}=p{0}.plot(voldata,pen='y')".format(pos))

global ptr, voldata
voldata = []
#merge the pickle load data to the datalines
## Animating the situation
for i,pdata in enumerate(test_re.datalines):
    print("the Length of the vol list==>",len(pdata['vol']))
    if len(pdata['vol'])>2:
        voldata = list(np.array(pdata['vol'][1:])-np.array(pdata['vol'][:-1]))
        # print(voldata[:20])
        mi, mx = min(pdata['price']),max(pdata['price'])
        # voldata = minMaxRange(pdata['vol'], (mi-down,mx-down))
        voldata = minMaxRange(voldata, (mi-down,mx-down))
        # print(voldata[:20])
    # exec("vol_curve{0}=p{0}.plot(voldata,pen='y',brush=(200,200,233),\
         # fillLevel=0)".format(i))
    plot_price_vol__curve(pdata, voldata, i)


## add the testing procedure to iminate the retrieving data
##

def update():
    global ptr, voldata
    if AtTransactionTime() ==  "after":
        MarketClosed = True
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
        exec("curve{}.setData(line_data['price'])".format(i))
        if len(line_data['vol']) > 2 :
            vol_data = list(np.array(line_data['vol'][1:]) \
                            -np.array(line_data['vol'][:-1]))
            mi, mx = min(line_data['price']),max(line_data['price'])
            vol_data = minMaxRange(vol_data, (mi-down,mx-down))
            print("vol_data==>{0} \n, the price max ==> {1}, min=={2}".\
                    format(vol_data, mx,mi))
            exec("vol_curve{}.setData(vol_data)".format(i))
        #display the current price in the title
        now_price = line_data["price"][-1]
        exec("p{0}.setTitle('{1}@price ={2}')".\
            format(i,line_data["name"],now_price))

timer = QtCore.QTimer()
timer.timeout.connect(update)
# interval 29 sec to update the plotting
# timer.start(23000)
timer.start(23000)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()

