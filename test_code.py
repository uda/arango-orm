from datetime import date
from arango import ArangoClient
from arango_orm.database import Database
from arango_orm.collections import Collection
from marshmallow.fields import List, String, UUID, Integer, Boolean, DateTime, Date
from marshmallow import (
    Schema, pre_load, pre_dump, post_load, validates_schema,
    validates, fields, ValidationError
)

client = ArangoClient(username='test', password='test')
test_db = client.db('test')

db = Database(test_db)

from tests.data import Car
lancer = Car(make='Mitsubishi', model='Lancer', year=2005)
db.add(lancer)
lancer._dump()

class Person(Collection):
    __collection__ = 'persons'

    class _Schema(Schema):
        _key = String(required=True)
        name = String(required=True, allow_none=False)
        dob = Date()



db.query(Person).count()
db.query(Person).all()

p = Person(name='test', _key='12312', dob=date(year=2016, month=9, day=12))
db.add(p)
db.query(Person).count()


pd = {'_key': '37405-4564665-7', 'dob': '2016-09-12', 'name': 'Kashif Iftikhar'}
data, errors = Person._Schema().load(pd)
new_person = Person._load(pd)

new_col = Collection('new_collection')
db.create_collection(new_col)
db.drop_collection(new_col)