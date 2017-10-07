from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('localhost', 27017)

db = client.baseprueba
coll = db.baseprueba

# # The web framework gets post_id from the URL and passes it as a string
# def get(post_id):
#     # Convert from string to ObjectId:
#     document = client.db.collection.find_one({'_id': ObjectId(post_id)})


class HelloWorld(Resource):
    def get(self):
        nom = request.args.get('Nombre')
        query = [{"Nombre": x["Nombre"], "Apellido": x["Apellido"]} for x in coll.find({"Nombre": nom})]
        return jsonify({"RESPONSE": query})


api.add_resource(HelloWorld, '/')


class User(Resource):
    def get(self, todo_id):
        query = [{"Nombre": x["Nombre"], "Apellido": x["Apellido"]} for x in coll.find({"Nombre": todo_id})]
        return jsonify({"RESPONSE": query})

    def put(self, todo_id):  # ObjectId(post_id)
        args = request.get_json()
        if not args:
            return jsonify({"RESPONSE": "La remil mierda"})
        else:
            nom = args.get('Nombre')
            chorongp = coll.find_one_and_update({"Nombre": todo_id}, {'$set': {"Nombre": nom}})
            return jsonify({"RESPONSE": nom})


api.add_resource(User, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
