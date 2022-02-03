from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash # funcion de sifrado para guardar las contraseñas 

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/porvarificar'
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def createUser():
    #Receiving data
    userName = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if userName and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'username':userName, 'email':email, 'password':hashed_password}
        )
        response = {
            'id' : str(id),
            'username': userName,
            'password': password,
            'email':email
        }
        return response
    else:
        {'message': 'received'} 
        return {'message': 'received'}



if __name__ =='__main__':
    app.run(debug=True)
