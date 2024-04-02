from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from .verification import generate_verification_token, send_verification_email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from flask_cors import cross_origin
from .models import User
from . import db
import json

main = Blueprint('main', __name__)

def get_user_profile_helper(columnkey, columnval):
    query = db.text(f'SELECT * FROM kkuser WHERE {columnkey} = :e')

    result = db.session.execute(query, {'e': columnval})
    
    user = result.fetchone()

    if not user:
        return None
    
    data =  {'userid': user[0],
            'email': user[1], 
            'firstname': user[3], 
            'role': user[5], 
            'politeness': user[9], 
            'honesty': user[10], 
            'quickness': user[11], 
            'numreviews': user[12]}
    
    return data

@main.route('/search_users', methods=['POST'])
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

@main.route('/add_listing', methods=['POST'])
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

@main.route('/user_profile', methods=['GET', 'POST'])
@jwt_required()
def get_user_profile():
    email = get_jwt_identity()  # Get current user by default

    if request.method == 'POST':
        data = request.json
        email = data.get('email')

    user_data = get_user_profile_helper('email', email)

    if not user_data:
        return {'status': 'error', 'message': 'Email address not in use!'}
    
    return {'status': 'success', 'data': user_data}
   
@main.route('/search_listings', methods=['POST'])
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

@main.route('/listing_profile', methods=['POST'])
@jwt_required()
def get_listing():
    data = request.json
    listingid = data.get('listingid')

    query = db.text(f"SELECT * FROM listing WHERE listingid = {listingid}")

    result = db.session.execute(query)

    listing = result.fetchone()

    if not listing:
        return {'status': 'error', 'message': 'No such listing!'}

    sellerid = listing[1]

    seller_data = get_user_profile_helper('userid', sellerid)

    if not seller_data:
        return {'status': 'error', 'message': 'No seller!'}
    
    data = {'listingid': listing[0],
            'seller': seller_data,
            'listing_name': listing[2],
            'listing_description': listing[3],
            'asking_price': listing[4],
            'category_type': listing[5],
            'condition': listing[7],
            'date_listed': listing[9]}

    return {'status': 'success', 'data': data}

@main.route('/edit_user_profile', methods=['POST'])
@jwt_required()
def edit_user_profile():
    data = request.json
    old_email = get_jwt_identity()
    new_email = data.get('new_email')
    
    query = db.text(f"UPDATE kkuser SET email = '{new_email}' WHERE email = '{old_email}'")

    result = db.session.execute(query)

    db.session.commit()
    
    return redirect('/api/user_profile')

@main.route('/get_chat', methods=['POST'])
@jwt_required()
def get_chat():
    data = request.json
    email = get_jwt_identity()

    user_data = get_user_profile_helper('email', email)

    if not user_data:
        return {'status': 'error', 'message': 'Email address not in use!'}

    query = db.text(f"SELECT * FROM chat WHERE messageto = :i OR messagefrom = :i")

    result = db.session.execute(query, {'i': user_data['userid']})

    searchchat = []
    for chatmsg in result.fetchall():
        data = {'messageid': chatmsg[0],
                'to': chatmsg[1],
                'from': chatmsg[2],
                'datesent': chatmsg[3],
                'message': chatmsg[4]
        }
        searchchat.append(data)

    return jsonify({'status': 'success', 'data': searchchat})

@main.route('/send_chat', methods=['POST'])
@jwt_required()
def send_chat():
    data = request.json
    sender = get_jwt_identity()
    receiver = data.get('receiver_email')
    message = data.get('message')

    sender_data = get_user_profile_helper('email', sender)
    receiver_data = get_user_profile_helper('email', receiver)

    if not sender_data or not receiver_data:
        return {'status': 'error', 'message': 'Email address not in use!'}

    query = db.text(
            '''
            INSERT INTO chat (messageto,
                            messagefrom,
                            datesent,
                            message)
            VALUES (:receiverid, :senderid, :datesent, :message)
            ''')

    result = db.session.execute(query, {'receiverid': receiver_data['userid'],
                                        'senderid': sender_data['userid'],
                                        'datesent': str(datetime.now()),
                                        'message': message})

    db.session.commit()

    return {'status': 'success'}