
"""Use candle stick module to plotting stock K -lines"""

from candlestick import CandlestickItem

import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

import tushare as ts


# read the sh index from the tushare module
shdata = ts.get_hist_data('sh',start = '2018-07-01',end='2018-09-09').sort_index()


## construct the candlestick required data structure
id_col  = [i for i in range(1, shdata.shape[0]+1)]  # rows
shdata["id"] = id_col


df_col_slice = shdata[["id", "open","close","low","high"]]
list_data = df_col_slice.values.tolist()
print(list_data)

item = CandlestickItem(list_data)
plt = pg.plot()
plt.addItem(item)
plt.setWindowTitle('pyqtgraph example: customGraphicsItem')


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    # QtGui.QApplication.instance().exec_()
    QtGui.QApplication([]).exec_()

