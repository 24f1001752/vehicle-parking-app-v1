from flask import Flask,render_template,request,redirect,url_for,flash,session
from functools import wraps
from models import db, User, Parkinglot, Parkingspace, Reserveparkingspot
from app import app
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to sign-in first')
            return redirect(url_for('signin'))
        return func(*args, **kwargs)
    return inner
@app.route('/')
@auth_required
def home():
    return render_template('home.html', user=User.query.get(session['user_id']))

@app.route('/profile')
@auth_required
def profile():
    return "profile"

@app.route('/signin')
def signin():
    return render_template('signin.html')
@app.route('/signin', methods=['POST'])
def signin_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username==" " or password==" ":
        flash('Username or password cannot be empty')
        return redirect(url_for('signin'))
    user = User.query.filter_by(username=username).first()    
    if not user:
        flash('User not found')
        return redirect(url_for('signin'))
    if not user.check_password(password):
        flash('Incorrect password')
        return redirect(url_for('signin'))
    session['user_id'] = user.id  
    return redirect(url_for('home'))        


@app.route('/signup')    
def signup():
    return render_template('signup.html')   
@app.route('/signup', methods=['POST']) 
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    name=request.form.get('name')
    if username==" " or password==" ":
        flash('Username or password cannot be empty')
        return redirect(url_for('signup'))    
    if User.query.filter_by(username=username).first():
        flash('Username already exists.Please choose some other username')
        return redirect(url_for('signup'))
 
   
    user = User(username=username, password=password, name=name)
    db.session.add(user)
    db.session.commit()
    flash('User successfully created')
    return redirect(url_for('signin'))

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    flash('You have been signed out')