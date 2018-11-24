from user import User
from werkzeug.security import safe_str_cmp



def authenticate(username, password):
    #user = username_mapping.get(username,None)
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload["identity"]
    #return userid_mapping.get(user_id, None)
    return User.find_by_id(user_id)


#OLD / replacements by DB code :

#Replaced by DB
#users = [
#    User(1,"bob","asdf")
    #{
    #    "id" : 1,
    #    "username" : "bob",
    #    "password" : "asdf"
    #}
#]

#Replaced by DB
#username_mapping = {u.username: u for u in users} #set comprehension to generate mapping
#userid_mapping = {u.id: u for u in users} #set comprehension to generate mapping
#{
#    "bob" : {
#        "id" : 1,
#        "username" : "bob",
#        "password" : "asdf"
#    }
#}

# userid_mapping = {
#     1 : {
#             "id" : 1,
#             "username" : "bob",
#             "password" : "asdf"
#         }
#     }
# }
