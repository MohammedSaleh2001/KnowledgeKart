from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from .verification import generate_verification_token, send_rateseller_email, send_ratebuyer_email, send_contact_email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from flask_cors import cross_origin
from .models import User
from . import db
import json
import sys

main = Blueprint('main', __name__)

review_tokens = dict()

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
            'numreviews': user[12],
            'blacklist': user[7],
            'blacklisted_until': user[8],
            'verified': user[6]}
    
    return data

def search_listings_helper(query, search_term, category_filter, price_filter, max_results):
    if max_results != -1:
        params = {
            'search_term': f'%{search_term}%',
            'category_filter': category_filter,
            'price_filter': price_filter,
            'max_results': max_results,
        }
        query += " LIMIT :max_results"
        # print("query:" + query, file=sys.stderr)
        # result = db.session.execute(query)
        result = db.session.execute(db.text(query), params)    
    
        searchlist = []
        for listing in result.fetchall():
            data = {'listingid': listing[0],
                    'sellerid': listing[1],
                    'listing_name': listing[2],
                    'listing_description': listing[3],
                    'asking_price': listing[4],
                    'category_type': listing[5],
                    'condition': listing[7],
                    'date_listed': listing[9],
                    'datechanged': listing[11],
                    'listingstatus': listing[10],
                    'soldto': listing[12],
                    'soldprice': listing[13]}
            searchlist.append(data)

        return searchlist
    else:
        params = {
            'search_term': f'%{search_term}%',
            'category_filter': category_filter,
            'price_filter': price_filter,
        }
        result = db.session.execute(db.text(query), params)    
    
        searchlist = []
        for listing in result.fetchall():
            data = {'listingid': listing[0],
                    'sellerid': listing[1],
                    'listing_name': listing[2],
                    'listing_description': listing[3],
                    'asking_price': listing[4],
                    'category_type': listing[5],
                    'condition': listing[7],
                    'date_listed': listing[9],
                    'datechanged': listing[11],
                    'listingstatus': listing[10],
                    'soldto': listing[12],
                    'soldprice': listing[13]}
            searchlist.append(data)

        return searchlist


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

@main.route('/edit_user_profile', methods=['POST'])
@jwt_required()
def edit_user_profile():
    data = request.json
    email = get_jwt_identity()
    new_name = data.get('new_name')
    
    query = db.text(f"UPDATE kkuser SET firstname = '{new_name}' WHERE email = '{email}'")

    result = db.session.execute(query)

    db.session.commit()
    
    return redirect('/api/user_profile')

@main.route('/search_users', methods=['POST'])
@jwt_required()
def search_users():
    data = request.json
    search_term = data.get('search_term').strip().lower()
    max_results = data.get('max_number_results')

    query = db.text(f"SELECT firstname, email FROM kkuser WHERE email LIKE '%{search_term}%' AND LOWER(userrole) = LOWER('U') LIMIT {max_results}")

    result = db.session.execute(query)

    # print(result)

    userlist = []
    for user in result.fetchall():
        userlist.append({'name': user[0], 'email': user[1]})

    return {'status': 'success', 'data': userlist}

@main.route('/add_listing', methods=['POST'])
@jwt_required()
def add_listing():
    data = request.json
    
    seller = get_jwt_identity()
    seller_data = get_user_profile_helper('email', seller)
    sellerid = seller_data['userid']

    listing_name = data.get('listing_name')
    listing_description = data.get('listing_description')
    asking_price = data.get('asking_price')

    category_map = {'other': 1, 'textbook': 2, 'lab equipment': 3}
    category_type = category_map[data.get('category_type').lower()]

    # category = data.get('category')
    condition = data.get('condition')
    date_listed = str(datetime.now())
    
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
                    {'user': sellerid,
                    'name': listing_name,
                    'desc': listing_description,
                    'price': asking_price,
                    'cat': category_type,
                    'cond': condition,
                    'date': date_listed})

    db.session.commit()

    return {'status': 'success'}
   
