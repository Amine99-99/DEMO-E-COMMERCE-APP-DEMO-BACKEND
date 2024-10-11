from flask import Flask, jsonify, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # Note: 'CROS' was misspelled
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hello from jamaica'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db) 
CORS(app) 



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128), unique=True)  

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)




class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    files = db.Column(db.PickleType, nullable=False)  

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='offers') 


with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            return jsonify({'message': 'successfully logged in'}), 200
        else:
            return jsonify({'message': 'invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.json  
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        
        if password != confirm_password:
            return jsonify({'message': 'Passwords do not match'}), 400

        
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already registered'}), 400

        # Create and save the new user
        new_user = User(email=email, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Successfully registered'}), 200

    return jsonify({'message': 'Invalid request method'}), 400

@app.route('/logout',methods=['POST'])
def logout():
   session.clear()
   return jsonify({'message':'successfully logged out'})

@app.route('/upload', methods=['POST'])
def upload():
  if request.method =='POST':
    request = data.json
    name_id = data.get('name_id')
    user_id = data.get('user_id')
    product = Product.query.filter_by(name_id=name_id).first()
    if product :
      return jsonify({'message':'product on the bid'}),400
    else:
      new_product=Product(name_id=name_id,user_id=user_id)
      db.session.add(new_product)
      db.session.commit()
      return jsonify({'message':'product successfully added to the bid'}),200


    
    


