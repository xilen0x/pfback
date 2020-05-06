from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True) #clave primaria
    nombre = db.Column(db.String(100), nullable=False)  #nullable=false -->que no puede estar nulo este campo
    apellido = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(100), unique=True) #unique=True --> que debe ser unico.
    pais = db.Column(db.String(100), nullable=True)
    ciudad = db.Column(db.String(100), nullable=True)
    sexo = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(250), nullable=True, default='default.jpg')#foto por default, mientras el usuario no suba una.
    

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "rut": self.rut,
	        "email":self.email,
    	    "pais":self.pais,
    	    "ciudad":self.ciudad,
    	    "sexo":self.sexo,
    	    "avatar":self.avatar
        }

class Tasks(db.Model):
    __tablename__ = "tasks"
    ta_id = db.Column(db.Integer, primary_key=True)
    task01 = db.Column(db.String(100), nullable=False)
    task02 = db.Column(db.String(100), nullable=True)
    task03 = db.Column(db.String(100), nullable=True)
    task04 = db.Column(db.String(100), nullable=True)
    task05 = db.Column(db.String(100), nullable=True)
    task06 = db.Column(db.String(100), nullable=True)
    task07 = db.Column(db.String(100), nullable=True)
    task08 = db.Column(db.String(100), nullable=True)
    task09 = db.Column(db.String(100), nullable=True)

    def serialize(self):
        return{
            "ta_id": self.ta_id,
            "task01": self.task01,
            "task02": self.task02,
            "task03": self.task03,
            "task04": self.task04,
            "task05": self.task05,
            "task06": self.task06,
            "task07": self.task07,
            "task08": self.task08,
            "task09": self.task09
        }

class Tramits(db.Model):
    __tablename__ = "tramits"
    tr_id = db.Column(db.Integer, primary_key=True)
    tramit = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(10000), nullable=False)
    tasks_details = db.relationship(Tasks)
    ta_id = db.Column(db.String, db.ForeignKey("tasks.ta_id"), nullable=False)

    def serialize(self):
        return{
            "tr_id": self.tr_id,
            "tramit": self.tramit,
            "description": self.description,
            "tasks_details": self.tasks_details.serialize(),
        }


# class Tramites(db.Model): 
#     __tablename__='Tramites'
#     id = db.Column(db.Integer, primary_key=True)
#     nombretramite = db.Column(db.String(100), nullable=False)
#     introtramite = db.Column(db.String(10000), nullable=False)
#     cuerpotramite = db.Column(db.String(10000), nullable=False)
#     pietramite = db.Column(db.String(10000), nullable=False)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "nombretramite": self.nombretramite,
#             "introtramite": self.introtramite,
#             "cuerpotramite": self.cuerpotramite,
#             "pietramite": self.pietramite
#         }

# class Tareas(db.Model):
#     __tablename__='Tareas'
#     id = db.Column(db.Integer, primary_key=True)
#     nombretarea = db.Column(db.String(20), nullable=True)
class Blog(db.Model):
    __tablename__='blog'
    id_entrada = db.Column(db.Integer, primary_key=True)
    e_titulo = db.Column(db.String(100), nullable=False)
    e_cuerpo = db.Column(db.String(500), nullable=False)
    e_cuerpopro = db.Column(db.String(1000), nullable=False)
    e_imagen = db.Column(db.String(250), nullable=True, default='vista.jpg')
    e_fecha = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    
    
    def serialize(self):
	    return {
            "id_entrada":self.id_entrada,	
            "e_titulo":self.e_titulo,
            "e_cuerpo":self.e_cuerpo,
            "e_cuerpopro":self.e_cuerpopro,
            "e_imagen":self.e_imagen,
            "e_fecha":self.e_fecha
	}
    
    
class Comment(db.Model):
    __tablename__='comentarios'
    id_comentario = db.Column(db.Integer, primary_key=True)
    users = db.relationship(User)
    id_user = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    c_cuerpo = db.Column(db.String(500), nullable=False)
    c_fecha = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    
    
    
    def serialize(self):
	    return {
            "id_comentario":self.id_comentario,
            "c_cuerpo":self.c_cuerpo,
            "c_fecha":self.c_fecha,
            "users":self.users.serialize(),
	}