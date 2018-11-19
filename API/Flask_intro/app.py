from flask import Flask, jsonify, request

app = Flask(__name__) #__name__ gives an applicaiton a specific name

#POST - used to receive data -> server (application) should send
#GET - used to send data back only
#(opposite from browser side)

#CASE: online store
#data:
stores = [
    {
        "name" : "My store",
        "items" : [
            {
                "name" : "My item",
                "price" : 15.39
            }
        ]
    }
]

#POST /store data: {name:}
@app.route("/store", methods =["POST"]) #broswer has only GET as default, so need to specify POST
def create_store():
    request_data = request.get_json()
    new_store = {
        "name" : request_data["name"],
        "items" : []
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET /store/<string:name>
@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify({"message":"Store not found!"})


#GET /store
@app.route("/store")
def get_stores():
    return jsonify({"stores" : stores})

#POST /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item", methods =["POST"])
def create_item_in_store(name):
        request_data = request.get_json()
        new_item = {
                    "name" : request_data["name"],
                    "price" : request_data["price"]
                    }
        for store in stores:
            if store["name"] == name:
                store["items"].append(new_item)
                return jsonify(new_item)
        return jsonify({"message":"Store not found! Item not added."})

#GET /store/<string:name>/item
@app.route("/store/<string:name>/item")
def get_item_in_store(name):
        for store in stores:
            if store["name"] == name:
                for item in store["items"]:
                    if item["name"] == name:
                        return jsonify(item)
                return jsonify({"message":"Item not found in store!"})
        return jsonify({"message":"Store not found!"})

#GET /store/<string:name>/items
@app.route("/store/<string:name>/items")
def get_items_in_store(name):
        for store in stores:
            if store["name"] == name:
                return jsonify({"items":store["items"]})
        return jsonify({"message":"Store not found!"})


#Home endpoint, all decorated needs to return something
@app.route("/") #home page = "/" | decorate main method
def home():
    return "Hellooo!"

app.run(port=5000)
