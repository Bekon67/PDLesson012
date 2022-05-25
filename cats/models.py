from peewee import SqliteDatabase, Model, CharField, IntegerField


db = SqliteDatabase('base.db')


class Cats(Model):
    name = CharField()
    breed = CharField()
    age: IntegerField()

    class Meta:
      database = db




db.create_tables([Cats])
