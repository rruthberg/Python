#Item model
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
#import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id")) #Refer to store id by Foreign Key
    store = db.relationship("StoreModel") #Joins StoreModel by the foreign key

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name" : self.name, "price" : self.price, "store_id" : self.store_id}

    @classmethod
    def find_by_name(cls, name):
        #Statements from SQLite replaced by SQLAlchemy:
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name=name LIMIT 1 !! Returns ItemModel object
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query, (name, ))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return cls(*row) #argument unpacking -> variables ordered in same way we want to return them
        #     #return {"item" : {"name" : row[0], "price" : row[1]}}
        #     #return {"item" : ItemModel.json(self)}

    #def insert(self):
    def save_to_db(self):
        #Statements from SQLite replaced by SQLAlchemy:
        db.session.add(self) #Updates data or inserting
        db.session.commit()
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

    #def delete(self, name):
    def delete_from_db(self):
        #Statements from SQLite replaced by SQLAlchemy:
        db.session.delete(self) #Updates data or inserting
        db.session.commit()
        #global items #refer to the outer items variable
        #items = list(filter(lambda x: x["name"] != name, items))
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name = ?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return {"message" : "Item deleted"}

    # def update(self):
    #     connection = sqlite3.connect("data.db")
    #     cursor = connection.cursor()
    #     query = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(query, (self.price, self.name))
    #     connection.commit()
    #     connection.close()