from flask_sqlalchemy import SQLAlchemy
import psycopg2

db = SQLAlchemy()


#aufrufen der methode connect zur Verbindung mit der PostgreSQL DB
conn = psycopg2.connect(
  database="project1",
  user="postgres",
  host="localhost",
  port="5432"
  )

class users(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100), unique=True)
  role = db.Column(db.String(100))
	
  def __init__(self, username, password, role):
    #Attribute der Klasse -> self.xxxx
    self.username = username
    self.password = password 
    self.role = role 

 