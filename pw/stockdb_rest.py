#from peewee import IntegerField, TextField, CharField, DateTimeField, SqliteDatabase, Model
from  peewee import *
import datetime
from sanic import Sanic
from sanic_crud import generate_crud
from dataStruct import db, Mins

#db = SqliteDatabase("stocks.db")
#class BaseModel(Model):
    #class Meta:
        #database = db

#class Mins(BaseModel):
    #"""new table for a concise field name"""
    #id = IntegerField()
    #stock = CharField(max_length=8)
    #detail = TextField()
    #dt = DateTimeField()
    ##Timestamp = DateTimeField()

    #class Meta:
        #table_name = 'mins'


#db.create_tables([Mins])

app = Sanic(__name__)
generate_crud(app, [Mins])
app.run(host="0.0.0.0", port=8000, debug=True)


