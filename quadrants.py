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
# import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
# from pyqtgraph.Point import Point
# import pickle
import json
from utilities import sleep_seconds
from urllib.request import urlopen

# Below code should be observed if duetime past ,should executed immediately
now = datetime.datetime.now()
print(str(now))



def percentage(now_price, open_price):
    return round(((now_price - open_price)/open_price)*100.0, 2)


class RestAPI:
    def __init__(self, ip_port="http://127.0.0.1:8000/"):
        # TODO:  read the config from this file
        # rest_config_file = "pw/rest.ini"
        # ip_port = "http://172.16.6.160:8000/"
        ip_port = "http://127.0.0.1:8000/"
        # ip_port = "http://192.168.1.04:8000/"
        day_all_ = "today/"
        history = "date/"
        hq = "hq/"
        self.sanic_day_rest_api = ip_port + day_all_
        self.sanic_his_rest_api = ip_port + history
        self.sanic_hq_rest_api = ip_port + hq

    def get_his_api(self):
        return self.sanic_his_rest_api

    def get_api_by(self, stock_code, vtype, hqdate):
        if vtype == "today":
            rest_api = self.sanic_day_rest_api + stock_code
        elif vtype == "his":
            rest_api = self.sanic_his_rest_api + stock_code + hqdate
        elif vtype == "mins":
            rest_api = self.sanic_hq_rest_api + stock_code
        else:
            print("BAD ROUTE, CHECK!!")

        return rest_api


def get_rest_pre_all(stock_code, vtype="today", hqdate=""):
    """retrieving all day biddings thru this api
    return a list of all transactions of this stock"""
    rest_api = RestAPI()
    stock_api = rest_api.get_api_by(stock_code, vtype, hqdate)
    detail_all = urlopen(stock_api).read()
    return json.loads(detail_all)


# TODO : move to the global definition file
# API returned data Structure
cols = ["open", "yclose", "price", "high", "low",
        "buy", "sell", "vol", "amt",
        "bv1", "b1", "bv2", "b2", "bv3", "b3", "bv4", "b4",
        "bv5", "b5",
        "sv1", "s1", "sv2", "s2", "sv3", "s3", "sv4", "s4",
        "sv5", "s5", "dt"]


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
    """voldata plotting size per price ,just for better look and feel on
    UI; pdata is a dictionary of {'price' :[], 'vol':[] } """
    try:
        assert len(pdata['vol']) > 2  # assure got a value list
    except Exception as e:  # May it be some huge stock got a long time to initating
        print(str(e), "data items less than 2")
    volst = list(np.array(pdata['vol'][1:])-np.array(pdata['vol'][:-1]))
    # Having second Axis , show the true value on it
    return volst


def datum_from_api(stockname, adate=""):
    if adate:
        skdatlst = get_rest_pre_all(stockname, "his", adate)
    else:
        skdatlst = get_rest_pre_all(stockname, "today")

    return skdatlst


def validate_list(input_lst):
    if not input_lst.any():
        print("Empty !! nothing in List!!")
        return False
    elif len(input_lst) < 2:
        print("Valid items must more than TWO!! ")
        return False
    else:
        return True


def acquiring_latest_plotting_datum(stockname, adate=""):
    pdata = {}  # for getting the whole trading data only
    skdatlst = datum_from_api(stockname, adate)
    sk_all_df = convert_dataframe(skdatlst)
    # convert list to numpy array
    price_lst = np.array(sk_all_df["price"].tolist())
    vol_lst = np.array(sk_all_df["vol"].tolist())/100.0
    if validate_list(vol_lst):
        pdata = {"name": stockname,  "price": price_lst, "vol": vol_lst}
        print("{}={}".format(stockname, len(pdata['vol'])))
        return pdata
    else:
        return 0


