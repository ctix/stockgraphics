# -*- coding: utf-8 -*-
"""
This example demonstrates quadrants plotting pricing/vol line capabilities
in pyqtgraph. All of the plots may be panned/scaled by dragging with
the left/right mouse buttons. Right click on any plot to show a context menu.
"""

## TODO 0  in each quadrants draw both pricing and volumn [done]
## if possible ,try to plotting the bidding distribution along the
## Y axis/pricing axis [not yet]
## TODO 1 , simulating the retrieving and displaying process , by
## using the dataset pickle dumped before
import numpy as np
import datetime
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import pickle
from utilities import minMaxRange, scale_vol, compute_vol
from realtimeline import RetrieveOnLine, DueTime, AtTransactionTime

# Below code should be observed if duetime past ,should executed immediately
now = datetime.datetime.now()
print(str(now))
stlist = ["sz300474","sz002049","sz000977","sz002642"]
test_re = RetrieveOnLine(stlist, 30)

global ptr, pre_data, _debug, vol_data ,pre_vol ,scaler
pre_data = []
_debug = False
vol_data = []
pre_vol = [[],[],[],[]]   ## should be [][] 2d , for eachone in 4 quadrants
scaler = [0,0,0,0]

### pickle save /load the previous data
# import os
filename = "stdata0.pkl"
# if os.path.exists(filename):
message = "previous pickled data reloaded! , try make simulations "
try:
    with open(filename, 'rb') as pkl_file:
        pre_data = pickle.load(pkl_file)
        print(message)
        _debug = True
except FileNotFoundError:
    message = "Sorry ,the file " + filename + " Not Found"
    print(message)
# validating the pickle loaded data
# for i, line in enumerate(pre_data):
    # print("the first 20 price of the pre_data lines===>", line['price'][:20])
    # print("the first 20 vol of the pre_data lines===>", line['vol'][:20])



#data file name for pickle dump data structure
stdatafile = open("stdata_.pkl",'wb')

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="stock pricing plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p0 = win.addPlot(title="jjw300474" )
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

#merge the pickle load data to the datalines
## iminating the situation
if pre_data:
    _debug = True
    ptr = 0   # pointer to increase 1 by 1
    test_re.datalines = pre_data

for i,pdata in enumerate(test_re.datalines):
    print("the Length of the vol list==>",len(pdata['vol']))
   # exec("vol_curve{0}=p{0}.plot(voldata,pen='y',brush=(200,200,233),\
         # fillLevel=0)".format(i))
    if _debug:
        # define the downwards size
        down = 0.4
        #define/tackle the previous vol data as a whole
        voldata = scale_vol(pdata['vol'],pdata['price'],down)
        vol_data.append(voldata)

    exec("vol_curve{0}=p{0}.plot(voldata,pen='y')".format(i))
    exec("curve{0}=p{0}.plot(pdata['price'],pen='r',)".format(i))


## add the testing procedure to iminate the retrieving data
##

def update():
    global ptr, vol_data, pre_vol, scaler
    if not _debug and  AtTransactionTime() ==  "after":
        MarketClosed = True
        pickle.dump(test_re.datalines,stdatafile)
        time.sleep(300)
        print("Market Closed Already!!!")
        # stdatafile.close()
        return 0
    if not _debug and AtTransactionTime() == "noon" :
        # sleep until 13:00,think recover Retrieving exactly on time
        time.sleep(180)
        print("HeartBeat 3 minutes,expected the Market @pm")
        return 0


    for i,line_data in enumerate(test_re.datalines):
        if _debug:
            ptr += 1
            line_datap= line_data["price"][0:ptr]
            exec("curve{}.setData(line_datap)".format(i))
            now_price = line_datap[-1]
            exec("p{0}.setTitle('{1}@price ={2}',pen='y')".\
                format(i,line_data["name"],now_price))
            ### reproduce the sequnce of the vol for previous
            ### vol dataset all in the list, this is ok
            # temporarily  comment while debug the realtime vol
            # voldata =  vol_data[i][0:ptr]
            # print(line_data['name'])
            # print(ptr,line_datap)
            # exec("vol_curve{}.setData(voldata)".format(i))
            ##ok for known whole data, but when recieved 1 by 1
            ## must got another algorithm , show below

            first_price = line_data["price"][0]
            print("fist price", first_price)
            raw_vol = line_data['vol'][0:ptr]
            print("raw vol data list ==>", raw_vol)
            raw_vol_length = len(raw_vol)
            ## the length of the fitted volume can be done by
            ## the proportion to the previous volume value
            ## TODO :Twice think that get/apply the current volume to
            ## the current pirce range anyway . cause it is about to fit more
            ## when more data recieved
            if raw_vol_length > 2 :
                # real_vol = compute_vol(raw_vol)
                voldata = list(np.array(raw_vol[1:])-np.array(raw_vol[:-1]))
                mi, mx = min(line_data['price']),max(line_data['price'])
                print("voldata==>{0} \n, the price max ==> {1}, min=={2}".\
                      format(voldata, mx,mi))
                voldata = minMaxRange(voldata, (mi-down,mx-down))
                print("fitted vol data list ==>", voldata)
            exec("vol_curve{}.setData(voldata)".format(i))

        else:
            test_re.getStockData(line_data["name"])
            exec("curve{}.setData(line_data['price'])".format(i))
            exec("vol_curve{}.setData(voldata)".format(i))
            now_price = line_data["price"][-1]
            exec("p{0}.setTitle('{1}@price ={2}')".\
                format(i,line_data["name"],now_price))

timer = QtCore.QTimer()
timer.timeout.connect(update)
# interval 29 sec to update the plotting
# timer.start(23000)
if _debug:
    timer.start(900)
else:
    timer.start(23000)
# timer.start(999000)  ## not updating the plotting ,for the trial


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
    pickle.dump(test_re.datalines,stdatafile)
    stdatafile.close()

