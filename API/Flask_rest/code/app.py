#FLASK REST - intro to creating RESTful APIs with Flask
#Done in virtual env
#Activate venv by: .\venv\Scripts\activate.bat from root folder

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "richardr"
api = Api(app)

jwt = JWT(app, authenticate, identity) #Creates new endpoint /auth

#items = []
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NDMwNTU0ODQsImlkZW50aXR5IjoxLCJleHAiOjE1NDMwNTU3ODQsIm5iZiI6MTU0MzA1NTQ4NH0.gmOB9u4lwmhg_i_zFYVIN9R64zfs1Ntyu6kYKCml3rM
#Api: every resource need to be a class
#HTTP codes: 1x = inform, 2x = OK request, 3x = redirect, 4x = client error , 5x = server error
#200  = OK (GET, most common)
#201 = CREATED (POST)
#202 = ACCEPTED
#400 = BAD REQUEST
#404 = NOT FOUND



api.add_resource(Item,"/item/<string:name>") #Add resource along with endpoint (similar to adding decorator in Flask)
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister, "/register")

#Only run app if the app.py file is the main program
if __name__ == "__main__":
    app.run(port=5000, debug = True)
