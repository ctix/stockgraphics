from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database


db.create_tables([Person, Pet])

from datetime import date
#uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
me = Person(name='me', birthday=date(1971, 6, 15))

#uncle_bob.save() # bob is now stored in the database
me.save()

#one = Person.get(Person.name == 'me')
lst = Person.select()

for i in lst:
    print(i.name, i.birthday)

# Returns: 1
