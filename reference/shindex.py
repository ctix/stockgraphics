"""this acting as a frame ,show the usage of the pyqtgraph
1. All of the necessary graph items to create the architecture
2. Experiment with the horizental line per biding price  ##TODO##
"""
import pyqtgraph as pg
import tushare as ts
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class BaseStockGraph:
    """first is a static daily graph"""
    def __init__(self,title,dataset):
        """dataset is like pandas data frame"""
        self.title = title
        self.DF = dataset   # DF is a data frame for short
        self.app = pg.QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title)
        # this line & below duplicated ??
        self.setAxies(self.DF.index)
        self.setGraphItems()
        self._scaleVol()
        self.drawGraph(self.DF[['open','close','voltrans']])
        # self.drawGraph(self.DF[['open','close']])

    def setAxies(self,date_index):
        """ set the vertical and horizontal axis  """
        self.xdict = dict(enumerate(date_index))
        axis_1 = [(i,list(date_index)[i]) for i in range(0,len(date_index),5)]
        stringaxis = pg.AxisItem(orientation='bottom')
        self.plot = self.win.addPlot(axisItems={'bottom':stringaxis},title="sh index")
        stringaxis.setTicks([axis_1, self.xdict.items()])

    def setGraphItems(self,):
        ## set Axis label
        self.plot.setLabel(axis='left', text='Index')
        self.plot.setLabel(axis='bottom', text='Date')
        ## Set the Cross cursor
        self.vLine = pg.InfiniteLine(angle=90, movable=False,)
        self.hLine = pg.InfiniteLine(angle=0, movable=False,)
        self.plot.addItem(self.vLine, ignoreBounds=True)
        self.plot.addItem(self.hLine, ignoreBounds=True)
        self.vb =self.plot.vb

        ##add text widget
        self.label = pg.TextItem()
        self.plot.addItem(self.label)
        #set the legend
        self.plot.addLegend(size=(150,80))

    def _scaleVol(self):
        """for the display purpose at same near coordination """
        min_max_scaler = MinMaxScaler((2300,3300))
        VOL = self.DF['volume'].values
        Vol = VOL.reshape(-1,1)
        Voltrans = min_max_scaler.fit_transform(Vol)
        self.DF['voltrans'] = Voltrans.T[0]



    def drawGraph(self,lines):
        """lines contains line data ,it's a subset of a data_frame"""
        openline = lines['open'].values
        closeline = lines['close'].values
        volline = lines['voltrans'].values
        # plot fill parameters to draw the volume line
        # self.plot.plot(x=list(self.xdict.keys()), y=data['voltrans'].values,pen='b',\
        #        name='vol', symbolBrush=(200,200,233))
        self.plot.plot(x=list(self.xdict.keys()), y=volline,name='vol',\
                  fillbrush=(200,200,233),fillLevel=1)
        #set the grid , show the horizental and vertical line ,transpency to 0.5
        self.plot.showGrid(x=True, y = True , alpha=0.5)
        ## paint the open and close index , pen as color
        self.plot.plot(x=list(self.xdict.keys()), y=openline,\
                       pen='r',name='openIndex',symbolBrush=(255,0,0),)
        self.plot.plot(x=list(self.xdict.keys()), y=closeline,\
                       pen='g',name='close Index',symbolBrush=(0,255,0))


    def mouseMoved(self,evt):
        pos = evt[0]  # using signal proxy turns original arguments into tuple
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint =self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            pos_y = int(mousePoint.y())
            # print(index)
            if 0 < index < len(data.index):
                print(self.xdict[index],self.DF['open'][index],self.DF['close'][index])
                self.label.setHtml("<p style='color:white'>date:{0}</p>\
                        <p style='color:white'>Open:{1}</p>\
                                   <p style='color:white'>close\
                        :{2}</p>".format(self.xdict[index],self.DF['open'][index],\
                                         self.DF['close'][index]))
                self.label.setPos(mousePoint.x(),mousePoint.y())
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def run(self):
        proxy = pg.SignalProxy(self.plot.scene().sigMouseMoved, \
                               rateLimit=60, slot=self.mouseMoved)
        self.app.exec_()


if __name__ == '__main__':
    data = ts.get_hist_data('sh',start = '2018-03-15',end='2018-08-11').sort_index()
    shgraph = BaseStockGraph("ShINDEX DEMO",data)
    shgraph.run()