def update_plot_data(indx,stockname,adate=""):
    pdata = acquiring_latest_plotting_datum(stockname, adate)
    price_lst = pdata['price']
    vol_lst = relative_data_vol(pdata)
    # plot_price_vol_curve(pdata, voldata, indx)
    return [price_lst, vol_lst]

    # plot_price_vol_curve(price_lst, vol_lst, indx)

    # now_price, open_price = price_lst[-1], price_lst[0]
    # return [now_price, open_price]


class StockGraph:
    def __init__(self, title, stock_list):
        self.stock_list =  stock_list
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title=title)
        self.win.resize(1000, 600)
        self.win.setWindowTitle(title)
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        # TODO: if eight securities , think how to tackle
        self.create_quadrants(stock_list)

    def create_quadrants(self, stlist):
        for i in range(4):
            if i == 2:
                self.win.nextRow()
            exec("self.p{} = self.win.addPlot(title='{}')"
                 .format(i, stlist[i]))
            # print("i===>", i)
            exec("self.p{}.showGrid(x=True, y=True, alpha=0.7)".format(i))
            # set right axis
            exec("self.pv{} = pg.ViewBox()".format(i))     # ViewBox
            exec("self.p{}.showAxis('right')".format(i))     #
            # self.p0.scene().addItem(self.pv0)
            exec("self.p{0}.scene().addItem(self.pv{0})".format(i))
            exec("self.p{0}.getAxis('right').linkToView(self.pv{0})".format(i))
            exec("self.pv{0}.setXLink(self.p{0})".format(i))

    def plot_price_vol_curve(self, price_lst, vol_lst, pos):
        mypen = pg.mkPen(color='r', width=3)
        exec("self.p{}.plot(price_lst , pen=mypen)".format(pos))
        exec("self.pv{}.addItem(pg.PlotCurveItem(vol_lst,pen='y'))"
                .format(pos))

    # Handle view resizing
    def updateViews(self):
        # view has resized; update auxiliary views to match
        for i in range(4):
            exec("self.pv{0}.setGeometry(self.p{0}\
                 .vb.sceneBoundingRect())".format(i))


    def update(self):
        # No need to check during the market trading period
        sleep_seconds()  # this shoule be considered to optimize
        # the following code toggle the displaying of more securities
        # stock_list = stlist if toggled_ else stlist1
        # toggled_ = 0  if toggled_ else 1
        for i, stockname in enumerate(self.stock_list):
            # pdatum = acquiring_latest_plotting_datum(stockname)
            pst, vlst = update_plot_data(i, stockname)
            self.plot_price_vol_curve(pst,vlst,i)
            now_price, open_price = pst[-1], pst[0]
            uprate = percentage(now_price, open_price)
            # pg.mkPen('g', width=2)  # seemed no use =======2018.12.12.11:21(星期三)=======
            exec("self.p{0}.setTitle('{1}@{2} {3}%')"
                .format(i, stockname, now_price, uprate))


    def run(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        # interval 29 sec to update the plotting
        timer.start(40000)

        self.updateViews()
        # win.vb.sigResized.connect(updateViews)
        for i in range(4):
            exec("self.p{}.vb.sigResized.connect(self.updateViews)".format(i))

        self.app.exec_()


# Thinking twice of add a button to toggle the views of
# more stock graphics, now , I change my mind that the timeout mechanism
# will do the job
# tglBtn = QtGui.QPushButton('<<Next>>')
# win.nextRow()
# win.addWidget(tglBtn)

# merge the pickle load data to the datalines
# Animating the situation

# add the testing procedure to iminate the retrieving data
###
# now_price


if __name__ == '__main__':
    stock_list = ["sh600460", "sz002389", "sz300059", "sz300474"]
    stlist1 = ["sh000001", "sz399001", "sz002008", "sz002414"]

    title_ = "Quadrant Display securities curves"
    quadrant_graph = StockGraph(title_, stock_list)
    # initiating the datum and plotting
    for i, stockname in enumerate(stock_list):
        pst, vlst = update_plot_data(i, stockname)
        quadrant_graph.plot_price_vol_curve(pst,vlst,i)

    quadrant_graph.run()
