from flask_sqlalchemy import SQLAlchemy
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