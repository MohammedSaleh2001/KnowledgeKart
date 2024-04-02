from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from .verification import generate_verification_token, send_verification_email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from flask_cors import cross_origin
from .models import User
from . import db
import json

auth = Blueprint('auth', __name__)

email_tokens = set()

# Used for testing
import time
@auth.route('/time')
def get_current_time():
    return {'time': time.time()}

@auth.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@auth.route('/verify_email', methods=['GET'])
def verify_email():
    token = request.args.get('token')

    if (not token) or (token not in email_tokens):
        return {'status': 'error', 'msg:': 'Invalid verification token.'}

    # Extract the email from the database record
    email_tokens.pop(token)

    # Perform email verification (e.g., update user's email_verified status in the database)
    # Here, you would typically update your user table to mark the email as verified
    # For demonstration purposes, let's assume there's a users table with an email_verified column
    # update_query = db.text('UPDATE users SET email_verified = true WHERE email = :email')
    # db.session.execute(update_query, {'email': email})
    # db.session.commit()

    # # Delete the verification token from the database (optional, depending on your requirements)
    # delete_query = db.text('DELETE FROM email_verification WHERE token = :token')
    # db.session.execute(delete_query, {'token': token})
    # db.session.commit()

    return {'status': 'success', 'msg': 'Email verification successful. You can now log in.'}

@auth.route('/login', methods=['POST'])
def login_post():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    # remember = True if request.form.get('remember') else False

    # print('login_post:', data)

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query,
                              {'e': email})
    
    user = result.fetchone()
    
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user[2], password):
        return {'status': 'error', 'message': 'Please check your login details!'} # if the user doesn't exist or password is wrong

    # print(user)

    access_token = create_access_token(identity=email)
    return {'status': 'success', 'access_token':access_token, 'role':user[5]}

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
        return {'status': 'error', 'message': 'Email address in use!'}
    
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
    
    # verification_token = generate_verification_token(email)
    # send_verification_email(email, verification_token)
    # email_tokens.add(verification_token)

    access_token = create_access_token(identity=email)
    return {'status': 'success', 'access_token':access_token}

@auth.route('/logout', methods=['POST'])
@jwt_required
def logout():
    response = jsonify({"status": "success"})
    # unset_jwt_cookies(response)
    return response

@auth.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.json
    email = get_jwt_identity()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # print('login_post:', data)

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query, {'e': email})
    
    user = result.fetchone()
    
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user[2], old_password):
        return {'status': 'error', 'message': 'Please check your current login details!'} # if the user doesn't exist or password is wrong

    query = db.text(f"UPDATE kkuser SET hashpass = '{generate_password_hash(new_password)}' WHERE email = '{email}'")

    result = db.session.execute(query)

    db.session.commit()

    return {'status': 'success'}

@auth.route('/reset_password', methods=['POST'])
@jwt_required()
def reset_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')

    # print('login_post:', data)

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query,
                              {'e': email})
    
    user = result.fetchone()
    
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user:
        return {'status': 'error', 'message': 'Email is not registered'} # if the user doesn't exist or password is wrong

    query = db.text(f"UPDATE kkuser SET hashpass = '{generate_password_hash(new_password)}' WHERE email = '{email}'")

    result = db.session.execute(query)

    db.session.commit()

    return {'status': 'success', 'data': data}