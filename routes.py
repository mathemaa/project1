# Module werden importiert 
from flask import Flask, request, redirect, render_template
#what is db, replacing the cursor?
from database import db, users

app = Flask(__name__)

#connecting to postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/project1'
db.init_app(app)

#ROUTING
@app.route("/")
def session_start():
  return render_template("session.html")

@app.route('/admin')
def admin_session():
  return render_template('admin.html')

@app.route('/user')
def user_session():
  return render_template('user.html')

@app.route('/superuser')
def superuser_session():
  return render_template('superuser.html')

@app.route('/new_user', methods=['POST'])
def add_user():
    newuser=users(request.form['username'], request.form['password'], request.form['role'])
    db.session.add(newuser)
    db.session.commit()
    return redirect('/admin')


#debug mode for occuring problems and mistake informations when debugging the code 
if __name__ == "__main__":
  app.run(debug=True)