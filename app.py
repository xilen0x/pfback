from flask import Flask, jsonify, request, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from models import db, User, Tramits, Tasks


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