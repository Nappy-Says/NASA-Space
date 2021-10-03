from peewee import *

db = SqliteDatabase('db.db')

class BaseModel(Model):
    class Meta:
        database = db


class Satellite(BaseModel):
    id = AutoField()
    name = CharField()

class Lines(BaseModel):
    id = AutoField()
    line = CharField()
    satellite = ForeignKeyField(Satellite, related_name='lines')


if __name__ == '__main__':
    Satellite.create_table()
    Lines.create_table()
