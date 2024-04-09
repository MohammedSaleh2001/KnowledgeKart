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

email_tokens = dict()

def convert_date(date_string):
    date_format = "%a, %d %b %Y %H:%M:%S %Z"
    return datetime.strptime(date_string, date_format)

# Used for testing
import time
@auth.route('/time')
def get_current_time():
    # email = 'ragur@ualberta.ca'
    # verification_token = generate_verification_token()
    # ok = send_verification_email(email, verification_token)
    # email_tokens[email] = verification_token

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

    if (not token) or (token not in email_tokens.values()):
        return {'status': 'error', 'msg:': 'Invalid verification token.'}

    email = [k for k, v in email_tokens.items() if v == token][0]

    query = db.text('UPDATE kkuser SET verified = true WHERE email = :email')
    db.session.execute(query, {'email': email})
    db.session.commit()

    email_tokens.pop(email, None)

    return {'status': 'success', 'msg': 'Email verification successful. You can now log in.'}

@auth.route('/login', methods=['POST'])
def login_post():
    data = request.json
    email = data.get('email').strip().lower()
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

    # if user is blacklisted
    if user[7]:
        blacklisted_until = user[8]
        current_date = datetime.now()

        if blacklisted_until > current_date:
            return {'status': 'error', 'message': f'User is blacklisted until {user[8]}'}
        else:
            query = db.text('UPDATE kkuser SET blacklist = false, blacklisteduntil = null WHERE email = :email')
            db.session.execute(query, {'email': email})
            db.session.commit()

    access_token = create_access_token(identity=email)
    return {'status': 'success', 'access_token':access_token, 'role':user[5]}

@auth.route('/signup', methods=['POST'])
def signup_post():
    data = request.json
    email = data.get('email').strip().lower()
    name = data.get('name')
    password = data.get('password')

    if not email.endswith('@ualberta.ca'):
        return {'status': 'error', 'message': 'Not a ualberta email!'}
    
    query = db.text('SELECT Email FROM kkuser WHERE Email = :e')

    user = db.session.execute(query,
                              {'e': email})
    
    if user.fetchone():
        return {'status': 'error', 'message': 'Email address in use!'}
    
    query = db.text(
            '''
            INSERT INTO kkuser (Email,
                                HashPass,
                                FirstName,
                                Verified)
            VALUES (:email, :pass, :name, false)
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
    
    verification_token = generate_verification_token()
    ok = send_verification_email(email, verification_token)
    email_tokens[email] = verification_token

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