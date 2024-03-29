from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from flask_cors import cross_origin
from .models import User
from . import db
import json

auth = Blueprint('auth', __name__)

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
    
    # # login_user(User(user), remember=False)
    # flash('You have signed up successfully!')
    # return {'status': 1} # redirect(url_for('main.profile'))

    access_token = create_access_token(identity=email)
    return {'status': 'success', 'access_token':access_token}

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
    
    # login_user(User(user), remember=False)
    flash('You have changed your password successfully!')
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@jwt_required
def logout():
    response = jsonify({"status": "success"})
    unset_jwt_cookies(response)
    return response

@auth.route('/search_users', methods=['POST'])
@jwt_required()
def search_users():
    data = request.json
    search_term = data.get('search_term')
    max_results = data.get('max_number_results')

    query = db.text(f"SELECT Email FROM kkuser WHERE Email LIKE '%{search_term}%'")

    result = db.session.execute(query)

    # print(result)

    userlist = []
    for user in result.fetchall():
        userlist.append(user[0])

    return {'status': 'success', 'data': userlist}

@auth.route('/add_listing', methods=['POST'])
@jwt_required()
def add_listing():
    data = request.json
    user = data.get('user')
    name = data.get('name')
    description = data.get('description')
    asking_price = data.get('asking_price')
    category_type = data.get('category_type')
    # category = data.get('category')
    condition = data.get('condition')
    date_listed = data.get('date_listed')
    
    query = db.text(
            '''
            INSERT INTO listing (userid,
                                listingname,
                                listingdescription,
                                askingprice,
                                categorytypeid,
                                condition,
                                datelisted)
            VALUES (:user, :name, :desc, :price, :cat, :cond, :date)
            ''')

    db.session.execute(query, 
                    {'user': user,
                    'name': name,
                    'desc': description,
                    'price': asking_price,
                    'cat': category_type,
                    'cond': condition,
                    'date': date_listed})

    db.session.commit()

    query = db.text('SELECT * FROM listing WHERE listingname = :name')

    result = db.session.execute(query,
                              {'name': name})
    
    listing = result.fetchone()

    return {'status': 'success' if listing else 'error'}

@auth.route('/user_profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    email = get_jwt_identity()

    query = db.text('SELECT * FROM kkuser WHERE Email = :e')

    result = db.session.execute(query,
                              {'e': email})
    
    user = result.fetchone()

    if not user:
        return {'status': 'error', 'message': 'Email address not in use!'}
    
    data = {'email': user[1], 
            'firstname': user[3], 
            'role': user[5], 
            'politeness': user[9], 
            'honesty': user[10], 
            'quickness': user[11], 
            'numreviews': user[12]}
    
    return {'status': 'success', 'data': data}
    
@auth.route('/search_listings', methods=['POST'])
@jwt_required()
def search_listings():
    data = request.json
    search_term = data.get('search_term')
    max_results = data.get('max_number_results')

    query = db.text(f"SELECT * FROM listing WHERE listingname LIKE '%{search_term}%'")

    result = db.session.execute(query)

    # print(result)

    searchlist = []
    for listing in result.fetchall():
        data = {'listingid': listing[0],
                'userid': listing[1],
                'listing_name': listing[2],
                'listing_description': listing[3],
                'asking_price': listing[4],
                'category_type': listing[5],
                'condition': listing[7],
                'date_listed': listing[9]}
        searchlist.append(data)

    return {'status': 'success', 'data': searchlist}

@auth.route('/listing_profile', methods=['POST'])
@jwt_required()
def get_listing():
    data = request.json
    listingid = data.get('listingid')

    query = db.text(f"SELECT * FROM listing WHERE listingid = {listingid}")

    result = db.session.execute(query)

    listing = result.fetchone()

    if not listing:
        return {'status': 'error', 'message': 'Email address not in use!'}

    data = {'listingid': listing[0],
            'userid': listing[1],
            'listing_name': listing[2],
            'listing_description': listing[3],
            'asking_price': listing[4],
            'category_type': listing[5],
            'condition': listing[7],
            'date_listed': listing[9]}

    return {'status': 'success', 'data': data}
