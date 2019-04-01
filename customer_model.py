from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'
    customerid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    cust_id = db.Column(db.Integer, nullable=False, unique=True)

    def json(self):
        return {'name': self.name, 'address': self.address, 'dob': self.dob, 'cust_id': self.cust_id}

    def add_customer(_name, _address, _dob, _cust_id):
        new_customer = Customer(name=_name, address = _address, dob = _dob, cust_id = _cust_id)
        db.session.add(new_customer)
        db.session.commit()

    def get_all_customers():
        return [Customer.json(customer) for customer in Customer.query.all()]

    def get_customer(_cust_id):
        return Customer.json(Customer.query.filter_by(cust_id=_cust_id).first())

    def delete_customer(_cust_id):
        is_successful = Customer.query.filter_by(cust_id=_cust_id).delete()
        db.session.commit()
        return bool(is_successful)

    def replace_customer(_cust_id, _name, _address, _dob):
        customer_to_replace = Customer.query.filter_by(cust_id=_cust_id).first()
        customer_to_replace.name = _name
        customer_to_replace.address = _address
        customer_to_replace.dob = _dob
        db.session.commit()

    def update_customer_address(_cust_id, _address):
        customer_to_replace = Customer.query.filter_by(cust_id=_cust_id).first()
        customer_to_replace.address = _address
        db.session.commit()

    def update_customer_name(_cust_id, _name):
        customer_to_replace = Customer.query.filter_by(cust_id=_cust_id).first()
        customer_to_replace.name = _name
        db.session.commit()

    def update_customer_dob(_cust_id, _dob):
        customer_to_replace = Customer.query.filter_by(cust_id=_cust_id).first()
        customer_to_replace.dob = _dob
        db.session.commit()



    def __repr__(self):
        customer_object = {
            'name': self.name,
            'address': self.address,
            'cust_id': self.cust_id,
            'dob': self.dob
        }
        return json.dumps(customer_object)
