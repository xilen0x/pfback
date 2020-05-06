import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True) #clave primaria
    nombre = db.Column(db.String(100), nullable=False)  #nullable=false -->que no puede estar nulo este campo
    apellido = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String, unique=True)
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
        
        
class Tramite(db.Model):
    __tablename__ = 'tramites'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    infointro = db.Column(db.String(1000), nullable=False)
    infocorps = db.Column(db.String(1000), nullable=False)
    infofoot = db.Column(db.String(1000), nullable=False)
    # tareas = db.relationship("TareaTramite")
    tareas = db.relationship("Tarea", backref="tareas", cascade="delete")       #
    
    def serialize(self):
        tareas = []
        tareas = list(map(lambda tarea: tarea.serialize(), self.tareas))
        return {
            "id": self.id,
            "titulo": self.titulo,
            "infointro": self.infointro,
            "infocorps": self.infocorps,
            "infofoot": self.infofoot,
            "tareas": tareas,
        }
        
        
class Tarea(db.Model):
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    tramite_id = db.Column(db.Integer, db.ForeignKey("tramites.id"))            #
    
    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
            "task": self.task
        }
        
        
class TareaTramite(db.Model):
    __tablename__ = 'tareastramites'
    id = db.Column(db.Integer, primary_key=True) 
    tramite_id = db.Column(db.Integer, db.ForeignKey('tramites.id', ondelete='CASCADE'), nullable=False)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id', ondelete='CASCADE'), nullable=False)
    tramite = db.relationship(Tramite)
    tarea = db.relationship(Tarea)
    
    def serialize(self):
        return {
            "id": self.id,
            "tramite_id": self.tramite_id,
            "tarea": self.tarea.serialize()
        }
        

class TramiteUser(db.Model):
    __tablename__ = 'tramitesusers'
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship(User)
    tramite_id = db.Column(db.Integer, db.ForeignKey('tramites.id', ondelete='CASCADE'), nullable=False)
    tramite = db.relationship(Tramite)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    status = db.Column(db.Boolean, nullable=False, default=True)
    tareas = db.relationship("TareaTramiteUser")
    
    def serialize(self):
        tareas = list(map(lambda tarea: tarea.serialize(), self.tareas))
        return {
            "id": self.id,
            "tramite": self.tramite.serialize(),    #AQUI SE GENERO UN PROBLEMA NO SE POR QUE!!!!
            "user": self.user.serialize(),
            "fecha": self.fecha,
            "status": self.status,
            "tareas": tareas 
        }
        
        
class TareaTramiteUser(db.Model):
    __tablename__ = 'tareastramitesusers'
    id = db.Column(db.Integer, primary_key=True) 
    tramiteuser_id = db.Column(db.Integer, db.ForeignKey('tramitesusers.id', ondelete='CASCADE'), nullable=False)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id', ondelete='CASCADE'), nullable=False)
    tarea = db.relationship(Tarea)
    status = db.Column(db.Boolean, nullable=False, default=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "tramiteuser_id": self.tramiteuser_id,
            "tarea": self.tarea.serialize(),
            "status": self.status
        }


class Blog(db.Model):
    __tablename__='blog'
    id_entrada = db.Column(db.Integer, primary_key=True)
    e_titulo = db.Column(db.String(100), nullable=False)
    e_cuerpo = db.Column(db.String(500), nullable=False)
    e_imagen = db.Column(db.String(250), nullable=True, default='vista.jpg')
    e_fecha = db.Column(db.String(200), nullable=False)
    
    
    def serialize(self):
	    return {
            "id_entrada":self.id_entrada,	
            "e_titulo":self.e_titulo,
            "e_cuerpo":self.e_cuerpo,
            "e_imagen":self.e_imagen,
            "e_fecha":self.e_fecha
	}

        
class Comment(db.Model):
    __tablename__='comentarios'
    id_comentario = db.Column(db.Integer, primary_key=True)
    c_cuerpo = db.Column(db.String(500), nullable=False)
    c_fecha = db.Column(db.String(200), nullable=False)
    blog = db.relationship(Blog)
    id_blog = db.Column(db.String, db.ForeignKey('blog.id_entrada'), nullable=False)#<--------- no estoy seguro pues ya tengo una variable id_entrada en la linea 103.
    
    
    def serialize(self):
	    return {
            "id_comentario":self.id_comentario,
            "c_cuerpo":self.c_cuerpo,
            "c_fecha":self.c_fecha,
            "blog":self.blog.serialize(),
	}



