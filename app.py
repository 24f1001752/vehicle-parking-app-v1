from flask import Flask,render_template,request,redirect,url_for,flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

db=SQLAlchemy(app)
import config

##models

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True,nullable=False)
    passhash=db.Column(db.String(512),nullable=False)
    isadmin=db.Column(db.Boolean,default=False)
    name=db.Column(db.String(64),nullable=True)

class Parkinglot(db.Model):
    __tablename__='parking_lot'
    id=db.Column(db.Integer,primary_key=True)
    primary_location_name=db.Column(db.String(64),unique=True,nullable=False)
    price=db.Column(db.Float,nullable=False)
    address=db.Column(db.String(128),nullable=False)
    pin_code=db.Column(db.String(16),nullable=False)
    maximum_number_of_spots=db.Column(db.Integer,nullable=False)

class Parkingspace(db.Model):
    __tablename__='parking_space'
    id=db.Column(db.Integer,primary_key=True)
    lot_id=db.Column(db.Integer,db.ForeignKey('parking_lot.id'),nullable=False)
    status=db.Column(db.String(16),nullable=False)

class Reserveparkingspot(db.model):
    __tablename='reserve_parking_spot'
    id=db.Column(db.Integer,primary_key=True)
    spot_id=db.Column(db.Integer,db.ForeignKey('parking_space.id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    










 