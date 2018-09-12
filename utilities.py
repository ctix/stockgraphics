import numpy as np

def minMaxRange(x,range_values):
    """scale data list to fit the range values"""
    return [round( ((xx-min(x))/(max(x)-min(x)))*\
                    (range_values[1] - range_values[0])+\
            range_values[0],2) for xx in x]



def Compute_Vol_all(vol_data):
    """pdata['vol'] contains all the accumulative volume """
    voldata = list(np.array(vol_data[1:])-np.array(vol_data[:-1]))
    return voldata

def scale_vol_fit_price(pdata):
    """pdata['price'] contains all the price @ given moments"""
    mi, mx = min(pdata['price']),max(pdata['price'])
    # voldata = minMaxRange(pdata['vol'], (mi-down,mx-down))
    voldata = minMaxRange(voldata, (mi-down,mx-down))
    # print(voldata[:20])
    return voldata

def compute_vol(vol_data):
    """get the vol in the pointer sequence , given that in this accumulative
    volume case , the latest vol is the last two
    pdata['vol'] contains all the accumulative volume
    pdata['vol'] at least have 2 members"""
    return vol_data[-1]-vol_data[-2]

def compute_vol_fit(pre_vol, vol, base_value):
    """scale to the previous ,and fit with the base value
        return the price fitted vol values"""
    return round(vol/pre_vol,3)*base_value


## for getting data vol 1 by 1 , assume the first vol scale to the middle
## then next coming per this value with equal proportions
def scale2Range(vol,range_values):
    """scale data list to fit the range values, return a value near the
    range"""
    mid = (range_values[0] + range_values[1])/2
    scaler = round(vol/mid, 2)
    return scaler

def scale2Range(vol,price):  # too simple ,omit it
    """scale data list to fit the price values, return a scaler"""
    scaler = round(vol/price, 2)
    return scaler

def scale_vol(pdata_vol, pdata_price,down):
    ## in debug mode show the range/spectrum of the volume
    voldata = list(np.array(pdata_vol[1:])-np.array(pdata_vol[:-1]))
    mi, mx = min(pdata_price),max(pdata_price)
    ## must use numpy array copy to save this respectively or
    ##  computed laterly
    voldata = minMaxRange(voldata, (mi-down,mx-down))
    return voldata