# INICIO BORRADOR
    # # class Tasks(db.Model):
    # #     __tablename__ = "tasks"
    # #     ta_id = db.Column(db.Integer, primary_key=True)
    # #     task01 = db.Column(db.String(100), nullable=False)
    # #     task02 = db.Column(db.String(100), nullable=True)
    # #     task03 = db.Column(db.String(100), nullable=True)
    # #     task04 = db.Column(db.String(100), nullable=True)
    # #     task05 = db.Column(db.String(100), nullable=True)
    # #     task06 = db.Column(db.String(100), nullable=True)
    # #     task07 = db.Column(db.String(100), nullable=True)
    # #     task08 = db.Column(db.String(100), nullable=True)
    # #     task09 = db.Column(db.String(100), nullable=True)

    # #     def serialize(self):
    # #         return{
    # #             "ta_id": self.ta_id,
    # #             "task01": self.task01,
    # #             "task02": self.task02,
    # #             "task03": self.task03,
    # #             "task04": self.task04,
    # #             "task05": self.task05,
    # #             "task06": self.task06,
    # #             "task07": self.task07,
    # #             "task08": self.task08,
    # #             "task09": self.task09
    # #         }

    # # class Tramits(db.Model):
    # #     __tablename__ = "tramits"
    # #     tr_id = db.Column(db.Integer, primary_key=True)
    # #     tramit = db.Column(db.String(100), nullable=False, unique=True)
    # #     description = db.Column(db.String(10000), nullable=False)
    # #     # tasks_details = db.relationship(Tasks)
    # #     # ta_id = db.Column(db.String, db.ForeignKey("tasks.ta_id"), nullable=False)
    # #     task01 = db.Column(db.String(100), nullable=False)
    # #     task02 = db.Column(db.String(100), nullable=True)
    # #     task03 = db.Column(db.String(100), nullable=True)
    # #     task04 = db.Column(db.String(100), nullable=True)
    # #     task05 = db.Column(db.String(100), nullable=True)
    # #     task06 = db.Column(db.String(100), nullable=True)
    # #     task07 = db.Column(db.String(100), nullable=True)
    # #     task08 = db.Column(db.String(100), nullable=True)
    # #     task09 = db.Column(db.String(100), nullable=True)

    # #     def serialize(self):
    # #         return{
    # #             "tr_id": self.tr_id,
    # #             "tramit": self.tramit,
    # #             "description": self.description,
    # #             # "tasks_details": self.tasks_details.serialize(),
    # #             "task01": self.task01,
    # #             "task02": self.task02,
    # #             "task03": self.task03,
    # #             "task04": self.task04,
    # #             "task05": self.task05,
    # #             "task06": self.task06,
    # #             "task07": self.task07,
    # #             "task08": self.task08,
    # #             "task09": self.task09,
    # #         }

    # class Tramits(db.Model):
    #     __tablename__ = "tramits"
    #     tr_id = db.Column(db.Integer, primary_key=True)
    #     tramit = db.Column(db.String(100), nullable=False, unique=True)
    #     description = db.Column(db.String(10000), nullable=False)
    #     task01 = db.Column(db.String(100), nullable=False)
    #     statust01 = db.Column(db.Boolean, unique=False, default=False)
    #     task02 = db.Column(db.String(100), nullable=True)
    #     statust02 = db.Column(db.Boolean, unique=False, default=False)
    #     task03 = db.Column(db.String(100), nullable=True)
    #     statust03 = db.Column(db.Boolean, unique=False, default=False)
    #     task04 = db.Column(db.String(100), nullable=True)
    #     statust04 = db.Column(db.Boolean, unique=False, default=False)
    #     task05 = db.Column(db.String(100), nullable=True)
    #     statust05 = db.Column(db.Boolean, unique=False, default=False)
    #     task06 = db.Column(db.String(100), nullable=True)
    #     statust06 = db.Column(db.Boolean, unique=False, default=False)
    #     task07 = db.Column(db.String(100), nullable=True)
    #     statust07 = db.Column(db.Boolean, unique=False, default=False)
    #     task08 = db.Column(db.String(100), nullable=True)
    #     statust08 = db.Column(db.Boolean, unique=False, default=False)
    #     task09 = db.Column(db.String(100), nullable=True)
    #     statust09 = db.Column(db.Boolean, unique=False, default=False)

    #     def serialize(self):
    #         return{
    #             "tr_id": self.tr_id,
    #             "tramit": self.tramit,
    #             "description": self.description,
    #             "task01": self.task01,
    #             "statust01": self.statust01,
    #             "task02": self.task02,
    #             "statust02": self.statust02,
    #             "task03": self.task03,
    #             "statust03": self.statust03,
    #             "task04": self.task04,
    #             "statust04": self.statust04,
    #             "task05": self.task05,
    #             "statust05": self.statust05,
    #             "task06": self.task06,
    #             "statust01": self.statust06,
    #             "task07": self.task07,
    #             "statust07": self.statust07,
    #             "task08": self.task08,
    #             "statust08": self.statust08,
    #             "task09": self.task09,
    #             "statust09": self.statust09,
    #         }

    # # class Tramites(db.Model): 
    #     #  __tablename__='Tramites'
    #     #  id = db.Column(db.Integer, primary_key=True)
    #     #  nombretramite = db.Column(db.String(100), nullable=False)
    #     #  introtramite = db.Column(db.String(10000), nullable=False)
    #     #  cuerpotramite = db.Column(db.String(10000), nullable=False)
    #     #  pietramite = db.Column(db.String(10000), nullable=False)
    #     # tasks_details = db.relationship(Tasks)
    #     # ta_id = db.Column(db.String, db.ForeignKey("tasks.ta_id"), nullable=False)

    #     #  def serialize(self):
    #     #      return {
    #     #          "id": self.id,
    #     #          "nombretramite": self.nombretramite,
    #     #          "introtramite": self.introtramite,
    #     #          "cuerpotramite": self.cuerpotramite,
    #     #          "pietramite": self.pietramite
    #     #          "tasks_details": self.tasks_details.serialize(),
    #     #      }

    # # class Tareas(db.Model):
    #     #  __tablename__='Tareas'
    #     #  id = db.Column(db.Integer, primary_key=True)
    #     #  nombretarea = db.Column(db.String(20), nullable=True)
