from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pymongo

from exception import ApiException, BadRequestException, ConflictException, NotFoundException


app = Flask(__name__)
api = Api(app)


@app.errorhandler(ApiException)
def handle_exception(err):
    response = jsonify(err.to_dict())
    response.status_code = err.status_code
    return response


@app.errorhandler(404)
def handle_general_exception(err):
    response = {
        "message": "Method not found",
        "code": 404
    }
    return response, response['code']


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.corider_db


class Index(Resource):
    def get(self):
        return {"msg": "Index"}


class ApiIndex(Resource):
    def get(self):
        return {"msg": "ApiIndex"}


class Users(Resource):
    def get(self, id=None):
        if not id:
            response = {
                "data": []
            }
            for user in db.users.find({}, {"_id": 0, "id":1, "name":1, "email":1}):
                response['data'].append(user)
            response['meta'] = {
                "count": len(response['data'])
            }
        else:
            user = db.users.find_one({'id': id}, {"_id": 0, "id":1, "name":1, "email":1})
            if not user:
                raise NotFoundException("id {} not found".format(id))
            else:
                response = {}
                response['data'] = user
        return response, 200


    def put(self, id=None):
        if not id:
            raise BadRequestException("Bad Request")
        elif not db.users.find_one({'id': id}):
            raise NotFoundException("id {} not found".format(id))
        elif id != request.json['id'] and db.users.find_one({'id': request.json['id']}):
            raise ConflictException("Can not modify, another object")
        else:
            new_value = {"$set": request.json}
            db.users.update_one({'id': id}, new_value)
            db.users.save
            response = {
                "message": "Object got modified".format(id)
            }
            return response, 200


    def post(self, id=None):
        if id:
            raise BadRequestException("Bad Request")
        elif db.users.find_one({'id': request.json['id']}):
            raise ConflictException("id {} aldreay present".format(request.json['id']))
        else:
            db.users.insert_one(request.json)
            db.users.save
            response = {
                "message": "Object added successfully"
            }
        return response, 200


    def delete(self, id=None):
        if not id:
            raise BadRequestException("Bad Request")
        if not db.users.find_one({'id': id}):
            raise NotFoundException("id {} not found".format(id))
        else:
            db.users.delete_one({'id': id})
            db.users.save
            response = {
                "message": "Object deleted successfully"
            }
        return response, 200



api.add_resource(Index, '/', endpoint="index")
api.add_resource(ApiIndex, '/api', endpoint="api_index")
api.add_resource(Users, '/api/users', endpoint='get_all_users')
api.add_resource(Users, '/api/users/<int:id>', endpoint='user')



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RV'
if __name__ == "__main__":
    app.run(debug=True)