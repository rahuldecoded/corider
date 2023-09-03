from flask import Flask, jsonify, request
import pymongo


app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
users = client.corider_db.users



# class User(db.Document):
#     name = db.StringField()
#     age = db.IntField()
#     birthday = db.StringField()

#     def to_json(self):
#         return {"name": self.name, "age": self.age, "birthday": self.birthday}


@app.route("/api/", methods=["GET"])
def index():
    data = {
        "message": "Index"
    }
    return jsonify(data)


def userExists(id):
    print(type(id))
    if not users.find_one({'id': id}):
        return False
    return True

@app.route("/api/users", methods=["POST"])
def addUsers():
    data = {}
    id = request.json["id"] 
    if not userExists(id):
        users.insert_one(request.json)
    return jsonify(data)


@app.route("/api/users", methods=["GET", "POST"])
def fetchUsers():    
    data = {}
    for user in users.find({}, {"_id": 0, "id":1, "name":1, "email":1}):
        id = user["id"]
        data[id] = {
            "user": user["name"],
            "email": user["email"]
        }
    return jsonify(data)

@app.route("/api/users/<id>", methods=["GET"])
def fetchUser(id):
    if not id.isdigit():    
        return {}
    id = int(id)
    data = {}
    user = users.find_one({'id': id}, {"_id": 0, "id":1, "name":1, "email":1})
    id = user["id"]
    data[id] = {
        "user": user["name"],
        "email": user["email"]
    }
    return jsonify(data)


@app.route("/api/users/<id>", methods=["PUT"])
def updateUser(id):
    if not id.isdigit():    
        return {}
    id = int(id)
    data = {}
    new_value = {"$set": request.json}
    users.update_one({'id': id}, new_value)
    return jsonify(data)


@app.route("/api/users/<id>", methods=["DELETE"])
def deleteUser(id):
    if not id.isdigit():    
        return {}
    id = int(id)
    data = {}
    users.delete_one({'id': id})
    return jsonify(data)



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RV'
if __name__ == "__main__":
    app.run(debug=True)