#coding=utf-8
"""
Demo the retrieving from stock pricing website , and
drawing the real time pricing and volume on the fly
Using the pyqtgraph and ,starting with one or two for examples
to Demonstrates the structure .
Fall in to 3 parts/functions 1, -- schedule the Market time to
perfom the whole Bidding data set .
2, Save to sqlite3  data base ,for after trail error debug
3, Real time Tracking use to call the place order system to buy/sell
    and long/short,  not include in this project
"""
###################
# TODO: 1, start before open/or after closed , returned date format
##    1.1 , the date time of every coming data set
## 2 , the Bidding price distribution info/dataset , add to the plotting
import time
import datetime
import threading
import sched
import numpy as np
from urllib.request import urlopen
import sqlite3
import os
import readconfig
import dataStruct

# from collections import namedtuple

#generating layout refer to layout file

# initiating the sched module scheduler
#


### TODO
# rethink the data structure, leave to next step
# Bidding = namedtuple('Bidding',['name','b1','b2'])
# namedtuple has no way to change the inside elements use
# dictionary data structure instead
# Stock = namedtuple('Stock',['name','price'])
# datum lines should be look like  list of dictionary

def AtTransactionTime():
    """ Transaction duration definition,and return which time segments """
    # print "Enter AtTransactionTime..."
    amStarttime, noonEndtime = datetime.time(9, 00), datetime.time(11, 30)
    pmStarttime, pmEndtime = datetime.time(13, 00), datetime.time(15, 00)
    nowtime = datetime.datetime.now().time()
    beforetime = nowtime < amStarttime
    AmDealtime = (nowtime > amStarttime) and (nowtime < noonEndtime)
    Noontime = (nowtime > noonEndtime) and (nowtime < pmStarttime)
    PmDealtime = (nowtime > pmStarttime) and (nowtime < pmEndtime)
    aftertime = (nowtime > pmEndtime)
    if beforetime:
        return "before"
    elif AmDealtime:
        return "amdeal"
    elif Noontime:
        return "noon"
    elif PmDealtime:
        return "pmdeal"
    elif aftertime:
        return "after"


def DueTime(duetime_hour, duetime_min):
    """ input duetime hour ,min Output Should return duetime ,used by enterabs """
    nowtime = time.localtime()
    yr, mo, dy = nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday  # get now date
    duetime = time.mktime((yr, mo, dy, duetime_hour, duetime_min, 0, 0, 0, 0))
    return duetime


