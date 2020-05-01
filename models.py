from flask_sqlalchemy import SQLAlchemy
from datetime import date , time
db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname
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