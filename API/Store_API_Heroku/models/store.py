#Store model
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic") #Finds items through the relationship w Foreign Key

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name" : self.name, "items" : [item.json() for item in self.items.all()]} #.all() / query builder will slow down the call to json(), but save on storing items directly = TRADEOFF

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name LIMIT 1 !! Returns ItemModel object

    def save_to_db(self):
        db.session.add(self) #Updates data or inserting
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self) #Updates data or inserting
        db.session.commit()
