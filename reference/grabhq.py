#coding=utf-8
import time
import datetime
import threading
import sched
import numpy as np
# import utilities
import sqlite3
import os

from urllib.request import urlopen

global SegmentData
global MarketCloseTime

SegmentData = []
global rDatum
rDatum = []


# initiating the sched module scheduler
s = sched.scheduler(time.time, time.sleep)
# logger = utilities.initlog()


def getStockData(stockCode):
    """use urllib to open and get real time stock pricing but delays exist """
    import time
    # for testing and generating
    # if _Debug_Mode_:  # or AtTransactionTime() not in ["amdeal", "pmdeal"]:
    HqString = "http://hq.sinajs.cn/list=" + stockCode
    # from the url return data, retrive the data items ,return the price List
    # reading realtime bidding info from sina
    while True:  # if IOError wait 30seconds to retry
        try:
            begin_t = time.time()
            print(HqString)
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
    print("====retrieved Hq from sina ,the length ===>", hqList)
    if len(hqList) != 33:
        print("Length Error != 33 Hqlist is invalid!!!!!!!!!!! return 0  \n")
        print("Error List contains===>", hqList)
        return 0
    todayOpen, yesClose, atTime = hqList[1], hqList[2], hqList[31].split('"')[
        0]
    # tmpHigh,tmpLow, tmpVol ,tmpMoney =  hqList[4], hqList[5], hqList[8] , hqList[9]
    # nowPrice = hqList[3]
    valList = list(map(float, hqList[1:30])) + [hqList[30]] + [atTime]
    return valList


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


def perform(inc, name):
    """perform cycle scheduled task of xxx seconds """

    global SegmentData
    if AtTransactionTime() in ["noon", "after"]:
        for task in s.queue:
            if task.time - time.time() < 300:  # remove the am event from stack
                s.cancel(task)
                print("scheduled latest removed by Close!!,clean up ready,save2db !!")
                # SaveRec2db()
            # should hold pm scheduled event in the queue
        #npDatum = np.array(SegmentData, dtype='|S12')
        #tdate = datetime.date.today()
        #datestr = tdate.strftime("%Y%m%d")
        #filename_saved = "datum" + datestr
        # np.save(filename_saved, npDatum)  # result = np.load("datefilename")
        return []  #
    s.enter(inc, 0, perform, (inc, name))
    oneline = getStockData(name)
    if not oneline:
        print("Previous getting url sinaHq Errors! ,return 0 ,do nothing!!")
        return 0
    # replace the last 2 pos gotten with the epoch time elapsed
    # bid_t = oneline[-2] + " " + oneline[-1]  #last 2 is date and time
    SegmentData.append([name] + oneline)
    timepoint = time.localtime()
    if timepoint.tm_min % 5 == 0:
        print("Time to Write to sqlite ,and empty this SegmentData Array!!!")
        SaveRec2db()


def SaveRec2db():
    global SegmentData
    if len(SegmentData) < 1:  # nothing in Array
        return
    conn = sqlite3.connect('stocks.db')
    curs = conn.cursor()
    query = 'INSERT INTO Hq1min(stockname, Dealdetails, Timestamp) VALUES(?,?,?)'
    for datline in SegmentData:
        stock, timestamp = datline[0],  " ".join(datline[30:])
        details = ', '.join(str(x) for x in datline[1:30])
        print("the data line ==>", datline)
        # stock, details, timestamp = datline[0], " ".join(datline[1]), " ".join(datline[2])
        vals = [stock, details, timestamp]
        print("Values to save to sqlite!!==>", vals)
        curs.execute(query, vals)
    conn.commit()
    SegmentData = []
    conn.close()


def realtimeDataTracking(inc=60):
    """ tracking all the stocks in List ,and retrieve data and store and analysis """
    global MarketCloseTime

    start = time.time()
    print(('START:', time.ctime(start)))
    # ÉèÖÃµ÷¶È
    # Below code should be observed if duetime past ,should executed immediately
    workAmTime = DueTime(9, 30)
    workPmTime = DueTime(13, 00)
    MarketCloseTime = DueTime(15, 00)

    stockCodeList = [ "300418", "002049", "600460","000977", "002389", "300474"]
    j = 0  # delay counter
    for stockcode in stockCodeList:  # improving below
        stockname = "sh" + \
            stockcode if stockcode[:2] == "60" else "sz" + stockcode
        s.enterabs(workAmTime + 40 * j, 1, perform, (inc, stockname))
        s.enterabs(workPmTime + 40 * j, 1, perform, (inc, stockname))
        j += 1

    print(s.queue)
    t = threading.Thread(target=s.run)  #
    t.start()  # Ïß³ÌÆô¶¯
    t.join()  # ×èÈûÏß³Ì


# ²âÊÔ´úÂë
if __name__ == "__main__":
    # os.chdir('D:/Runnings/')
    now = datetime.datetime.now()
    print(os.getcwd())
    print(str(now))
    realtimeDataTracking(59)
