import os, getpass
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from werkzeug.utils import secure_filename
from functions import allowed_file
from models import db, User, Tramits, Tasks, Blog, Comment

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


@app.route('/users/avatar/<filename>')
def avatar(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'images/avatars'),
                               filename)

""" @app.route('/users', methods=['GET', 'POST'])
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
        return jsonify({"msg": "users delete"}), 200 """

#DESDE AQUI PARTE DASHBOARD TODOLIST

@app.route('/tramits', methods=['GET', 'POST'])                           #ESTAS SON LAS RUTAS PARA LA TABLA TRAMITS 
@app.route('/tramits/<int:tr_id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
def tramits(tr_id = None):
    if request.method == 'GET':
        if tr_id is not None:
            tramit = Tramits.query.get(tr_id)
            if tramit:
                return jsonify(tramit.serialize()), 200
            else:
                return jsonify({"msg": "No se encuentra dicho tramite"}), 404
        else:
            tramits = Tramits.query.all()
            tramits = list(map(lambda tramit: tramit.serialize(), tramits))
            return jsonify(tramits), 200                      #Validacion de contenido
        
    if request.method == 'POST':
        tramit = request.json.get('tramit', None)
        description = request.json.get("description", None)
        ta_id = request.json.get('ta_id', None)

        if not tramit and tramit == "":
            return jsonify({"msg": "Ingresar Nombre del Tramite"}), 400
        elif not ta_id and ta_id == "":
            return jsonify({"msg": "No hay tareas"}), 400     #Validando las variables

        tramits = Tramits()
        tramits.tramit = tramit
        tramits.description = description
        tramits.ta_id = ta_id                        #Guardando/Asignando valores

        db.session.add(tramits)
        db.session.commit()

        return jsonify(tramits.serialize()), 200

    if request.method == 'PUT':
        tramit = request.json.get("tramit", None)
        description = request.json.get("description", None)
        ta_id = request.json.get("ta_id", None)

        if not tramit and tramit == "":
            return jsonify({"msg": "Field tramite is required"}), 400  # 400 o 422
        elif not ta_id and ta_id == "":
            return jsonify({"msg": "Field tareas is required"}), 400  # 400 o 422

        tramitpost = Tramits.query.get(tr_id) #busca por el id
    
        if not tramitpost:
            return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

        tramitpost.tramit = tramit
        tramitpost.description = description
        tramitpost.ta_id = ta_id

        db.session.commit() # para actualizar y guardar en la bd

        return jsonify(tramitpost.serialize()), 200

    if request.method == 'DELETE':
        tramits = Tramits.query.get(tr_id)
        if not tramits:
            return jsonify({"msg": "Item not found"}), 400
        db.session.delete(tramits)
        db.session.commit()
        return jsonify({"msg": "Item deleted"}), 200

@app.route('/tasks', methods=['GET', 'POST'])                              #ESTAS SON LAS RUTAS PARA LA TABLA DE TASKS
@app.route('/tasks/<int:ta_id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
def tasks(ta_id = None):
    if request.method == 'GET':
        if ta_id is not None:
            task = Tasks.query.get(ta_id)
            if task:
                return jsonify(task.serialize()), 200
            else:
                return jsonify({"msg": "No se encuentra dicha tarea"}), 404
        else:
            tasks = Tasks.query.all()
            tasks = list(map(lambda task: task.serialize(), tasks))
            return jsonify(tasks), 200                      #Validacion de contenido

    if request.method == 'POST':
        task01 = request.json.get('task01', None)
        task02 = request.json.get('task02', None)
        task03 = request.json.get('task03', None)
        task04 = request.json.get('task04', None)
        task05 = request.json.get('task05', None)
        task06 = request.json.get('task06', None)
        task07 = request.json.get('task07', None)
        task08 = request.json.get('task08', None)
        task09 = request.json.get('task09', None)

        if not task01 and task01 == "":
            return jsonify({"msg": "Ingresar por lo menos la primera tarea"}), 400

        tasks = Tasks()
        tasks.task01 = task01
        tasks.task02 = task02
        tasks.task03 = task03
        tasks.task04 = task04
        tasks.task05 = task05
        tasks.task06 = task06
        tasks.task07 = task07
        tasks.task08 = task08
        tasks.task09 = task09

        db.session.add(tasks)
        db.session.commit()

        return jsonify(tasks.serialize()), 200

    if request.method == 'PUT':
        task01 = request.json.get('task01', None)
        task02 = request.json.get('task02', None)
        task03 = request.json.get('task03', None)
        task04 = request.json.get('task04', None)
        task05 = request.json.get('task05', None)
        task06 = request.json.get('task06', None)
        task07 = request.json.get('task07', None)
        task08 = request.json.get('task08', None)
        task09 = request.json.get('task09', None)

        if not task01 and task01 == "":
            return jsonify({"msg": "Ingresar por lo menos la primera tarea"}), 400

        taskpost = Tasks.query.get(ta_id) #busca por el id
    
        if not taskpost:
            return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

        taskpost.task01 = task01
        taskpost.task02 = task02
        taskpost.task03 = task03
        taskpost.task04 = task04
        taskpost.task05 = task05
        taskpost.task06 = task06
        taskpost.task07 = task07
        taskpost.task08 = task08
        taskpost.task09 = task09

        db.session.commit() # para actualizar y guardar en la bd

        return jsonify(taskpost.serialize()), 200
        
    if request.method == 'DELETE':
        tasksid = Tasks.query.get(ta_id)
        if not tasksid:
            return jsonify({"msg": "Item not found"}), 400
        db.session.delete(tasksid)
        db.session.commit()
        return jsonify({"msg": "Tasks deleted"}), 200



if __name__ == '__main__':
    manager.run()


# @app.route("/dashboard/todotramite")
# @app.route("/dashboard/todotramite/<input1>", methods=["GET", "POST", "PUT", "DELETE"])
# def handler(input1=None):
#     if request.method == "GET":
#         # if the api received a name, get the column with the name.
#         if input1 is not None:
#             todos = Todos.query.filter_by(name=input1).first()
#             if todos:
#                 return jsonify(todos.serialize()), 200
#             else:
#                 return jsonify({"msg": "Not Found"}), 404
#         else:
#             # else the api did not get a name, get all columns
#             todos = Todos.query.all()
#             # create the array contacts, containing an array of the serialization of all the elements in the table Todos
#             # using the function lambda and the map method
#             todos = list(map(lambda todos: todos.serialize(), todos))
#             # jsonify it and returns it to the request
#             return jsonify(todos), 200

#     if request.method == "POST":

#         if not input1 or input1 == "":  # si no llego un nombre o el nombre esta vacio
#             return {"msg": "Field name is required"}, 400  # 422
#         # todo =  object Todos,
#         todo = Todos()
#         todo.name = input1
#         todo.tareas = ""
#         db.session.add(todo)
#         db.session.commit()
#         return {"result": "ok"}, 200  # 422

#     if request.method == "PUT":
#         # revisa la request y captura el elemento name, idem para phone
#         tareas = request.json

#         if not tareas or tareas == "":  # si no llego una tarea o las tareas estan vacias
#             return {"msg": "Field tareas is required"}, 400  # 422

#         todos = Todos.query.filter_by(name=input1).first()

#         if not todos:
#             return {"msg": "user not found"}, 404
        
#         jsonify(tareas)
#         print(tareas)
#         todos.tareas = json.dumps(tareas)
#         db.session.commit()

#         # CREATED
#         return {"result": "A list with " + str(len(tareas))+" todos was succesfully saved"}, 200

#     if request.method == "DELETE":

#         todos = Todos.query.filter_by(name=input1).first()

#         if not todos:
#             return {"msg": "Not Found"}, 400

#         db.session.delete(todos)
#         db.session.commit()
#         return {"msg": "ok"}, 200


# @app.route("/api/todos/names", methods=["GET"])
# def namegiver():
#     users = Todos.query.all()
#     users = list(map(lambda user: user.name, users))
#     return jsonify(users), 200