@main.route('/search_listings', methods=['POST'])
@jwt_required()
def search_listings():
    data = request.json
    search_term = data.get('search_term')
    category_filter = data.get('category_filter', -1)
    price_filter = data.get('price_filter', 'All')
    date_sort = data.get('date_sort', 'None')
    price_sort = data.get('price_sort', 'None')
    max_results = data.get('max_number_results')

    # query = db.text(f"SELECT * FROM listing WHERE LOWER(listingname) LIKE LOWER('%{search_term}%') LIMIT {max_results}")
    query = "SELECT * FROM listing WHERE listingstatus = 'O' AND LOWER(listingname) LIKE LOWER(:search_term)"

    if category_filter != -1:
        query += " AND categorytypeid = :category_filter"
    if price_filter != 'All':
        split = price_filter.split('-')
        price_filter = int(split[1])
        query += " AND askingprice <= :price_filter"
    order_clause = []
    if date_sort != 'None':
        if date_sort == 'Newest to Oldest':
            order_clause.append("datelisted DESC")
        elif date_sort == 'Oldest to Newest':
            order_clause.append("datelisted ASC")
    if price_sort != 'None':
        if price_sort == 'High to Low':
            order_clause.append("askingprice DESC")
        elif price_sort == 'Low to High':
            order_clause.append("askingprice ASC")
    if order_clause:
        query += " ORDER BY " + ", ".join(order_clause)

    # searchlist = search_listings_helper(query)
    searchlist = search_listings_helper(query, search_term, category_filter, price_filter, max_results)

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

    buyer_data = dict()
    if listing[12] and listing[12] > 1:
        buyer_data = get_user_profile_helper('userid', listing[12])

    if not seller_data:
        return {'status': 'error', 'message': 'No seller!'}
    
    data = {'listingid': listing[0],
            'seller': seller_data,
            'buyer': buyer_data,
            'listing_name': listing[2],
            'listing_description': listing[3],
            'asking_price': listing[4],
            'category_type': listing[5],
            'condition': listing[7],
            'date_listed': listing[9],
            'datechanged': listing[11],
            'listingstatus': listing[10],
            'soldto': listing[12],
            'soldprice': listing[13]}

    return {'status': 'success', 'data': data}

@main.route('/get_user_listings', methods=['POST'])
@jwt_required()
def get_user_listings():
    data = request.json
    seller = data.get('email')
    
    seller_data = get_user_profile_helper('email', seller)
    if not seller_data:
        return {'status': 'error', 'message': 'Email address not in use!'}
    sellerid = seller_data['userid']

    # query = db.text(f"SELECT * FROM listing WHERE userid = '{sellerid}'")
    query = f"SELECT * FROM listing WHERE userid = '{sellerid}'"

    searchlist = search_listings_helper(query, f"%{'%'}%", -1, 'All', -1)

    return {'status': 'success', 'data': searchlist}

