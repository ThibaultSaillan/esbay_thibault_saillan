from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String,DATE,ForeignKey

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)
    return db

def create_table(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seller = db.Column(db.String(255), nullable=False)
    buyer = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'seller': self.seller,
            'buyer': self.buyer,
            'date_added': self.date_added,
        }

class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=True)
    last_name = db.Column(db.String(255), unique=False, nullable=True)
    password = db.Column(db.String(255), unique=False, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(255), unique=True, nullable=True)

    def encode_api_key(self):
        self.api_key = sha256_crypt.hash(self.username + str(datetime.utcnow))

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_email(self):
        return self.email

    def __repr__(self):
        return '<User %r>' %(self.email)

    def to_json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'api_key': self.api_key,
            'is_active': True
        }

class Bidding(db.Model):
    __tablename__ = 'bidding'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    user_id = db.Column(db.String(255), db.ForeignKey('user.email'), nullable=True)
    price = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'price': self.price,
        }
