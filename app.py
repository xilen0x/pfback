import os, getpass
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from werkzeug.utils import secure_filename
from functions import allowed_file
from models import db, User, Blog, Comment, Tramite, Tarea, TareaTramite, TramiteUser, TareaTramiteUser

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
        e_cuerpopro = request.form.get('e_cuerpopro', None)
        e_fecha = request.form.get('e_fecha', None)
       
              
        if not e_titulo and e_titulo == "":
            return jsonify({"msg":"Field titulo is required"}), 400
        if not e_cuerpo and e_cuerpo == "":
            return jsonify({"msg":"Field cuerpo is required"}), 400
        if not e_cuerpopro and e_cuerpopro == "":
            return jsonify({"msg":"Field cuerpopro is required"}), 400    
        

        file = request.files['e_imagen'] 
        if file and file.filename !='' and allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGES):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'images/blogs'), filename)) 
        else:
            return jsonify({"msg":"File not allowed"}), 400
        blog = Blog()
         
        blog.e_titulo = e_titulo 
        blog.e_cuerpo = e_cuerpo 
        blog.e_cuerpopro = e_cuerpopro
        blog.e_fecha = e_fecha
        if file:
            blog.e_imagen = filename

        db.session.add(blog) 
        db.session.commit()  

        return jsonify(blog.serialize()), 201

    if request.method == 'PUT':
        e_titulo = request.form.get('e_titulo', None)
        e_cuerpo = request.form.get('e_cuerpo', None)
        e_cuerpopro = request.form.get('e_cuerpopro', None)
        
       
              
        if not e_titulo and e_titulo == "":
            return jsonify({"msg":"Field titulo is required"}), 400
        if not e_cuerpo and e_cuerpo == "":
            return jsonify({"msg":"Field cuerpo is required"}), 400
        if not e_cuerpopro and e_cuerpopro == "":
            return jsonify({"msg":"Field cuerpopro is required"}), 400    
        

        file = request.files['e_imagen'] 
        if file and file.filename !='' and allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGES):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'images/blogs'), filename)) 
        else:
            return jsonify({"msg":"File not allowed"}), 400

        blog = Blog.query.get(id) 

        blog.e_titulo = e_titulo 
        blog.e_cuerpo = e_cuerpo 
        blog.e_cuerpopro = e_cuerpopro
        
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
        id_user = request.json.get('id_user', None)
        
        if not c_cuerpo and c_cuerpo == "":
            return jsonify({"msg":"Field coment is required"}), 400
        if not c_fecha and c_fecha == "":
            return jsonify({"msg":"Field fecha is required"}), 400   
        if not id_user and id_user == "":
            return jsonify({"msg":"Field id_user is required"}), 400

        coment = Comment()
        
        
        coment.c_cuerpo = c_cuerpo
        coment.c_fecha = c_fecha
        coment.id_user = id_user

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

    nombre = request.form.get('nombre', '')
    apellido = request.form.get('apellido', '')
    rut = request.form.get('rut', '')
    email = request.form.get('email', None)
    pais = request.form.get('pais', '')
    ciudad = request.form.get('ciudad', '')
    sexo = request.form.get('sexo', '')
    password = request.form.get('password', None)
    #avatar = request.json.get('avatar', '')
    #VALIDACIONES OBLIGATORIAS

    if not nombre or nombre == '':
        return jsonify({"msg": "Missing nombre"}), 400
    if not apellido or apellido == '':
        return jsonify({"msg": "Missing apellido"}), 400
    if not rut or rut == '':
        return jsonify({"msg": "Missing rut"}), 400
    if not email or email == '':
        return jsonify({"msg": "Missing email"}), 400
    if not pais or pais == '':
        return jsonify({"msg": "Missing País"}), 400
    if not ciudad or ciudad == '':
        return jsonify({"msg": "Missing Ciudad"}), 400
    if not password or password == '':
        return jsonify({"msg": "Missing password."}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "email already exist"}),400
    userrut = User.query.filter_by(rut=rut).first()
    if userrut:
        return jsonify({"msg": "rut already exist"}),400

    file = request.files['avatar']
    if file and file.filename != '' and allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGES):#si existe el archivo y esta dentro de las extensiones permitidas
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'images/avatars'), filename))
    else:
        return jsonify({"msg":"Archivo no permitido, debe ser de extensión png, jpg, jpeg, gif o svg"}), 400

    

    user = User() # se crea una instancia de la clase User
    #asignando valores a los campos corresp.
    user.nombre = nombre
    user.apellido = apellido
    user.rut = rut
    user.email = email 
    user.pais = pais
    user.ciudad = ciudad
    user.sexo = sexo
    user.password = bcrypt.generate_password_hash(password)
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

