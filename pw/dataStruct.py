from peewee import Model, SqliteDatabase, \
    IntegerField, CharField, TextField, DateTimeField

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


class Onem(BaseModel):
    """old table full of datum of realtime stock bidding info"""
    id = IntegerField()
    stockname = TextField()
    dealdetails = TextField()
    timestamp = TextField()


    class Meta:
        table_name = 'onem'


if __name__ == "__main__":
    p = Onem.get(Onem.timestamp == '2018-09-05 10:20:33')
    print(p.stockname)
    print(p.dealdetails)
    print(p.timestamp)
    ## append the first to Mins table
    last_tmp = Mins(stock=p.stockname, detail=p.dealdetails, dt=p.timestamp)
    last_tmp.save()
