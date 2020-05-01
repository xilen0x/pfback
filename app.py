import os
from flask import Flask, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from werkzeug.utils import secure_filename
from models import db, User , Blog , Comment
from datetime import date , time
from functions import allowed_file

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



@app.route('/')
def main():
    return render_template('index.html')



@app.route('/blog', methods=['GET', 'POST'])
@app.route('/blog/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def blog(id = None):
    if request.method == 'GET':

        if id is not None :
            blog = Blog.query.get(id)
            if blog:
               return jsonify(blog.serialize()), 200
            else:
               return jsonify({"msg": "Not Found"}), 404   
        else :
            blogs = Blog.query.all()
            blogs = list(map(lambda blog: blog.serialize(), blogs))
            return jsonify(blogs), 200

    if request.method == 'POST':
        
        e_titulo = request.form.get('e_titulo', None)
        e_cuerpo = request.form.get('e_cuerpo', None)
        e_fecha = request.form.get('e_fecha', None)
       
              
        if not e_titulo and e_titulo == "":
            return jsonify({"msg":"Field titulo is required"}), 400
        if not e_cuerpo and e_cuerpo == "":
            return jsonify({"msg":"Field cuerpo is required"}), 400
        if not e_fecha and e_fecha == "":
            return jsonify({"msg":"Field fecha is required"}), 400

        file = request.files['e_imagen'] 
        if file and file.filename !='' and allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGES):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'images/blogs'), filename)) 
        else:
            return jsonify({"msg":"File not allowed"}), 400
        blog = Blog()
         
        blog.e_titulo = e_titulo 
        blog.e_cuerpo = e_cuerpo 
        blog.e_fecha = e_fecha
        if file:
            blog.e_imagen = filename

        db.session.add(blog) 
        db.session.commit()  

        return jsonify(blog.serialize()), 201

    if request.method == 'PUT':
        e_titulo = request.form.get('e_titulo', None)
        e_cuerpo = request.form.get('e_cuerpo', None)
        e_fecha = request.form.get('e_fecha', None)
       
              
        if not e_titulo and e_titulo == "":
            return jsonify({"msg":"Field titulo is required"}), 400
        if not e_cuerpo and e_cuerpo == "":
            return jsonify({"msg":"Field cuerpo is required"}), 400
        if not e_fecha and e_fecha == "":
            return jsonify({"msg":"Field fecha is required"}), 400

        file = request.files['e_imagen'] 
        if file and file.filename !='' and allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGES):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'images/blogs'), filename)) 
        else:
            return jsonify({"msg":"File not allowed"}), 400

        blog = Blog.query.get(id) 

        blog.e_titulo = e_titulo 
        blog.e_cuerpo = e_cuerpo 
        blog.e_fecha = e_fecha
        if file:
            blog.e_imagen = filename
 
        db.session.commit()
        return jsonify(blog.serialize()), 201   
        
    if request.method == 'DELETE':
        blog = Blog.query.get(id)
        if not blog:
            return jsonify({"msg": "Not Found"}), 404
        db.session.delete(blog)
        db.session.commit()
        return jsonify({"msg":"Blog was deleted"}), 200       

@app.route('/coment', methods=['GET', 'POST'])
@app.route('/coment/<int:id>', methods=['GET', 'DELETE'])
def comment(id = None):
    if request.method == 'GET':
        
        if id is not None:
         pass
        else :
         coments = Comment.query.all()
         coments = list(map(lambda coment: coment.serialize(), coments))
         return jsonify(coments), 200

    if request.method == 'POST':
        if not request.is_json:
          return jsonify({"msg": "No es un objeto JSON"}), 400
        
        
        
        c_cuerpo = request.json.get('c_cuerpo', None)
        c_fecha = request.json.get('c_fecha', None)
        id_blog = request.json.get('id_blog', None)
        
        
        if not c_cuerpo and c_cuerpo == "":
            return jsonify({"msg":"Field coment is required"}), 400
        if not c_fecha and c_fecha == "":
            return jsonify({"msg":"Field fecha is required"}), 400
        if not id_blog and id_blog == "":
            return jsonify({"msg":"Field id_blog is required"}), 400    

        coment = Comment()
        
        
        coment.c_cuerpo = c_cuerpo
        coment.c_fecha = c_fecha
        coment.id_blog = id_blog

        db.session.add(coment)
        db.session.commit()
        return jsonify(coment.serialize()),201    

    if request.method == 'DELETE':
        return jsonify({"msg": "users delete"}), 200

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
        return jsonify({"msg": "usuario get"}), 200
    if request.method == 'POST':
        return jsonify({"msg": "users post"}), 200
    if request.method == 'PUT':
        return jsonify({"msg": "users put"}), 200
    if request.method == 'DELETE':
        return jsonify({"msg": "users delete"}), 200


if __name__ == '__main__':
    manager.run()