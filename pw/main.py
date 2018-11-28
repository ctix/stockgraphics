# from peewee import IntegerField, TextField, CharField, DateTimeField, SqliteDatabase, Model
from  peewee import *
from datetime import datetime
import time
from sanic import Sanic
from sanic.response import text,json
#from sanic_crud import generate_crud
#import sqlite3


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
    #Timestamp = DateTimeField()

    # Failed attempt, employ query outside instead
    #def getDaily(self,name,st_dt):
        #return (Mins
               #.select()
               #.where(
                   #(stock==name)
                   #&(dt > st_dt)
                   #&(dt < datetime.now())
               #).limit(6))


    class Meta:
        table_name = 'mins'

    #db.create_tables([Mins])


def get_hq_dt(type):
    dt = time.localtime()
    ## trading starting daily time
    hr,min = 9,30
    if type =='start':
        return datetime(dt.tm_year,dt.tm_mon,dt.tm_mday,hr,min,0,0)
    elif type =='now':
        return datetime(dt.tm_year,dt.tm_mon,dt.tm_mday,
                dt.tm_hour,dt.tm_min,dt.tm_sec,0)
    elif type =='1m_ago': ## only get datum of the specified stock @1minute ago
        return datetime(dt.tm_year,dt.tm_mon,dt.tm_mday,
                dt.tm_hour,dt.tm_min-1,dt.tm_sec,0)



app = Sanic(__name__)
#generate_crud(app, [Mins])
now_dt= get_hq_dt("now")
name = "sz300474"
hq_st_dt = get_hq_dt("start")
minhq=Mins.select().where((Mins.stock == name)
                            & (Mins.dt > hq_st_dt))#.limit
#lsthq = minhq.where(Mins.dt > hq_st_dt)
lsthq = []
#for it in minhq:
    #print("Details ==> {}\n @time ==> {}".format(it.detail,it.dt))
    #lsthq.append([it.detail, it.dt])

## Jsonfy,versus  text response , had different format, don't figure out Y
@app.route("/")
async def df_handler(request):
    return json("HoW R U ,Now {}, \n start date,time ==> {}".format(now_dt, hq_st_dt))
    #return text("HoW R U ,Now {}, \n start date,time ==> {}".format(now_dt, hq_st_dt))

#the Rest api get the datum 1 minute ago
@app.route("/hq/<name:[A-z0-9]+>")
async def stock_hq_handler(request,name):
    hq_1min = get_hq_dt("1m_ago")
    result_lst = []
    minhq=Mins.select().where((Mins.stock == name)
                            & (Mins.dt > hq_1min))#.limit
    for it in minhq:
       result_lst.append([it.detail,it.dt])

    #return json(minhq)
    return text(result_lst)

@app.route("/today/<name:[A-z0-9]+>")
async def stock_hq_handler(request,name):
    result_lst = []
    minhq=Mins.select().where((Mins.stock == name)
                            & (Mins.dt > hq_st_dt))#.limit
    print("name  name name ",name)
    for it in minhq:
       dt_ = it.dt
       dt_str = (dt_).strftime("%Y-%m-%d %H:%M:%S")
       result_lst.append([it.detail,dt_str])

    return json(result_lst)

@app.route("/date/<namedate:[A-z0-9]+>")
async def stock_his_handler(request,namedate):
    """handler query datum for the specified stock
    @ the history date"""
    result_lst = []
    name, yr,mn,dy = namedate[:8],namedate[8:12], namedate[12:14],namedate[14:]
    sdate = yr+"-"+mn+"-"+dy
    #_date = datetime.strptime(sdate,"%Y%m%d") print("namedate splite {} == {}".format(name,sdate))
    items=Mins.select().where((Mins.stock == name)
                            & (Mins.dt.contains(sdate)))
    for it in items:
       dt_ = it.dt
       dt_str = (dt_).strftime("%Y-%m-%d %H:%M:%S")
       result_lst.append([it.detail,dt_str])

    return json(result_lst)



app.run(host="0.0.0.0", port=8000, debug=True)


