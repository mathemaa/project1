# Module werden importiert 
from flask import Flask, request, redirect, render_template
from database import db, users, projects, rooms, test, cur 
from werkzeug.utils import secure_filename
import psycopg2, csv



app = Flask(__name__)


#connecting to postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/project1'
db.init_app(app)

#ROUTING
@app.route("/")
def session_start():
  return render_template("session.html")

#@app.route("/login")
#def login(username, password):
#  user = users.query.filter_by(username=username).first()
#  passw = zustand.query.filter_by(id=id).first()
#  return render_template('editroom.html', datas=x, room=room)

@app.route("/login", methods=['POST'])
def login():

    conn = psycopg2.connect(
    database="project1",
    user="postgres",
    host="localhost",
    port="5432"
    )
    cur = conn.cursor()
    x = request.form['username']
    y = request.form['password']
    

    cur.execute( "SELECT id FROM users WHERE username = %s AND password = %s ",
      (x,y)
    )
    userid = cur.fetchone()


    cur.execute("SELECT role FROM users Where id = %s ",
      (userid,)
      )
    role = cur.fetchone()

    if role == '2' : 
    #return str(role)
      return redirect ('/user')
    else:
      return ('no permisson')







@app.route('/admin')
def admin_session():
  all_projects = projects.query.all()
  all_rooms = rooms.query.all()
  return render_template('admin.html',  datas=all_projects, room_data=all_rooms)

@app.route('/user')
def user_session():
  datas = rooms.query.all()
  return render_template('user.html', datas=datas )

@app.route('/superuser')
def superuser_session():
  all_rooms = rooms.query.all()
  return render_template('superuser.html', datas=all_rooms )



#CSV Daten importieren
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    	f = request.files['the_file']
    	f.save(secure_filename(f.filename))
    	newProject=projects(projectname=request.form['name'], filename=f.filename)
    	db.session.add(newProject)
    	db.session.commit()
        return 'file uploaded successfully'



@app.route('/new_user', methods=['POST'])
def add_user():
        #verifying the role, than adding new user
            role = request.form['role']
            newuser=users(request.form['username'], request.form['password'], request.form['role'], request.form['projectname'])
            db.session.add(newuser)
            db.session.flush()
            #diff between sessions and cursor objects
            db.session.commit()
            userid = str(newuser.id)

            #adding within this userid all the rooms to the test table
            conn = psycopg2.connect(
            database="project1",
            user="postgres",
            host="localhost",
            port="5432"
            )
            cur = conn.cursor()
            if role == '2' : 
                #extracting the floors & rooms from the csv and instert to table
                with open('Duplex_A_20110907_rooms.csv', 'r') as f:
                    reader = csv.reader(f, delimiter=';')
                    for row in reader:
                      #print(row[1],row[2])
                      cur.execute(
                            " INSERT INTO rooms (userid, floor, room) VALUES (%s, %s, %s)",
                            (userid ,row[1],row[2])
                      )
                conn.commit()

                return redirect('/admin')
            else:
                return redirect('/admin')




#debug mode for occuring problems and mistake informations when debugging the code 
if __name__ == "__main__":
  app.run(debug=True)