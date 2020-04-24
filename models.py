from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#clase que crea la tabla users y c/u de sus columnas con sus propiedades
class User(db.Model):
    __tablename__='users'
    id_usuario = db.Column(db.Integer, primary_key=True) #clave primaria
    u_nombre = db.Column(db.String(100), nullable=False)  #nullable=false -->que no puede estar nulo este campo
    u_apellido = db.Column(db.String(100), nullable=False)
    u_rut = db.Column(db.Integer, unique=True nullable=False)
    u_email = db.Column(db.String(100), unique=True nullable=True) #unique=True --> que debe ser unico.
    u_pais = db.Column(db.String(100), nullable=True)
    u_ciudad = db.Column(db.String(100), nullable=True)
    u_sexo = db.Column(db.String(100), nullable=True)
    u_password = db.Column(db.String(100), nullable=False)
    u_avatar = db.Column(db.String(250), nullable=True, default='default.jpg')#foto por default, mientras el usuario no suba una.
    id_tramite = db.Column(db.Integer, db.ForeignKey('tramites.id_tramite'), nullable=False)#clave foránea que permite que se conecten ambas tablas.
	tramite = db.relationship(Tramit)  


    def serialize(self): #funcion que serializa(transforma)los datos que fueron almacenados en las variables arriba y los deja legibles para cualquier motor de BD(si no me equivoco :)).
        return {
            "id_usuario": self.id_usuario,
            "u_nombre": self.u_nombre,
            "u_apellido": self.u_apellido,
            "u_rut": self.u_rut,
	        "u_email":self.u_email,
    	    "u_pais":self.u_pais,
    	    "u_ciudad":self.u_ciudad,
    	    "u_sexo":self.u_sexo,
    	    "u_password":self.u_password,
    	    "u_avatar":self.u_avatar,
    	    "id_tramite":self.id_tramite

        }

#clase que crea la tabla tramites
class Tramit(db.Model):
    __tablename__='tramites'
    id_tramite = db.Column(db.String(100), primary_key=True)
    tr_nombre = db.Column(db.String(100), nullable=False)
    tr_descripcion = db.Column(db.String(500), nullable=False)
    tr_costo = db.Column(db.Integer(10), nullable=False)
    tr_tarea = db.Column(db.String(100), nullable=False)
    tr_estado = db.Column(db.String(50), nullable=False)

    def serialize(self):
	    return {
            "id_tramite":self.id_tramite,	
            "tr_nombre":self.tr_nombre,
            "tr_descripcion":self.tr_descripcion,
            "tr_costo":self.tr_costo,
            "tr_tarea":self.tr_tarea,
            "tr_estado":self.tr_estado
	}


#clase que crea la tabla tareas
class Tasks(db.Model):
    __tablename__='tareas'
    id_tarea = db.Column(db.String(100), primary_key=True)
    ta_nombre = db.Column(db.String(100), nullable=False)
    ta_descripcion = db.Column(db.String(500), nullable=False)
    ta_costo = db.Column(db.Integer(10), nullable=False)
    ta_doc = db.Column(db.String(100), nullable=False)
    id_tramite = db.Column(db.Integer, db.ForeignKey('tramites.id_tramite'), nullable=False)#<--------- no estoy seguro pues ya tengo una variable id_tramite en la linea 17.
	tramite = db.relationship(Tramit) #  <------------------------------------------------------------no estoy seguro pues ya tengo una variable tramite en la linea 18.

    def serialize(self):
	    return {
            "id_tarea":self.id_tarea,	
            "ta_nombre":self.ta_nombre,
            "ta_descripcion":self.ta_descripcion,
            "ta_costo":self.ta_costo,
            "ta_doc":self.ta_doc,
            "id_tramite":self.id_tramite
	}


#clase que crea la tabla documentos
class Docs(db.Model):
    __tablename__='documentos'
    id_doc = db.Column(db.String(100), primary_key=True)
    d_nombre = db.Column(db.String(100), nullable=False)
    d_descripcion = db.Column(db.String(100), nullable=False)
    d_tipo = db.Column(db.String(50), nullable=False)
    id_tarea = db.Column(db.String, db.ForeignKey('tareas.id_tarea'), nullable=False)
	tareas = db.relationship(Tasks)   

    def serialize(self):
	    return {
            "id_doc":self.id_doc,	
            "d_nombre":self.d_nombre,
            "d_descripcion":self.d_descripcion,
            "d_tipo":self.d_tipo,
            "id_tarea":self.id_tarea
	}


#clase que crea la tabla blog
class Blog(db.Model):
    __tablename__='blog'
    id_entrada = db.Column(db.String(100), primary_key=True)
    e_titulo = db.Column(db.String(100), nullable=False)
    e_cuerpo = db.Column(db.String(500), nullable=False)
    e_imagen = db.Column(db.String(200), nullable=False)
    e_fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def serialize(self):
	    return {
            "id_entrada":self.id_entrada,	
            "e_titulo":self.e_titulo,
            "e_cuerpo":self.e_cuerpo,
            "e_imagen":self.e_imagen,
            "e_fecha":self.e_fecha
	}

#clase que crea la tabla comentarios
class Comment(db.Model):
    __tablename__='comentarios'
    id_comentario = db.Column(db.String(100), primary_key=True)
    id_usuario = db.Column(db.String, db.ForeignKey('users.id_usuario'), nullable=False)#<--------- no estoy seguro pues ya tengo una variable id_usuario en la linea 7.
     users = db.relationship(User)   
    c_cuerpo = db.Column(db.String(500), nullable=False)
    c_fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_entrada = db.Column(db.String, db.ForeignKey('blog.id_entrada'), nullable=False)#<--------- no estoy seguro pues ya tengo una variable id_entrada en la linea 103.
     blog = db.relationship(Blog)  

    def serialize(self):
	    return {
            "id_comentario":self.id_comentario,
            "id_usuario":self.id_usuario,
            "c_cuerpo":self.c_cuerpo,
            "c_fecha":self.c_fecha,
            "id_entrada":self.id_entrada
	}
















