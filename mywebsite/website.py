from flask import Flask,render_template,request
from jinja2 import Template
import MySQLdb
from datetime import datetime
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'kousikporey1234@gmail.com',
    MAIL_PASSWORD ='Kp_590@422'
)
mail = Mail(app)

with open('config.json','r') as c:
    params = json.load(c)["params"]

localserver = params['localserver']

if(localserver == True):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_url']
db = SQLAlchemy(app)

class Contact(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    phoneno = db.Column(db.Integer,nullable=False)
    msg = db.Column(db.String(150),nullable=False)
    date = db.Column(db.String(50),nullable=True)

class Posts(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    slug = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(50),nullable=False)
    postby = db.Column(db.String(50),nullable=False)
    date = db.Column(db.String(50),nullable=False)
    img_file = db.Column(db.String(50),nullable=True)



@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:3]
    return render_template("index.html",params = params,posts=posts)

@app.route("/about")    
def about():
    return render_template("about.html",params = params)

@app.route("/contact",methods = ['GET','POST'])      
def contact():
    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phoneno = request.form.get('phoneno')
        msg = request.form.get('msg')
        entry = Contact(name = name,email=email,phoneno=phoneno,msg=msg,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New Message from  ' + name ,sender=email,recipients=['kousikporey1234@gmail.com'],body=msg +'\n' +phoneno)
    return render_template("contact.html",params = params) 

@app.route("/post_route/<string:post_slug>",methods=['GET'])     
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",params = params,post = post)

@app.route("/dashboard")     
def post():
    return render_template("login.html",params = params)     

@app.route("/editpage",methods=['GET','POST'])     
def edit():
    username = request.form.get('username')
    password = request.form.get('psw')
    if(username == 'kousikporey' and password == 'kp590'):
        posts = Posts.query.filter_by().all()
        return render_template("edit.html",params = params,posts=posts) 
    else:
        return render_template("login.html",params = params)        

@app.route("/delete",methods=['POST'])     
def delete():
    slno = request.form.get('button')
    user = Posts.query.get(slno)
    db.session.delete(user)
    db.session.commit()
    posts = Posts.query.filter_by().all()
    return render_template("edit.html",params = params,posts=posts)                             
app.run(debug = True)    