@app.route('/change-pass', methods=['PUT'])
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
    nombre = request.form.get('nombre', '')
    apellido = request.form.get('apellido', '')
    rut = request.form.get('rut', '')
    email = request.form.get('email', None)
    pais = request.form.get('pais', '')
    ciudad = request.form.get('ciudad', '')

    #VALIDACIONES OBLIGATORIAS
    if not nombre or nombre == '':
        return jsonify({"msg": "Missing nombre"}), 400
    if not apellido or apellido == '':
        return jsonify({"msg": "Missing apellido"}), 400
    if not rut or rut == '':
        return jsonify({"msg": "Missing rut"}), 400
    if not email or email == '':
        return jsonify({"msg": "Missing email"}), 400
    if not pais or pais == '':
        return jsonify({"msg": "Missing País"}), 400
    if not ciudad or ciudad == '':
        return jsonify({"msg": "Missing Ciudad"}), 400

    
    user = User.query.get(id)

    #asignando valores a los campos corresp.
    user.nombre = nombre
    user.apellido = apellido
    user.rut = rut
    user.email = email 
    user.pais = pais
    user.ciudad = ciudad

    db.session.commit()

    return jsonify(user.serialize()), 200


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





@app.route('/tramites', methods=['GET', 'POST'])
@app.route('/tramites/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
def tramites(id = None):
    if request.method == 'GET':
        if id is not None:
            tramite = Tramite.query.get(id)
            if tramite:
                return jsonify(tramite.serialize()), 200
            else:
                return jsonify({"msg": "No se encuentra dicho tramite"}), 404
        else:
            tramites = Tramite.query.all()
            tramites = list(map(lambda tramite: tramite.serialize(), tramites))
            return jsonify(tramites), 200
    if request.method == 'POST':
        titulo = request.json.get('titulo', None)
        infointro = request.json.get('infointro', None)
        infocorps = request.json.get('infocorps', None)
        infofoot = request.json.get('infofoot', None)
            
        if not titulo and titulo == "":
            return jsonify({"msg": "Ingresar titulo del tramite"}), 400
        if not infointro and infointro == "":
            return jsonify({"msg": "Ingresar la introducción del tramite"}), 400
        if not infocorps and infocorps == "":
            return jsonify({"msg": "Ingresar el cuerpo del tramite"}), 400
        if not infofoot and infofoot == "":
            return jsonify({"msg": "Ingresar el pie de pagina del tramite"}), 400

        tramite = Tramite()
        tramite.titulo = titulo
        tramite.infointro = infointro
        tramite.infocorps = infocorps
        tramite.infofoot = infofoot
    

        db.session.add(tramite)
        db.session.commit()

        return jsonify(tramite.serialize()), 200
    if request.method == 'PUT':
        titulo = request.json.get('titulo', None)
        infointro = request.json.get('infointro', None)
        infocorps = request.json.get('infocorps', None)
        infofoot = request.json.get('infofoot', None)
            
        if not titulo and titulo == "":
            return jsonify({"msg": "Ingresar titulo del tramite"}), 400
        if not infointro and infointro == "":
            return jsonify({"msg": "Ingresar la introducción del tramite"}), 400
        if not infocorps and infocorps == "":
            return jsonify({"msg": "Ingresar el cuerpo del tramite"}), 400
        if not infofoot and infofoot == "":
            return jsonify({"msg": "Ingresar el pie de pagina del tramite"}), 400

        tramiteput = Tramite.query.get(id) #busca por el id
    
        if not tramiteput:
            return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

        tramiteput.titulo = titulo
        tramiteput.infointro = infointro
        tramiteput.infocorps = infocorps
        tramiteput.infofoot = infofoot       

        db.session.commit() # para actualizar y guardar en la bd

        return jsonify(tramiteput.serialize()), 200
    if request.method == 'DELETE':
        tramite = Tramite.query.get(id)
        if not tramite:
            return jsonify({"msg": "Tramite no encontrado"}), 400
        db.session.delete(tramite)
        db.session.commit()
        return jsonify({"msg": "Tramite borrado"}), 200



@app.route('/tareaintotramite/<int:tramit>', methods=['GET', 'POST'])
@app.route('/tareaintotramite/<int:tramit>/<int:tar>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
def tareas2(tramit = None, tar = None):
    if request.method == 'POST':
        task = request.json.get('task', None)
        status = request.json.get('status', None)
            
        if not task and task == "":
            return jsonify({"msg": "Ingresar Nombre de la Tarea"}), 400

        tramite = Tramite.query.filter_by(id = tramit).first()

        if not tramite and tramite == "":
            return jsonify({"msg": "tramite no existe"}), 404

        tarea = Tarea()
        tarea.task = task
        tarea.status = status
        tarea.tramite_id = tramit
        
        db.session.add(tarea)
        db.session.commit()

        tareas = Tarea.query.filter_by(tramite_id = tramit).all()
        tareas = list(map(lambda tarea: tarea.serialize(), tareas))

        return jsonify({"tramite": tramite.serialize(),
                        "tareas": tareas}), 200
    if request.method == 'PUT':
        task = request.json.get('task', None)
        status = request.json.get('status', None)

        tramite = Tramite.query.filter_by(id = tramit).first()

        if not tramite and tramite == "":
            return jsonify({"msg": "tramite no existe"}), 404

        taskput = Tarea.query.get(tar) #busca por el id
    
        if not taskput:
            return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

        taskput.task = task
        taskput.status = status       

        db.session.commit() # para actualizar y guardar en la bd

        return jsonify(taskput.serialize()), 200
    if request.method == 'DELETE':
        tareadel = Tarea.query.get(tar)
        if not tareadel:
            return jsonify({"msg": "Lo que quieres borrar no se encuentra"}), 400

        db.session.delete(tareadel)
        db.session.commit()
        return jsonify({"msg": "Elemento borrado"}), 200


# @app.route('/tareastramites/<int:idtramite>', methods=['POST'])     #NO ES NECESARIO EL GET PARA TODA LA INFORMACION DEBIDO A QUE ESTA SE PUEDE VER EN EL GET DE TRAMITE
# @app.route('/tareastramites/<int:idtramite>/<int:idtarea>', methods=['GET', 'PUT', 'DELETE'])
# # @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
# def tareastramites(idtramite = None):
#     if request.method == 'POST':
#         task = request.json.get('task', None)
            
#         if not task and task == "":
#             return jsonify({"msg": "Ingresar una tarea"}), 400

#         tramite = Tramite.query.filter_by(id = idtramite).first()

#         if not tramite and tramite == "":
#             return jsonify({"msg": "tramite no existe"}), 404

#         tareastramites = TareaTramite()
#         tareastramites.task = task
#         tareastramites.tramite_id = tramite

#         db.session.add(tareastramites)
#         db.session.commit()

#         return jsonify(tareastramites.serialize()), 200
#     if request.method == 'PUT':
#         tramite_id = request.json.get('tramite_id', None)
#         tarea_id = request.json.get('tarea_id', None)
            
#         if not tramite_id and tramite_id == "":
#             return jsonify({"msg": "Ingresar id del tramite"}), 400
#         if not tarea_id and infointro == "":
#             return jsonify({"msg": "Ingresar id de la tarea"}), 400

#         tareastramitesput = TareaTramite.query.get(id) #busca por el id
    
#         if not tareastramitesput:
#             return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

#         tareastramitesput.tramite_id = tramite_id
#         tareastramitesput.tarea_id = tarea_id      

#         db.session.commit() # para actualizar y guardar en la bd

#         return jsonify(tareastramitesput.serialize()), 200
#     if request.method == 'DELETE':
        # tareastramitesdel = TareaTramite.query.get(id)
        # if not tareastramitesdel:
        #     return jsonify({"msg": "Lo que quieres borrar no se encuentra"}), 400
        # db.session.delete(tareastramitesdel)
        # db.session.commit()
        # return jsonify({"msg": "Elemento borrado"}), 200


@app.route('/tramitesusers', methods=['GET', 'POST'])
@app.route('/tramitesusers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
def tramitesusers(id = None):
    if request.method == 'GET':
        if id is not None:
            tramiteuser = TramiteUser.query.get(id)
            if tramiteuser:
                return jsonify(tramiteuser.serialize()), 200
            else:
                return jsonify({"msg": "No se encuentra lo que buscas"}), 404
        else:
            tramitesusers = TramiteUser.query.all()
            tramitesusers = list(map(lambda tramiteuser: tramiteuser.serialize(), tramitesusers))
            return jsonify(tramitesusers), 200
    if request.method == 'POST':
        user_id = request.json.get('user_id', None)
        tramite_id = request.json.get('tramite_id', None)
            
        if not user_id and user_id == "":
            return jsonify({"msg": "Ingresar identificacion del usuario"}), 400
        if not tramite_id and tramite_id == "":
            return jsonify({"msg": "Ingresar la identificacion del tramite"}), 400
        
        tramiteuser = TramiteUser()
        tramiteuser.user_id = user_id
        tramiteuser.tramite_id = tramite_id
    
        db.session.add(tramiteuser)
        db.session.commit()

        return jsonify(tramiteuser.serialize()), 200
    if request.method == 'PUT':
        user_id = request.json.get('user_id', None)
        tramite_id = request.json.get('tramite_id', None)
        status = request.json.get('status', None)
            
        if not user_id and user_id == "":
            return jsonify({"msg": "Ingresar identificacion del usuario"}), 400
        if not tramite_id and tramite_id == "":
            return jsonify({"msg": "Ingresar la identificacion del tramite"}), 400

        tramiteuserput = TramiteUser.query.get(id) #busca por el id
    
        if not tramiteuserput:
            return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

        tramiteuserput.user_id = user_id
        tramiteuserput.tramite_id = tramite_id
        tramiteuserput.status = status
    
        db.session.commit()

        return jsonify(tramiteuserput.serialize()), 200
    if request.method == 'DELETE':
        tramiteuser = TramiteUser.query.get(id)
        if not tramiteuser:
            return jsonify({"msg": "Lo que buscas no fue encontrado"}), 400
        db.session.delete(tramiteuser)
        db.session.commit()
        return jsonify({"msg": "Elemento borrado"}), 200


@app.route('/tareatramiteuser', methods=['GET', 'POST'])
@app.route('/tareatramiteuser/<int:id>', methods=['GET', 'PUT', 'DELETE'])
#@jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
def tareatramiteuser(id = None):
    if request.method == 'GET':
        if id is not None:
            tareatramiteuser = TareaTramiteUser.query.get(id)
            if tareatramiteuser:
                return jsonify(tareatramiteuser.serialize()), 200
            else:
                return jsonify({"msg": "No se encuentra lo que buscas"}), 404
        else:
            tareastramitesusers = TareaTramiteUser.query.all()
            tareastramitesusers = list(map(lambda tareatramiteuser: tareatramiteuser.serialize(), tareastramitesusers))
            return jsonify(tareastramitesusers), 200
    if request.method == 'POST':
        tramiteuser_id = request.json.get('tramiteuser_id', None)
        tarea_id = request.json.get('tarea_id', None)
            
        if not tramiteuser_id and tramiteuser_id == "":
            return jsonify({"msg": "Falta ingresar información"}), 400
        if not tarea_id and tarea_id == "":
            return jsonify({"msg": "Falta ingresar información"}), 400
        
        tareatramiteuser = TareaTramiteUser()
        tareatramiteuser.tramiteuser_id = tramiteuser_id
        tareatramiteuser.tarea_id = tarea_id
    
        db.session.add(tareatramiteuser)
        db.session.commit()

        return jsonify(tareatramiteuser.serialize()), 200
    if request.method == 'PUT':
        tramiteuser_id = request.json.get('tramiteuser_id', None)
        tarea_id = request.json.get('tarea_id', None)
        status = request.json.get('tarea_id', None)        
            
        if not tramiteuser_id and tramiteuser_id == "":
            return jsonify({"msg": "Falta ingresar información"}), 400
        if not tarea_id and tarea_id == "":
            return jsonify({"msg": "Falta ingresar información"}), 400

        tareatramiteuserput = TareaTramiteUser.query.get(id) #busca por el id
    
        if not tareatramiteuserput:
            return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

        tareatramiteuserput.tramiteuser_id = tramiteuser_id
        tareatramiteuserput.tarea_id = tarea_id
        tareatramiteuserput.status = status
    
        db.session.commit()

        return jsonify(tareatramiteuserput.serialize()), 200
    if request.method == 'DELETE':
        tareatramiteuser = TareaTramiteUser.query.get(id)
        if not tareatramiteuser:
            return jsonify({"msg": "Lo que buscas no fue encontrado"}), 400
        db.session.delete(tareatramiteuser)
        db.session.commit()
        return jsonify({"msg": "Elemento borrado"}), 200







        
if __name__ == '__main__':
    manager.run()


#DESDE AQUI PARTE DASHBOARD TODOLIST

    # @app.route('/tramits', methods=['GET', 'POST'])                           #ESTAS SON LAS RUTAS PARA LA TABLA TRAMITS 
    # @app.route('/tramits/<int:tr_id>', methods=['GET', 'PUT', 'DELETE'])
    # # @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
    # def tramits(tr_id = None):
    #     if request.method == 'GET':
    #         if tr_id is not None:
    #             tramit = Tramits.query.get(tr_id)
    #             if tramit:
    #                 return jsonify(tramit.serialize()), 200
    #             else:
    #                 return jsonify({"msg": "No se encuentra dicho tramite"}), 404
    #         else:
    #             tramits = Tramits.query.all()
    #             tramits = list(map(lambda tramit: tramit.serialize(), tramits))
    #             return jsonify(tramits), 200                      #Validacion de contenido
            
    #     if request.method == 'POST':
    #         tramit = request.json.get('tramit', None)
    #         description = request.json.get("description", None)
    #         # ta_id = request.json.get('ta_id', None)
    #         task01 = request.json.get('task01', None)
    #         statust01 = request.json.get('statust01', None)
    #         task02 = request.json.get('task02', None)
    #         statust02 = request.json.get('statust02', None)
    #         task03 = request.json.get('task03', None)
    #         statust03 = request.json.get('statust03', None)
    #         task04 = request.json.get('task04', None)
    #         statust04 = request.json.get('statust04', None)
    #         task05 = request.json.get('task05', None)
    #         statust05 = request.json.get('statust05', None)
    #         task06 = request.json.get('task06', None)
    #         statust06 = request.json.get('statust06', None)
    #         task07 = request.json.get('task07', None)
    #         statust07 = request.json.get('statust07', None)
    #         task08 = request.json.get('task08', None)
    #         statust08 = request.json.get('statust08', None)
    #         task09 = request.json.get('task09', None)
    #         statust09 = request.json.get('statust09', None)

    #         if not tramit and tramit == "":
    #             return jsonify({"msg": "Ingresar Nombre del Tramite"}), 400
    #         elif not description and description == "":
    #             return jsonify({"msg": "Falta agregar una Descripción"}), 400     #Validando las variables
    #         elif not task01 and task01 == "":
    #             return jsonify({"msg": "Falta agregar una Tarea"}), 400     #Validando las variables

    #         tramits = Tramits()
    #         tramits.tramit = tramit
    #         tramits.description = description
    #         tramits.task01 = task01
    #         tramits.statust01 = statust01
    #         tramits.task02 = task02
    #         tramits.statust02 = statust02
    #         tramits.task03 = task03
    #         tramits.statust03 = statust03
    #         tramits.task04 = task04
    #         tramits.statust04 = statust01
    #         tramits.task05 = task05
    #         tramits.statust05 = statust05
    #         tramits.task06 = task06
    #         tramits.statust06 = statust06
    #         tramits.task07 = task07
    #         tramits.statust07 = statust07
    #         tramits.task08 = task08
    #         tramits.statust08 = statust08
    #         tramits.task09 = task09
    #         tramits.statust09 = statust09

    #         db.session.add(tramits)
    #         db.session.commit()

    #         return jsonify(tramits.serialize()), 200

    #     if request.method == 'PUT':
    #         tramit = request.json.get('tramit', None)
    #         description = request.json.get("description", None)
    #         # ta_id = request.json.get('ta_id', None)
    #         task01 = request.json.get('task01', None)
    #         statust01 = request.json.get('statust01', None)
    #         task02 = request.json.get('task02', None)
    #         statust02 = request.json.get('statust02', None)
    #         task03 = request.json.get('task03', None)
    #         statust03 = request.json.get('statust03', None)
    #         task04 = request.json.get('task04', None)
    #         statust04 = request.json.get('statust04', None)
    #         task05 = request.json.get('task05', None)
    #         statust05 = request.json.get('statust05', None)
    #         task06 = request.json.get('task06', None)
    #         statust06 = request.json.get('statust06', None)
    #         task07 = request.json.get('task07', None)
    #         statust07 = request.json.get('statust07', None)
    #         task08 = request.json.get('task08', None)
    #         statust08 = request.json.get('statust08', None)
    #         task09 = request.json.get('task09', None)
    #         statust09 = request.json.get('statust09', None)

    #         if not tramit and tramit == "":
    #             return jsonify({"msg": "Field tramite is required"}), 400  # 400 o 422

    #         tramitpost = Tramits.query.get(tr_id) #busca por el id
        
    #         if not tramitpost:
    #             return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

    #         tramitpost.tramit = tramit
    #         tramitpost.description = description
    #         tramitpost.task01 = task01
    #         tramitpost.statust01 = statust01
    #         tramitpost.task02 = task02
    #         tramitpost.statust02 = statust02
    #         tramitpost.task03 = task03
    #         tramitpost.statust03 = statust03
    #         tramitpost.task04 = task04
    #         tramitpost.statust04 = statust01
    #         tramitpost.task05 = task05
    #         tramitpost.statust05 = statust05
    #         tramitpost.task06 = task06
    #         tramitpost.statust06 = statust06
    #         tramitpost.task07 = task07
    #         tramitpost.statust07 = statust07
    #         tramitpost.task08 = task08
    #         tramitpost.statust08 = statust08
    #         tramitpost.task09 = task09
    #         tramitpost.statust09 = statust09

    #         db.session.commit() # para actualizar y guardar en la bd

    #         return jsonify(tramitpost.serialize()), 200

    #     if request.method == 'DELETE':
    #         tramits = Tramits.query.get(tr_id)
    #         if not tramits:
    #             return jsonify({"msg": "Item not found"}), 400
    #         db.session.delete(tramits)
    #         db.session.commit()
    #         return jsonify({"msg": "Item deleted"}), 200


    # @app.route('/tasks', methods=['GET', 'POST'])                              #ESTAS SON LAS RUTAS PARA LA TABLA DE TASKS
    # @app.route('/tasks/<int:ta_id>', methods=['GET', 'PUT', 'DELETE'])
    # # @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
    # def tasks(ta_id = None):
    #     if request.method == 'GET':
    #         if ta_id is not None:
    #             task = Tasks.query.get(ta_id)
    #             if task:
    #                 return jsonify(task.serialize()), 200
    #             else:
    #                 return jsonify({"msg": "No se encuentra dicha tarea"}), 404
    #         else:
    #             tasks = Tasks.query.all()
    #             tasks = list(map(lambda task: task.serialize(), tasks))
    #             return jsonify(tasks), 200                      #Validacion de contenido

    #     if request.method == 'POST':
    #         task01 = request.json.get('task01', None)
    #         task02 = request.json.get('task02', None)
    #         task03 = request.json.get('task03', None)
    #         task04 = request.json.get('task04', None)
    #         task05 = request.json.get('task05', None)
    #         task06 = request.json.get('task06', None)
    #         task07 = request.json.get('task07', None)
    #         task08 = request.json.get('task08', None)
    #         task09 = request.json.get('task09', None)

    #         if not task01 and task01 == "":
    #             return jsonify({"msg": "Ingresar por lo menos la primera tarea"}), 400

    #         tasks = Tasks()
    #         tasks.task01 = task01
    #         tasks.task02 = task02
    #         tasks.task03 = task03
    #         tasks.task04 = task04
    #         tasks.task05 = task05
    #         tasks.task06 = task06
    #         tasks.task07 = task07
    #         tasks.task08 = task08
    #         tasks.task09 = task09

    #         db.session.add(tasks)
    #         db.session.commit()

    #         return jsonify(tasks.serialize()), 200

    #     if request.method == 'PUT':
    #         task01 = request.json.get('task01', None)
    #         task02 = request.json.get('task02', None)
    #         task03 = request.json.get('task03', None)
    #         task04 = request.json.get('task04', None)
    #         task05 = request.json.get('task05', None)
    #         task06 = request.json.get('task06', None)
    #         task07 = request.json.get('task07', None)
    #         task08 = request.json.get('task08', None)
    #         task09 = request.json.get('task09', None)

    #         if not task01 and task01 == "":
    #             return jsonify({"msg": "Ingresar por lo menos la primera tarea"}), 400

    #         taskpost = Tasks.query.get(ta_id) #busca por el id
        
    #         if not taskpost:
    #             return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

    #         taskpost.task01 = task01
    #         taskpost.task02 = task02
    #         taskpost.task03 = task03
    #         taskpost.task04 = task04
    #         taskpost.task05 = task05
    #         taskpost.task06 = task06
    #         taskpost.task07 = task07
    #         taskpost.task08 = task08
    #         taskpost.task09 = task09

    #         db.session.commit() # para actualizar y guardar en la bd

    #         return jsonify(taskpost.serialize()), 200
            
        # if request.method == 'DELETE':
        #     tasksid = Tasks.query.get(ta_id)
        #     if not tasksid:
        #         return jsonify({"msg": "Item not found"}), 400
        #     db.session.delete(tasksid)
        #     db.session.commit()
        #     return jsonify({"msg": "Tasks deleted"}), 20
    
    
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



    # @app.route('/tareas', methods=['GET', 'POST'])
    # @app.route('/tareas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    # # @jwt_required # llamando a jwt_required le indico q las rutas abajo son privadas y requiere autorización pra acceder
    # def tareas(id = None):
    #     if request.method == 'GET':
    #         if id is not None:
    #             task = Tarea.query.get(id)
    #             if task:
    #                 return jsonify(task.serialize()), 200
    #             else:
    #                 return jsonify({"msg": "No se encuentra dicha tarea"}), 404
    #         else:
    #             tareas = Tarea.query.all()
    #             tareas = list(map(lambda tarea: tarea.serialize(), tareas))
    #             return jsonify(tareas), 200
    #     if request.method == 'POST':
    #         task = request.json.get('task', None)
                
    #         if not task and task == "":
    #             return jsonify({"msg": "Ingresar Nombre de la Tarea"}), 400

    #         tarea = Tarea()
    #         tarea.task = task
            

    #         db.session.add(tarea)
    #         db.session.commit()

    #         return jsonify(tarea.serialize()), 200
    #     if request.method == 'PUT':
    #         task = request.json.get('task', None)
            
    #         if not task and task == "":
    #             return jsonify({"msg": "Field Task is required"}), 400  # 400 o 422

    #         taskput = Tarea.query.get(id) #busca por el id
        
    #         if not taskput:
    #             return jsonify({"msg": "Not Found"}), 404 # para no actualizar algo q no existe

    #         taskput.task = task        

    #         db.session.commit() # para actualizar y guardar en la bd

    #         return jsonify(taskput.serialize()), 200
    #     if request.method == 'DELETE':
    #         task = Tarea.query.get(id)
    #         if not task:
    #             return jsonify({"msg": "Tarea no encontrada"}), 400
    #         db.session.delete(task)
    #         db.session.commit()
    #         return jsonify({"msg": "Tarea borrada"}), 200

    #         task = Tarea.query.get(id)
    #         if not task:
    #             return jsonify({"msg": "Tarea no encontrada"}), 400
    #         db.session.delete(task)
    #         db.session.commit()
    #         return jsonify({"msg": "Tarea borrada"}), 200
# @app.route("/api/todos/names", methods=["GET"])
# def namegiver():
#     users = Todos.query.all()
#     users = list(map(lambda user: user.name, users))
#     return jsonify(users), 200
