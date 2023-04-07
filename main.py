from src.facade import facade as facade_
from src.olt import olt_
from src.olt import ont_
from src.mediator import mediator_
from src.snmp import snmp_
from src.func.time import setInterval
snmp=snmp_
facade=facade_.Facade()
import json
from distutils.log import debug
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'jwt.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change on production
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
#liberadas=facade.get_liberadas()
# DB set up and seeders
@app.cli.command('db_create')
def db_create():
    db.create_all()


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()


@app.cli.command('db_seed')
def db_seed():
    test_user = User(first_name='user',
                     last_name='last',
                     email='email',
                     password='admin')
    db.session.add(test_user)
    db.session.commit()

@jwt_required()
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login Successful', access_token=access_token)
    else:
        return jsonify('Bad email or Password'), 401

# Database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
# DB Schemas
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
# Marsh mellow db adds
user_schema = UserSchema()
users_schema = UserSchema(many=True)
@jwt_required()
@app.route('/autofind', methods=['GET'])
def auto_find():
    a=facade.onu_auto_find()
    b=0
    for i in a:
        print(len(a[i]))
        for j in range(len(a[i])):
            b+=1
            a[i][j]=json.dumps(a[i][j].__dict__)
    a["0"]=b
    return jsonify(a),200
@jwt_required()
@app.route('/off', methods=["GET"])
def get_off():
    b=facade.ont_of()
    for i in b:
        for j in range(len(b[i])):
            b[i][j]=json.dumps(b[i][j].__dict__)
    return jsonify(b)
@jwt_required()
@app.route('/ont',methods=["GET"])
def get_ont():
    return jsonify(facade.onu_on_all()), 200
@jwt_required()
@app.route('/onoff', methods=["GET"])
def get_off_on():
    b=facade.ont_on_off()
    return jsonify(b)
@jwt_required()
@app.route('/liberadas', methods=["GET"])
def get_liberadas():
    return 200
    b=liberadas
    for i in b:
        for j in range(len(b[i])):
            if(type(b[i][j])==str):
                pass
            else:
                b[i][j]=json.dumps(b[i][j].__dict__)
    return jsonify(b)
@jwt_required()
@app.route("/lib",methods=['POST'])
def lib():
    re=''
    onu=ont_.ont()
    if request.is_json:
        re=request.json
    else:
        re=request.form
    onu.set_gpon(re['board'])
    onu.set_port(re['port'])
    onu.set_sn(re['sn'])
    onu.set_modelo(re["tipo"])
    onu.set_zone(re['zona'])
    onu.set_vlan(re['vlan'])
    onu.set_descricao(re['nome'])
    onu.set_generic(re['generic'])
    onu.set_olt(re['olt'])
    media=mediator_.concreteMediator()
    media.liberar(onu)
    return jsonify(200)
if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')