class RetrieveOnLine:
    """Retrieving the the list stocks' bidding and pricing data from on line,
    return the data lines from the open moment """
    def __init__(self,stocklist,interval):
        self.stocklist = stocklist
        # initiating the sched module scheduler
        self._sched = sched.scheduler(time.time, time.sleep)
        self.datalines = []
        self.interval =  interval
        self.SegmentData = []
        for stk in stocklist:  # under change for the above reason
            self.datalines.append({"name":stk, "price": [],\
                                   "vol": []})
            # self.datalines.append({"name":stk, "price": np.array([]),\
                                   # "vol": np.array([])})
            # stock = Stock(stk,np.array([]))
            # self.datalines.append(stock)

        # show the updating the data in-place, otherwise it will be only a copy
        # self.datalines[0].price =np.append(self.datalines[0].price,new_data)


    def perform(self, name):
        """perform cycle scheduled task of xxx seconds """
        # if in between the noon , it should be waiting until the next
        #  Transaction, while other hand in afterwards , shall end
        if AtTransactionTime() in ["noon", "after"]:
            for task in self._sched.queue:
                if task.time - time.time() < 300:  # remove the am event from stack
                    self._sched.cancel(task)
                    print("scheduled latest removed by Market Close!!,clean up ready,save2db !!")
                    #self.SaveRec2db()  #store on received!, no need for clean task
                    # appendLineData()
            return []  # think twice no need to return
        self._sched.enter(self.interval, 0, self.perform, (name,))
        oneline = self.getStockData(name)
        if not oneline:
            print("Previous getting url sinaHq Errors! ,return 0 ,do nothing!!")
            return 0  #  will me ??
        ## compose the data item
        data_item = [name] + oneline
        self.pw_save(data_item)
        #self.SegmentData.append([name] + oneline)  # also store into sqlite3
        #timepoint = time.localtime()
        # about to remove every 5 minutes to save and clear
        #if timepoint.tm_min % 5 == 0:
        #if timepoint.tm_sec % 20 == 0:
        #    print("Time to Write to sqlite ,and empty this SegmentData Array!!!")
        #    self.SaveRec2db()



    def realtimeDataTracking(self):
        """ From the time of Open Market to Closed time , perform
        the Threading ,and scheduled tracking all the stocks
        in List ,and retrieve data and store and analysis """

        start = time.time()
        print(('START:', time.ctime(start)))
        # Below code should be observed if duetime past ,should executed immediately
        workAmTime = DueTime(9, 30)
        workPmTime = DueTime(13, 00)
        j = 0  # delay counter
        for stockcode in self.stocklist:  # improving below
            # stockname = "sh" + \
            #            stockcode if stockcode[:2] == "60" else "sz" + stockcode
            #before the Market open ,scheduled the inqury tasks
            self._sched.enterabs(workAmTime + 40 * j, 1, self.perform, (stockname,))
            self._sched.enterabs(workPmTime + 40 * j, 1, self.perform, (stockname,))
            j += 1

        print(self._sched.queue)
        t = threading.Thread(target=self._sched.run)  #
        t.start()  #
        t.join()  #


    def getStockData(self,stockCode):
        """open stock data provider  url get real time stock pricing/bidding
        but delays exist """
        import time
        # for testing and generating
        # if _Debug_Mode_:  # or AtTransactionTime() not in ["amdeal", "pmdeal"]:
        HqString = "http://hq.sinajs.cn/list=" + stockCode
        # from the url return data, retrive the data items ,return the price List
        # reading realtime bidding info from sina
        while True:  # if IOError wait 30seconds to retry
            try:
                begin_t = time.time()
                # print(HqString)
                hqList = urlopen(HqString).read()
                consume_t = time.time() - begin_t
                # print "getting from remote hq.sina,consumes %f seconds....." % consume_t
                # logger.info("Check if the HqString changed!!==> \n %s" % hqList)
                break
            except IOError:
                print("IOError ,sleep 20 second,then fetch again")
                time.sleep(20)

        hqList = str(hqList)
        hqList = hqList.split(',')
        # print("====retrieved Hq from sina ,the length ===>", hqList)
        if len(hqList) != 33:
            print("Length Error != 33 Hqlist is invalid!!!!!!!!!!! return 0  \n")
            print("Error List contains===>", hqList)
            return 0
        ### below code block show the data structure of the retrieved data
        todayOpen, yesClose, atTime = hqList[1], hqList[2],\
                                      hqList[31].split('"')[0]
        tmpHigh,tmpLow, tmpVol ,tmpMoney =  hqList[4], hqList[5],\
                                            hqList[8] , hqList[9]
        #only interest in price and vol , Biddings not used
        now_price = float(hqList[3])
        now_vol =  float(tmpVol)
        self.feed_datalines(stockCode, now_price, now_vol)
        # stkcode = stockCode[-6:]
        #stkcode = stockCode
        #indx = self.stocklist.index(stkcode)  #list index by stock name
        #assert self.datalines[indx]["name"] ==  stkcode
        #self.datalines[indx]["price"].append(now_price)
        #self.datalines[indx]["vol"].append(now_vol)

        valList = list(map(float, hqList[1:30])) + [hqList[30]] + [atTime]
        return valList

    def feed_datalines(self, stockCode, now_price, now_vol):
            ##   only interest in price and vol ,
            ##      Biddings not used
            indx = self.stocklist.index(stockCode)  #list index by stock name
            assert self.datalines[indx]["name"] ==  stockCode
            self.datalines[indx]["price"].append(now_price)
            self.datalines[indx]["vol"].append(now_vol)


    def pw_save(self,dt_item):
        if len(dt_item) < 1:  # nothing in Array
            print("Warning: Nothing in the received item !!")
            return
        stock, timestamp = dt_item[0],  " ".join(dt_item[30:])
        details = ', '.join(str(x) for x in dt_item[1:30])

        ## append the first to Mins table
        last_tmp = dataStruct.Mins(stock=stock, detail=details , dt=timestamp)
        save_n = last_tmp.save()
        print("numbers to save to sqlite!!==>",save_n )



    def SaveRec2db(self):
        if len(self.SegmentData) < 1:  # nothing in Array
            print("Warning: Nothing in the SegmentData!!")
            return
        #conn = sqlite3.connect('stocks.db')
        #curs = conn.cursor()
        #query = 'INSERT INTO Hq1min(stockname, Dealdetails, Timestamp) VALUES(?,?,?)'
        for datline in self.SegmentData:
            stock, timestamp = datline[0],  " ".join(datline[30:])
            details = ', '.join(str(x) for x in datline[1:30])
            # print("the data line ==>", datline)
            # stock, details, timestamp = datline[0], " ".join(datline[1]), " ".join(datline[2])
            vals = [stock, details, timestamp]

            ## append the first to Mins table
            last_tmp = dataStruct.Mins(stock=stock, detail=details , dt=timestamp)
            last_tmp.save()

            print("Values to save to sqlite!!==>", vals)
            curs.execute(query, vals)
        #conn.commit()
        self.SegmentData = []
        #conn.close()





if __name__ == "__main__":
    # MarketCloseTime = DueTime(15, 00)
    # Below code should be observed if duetime past ,should executed immediately
    # workAmTime = DueTime(9, 30)
    # workPmTime = DueTime(13, 00)
    now = datetime.datetime.now()
    print(str(now))
    #stlist = ["sz300474","sz002049"]
    stlist = readconfig.get_all()
    print("ALL options will be read from URL ==> {}".format(stlist))

    #test_re = RetrieveOnLine(stlist, 30)
    #test_re.realtimeDataTracking()
    #print(test_re.datalines)



