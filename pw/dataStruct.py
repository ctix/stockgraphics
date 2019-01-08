
from peewee import *

db = SqliteDatabase("stocks.db")

class BaseModel(Model):
    class Meta: database = db

class Mins(BaseModel):
    """new table for a concise field name"""
    id = IntegerField()
    stock = CharField(max_length=8)
    detail = TextField()
    dt = DateTimeField()
    #Timestamp = DateTimeField()

    class Meta:
        table_name = 'mins'

class Onem(BaseModel):
    """old table full of datum of realtime stock bidding info"""
    id = IntegerField()
    stockname = TextField()
    dealdetails = TextField()
    timestamp = TextField()
    #Timestamp = DateTimeField()

    class Meta:
        table_name = 'onem'


if __name__  == "__main__" :
    #db.connect()
    p = Onem.get(Onem.timestamp == '2018-09-05 10:20:33')
    #p = Mins.get(Mins.timestamp == '2018-09-05 10:20:33')
    #p = Onem.select().where(Onem.stockname == '20:33').get()
    print(p.stockname)
    print(p.dealdetails)
    print(p.timestamp)
    ## append the first to Mins table
    last_tmp = Mins(stock=p.stockname, detail=p.dealdetails , dt=p.timestamp)
    last_tmp.save()