@main.route('/edit_listing', methods=['POST'])
@jwt_required()
def edit_listing():
    data = request.json
    
    seller = get_jwt_identity()
    seller_data = get_user_profile_helper('email', seller)
    sellerid = seller_data['userid']

    listingid = data.get('listingid')

    query = db.text(f"SELECT * FROM listing WHERE listingid = {listingid}")
    result = db.session.execute(query)
    listing = result.fetchone()
    if not listing:
        return {'status': 'error', 'message': 'No such listing!'}
    if sellerid != listing[1]:
        return {'status': 'error', 'message': "User cannot edit other seller's listings"}

    listing_name = data.get('listing_name')
    listing_description = data.get('listing_description')
    asking_price = data.get('asking_price')

    category_map = {'other': 1, 'textbook': 2, 'lab equipment': 3}
    category_type = category_map[data.get('category_type').lower()]

    condition = data.get('condition')
    date_changed = str(datetime.now())
    status = data.get('status')
    sold_to = data.get('sold_to')
    sold_price = data.get('sold_price')

    query = db.text(
            '''
            UPDATE listing SET  listingname = :name,
                                listingdescription = :desc,
                                askingprice = :price,
                                categorytypeid = :cat,
                                condition = :cond,
                                datechanged = :date,
                                listingstatus = :status,
                                soldto = :soldto,
                                soldprice = :soldprice 
            WHERE listingid = :listingid              
            ''')

    db.session.execute(query, 
                    {'name': listing_name,
                    'desc': listing_description,
                    'price': asking_price,
                    'cat': category_type,
                    'cond': condition,
                    'date': date_changed,
                    'status': status,
                    'soldto': sold_to,
                    'soldprice': sold_price,
                    'listingid': listingid})

    db.session.commit()

    if status == 'S' and sold_to is not None:
        buyer_data = get_user_profile_helper('userid', sold_to)
        
        verification_token = generate_verification_token()
        send_rateseller_email(seller_data['email'], buyer_data['email'], verification_token)
        review_tokens[(listingid, 'seller')] = {'email': seller_data['email'],
                                                            'token': verification_token}
        
        verification_token = generate_verification_token()
        send_ratebuyer_email(seller_data['email'], buyer_data['email'], verification_token)
        review_tokens[(listingid, 'buyer')] = {'email': buyer_data['email'],
                                                            'token': verification_token}

    return {'status': 'success'}

@main.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.json
    token = data.get('review_token')
    honesty = max(min(data.get('honesty'), 5), 0)
    politeness = max(min(data.get('politeness'), 5), 0)
    quickness = max(min(data.get('quickness'), 5), 0)

    for k, v in review_tokens.items():
        if v['token'] == token:            
            # listingid = k[0]
            email = v['email']

            user_data = get_user_profile_helper('email', email)
            numreviews = user_data['numreviews'] + 1
            honesty = (honesty + user_data['honesty']*user_data['numreviews']) / numreviews
            politeness = (politeness + user_data['politeness']*user_data['numreviews']) / numreviews
            quickness = (quickness + user_data['quickness']*user_data['numreviews']) / numreviews
            review_tokens.pop(k)

            query = db.text('''UPDATE kkuser SET numreviews = :numreviews,
                                                honesty = :honesty,
                                                politeness = :politeness,
                                                quickness = :quickness
                              WHERE email = :email''')
            db.session.execute(query, {'email': email,
                                       'numreviews': numreviews,
                                       'honesty': honesty,
                                       'politeness': politeness,
                                       'quickness': quickness})
            db.session.commit()

            return {'status': 'success'}
        
    return {'status': 'error', 'msg': 'Invalid review token'}

@main.route('/get_review', methods=['POST'])
def get_review():
    data = request.json
    token = data.get('review_token')

    for k, v in review_tokens.items():
        if v['token'] == token:
            res = {'status': 'success',
                   'listingid': k,
                   'seller': v['seller'],
                   'buyer': v['buyer']}
            review_tokens.pop(token)
            return res
    
    return {'status': 'error', 'msg': 'Invalid review token'}

@main.route('/get_reports', methods=['POST'])
@jwt_required()
def get_reports():
    data = request.json
    # email = get_jwt_identity()
    # user_data = get_user_profile_helper('email', email)
    # if not user_data:
    #     return {'status': 'error', 'message': 'Email address not in use!'}

    query = db.text(f"SELECT * FROM report")
    result = db.session.execute(query)

    reports = dict()
    for report in result.fetchall():
        by_data = get_user_profile_helper('userid', report[2])
        data = {'reportid': report[0],
                'report_by': report[1],
                'report_for': report[2],
                'report_for_email': by_data['email'],
                'report_text': report[3],
                'date_reported': report[4],
                'moderator_assigned': report[5],
                'report_open': report[6],
                'date_closed': report[7],
                'verdict': report[8]
        }
        reports[report[0]] = data

    return {'status': 'success', 'data': reports}  

