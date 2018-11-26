#FLASK REST - intro to creating RESTful APIs with Flask
#Done in virtual env

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" #works with MySql, PostgreSQL etc.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #do not track modifications explicitly in Flask (but not in SQLAlchemy)
app.secret_key = "richardr"
api = Api(app)

#Create db automatically by calling decorated/overloaded method before_first_request
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #Creates new endpoint /auth

api.add_resource(Item,"/item/<string:name>") #Add resource along with endpoint (similar to adding decorator in Flask)
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/store/<string:name>")

#Only run app if the app.py file is the main program
if __name__ == "__main__":
    from db import db #prevent circular import by importing at this point
    db.init_app(app)
    app.run(port=5000, debug = True)
