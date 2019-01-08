from  peewee import *
#import sqlite3
import datetime
db = SqliteDatabase("stocks.db")

class BaseModel(Model):
    class Meta:
        database = db

class Onem(BaseModel):
    id = IntegerField()
    stockname = TextField()
    dealdetails = TextField()
    #timestamp = TextField()
    timestamp = DateTimeField()
    #Timestamp = DateTimeField()

    class Meta:
        table_name = 'onem'

def get_hq_dt(type):
    dt = time.localtime()
    if type =='start':
        return datetime.datetime(dt.tm_year,dt.tm_mon,dt.tm_mday,9,30,0,0)
    elif type =='now':
        return datetime.datetime(dt.tm_year,dt.tm_mon,dt.tm_mday,
                dt.tm_hour,dt.tm_min,dt.tm_sec,0)


if __name__  == "__main__" :
    db.connect()
    #p = Onem.get(Onem.timestamp == '2018-09-05 10:20:33')
    plist = Onem.select().where(
            (Onem.timestamp >= datetime.datetime(2018,8,5,9,0,0,0))
            & (Onem.timestamp < datetime.datetime(2018,9,5,10,30,0,0))
            )
            #.limit(30)
    #plist = Onem.select().where(Onem.timestamp >= datetime.datetime(2018,8,5,9,0,0,0))
    #p = Onem.select().where(Onem.stockname == '20:33').get()
    for p in plist :
        print(p.stockname)
        print(p.dealdetails)
        print(p.timestamp)

