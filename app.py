from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pymongo


app = Flask(__name__)
api = Api(app)


client = pymongo.MongoClient("mongodb://localhost:27017/")
users = client.corider_db.users


class Index(Resource):
    def get(self):
        return {"msg": "Index"}


class ApiIndex(Resource):
    def get(self):
        return {"msg": "ApiIndex"}


class Users(Resource):
    def get(self, id=None):
        data = {}
        if not id:
            for user in users.find({}, {"_id": 0, "id":1, "name":1, "email":1}):
                id = user["id"]
                data[id] = {
                    "user": user["name"],
                    "email": user["email"]
                }
        else:
            user = users.find_one({'id': id}, {"_id": 0, "id":1, "name":1, "email":1})
            if not user:
                pass
            else:
                id = user["id"]
                data[id] = {
                    "user": user["name"],
                    "email": user["email"]
                }
        return jsonify(data)


    def put(self, id):
        data = {}
        new_value = {"$set": request.json}
        users.update_one({'id': id}, new_value)
        return jsonify(data)


    def post(self):
        data = {}
        id = request.json["id"]
        if users.find_one({'id': id}):
            pass
        else:
            users.insert_one(request.json)
        return jsonify(data)


    def delete(self, id):
        data = {}
        if not users.find_one({'id': id}):
            pass
        else:
            users.delete_one({'id': id})
        return jsonify(data)



api.add_resource(Index, '/', endpoint="index")
api.add_resource(Index, '/api', endpoint="api_index")
api.add_resource(Users, '/api/users', endpoint='get_all_users')
api.add_resource(Users, '/api/users/<int:id>', endpoint='get_user')
api.add_resource(Users, '/api/users/<int:id>', endpoint='update_user')
api.add_resource(Users, '/api/users', endpoint='add_user')
api.add_resource(Users, '/api/users/<int:id>', endpoint='remove_user')



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RV'
if __name__ == "__main__":
    app.run(debug=True)