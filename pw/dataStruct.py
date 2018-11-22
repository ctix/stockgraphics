
from peewee import *

db = SqliteDatabase("stocks.db")

class BaseModel(Model):
    class Meta: database = db

class Mins(BaseModel):
    id = IntegerField()
    stock = CharField(max_length=8)
    detail = TextField()
    dt = DateTimeField()
    #Timestamp = DateTimeField()

    class Meta:
        table_name = 'mins'


