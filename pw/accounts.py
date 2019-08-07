from peewee import *

# create a peewee database instance -- our models will use this database to
# persist information

DATABASE = 'accounts.db'
database = SqliteDatabase(DATABASE)

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage.
class BaseModel(Model):
    class Meta:
        database = database

# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
    username = CharField()     # could be the same with others , as
    password = BlobField()     # Must be Hash digest    bytes
    salt = BlobField()      # bytes
    email = CharField(unique=True) 
    join_date = DateField()
    expire_date = DateField()
    account_type = CharField()  # guest , test , payment, vip

def create_tables():
    with database:
        database.create_tables([User])



if __name__ == "__main__":
    pass
