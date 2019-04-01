from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'accounts'
    customerid = db.Column(db.Integer, primary_key=True)
    accountid = db.Column(db.Integer, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(1), nullable=False)

    def json(self):
        return {'accountid': self.accountid, 'balance': self.balance, 'status': self.status}

    def add_account(_accountid, _balance, _status):
        new_account = Account(accountid = _accountid, balance = _balance, status=_status)
        db.session.add(new_account)
        db.session.commit()

    def get_all_accounts():
        return [Account.json(account) for account in Account.query.all()]

    def get_account(_accountid):
        return Account.json(Account.query.filter_by(accountid=_accountid).first())

    def delete_account(_accountid):
        is_successful = Account.query.filter_by(accountid=_accountid).delete()
        db.session.commit()
        return bool(is_successful)



    def update_account_balance(_accountid, _balance):
        account_to_replace = Account.query.filter_by(accountid=_accountid).first()
        account_to_replace.balance = _balance
        db.session.commit()

    def update_account_status(_accountid, _status):
        account_to_replace = Account.query.filter_by(accountid=_accountid).first()
        account_to_replace.status = _status
        db.session.commit()

    def __repr__(self):
        account_object = {
            'accountid': self.accountid,
            'balance': self.balance,
            'status': self.status
        }
        return json.dumps(account_object)
