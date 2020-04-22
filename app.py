from flask import Flask, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from models import db, User


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG '] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Cambiar luego!!!
jwt = JWTManager(app)

db.init_app(app)
Migrate(app, db)
bcrypt = Bcrypt(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

CORS(app)

""" rutas """
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "No es un objeto JSON"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
   

    if not username or username == '':
        return jsonify({"msg": "Se requiere el username"}), 400
    if not password or password == '':
        return jsonify({"msg": "Se requiere el password"}), 400

    user = User.query.filter_by(username=username).first()#si existe el usuario...se almacena en user
    if not user:
        return jsonify({"msg": "El username o password no son correctos!"}),401 #si no existe le envia este msg

    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "The username or password are not correct!"}),401

@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Al parecer no es un objeto JSON"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    name = request.json.get('name', '')
    lastname = request.json.get('lastname', '')

    if not username or username == '':
        return jsonify({"msg": "Missing username req."}), 400
    if not password or password == '':
        return jsonify({"msg": "Missing password req."}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"msg": "username already exist"}),400

    user = User()
    user.username = username
    user.password = bcrypt.generate_password_hash(password)
    user.name = name
    user.lastname = lastname

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.username)
    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify(data), 201

@app.route('/users', methods=['GET', 'POST'])
@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
def users(id = None):
    if request.method == 'GET':
        return jsonify({"msg": "users get"}), 200
    if request.method == 'POST':
        return jsonify({"msg": "users post"}), 200
    if request.method == 'PUT':
        return jsonify({"msg": "users put"}), 200
    if request.method == 'DELETE':
        return jsonify({"msg": "users delete"}), 200


if __name__ == '__main__':
    manager.run()