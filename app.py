from urllib import response
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash # funcion de sifrado para guardar las contraseñas 
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/restapi'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def createUser():

    #Receiving data
    userName = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if userName and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {'username':userName, 'email':email, 'password':hashed_password}
        )
        response = {
            'id' : str(id),
            'username': userName,
            'password': hashed_password,
            'email':email
        }
        return response
    else:
        return not_found()
    return {'message': 'received'}

@app.route('/users',methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response,mimetype='application/json')

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resource Not Found: ' + request.url,
        "status": 404
        
    })
    response.status_code = 404
    return response
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return response
if __name__ =='__main__':
    app.run(debug=True)