@main.route('/close_report', methods=['POST'])
@jwt_required()
def close_report():
    data = request.json
    assignee = get_jwt_identity()
    verdict = data.get('verdict')
    reportid = data.get('reportid')
    date_closed = str(datetime.now())

    assignee_data = get_user_profile_helper('email', assignee)
    if not assignee_data:
        return {'status': 'error', 'message': 'Email address not in use!'}
    assigneeid = assignee_data['userid']

    query = db.text(
            '''
            UPDATE report SET verdict = :verdict,
                            reportopen = :reportopen,
                            dateclosed = :dateclosed,
                            moderatorassigned = :moderatorassigned 
            WHERE reportid = :reportid
            ''')

    result = db.session.execute(query, {'verdict': verdict,
                                        'reportopen': False,
                                        'dateclosed': date_closed,
                                        'moderatorassigned': assigneeid,
                                        'reportid': reportid})

    db.session.commit()

    return {'status': 'success'}

@main.route('/add_report', methods=['POST'])
@jwt_required()
def add_report():
    data = request.json
    report_by = get_jwt_identity()
    by_data = get_user_profile_helper('email', report_by)

    message = data.get('message')

    report_for = data.get('report_for')
    for_data = get_user_profile_helper('email', report_for)

    if not by_data or not for_data:
        return {'status': 'error', 'message': 'Email address not in use!'}

    query = db.text(
            '''
            INSERT INTO report (reportby,
                            reportfor,
                            datereported,
                            reporttext,
                            moderatorassigned,
                            reportopen)
            VALUES (:reportby, :reportfor, :datereported, :reporttext, :moderatorassigned, :reportopen)
            ''')

    result = db.session.execute(query, {'reportby': by_data['userid'],
                                        'reportfor': for_data['userid'],
                                        'datereported': str(datetime.now()),
                                        'reporttext': message,
                                        'moderatorassigned': 3,
                                        'reportopen': True
                                        })

    db.session.commit()

    return {'status': 'success'} 

@main.route('/suspend_user', methods=['POST'])
@jwt_required()
def suspend_user():
    data = request.json
    email = data.get('email')
    blacklist = data.get('blacklist')
    blacklisted_until = data.get('blacklisted_until')

    query = db.text('''UPDATE kkuser SET blacklist = :blacklist, 
                                        blacklisteduntil = :blacklisted_until 
                        WHERE email = :email
                    ''')

    result = db.session.execute(query, {'blacklist': blacklist,
                                        'blacklisted_until': blacklisted_until,
                                        'email': email})

    db.session.commit()
    
    return {'status': 'success', 'data': get_user_profile_helper('email', email)}

@main.route('/get_chat', methods=['POST'])
@jwt_required()
def get_chat():
    data = request.json
    email = data.get('email')

    user_data = get_user_profile_helper('email', email)

    if not user_data:
        return {'status': 'error', 'message': 'Email address not in use!'}

    query = db.text(f"SELECT * FROM chat WHERE messageto = :i OR messagefrom = :i")

    result = db.session.execute(query, {'i': user_data['userid']})

    searchchat = dict()
    for chatmsg in result.fetchall():
        data = {'messageid': chatmsg[0],
                'to': chatmsg[1],
                'from': chatmsg[2],
                'datesent': chatmsg[3],
                'message': chatmsg[4]
        }

        otherid = data['to'] if data['to'] != user_data['userid'] else data['from']
        other_data = get_user_profile_helper('userid', otherid)
        other = other_data['email']

        if other not in searchchat:
            searchchat[other] = list()

        searchchat[other].append(data)

    return {'status': 'success', 'data': searchchat}

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

@main.route('/send_contact_email', methods=['POST'])
@jwt_required()
def send_contact():
    data = request.json
    buyer = data.get('buyer').strip().lower()
    seller = data.get('seller').strip().lower()

    send_contact_email(seller, buyer)

    return {'status': 'success'}