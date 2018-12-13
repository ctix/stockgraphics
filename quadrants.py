# -*- coding: utf-8 -*-
"""
Notice: only support to get whole bulk of datum , not one by one ,
Because , when evaluated as whole , it can decides the relative plotting size , and positions for price and volumn
This example demonstrates quadrants plotting pricing/vol line capabilities
in pyqtgraph.  Now the demo can show 4 stocks in quadrants with pricing and
volume, act as a stock pricing client in linux
"""

# TODO 0  in each quadrants draw both pricing and volumn [done]
# if possible ,try to plotting the bidding distribution along the
# Y axis/pricing axis [not yet]
# TODO 1 , simulating the retrieving and displaying process , by
# using the dataset pickle dumped before [done], in quadrants_vol

import numpy as np
import pandas as pd
import datetime
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import pickle
import json
from utilities import minMaxRange, getCurrentDate, sleep_seconds

from urllib.request import urlopen

# Below code should be observed if duetime past ,should executed immediately
now = datetime.datetime.now()
print(str(now))
stlist = ["sh600460", "sz002389", "sz300059", "sz300474"]

# TODO:  read the config from this file
rest_config_file = "pw/rest.ini"

#ip_port = "http://172.16.6.160:8000/"
ip_port = "http://127.0.0.1:8000/"
# ip_port = "http://192.168.1.04:8000/"
day_all_ = "today/"
history = "date/"
hq = "hq/"
sanic_day_rest_api = ip_port + day_all_
sanic_his_rest_api = ip_port + history
sanic_hq_rest_api = ip_port + hq

# TODO : move to the global definition file
# API returned data Structure
cols = ["open", "yclose", "price", "high", "low",
        "buy", "sell", "vol", "amt",
        "bv1", "b1", "bv2", "b2", "bv3", "b3", "bv4", "b4",
        "bv5", "b5",
        "sv1", "s1", "sv2", "s2", "sv3", "s3", "sv4", "s4",
        "sv5", "s5", "dt"]


def get_rest_pre_all(stock_name, type, hqdate=""):
    """retrieving all day biddings thru this api
    return a list of all transactions of this stock"""
    if type == "today":
        rest_api = sanic_day_rest_api + stock_name
    elif type == "his":
        rest_api = sanic_his_rest_api+stock_name + hqdate
    elif type == "mins":
        rest_api = sanic_hq_rest_api+_stockname
    else:
        print("BAD ROUTE, CHECK!!")

    detail_all = urlopen(rest_api).read()
    return json.loads(detail_all)


def get_minute_datum(stock_name):
    # read_rest_config(rest.ini)
    pass


def convert_dataframe(datum_lst):
    """convert the retrieved list datum to
    pandas DataFrame"""
    _dat_ls = []
    for dt in datum_lst:
        _spd = dt[0].split(",")
        _spd.append(dt[1])
        _dat_ls.append(_spd)
    return pd.DataFrame(_dat_ls, columns=cols, dtype=np.float)


def relative_data_vol(pdata):
    """voldata plotting size per price ,just for better look and feel on UI; pdata is a dictionary of {'price' :[], 'vol':[] } """
    try:
        assert len(pdata['vol']) > 2  # assure got a value list
    except Exception as e:  # May it be some huge stock got a long time to initating
        print(str(e), "data items less than 2")
    voldata = list(np.array(pdata['vol'][1:])-np.array(pdata['vol'][:-1]))
    mi, mx = min(pdata['price']), max(pdata['price'])
    #_voldata = minMaxRange(voldata, (mi-down,mx-down))
    _voldata = voldata   # Having second Axis , show the true value on it
    return _voldata


def plot_price_vol_curve(pdata, voldata, pos):
    mypen = pg.mkPen(color='r', width=3)
    exec("p{0}.plot(pdata['price'],pen=mypen)".format(pos))
    exec("pv{0}.addItem(pg.PlotCurveItem(voldata,pen='y'))".format(pos))


# def plot_parse_per_stock(stock_name, datum):
    # get_rest_pre_all(stock_name,type,hqdate=""):
    # get_minute_datum(stock_name)
    # for i,pdata in enumerate(test_re.datalines):
    #print("the Length of the vol list==>",len(pdata['vol']))
    #voldata = relative_data_vol(pdata)
    # plot_price_vol_curve(pdata,voldata,i)

# Handle view resizing
def updateViews():
    # view has resized; update auxiliary views to match
    for i in range(4):
        exec("pv{0}.setGeometry(p{0}.vb.sceneBoundingRect())".format(i))


app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="stock pricing plotting examples")
win.resize(1000, 600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

for i in range(4):
    if i == 2:
        win.nextRow()
    exec("p{} = win.addPlot(title='{}')".format(i, stlist[i]))
    exec("p{}.showGrid(x=True, y=True, alpha=0.7)".format(i))
    # set right axis
    exec("pv{} = pg.ViewBox()".format(i))     # ViewBox
    exec("p{}.showAxis('right')".format(i))     #
    exec("p{0}.scene().addItem(pv{0})".format(i))
    exec("p{0}.getAxis('right').linkToView(pv{0})".format(i))
    exec("pv{0}.setXLink(p{0})".format(i))
    # exec("p{}.getAxis('right').setLabel('axis2', color='#0000ff')".format(i))
    # print("i===={}".format(i))

# define the downwards size
down = 0.4


# merge the pickle load data to the datalines
# Animating the situation

def acquiring_plotting(indx, stockname, adate=""):
    if adate:
        skdatlst = get_rest_pre_all(stockname, "his", adate)
    else:
        skdatlst = get_rest_pre_all(stockname, "today")
    sk_all_df = convert_dataframe(skdatlst)
    # convert list to numpy array
    price_lst = np.array(sk_all_df["price"].tolist())
    vol_lst = np.array(sk_all_df["vol"].tolist())/100.0
    if not vol_lst.any():
        print("Error Ocurred!! , {} got nothing, next loop!!".format(stockname))
        return 0
    pdata = {"name": stockname,  "price": price_lst, "vol": vol_lst}

    if len(pdata['vol']) < 2:
        print("stock ==> {} has less than 2  items !!".format(stockname))
        return 0
    print("{}={}".format(stockname, len(pdata['vol'])))
    voldata = relative_data_vol(pdata)
    plot_price_vol_curve(pdata, voldata, indx)

    now_price, open_price = price_lst[-1], price_lst[0]
    return [now_price, open_price]


for i, stockname in enumerate(stlist):
    acquiring_plotting(i, stockname)

# add the testing procedure to iminate the retrieving data
###
# now_price

def percentage(now_price, open_price):
    return round(((now_price - open_price)/open_price)*100.0, 2)


def update():

    sleep_seconds()
    for i, stockname in enumerate(stlist):
        now_price, open_price = acquiring_plotting(i, stockname)
        uprate = percentage(now_price, open_price)
        # pg.mkPen('g', width=2)  # seemed no use =======2018.12.12.11:21(星期三)=======
        exec("p{0}.setTitle('{1}@{2} {3}%')"
             .format(i, stockname, now_price, uprate))


timer = QtCore.QTimer()
timer.timeout.connect(update)
# interval 29 sec to update the plotting
timer.start(40000)

updateViews()
# win.vb.sigResized.connect(updateViews)
for i in range(4):
    exec("p{}.vb.sigResized.connect(updateViews)".format(i))


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    # QtGui.QApplication.instance().exec_()
    app.exec_()
