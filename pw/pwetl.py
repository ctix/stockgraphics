from  peewee import *
#import sqlite3

db = SqliteDatabase("stocks.db")

class BaseModel(Model):
    class Meta:
        database = db

class Onem(BaseModel):
    id = IntegerField()
    stockname = TextField()
    dealdetails = TextField()
    timestamp = TextField()
    #Timestamp = DateTimeField()

    class Meta:
        table_name = 'onem'


if __name__  == "__main__" :
    db.connect()
    p = Onem.get(Onem.timestamp == '2018-09-05 10:20:33')
    #p = Onem.select().where(Onem.stockname == '20:33').get()
    print(p.stockname)
    print(p.dealdetails)
    print(p.timestamp)

