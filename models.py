from flask_sqlalchemy import SQLAlchemy
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