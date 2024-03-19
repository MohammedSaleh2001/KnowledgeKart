from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# Used for testing
import time
@auth.route('/time')
def get_current_time():
    return {'time': time.time()}

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query,
                              {'e': email})
    
    user = result.fetchone()
    
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user[2], password):
        flash('Please check your login details!')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(User(user), remember=remember)
    return redirect(url_for('main.profile'))

# @auth.route('/signup')
# def signup():
#     return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    # Add check for ualberta address

    query = db.text('SELECT Email FROM kkuser WHERE Email = :e')

    user = db.session.execute(query,
                              {'e': email})
    
    if user.fetchone():
        flash('Email address in use!')
        return {'status': 1}
        # return redirect(url_for('auth.signup'))
    
    query = db.text(
            '''
            INSERT INTO kkuser (Email,
                                HashPass,
                                FirstName)
            VALUES (:email, :pass, :name)
            ''')
    
    db.session.execute(query, 
                       {'email': email,
                        'pass': generate_password_hash(password),
                        'name': name})
    
    db.session.commit()

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query,
                              {'e': email})
    
    user = result.fetchone()
    
    # login_user(User(user), remember=False)
    flash('You have signed up successfully!')
    return {'status': 1} # redirect(url_for('main.profile'))

@auth.route('/changepass')
def changepass():
    return render_template('changepass.html')

@auth.route('/changepass', methods=['POST'])
def changepass_post():
    email = request.form.get('email')
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')

    # Add check for ualberta address

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query,
                              {'e': email})
    
    user=result.fetchone()
    
    if not user:
        flash('Email does not exist!')
        return redirect(url_for('auth.changepass'))
    
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not check_password_hash(user[2], oldpassword):
        flash('Incorrect password!')
        return redirect(url_for('auth.changepass')) # if the user doesn't exist or password is wrong, reload the page
    
    query = db.text(
            '''
            UPDATE kkuser SET HashPass = :pass
                          WHERE Email = :email
            ''')
    
    db.session.execute(query, 
                       {'email': email,
                        'pass': generate_password_hash(newpassword)})
    
    db.session.commit()

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query,
                              {'e': email})
    
    user = result.fetchone()
    
    login_user(User(user), remember=False)
    flash('You have changed your password successfully!')
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))