from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    #Using parser allows for nice error handling and also use accepted arguments
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank."
    )

    @jwt_required()
    def get(self, name):
        #item = next(filter(lambda x: x["name"] == name, items),None) #Find item with lambda expression instead of for loop, lambda returns a list of objects
        #return {"item":item}, 200 if item is not None else 404 #ternary statement on item
        item = self.find_by_name(name)
        if item:
            return item
        return {"message" : "Item not found."}

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()
        if row:
            return {"item" : {"name" : row[0], "price" : row[1]}}



    def post(self, name):
        if self.find_by_name(name):
            return {"message":"An item with name '{}' already exists.".format(name)}, 400
        request_data = Item.parser.parse_args()
        #request_data = request.get_json() #force=True ->=no need for header
        item = {"name": name, "price":request_data["price"]}
        #items.append(item)
        try:
            self.insert(item)
        except:
            return {"message" : "An error occured when inserting item."}, 500
        return item,201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item["name"], item["price"]))
        connection.commit()
        connection.close()

    def delete(self, name):
        #global items #refer to the outer items variable
        #items = list(filter(lambda x: x["name"] != name, items))
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {"message" : "Item deleted"}

    def put(self, name):
        request_data = Item.parser.parse_args()
        #item = next(filter(lambda x: x["name"] == name, items),None)
        item = self.find_by_name(name)
        updated_item = {"name": name, "price":request_data["price"]}
        if item is None:
            #item = {"name": name, "price":request_data["price"]}
            #items.append(item)
            try:
                self.insert(updated_item)
            except:
                return {"message" : "An error occured when inserting item."}, 500
        else:
            #item.update(request_data)
            try:
                self.update(item)
            except:
                return {"message" : "An error occured when updating item."}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))
        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name": row[0], "price" : row[1]})
        connection.commit()
        connection.close()
        return {"items":items}
