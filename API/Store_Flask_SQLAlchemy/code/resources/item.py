#Item resource
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
#import sqlite3
from models.item import ItemModel

class Item(Resource):
    #Using parser allows for nice error handling and also use accepted arguments
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message" : "Item not found."}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message":"An item with name '{}' already exists.".format(name)}, 400
        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data) #**request_data replaces request_data["price"], request_data["store_id"]
        try:
            #ItemModel.insert(item)
            item.save_to_db()
        except:
            return {"message" : "An error occured when inserting item."}, 500
        return item.json(),201

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name) #Just a python entity
        if item is None:
            item = ItemModel(name, **request_data) #**request_data replaces request_data["price"], request_data["store_id"]
        else:
            item.price = request_data["price"]
            item.store_id = request_data["store_id"]
        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message" : "Item deleted"}


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]} #list comprehension which jsonifies the items in the fesult from query.all()
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name": row[0], "price" : row[1]})
        # connection.commit()
        # connection.close()
