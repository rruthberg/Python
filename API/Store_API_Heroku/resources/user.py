#Class for user register resource
#Resources: what we handle externally, i.e. what client interacts with
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument("password",
        type=str,
        required=True,
        help="This field cannot be left blank."
    )
    def post(self):
        request_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(request_data["username"]):
            return {"message" : "User with that username already exists."}, 400
        #user = UserModel(request_data["username"],request_data["password"])
        user = UserModel(**request_data)
        user.save_to_db()
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO users VALUES (NULL, ?, ?)" #NULL since auto-incrementing
        # cursor.execute(query, (request_data["username"], request_data["password"]))
        # connection.commit()
        # connection.close()
        return {"message" : "User created successfully."}, 201
