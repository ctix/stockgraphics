from peewee import SqliteDatabase, Model, \
        IntegerField, CharField, TextField, DateTimeField
from datetime import datetime
import time
from sanic import Sanic
from sanic.response import html,json

db = SqliteDatabase("stocks.db")


class BaseModel(Model):
    class Meta:
        database = db


class Mins(BaseModel):
    """new table for a concise field name"""
    id = IntegerField()
    stock = CharField(max_length=8)
    detail = TextField()
    dt = DateTimeField()

    class Meta:
        table_name = 'mins'


def get_hq_dt(type):
    """get the current time ,return 3 types of datetime"""
    dt = time.localtime()
    hr, min = 9, 30
    if type == 'start':
        return datetime(dt.tm_year, dt.tm_mon, dt.tm_mday, hr, min, 0, 0)
    elif type == 'now':
        return datetime(dt.tm_year, dt.tm_mon, dt.tm_mday,
                        dt.tm_hour, dt.tm_min, dt.tm_sec, 0)
    # only get datum of the specified stock @1minute ago
    elif type == '1m_ago':
        return datetime(dt.tm_year, dt.tm_mon, dt.tm_mday,
                        dt.tm_hour, dt.tm_min-1, dt.tm_sec, 0)


app = Sanic(__name__)


@app.route("/")
async def df_handler(request):
    # return json("HoW R U ,Now {}, \n start date,time ==> {}".format(now_dt, hq_st_dt))
    return html(""" <html> <title>Available exposed Restful API</title>
            <P> <h1>Available exposed Restful API
        <p>
		<HR align=left width=300 color=#987cb9 SIZE=3>
        <p>
            <p> <h2> http://ip_address/      ==> this help
            <p> http://ip_address/hq/stockcode  ==> dataset 1 minuts ago
            <p> http://ip_address/today/stockcode
                        ==>dataset of the stock from today market open
            <p> http://ip_address/date/stockcode+date  ==> the history date data
            </html>""")


# the Rest api get the datum 1 minute ago
@app.route("/hq/<name:[A-z0-9]+>")
async def stock_hq_handler(request, name):
    hq_1min = get_hq_dt("1m_ago")
    result_lst = []
    minhq = Mins.select().where((Mins.stock == name)
                                & (Mins.dt > hq_1min))  # .limit
    for it in minhq:
        dt_str = (it.dt).strftime("%Y-%m-%d %H:%M:%S")
        result_lst.append([it.detail, dt_str])

    return json(result_lst)


@app.route("/today/<name:[A-z0-9]+>")
async def stock_hq_handler(request, name):
    # hq_today = get_hq_dt("now")
    hq_st_dt = get_hq_dt("start")
    result_lst = []
    minhq = Mins.select().where((Mins.stock == name)
                                & (Mins.dt > hq_st_dt))  # .limit
    for it in minhq:
        dt_ = it.dt
        dt_str = (dt_).strftime("%Y-%m-%d %H:%M:%S")
        result_lst.append([it.detail, dt_str])

    return json(result_lst)


@app.route("/date/<namedate:[A-z0-9]+>")
async def stock_his_handler(request, namedate):
    """handler query datum for the specified stock
    @ the history date"""
    result_lst = []
    name, yr, mn, dy = namedate[:8], namedate[8:12], namedate[12:14], namedate[14:]
    sdate = yr+"-"+mn+"-"+dy
    items = Mins.select().where((Mins.stock == name)
                                & (Mins.dt.contains(sdate)))
    for it in items:
        dt_ = it.dt
        dt_str = (dt_).strftime("%Y-%m-%d %H:%M:%S")
        result_lst.append([it.detail, dt_str])

    return json(result_lst)


app.run(host="0.0.0.0", port=8000, debug=True)
