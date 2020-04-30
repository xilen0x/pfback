import os, getpass
from flask import Flask, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from werkzeug.utils import secure_filename
from functions import allowed_file
from models import db, User

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS_IMAGES = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG '] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Cambiar luego!!!
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static')

jwt = JWTManager(app)

db.init_app(app)
Migrate(app, db)
bcrypt = Bcrypt(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

CORS(app)

################# RUTAS #################
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "No es un objeto JSON"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

 #VALIDACIONES
    if not email or email == '':
        return jsonify({"msg": "Missing email"}), 400
    if not password or password == '':
        return jsonify({"msg": "Missing password."}), 400

    user = User.query.filter_by(email=email).first()#si existe el usuario...se almacena en user
    if not user:
        return jsonify({"msg": "El email o password no son correctos!"}),401 #si no existe le envia este msg

    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)
        print(access_token)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "El email o password no son correctos!"}),401

@app.route('/register', methods=['POST'])#REGISTRO
def register():
    #if not request.is_form:
    #    return jsonify({"msg": "Missing Form request"}), 400

    email = request.form.get('email', None)
    password = request.form.get('password', None)
    nombre = request.form.get('nombre', '')
    apellido = request.form.get('apellido', '')
    rut = request.form.get('rut', '')
    pais = request.form.get('pais', '')
    ciudad = request.form.get('ciudad', '')
    sexo = request.form.get('sexo', '')
    #avatar = request.json.get('avatar', '')
#VALIDACIONES
    if not email or email == '':
        return jsonify({"msg": "Missing email"}), 400
    if not password or password == '':
        return jsonify({"msg": "Missing password."}), 400
    if not nombre or nombre == '':
        return jsonify({"msg": "Missing nombre"}), 400
    if not apellido or apellido == '':
        return jsonify({"msg": "Missing apellido"}), 400
    if not rut or rut == '':
        return jsonify({"msg": "Missing rut"}), 400
    if not pais or pais == '':
        return jsonify({"msg": "Missing País"}), 400
    if not ciudad or ciudad == '':
        return jsonify({"msg": "Missing Ciudad"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "email already exist"}),400
    rut = User.query.filter_by(rut=rut).first()
    if rut:
        return jsonify({"msg": "rut already exist"}),400

    file = request.files['avatar']
    if file and file.filename != '' and allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGES):#si existe el archivo y esta dentro de las extensiones permitidas
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'images/avatars'), filename))
    else:
        return jsonify({"msg":"Archivo no permitido, debe ser de extensión png, jpg, jpeg, gif o svg"})

    user = User() # se crea una instancia de la clase User
    #asignando valores a los campos corresp.
    user.email = email 
    user.password = bcrypt.generate_password_hash(password)
    user.nombre = nombre
    user.apellido = apellido
    user.rut = rut
    user.pais = pais
    user.ciudad = ciudad
    user.sexo = sexo
    if file:
        user.avatar = filename

    db.session.add(user) #se agrega todo lo anterior y se hace commit
    db.session.commit()

    access_token = create_access_token(identity=user.email)
    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify(data), 201

@app.route('/update-profile', methods=['POST'])
@jwt_required
def changePassword():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON request"}), 400

    oldpassword = request.json.get('oldpassword', None)
    password = request.json.get('password', None)

    if not oldpassword or oldpassword == '':
        return jsonify({"msg": "Ingrese su actual contraseña!"}), 400
    if not password or password == '':
        return jsonify({"msg": "Ingrese su nueva contraseña!"}), 400

    email = get_jwt_identity()

    user = User.query.filter_by(email=email).first()
    
    if bcrypt.check_password_hash(user.password, oldpassword):
        user.password = bcrypt.generate_password_hash(password)
        db.session.commit()
        return jsonify({"success": "Tu contraseña ha cambiado exitosamente!"}), 200
    else:
        return jsonify({"msg": "La contraseña actual no es correcta!"}), 400

@app.route('/update-profile/<int:id>', methods=['PUT'])
@jwt_required
def updateProfile(id):
    if not request.is_json:
        return jsonify({"msg": "Al parecer no es un objeto JSON"}), 400

    email = request.json.get('email', None)
    nombre = request.json.get('nombre', '')
    apellido = request.json.get('apellido', '')
    rut = request.json.get('rut', '')
    pais = request.json.get('pais', '')
    ciudad = request.json.get('ciudad', '')
    sexo = request.json.get('sexo', '')
    #avatar = request.json.get('avatar', '')

    user = User.query.filter_by(email=email).first()
    user = User() # se crea una instancia de la clase User
    #asignando valores a los campos corresp.
    user.email = email 
    user.nombre = nombre
    user.apellido = apellido
    user.rut = rut
    user.pais = pais
    user.ciudad = ciudad
    #user.u_avatar = u_avatar
    
    db.session.commit()

    access_token = create_access_token(identity=user.email)
    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify(data), 201

""" @app.route('/users', methods=['GET', 'POST'])
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
        return jsonify({"msg": "users delete"}), 200 """


if __name__ == '__main__':
    manager.run()