#coding=utf-8
"""
Demo the retrieving from stock pricing website , and
drawing the real time pricing and volume on the fly
Using the pyqtgraph and ,starting with one or two for examples
to Demonstrates the structure .

"""

import time
import datetime
from urllib.request import urlopen

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point

#generate layout
app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.setWindowTitle('Real time stock pricing graph')
label = pg.LabelItem(justify='right')
win.addItem(label)
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)

region = pg.LinearRegionItem()
region.setZValue(10)
# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
# item when doing auto-range calculations.
p2.addItem(region, ignoreBounds=True)

p1.setAutoVisible(y=True)

global SegmentData
global MarketCloseTime

SegmentData = []
global rDatum
rDatum = []

    # replace the last 2 pos gotten with the epoch time elapsed


def perform(inc, name):
    """perform cycle scheduled task of xxx seconds """

    global SegmentData
    if AtTransactionTime() in ["noon", "after"]:
        for task in s.queue:
            if task.time - time.time() < 300:  # remove the am event from stack
                s.cancel(task)
                print("scheduled latest removed by Close!!,clean up ready,save2db !!")
                SaveRec2db()
        return []  #
    oneline = getStockData(name)
    if not oneline:
        print("Previous getting url sinaHq Errors! ,return 0 ,do nothing!!")
        return 0
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

    stockCodeList = ["300251", "300070", "002594",
                     "002415", "002349", "600869", "601336", "601727"]
    j = 0  # delay counter
    for stockcode in stockCodeList:  # improving below
        stockname = "sh" + \
            stockcode if stockcode[:2] == "60" else "sz" + stockcode
        s.enterabs(workAmTime + 40 * j, 1, perform, (inc, stockname))
        s.enterabs(workPmTime + 40 * j, 1, perform, (inc, stockname))
        j += 1

    print(s.queue)
    # Æô¶¯Ïß³Ì
    t = threading.Thread(target=s.run)  # Í¨¹ý¹¹Ôìº¯ÊýÀý»¯Ïß³Ì
    t.start()  # Ïß³ÌÆô¶¯
    t.join()  # ×èÈûÏß³Ì


#######################################
### copied old functions  ###
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



#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

p1.plot(data1, pen="r")
p1.plot(data2, pen="g")

p2.plot(data1, pen="w")

def update():
    region.setZValue(10)
    minX, maxX = region.getRegion()
    p1.setXRange(minX, maxX, padding=0)

region.sigRegionChanged.connect(update)

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
            label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())



proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)

# data = np.random.normal(size=(50,500))
data = np.random.normal(size=(50,1))
ptr = 0
lastTime = time()
fps = None
alldt = []
print("the data as it's",data,end='')
def update():
    global curve, data, ptr, p, lastTime, fps,alldt
    # data = np.roll(data,1)
    alldt = np.append(alldt,data[ptr%50])  # rolling the dataset over and over
    # curve.setData(data[ptr%10])
    curve.setData(alldt)
    # curve.setPos(ptr*10 ,0)
    # line2 = -alldt + np.random.normal(3)  # change the whole line over time
    line2 = -alldt + 3  # move above 3 units
    # curve.setData[line2]
    p.plot(line2,pen='y')

    ptr += 1
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    p.setTitle('%0.2f fps' % fps)
    # app.processEvents()  ## force complete edraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(800)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    QtGui.QApplication.instance().exec_()


# ²âÊÔ´úÂë
if __name__ == "__main__":
    # os.chdir('D:/Runnings/')
    now = datetime.datetime.now()
    print(os.getcwd())
    print(str(now))
    realtimeDataTracking(59)



