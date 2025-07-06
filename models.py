
from app import db,app

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True,nullable=False)
    passhash=db.Column(db.String(512),nullable=False)
    isadmin=db.Column(db.Boolean,default=False)
    name=db.Column(db.String(64),nullable=True)
    reservations=db.relationship('Reserveparkingspot',backref='user',lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.passhash=generate_password_hash(password)    
    
    def check_password(self,password):
        return check_password_hash(self.passhash,password)

class Parkinglot(db.Model):
    __tablename__='parking_lot'
    id=db.Column(db.Integer,primary_key=True)
    primary_location_name=db.Column(db.String(64),unique=True,nullable=False)
    price=db.Column(db.Float,nullable=False)
    address=db.Column(db.String(128),nullable=False)
    pin_code=db.Column(db.String(16),nullable=False)
    maximum_number_of_spots=db.Column(db.Integer,nullable=False)
    spaces=db.relationship('Parkingspace',backref='parkinglot',lazy=True)

class Parkingspace(db.Model):
    __tablename__='parking_space'
    id=db.Column(db.Integer,primary_key=True)
    lot_id=db.Column(db.Integer,db.ForeignKey('parking_lot.id'),nullable=False)
    status=db.Column(db.String(16),nullable=False)
    reservations=db.relationship('Reserveparkingspot',backref='parkingspace',lazy=True)

    
class Reserveparkingspot(db.Model):
    __tablename__='reserve_parking_spot'
    id=db.Column(db.Integer,primary_key=True)
    spot_id=db.Column(db.Integer,db.ForeignKey('parking_space.id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    parking_timestamp=db.Column(db.DateTime,nullable=False)
    leaving_timestamp=db.Column(db.DateTime,nullable=False)
    parking_cost=db.Column(db.Float,nullable=False)

with app.app_context():
    db.create_all()
    admin=User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin',password='1234',isadmin=True)
        db.session.add(admin)
        db.session.commit()


  


    










 