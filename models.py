
from utils import db

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    money = db.Column(db.Integer,nullable=False,default=100)

class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    task = db.Column(db.String(100),nullable=False)
    value = db.Column(db.Integer,nullable=False)