from flask import Flask, request, jsonify, Response
import json, datetime
from settings import *
from customer_model import *
import jwt
from user_model import User
from functools import wraps
from account_model import *

app.config['SECRET_KEY'] = 'meow'

def valid_customer_object(customer_object):
    if ("name" in customer_object and "address" in customer_object and "cust_id" in customer_object and "dob" in customer_object):
        return True
    else:
        return False

def valid_account_object(account_object):
    if ("accountid" in account_object and "balance" in account_object and "status" in account_object):
        return True
    else:
        return False

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Token invalid.'}), 401
    return wrapper
#
# GETs
#
################################################################################
@app.route('/')
def hello_world():
    return 'Totes the home page!'

@app.route('/accounts')
def get_accounts():
    return jsonify({'accounts': Account.get_all_accounts()})

@app.route('/accounts', methods=['POST'])
def add_accounts():
    req_data = request.get_json()
    if(valid_account_object(req_data)):
        Account.add_account(req_data['accountid'], req_data['balance'], req_data['status'])
        # construct response
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/accounts/" + str(req_data['accountid'])

        return response
    else:
        invalid_account_object_error_message = {
            "error": "Invalid account passed in the request",
            "help_string": "Data passed in should be formatted like this: {...things...}"
        }
        # construct response
        # json.dumps() converts our dictionary into json
        response = Response(json.dumps(invalid_account_object_error_message), status=400, mimetype='application/json')
        return response

@app.route('/accounts/<int:accountid>/<int:balance>', methods=['PATCH'])
def add_funds(accountid,balance):
        Account.update_account_balance(accountid,balance)
        response = Response("", status=204)
        response.headers['Location'] = "/accounts/" + str(accountid)
        return response

# GET /books?<token>
@app.route('/customers')
#@token_required
def get_customers():
    return jsonify({'customers': Customer.get_all_customers()})

# GET /books/<isbn>
    # 2nd parameter passed in url will be stored as 'isbn'
    #   and can then be used as a parameter for the method
@app.route('/customers/<int:cust_id>')
def get_customer_by_cust_id(cust_id):
    return_value = Customer.get_customer(cust_id)
    return jsonify(return_value)


#
################################################################################
# POST /books
# {
#     "name": "Book Name",
#     "price": 6.99,
#     "isbn": 0123456789
# }
@app.route('/customers', methods=['POST'])
def add_customers():
    req_data = request.get_json()

    # sanitize data
    if(valid_customer_object(req_data)):
        Customer.add_customer(req_data['name'], req_data['address'], req_data['dob'], req_data['cust_id'])
        # construct response
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/customers/" + str(req_data['cust_id'])

        return response
    else:
        invalid_customer_object_error_message = {
            "error": "Invalid customer passed in the request",
            "help_string": "Data passed in should be formatted like this: {...things...}"
        }
        # construct response
            # json.dumps() converts our dictionary into json
        response = Response(json.dumps(invalid_customer_object_error_message), status=400, mimetype='application/json')
        return response


# POST /login
@app.route('/login', methods=['POST'])
def get_token():
    req_data = request.get_json()
    username = str(req_data['username'])
    password = str(req_data['password'])
    
    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')

#
# PUTs
#
################################################################################
# PUT /books/0123456789
# {
#     "name": "The Odyssey",
#     "price": 19.99
# }
@app.route('/customers/<int:cust_id>', methods=['PUT'])
def replace_customer(cust_id):
    req_data = request.get_json()
    Customer.replace_customer(cust_id, req_data['name'], req_data['address'], req_data['dob'])
    response = Response("", status=204)

    return response


#
# PATCHs
#
################################################################################
@app.route('/customers/<int:cust_id>', methods=['PATCH'])
def update_customer(cust_id):
    req_data = request.get_json()
    updated_customer = {}
    if('name' in req_data):
        Customer.update_customer_name(cust_id, req_data['name'])
    # TODO: fix this section. Sending a PATCH with price returns a 500
    if('address' in req_data):
        Customer.update_customer_address(cust_id,req_data['address'])

    if('dob' in req_data):
        Customer.update_customer_dob(cust_id,req_data['dob'])


    
    response = Response("", status=204)
    response.headers['Location'] = "/customers/" + str(cust_id)
    return response


#
# DELETEs
#
################################################################################
# DELETE /books/0123456789

@app.route('/customers/<int:cust_id>', methods=['DELETE'])
def delete_customer(cust_id):
    if(Customer.delete_customer(cust_id)):
        response = Response("", status=204)
        return response
    else:
        response = Response("Something when wrong.", status=404)
        return response  

# start server
app.run(debug=True, port=5000)


