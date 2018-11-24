#FLASK REST - intro to creating RESTful APIs with Flask
#Done in virtual env
#Activate venv by: .\venv\Scripts\activate.bat from root folder

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = "richardr"
api = Api(app)

jwt = JWT(app, authenticate, identity) #Creates new endpoint /auth

items = []
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NDMwNTU0ODQsImlkZW50aXR5IjoxLCJleHAiOjE1NDMwNTU3ODQsIm5iZiI6MTU0MzA1NTQ4NH0.gmOB9u4lwmhg_i_zFYVIN9R64zfs1Ntyu6kYKCml3rM
#Api: every resource need to be a class
#HTTP codes: 1x = inform, 2x = OK request, 3x = redirect, 4x = client error , 5x = server error
#200  = OK (GET, most common)
#201 = CREATED (POST)
#202 = ACCEPTED
#400 = BAD REQUEST
#404 = NOT FOUND

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
        item = next(filter(lambda x: x["name"] == name, items),None) #Find item with lambda expression instead of for loop, lambda returns a list of objects
        return {"item":item}, 200 if item is not None else 404 #ternary statement on item

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items),None) is not None:
            return {"message":"An item with name '{}' already exists.".format(name)}, 400
        request_data = Item.parser.parse_args()
        #request_data = request.get_json() #force=True ->=no need for header
        item = {"name": name, "price":request_data["price"]}
        items.append(item)
        return item,201

    def delete(self, name):
        global items #refer to the outer items variable
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message" : "Item deleted"}

    def put(self, name):
        request_data = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items),None)
        if item is None:
            item = {"name": name, "price":request_data["price"]}
            items.append(item)
        else:
            item.update(request_data)
        return item,201


class ItemList(Resource):
    def get(self):
        return {"items":items}

api.add_resource(Item,"/item/<string:name>") #Add resource along with endpoint (similar to adding decorator in Flask)
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister, "/register")

app.run(port=5000, debug = True)
