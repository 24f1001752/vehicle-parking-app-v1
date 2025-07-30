from flask import Flask,render_template,request,redirect,url_for,flash,session
from functools import wraps
import time
from datetime import datetime
from models import db, User, Parkinglot, Parkingspace, Reserveparkingspot
from app import app
def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to sign-in first')
            return redirect(url_for('signin'))
        return func(*args, **kwargs)
    return inner

def admin_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if'user_id' not in session:
            flash('You need to login first')
            return redirect(url_for('signin'))
        user=User.query.get(session['user_id'])
        if not user.isadmin:
            flash('You are not allowed to view this page')
            return redirect(url_for('home'))
        return func(*args,**kwargs)
    return inner

#__________________________________SIGNIN AND SIGNUP________________________________

@app.route('/')
def signin():
    return render_template('signin.html',user=User.query.get(session.get('user_id')))
@app.route('/', methods=['POST'])
def signin_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username==" " or password==" ":
        flash('Username or password cannot be empty')
        return redirect(url_for('signin'))
    user = User.query.filter_by(username=username).first()    
    if not user:
        flash('User not found')
        return redirect(url_for('signin'))
    if not user.check_password(password):
        flash('Incorrect password')
        return redirect(url_for('signin'))
    session['user_id'] = user.id  
    return redirect(url_for('home'))        


@app.route('/signup')    
def signup():
    return render_template('signup.html',user=User.query.get(session.get('user_id')))   
@app.route('/signup', methods=['POST']) 
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    name=request.form.get('name')
    email=request.form.get('email')
    address=request.form.get('address')
    pincode=request.form.get('pincode')
    if username==" " or password==" " or name==" " or email==" " or address==" " or pincode==" ":
        flash('All fields are required')
        return redirect(url_for('signup'))    
    if User.query.filter_by(username=username).first():
        flash('Username already exists.Please choose some other username')
        return redirect(url_for('signup'))
 
   
    user = User(username=username, password=password, name=name, email=email, address=address, pincode=pincode)
    db.session.add(user)
    db.session.commit()
    flash('User successfully created')
    return redirect(url_for('signin'))

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    flash('You have been signed out')
    return redirect(url_for('home'))
#__________________________________ADMIN SIDE__________________________________

@app.route('/admin_home')
@admin_required
def admin_home():
    user = User.query.get(session['user_id'])
    if not user.isadmin:
        flash('You are not allowed to access this page')
        return redirect(url_for('home'))
    lots=Parkinglot.query.all()    
    for lot in lots:
        lot.occupied=lot.spaces.filter_by(status='occupied').count()
        lot.total=lot.spaces.count()
        lot.available=lot.total- lot.occupied
    return render_template('admin_home.html', user=user,lots=lots)

@app.route('/profile')
@auth_required
def profile():
    return render_template('profile.html',user=User.query.get(session['user_id']))

@app.route('/profile', methods=['POST'])
@auth_required
def profile_post():
    user = User.query.get(session['user_id'])
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    cpassword=request.form.get('cpassword')
    if username==" " or password==" " or cpassword==" ":
        flash('Username or password cannot be empty')
        return redirect(url_for('profile'))
    if not user.check_password(cpassword):
        flash(" Password is Incorrect")    
        return redirect(url_for('profile'))
    if User.query.filter_by(username=username).first() and username != user.username:
        flash('User with this username already exists.Please select some other username')
        return redirect(url_for('profile'))    
    user.name = name
    user.username = username
    user.password=password
    db.session.commit()
    flash('Profile updated successfully.')
    return redirect(url_for('profile'))

@app.route('/admin_home/admin_user')
@admin_required
def admin_user():
    user = User.query.get(session['user_id'])
    if not user.isadmin:
        flash('You are not allowed to access this page')
        return redirect(url_for('home'))
    users = User.query.filter_by(isadmin=False).all()
    return render_template('admin_user.html',users=users,user=user)

def create_admin_graph():
    import matplotlib
    matplotlib.use('Agg')  
    import matplotlib.pyplot as plt
    from models import Reserveparkingspot,Parkinglot,Parkingspace
    from datetime import datetime
    lots= Parkinglot.query.all()
    name_lot=[]
    count_available=[]
    count_occupied=[]
    for lot in lots:
        name_lot.append(lot.primary_location_name)
        available_count=Parkingspace.query.filter_by(lot_id=lot.id,status='available').count()
        occupied_count=Parkingspace.query.filter_by(lot_id=lot.id,status='occupied').count()
        
        count_available.append(available_count)
        count_occupied.append(occupied_count)
    plt.bar(name_lot, count_available, label='Available', color='green')
    plt.bar(name_lot, count_occupied, bottom=count_available, label='Occupied', color='red')
    
    plt.ylabel('Number of Parking Spots')
    plt.title('Summary on Available and Occupied Parking Lots')
    
    plt.savefig('./static/parking_lot_summary.png')
    plt.close()

@app.route('/summary')
@admin_required
def admin_summary():
    create_admin_graph()
    return render_template('admin_summary.html', user=User.query.get(session['user_id']))

@app.route('/admin_home/add')
@admin_required
def add_lot():
    return render_template('parkinglot/add.html', user=User.query.get(session['user_id']))

@app.route('/admin_home/add', methods=['POST'])
@admin_required
def add_lot_post():
    
    name = request.form.get('primary_location_name')
    if name == '':
        flash('Location name cannot be empty')
        return redirect(url_for('add_lot'))
    if Parkinglot.query.filter_by(primary_location_name=name).first():
        flash('Parking lot with this location name already exists')
        return redirect(url_for('add_lot'))
    
    price = request.form.get('price')
    if price == '' or not price.isdigit():
        flash('Price must be a valid number')
    address = request.form.get('address')
    if address == '':
        flash('Address cannot be empty')
        return redirect(url_for('add_lot'))
    pin_code = request.form.get('pin_code')
    
    maximum_number_of_spots = request.form.get('maximum_number_of_spots')
    
    
    
    lot = Parkinglot(primary_location_name=name,address=address, pin_code=pin_code, price=float(price), maximum_number_of_spots=int(maximum_number_of_spots))
    db.session.add(lot)
    db.session.commit()
    for i in range(int(maximum_number_of_spots)):
        spot = Parkingspace(lot_id=lot.id, status='available')
        db.session.add(spot)
    db.session.commit()
    flash('Parking lot added successfully')
    return redirect(url_for('admin_home'))

@app.route('/admin_home/<int:lot_id>/show')
@admin_required
def show_spot(lot_id):
    lot= Parkinglot.query.get(lot_id)
    db.session.refresh(lot)
    for spot in lot.spaces:
        db.session.refresh(spot)
    return render_template('parkinglot/show.html',user=User.query.get(session['user_id']),parking_lot=lot,now=datetime.now())


@app.route('/admin_home/<int:spot_id>/delete_spot')    
@admin_required
def delete_spot(spot_id):
    spot=Parkingspace.query.get(spot_id)
    if not spot:
        flash('Parking spot does not exist')
        return redirect(url_for('admin_home'))
    return render_template('parking_spot/delete.html',user=User.query.get(session['user_id']),spot=spot)

@app.route('/admin_home/<int:spot_id>/delete_spot',methods=['POST'])    
@admin_required
def delete_spot_post(spot_id):
    spot=Parkingspace.query.get(spot_id)
    if not spot:
        flash('Spot does not exist')
        return redirect(url_for('admin_home'))
    db.session.delete(spot)
    db.session.commit()
    flash('Parking Spot deleted successfully')
    return redirect(url_for('admin_home',lot_id=spot.lot_id))

@app.route('/admin_home/<int:lot_id>/edit_lot')
@admin_required
def edit_lot(lot_id):
    parking_lot=Parkinglot.query.get(lot_id)
    return render_template('parkinglot/edit.html',user=User.query.get(session['user_id']),parking_lot=parking_lot)

@app.route('/admin_home/<int:lot_id>/edit_lot',methods=['POST'])
@admin_required
def edit_lot_post(lot_id):
    name = request.form.get('primary_location_name')
    if name == '':
        flash('Location name cannot be empty')
        return redirect(url_for('edit_lot',lot_id=lot_id))
    price = request.form.get('price')
    if price == '' or not price.isdigit():
        flash('Price must be a valid number')
        return redirect(url_for('edit_lot',lot_id=lot_id))
    address = request.form.get('address')
    if address == '':
        flash('Address cannot be empty')
        return redirect(url_for('edit_lot',lot_id=lot_id))
    pin_code = request.form.get('pin_code')

    lot=Parkinglot.query.get(lot_id)
    lot.primary_location_name = name
    lot.address = address
    lot.pin_code = pin_code
    lot.price = price
    available = int(request.form.get('available_spots'))
    occupied = Parkingspace.query.filter_by(lot_id=lot_id, status='occupied').count()
    total = available + occupied
    lot.maximum_number_of_spots = total

    current_spots = Parkingspace.query.filter_by(lot_id=lot_id).all()
    current_max = len(current_spots)
    if total > current_max:
        for i in range(total - current_max):
            spot = Parkingspace(lot_id=lot.id, status='available')
            db.session.add(spot)
    elif total < current_max:
        removable = [spot for spot in current_spots if spot.status == 'available']
        to_remove = current_max - total
        if to_remove <= len(removable):
            for spot in removable[:to_remove]:
                db.session.delete(spot)
        else:
            flash('Not enough available spots to remove')
            return redirect(url_for('edit_lot', lot_id=lot_id))        
     
    db.session.commit()
    flash('Parking lot updated successfully')
    return redirect(url_for('admin_home'))


@app.route('/admin_home/<int:lot_id>/delete_lot')

@admin_required  
def delete_lot(lot_id):
    return render_template('delete_lot.html',user=User.query.get(session['user_id']))
@app.route('/admin_home/<int:lot_id>/delete_lot',methods=['POST']) 
@admin_required
def delete_lot_post(lot_id):
    
    lot=Parkinglot.query.get(lot_id)
    if not lot:
        flash('Lot does not exist')
        return redirect(url_for('admin_home'))
    for space in lot.spaces:
        Reserveparkingspot.query.filter_by(spot_id=space.id).delete()
    Parkingspace.query.filter_by(lot_id=lot_id).delete()        
    db.session.delete(lot)
    db.session.commit()
    flash('Parking lot deleted successfully')
    return redirect(url_for('admin_home'))  
    
#__________________________________USER SIDE__________________________________

@app.route('/home')
@auth_required
def home():
    user = User.query.get(session['user_id'])
    if user.isadmin:
        return redirect(url_for('admin_home'))
    parameter = request.args.get('parameter')
    query = request.args.get('query')
    
    parameters = {
        'primary_location_name': 'Location Name',
        'pin_code': 'Pincode'
    }
    if not parameter or not query:
        return render_template('home.html', user=user, parking_lots=Parkinglot.query.all(), parameters=parameters)
    if parameter=='primary_location_name':
        parking_lots = Parkinglot.query.filter(Parkinglot.primary_location_name.ilike(f'%{query}%')).all()
        return render_template('home.html', user=user, parking_lots=parking_lots,parameters=parameters,parameter=parameter,query=query)
    if parameter=='pin_code':
        parking_lots = Parkinglot.query.filter(Parkinglot.pin_code.ilike(f'%{query}%')).all()
        return render_template('home.html', user=user, parking_lots=parking_lots,parameters=parameters,parameter=parameter,query=query)
    return render_template('home.html', user=user, parking_lots=Parkinglot.query.all(),parameters=parameters)

    


@app.route('/<int:spot_id>/book_parking')
@auth_required
def book_parking(spot_id):
    spot = Parkingspace.query.get(spot_id)
    lot=Parkinglot.query.get(spot.lot_id)
   
    if not spot:
        flash('Parking spot does not exist')
        return redirect(url_for('home'))
    if spot.status == 'occupied':
        flash('This parking spot is already occupied')
        return redirect(url_for('home'))
    return render_template('parking_spot/book_parking.html', user=User.query.get(session['user_id']), spot=spot, lot=lot)

@app.route('/<int:spot_id>/book_parking', methods=['POST'])
@auth_required
def book_parking_post(spot_id):
    spot=Parkingspace.query.get(spot_id)
    lot=Parkinglot.query.get(spot.lot_id)
    
    vehicle_number=request.form['vehicle_number']
    parking_cost=lot.price
    if spot.status=="occupied":
        flash('This parking spot is already occupied')
        return redirect(url_for('home'))
    spot.status = 'occupied'
    reserve = Reserveparkingspot(user_id=request.form['user_id'], spot_id=spot.id, lot_id=lot.id, vehicle_number=vehicle_number, parking_timestamp=datetime.now(), leaving_timestamp=None, parking_cost=parking_cost)
    db.session.add(reserve)
    db.session.commit()
    flash('Parking spot reserved successfully')   
        
    return redirect(url_for('home'))
@app.route('/parked_history')
@auth_required
def parked_history():
    user = User.query.get(session['user_id'])
    if not user:
        flash('You need to sign in first')
        return redirect(url_for('signin'))
    
    return render_template('parked_history.html', user=user,
                           reservations=Reserveparkingspot.query.filter_by(user_id=user.id).all())

@app.route('/leave_spot/<int:reservation_id>')
@auth_required
def leave_spot(reservation_id):
    reservation = Reserveparkingspot.query.get(reservation_id)
    curr_time = datetime.now()
    if not reservation:
        flash('Reservation does not exist')
    return render_template('parking_spot/leave_spot.html', user=User.query.get(session['user_id']), reservation=reservation, spot=Parkingspace.query.get(reservation.spot_id), lot=Parkinglot.query.get(reservation.lot_id),curr_time=curr_time)

@app.route('/leave_spot/<int:reservation_id>', methods=['POST'])
@auth_required
def leave_spot_post(reservation_id):
    reservation = Reserveparkingspot.query.get(reservation_id)
    lot= Parkinglot.query.get(reservation.lot_id)
    spot= Parkingspace.query.get(reservation.spot_id)
    if not reservation:
        flash('Reservation does not exist')
        return redirect(url_for('parked_history'))
    lot= Parkinglot.query.get(reservation.lot_id)    
    reservation.leaving_timestamp = datetime.now()
    lot.price=float(lot.price)
    
    spot.status='available'
    db.session.add(spot)
    db.session.add(reservation)
    db.session.commit()
    flash('Parking spot released successfully') 
    return redirect(url_for('parked_history'))

def create_user_graph():
    import matplotlib
    matplotlib.use('Agg')  
    import matplotlib.pyplot as plt
    from models import Reserveparkingspot
    from datetime import datetime
    user = User.query.get(session['user_id'])
    
    reservations = Reserveparkingspot.query.filter_by(user_id=user.id).all()
    parked_out=len([res for res in reservations if res.leaving_timestamp is not None])
    current= len([res for res in reservations if res.leaving_timestamp is None])
    total=len(reservations)

    x= ['Parked Out', 'Current']
    y= [parked_out, current]
    plt.bar(x, y)
    for i in range(len(y)):
        plt.text(i, y[i], str(y[i]), ha='center', va='bottom')
    plt.title('Usage History of Parking Spots')
    
    plt.savefig('./static/user_parking_history.png')
    plt.close()

@app.route('/user_summary')
@auth_required
def user_summary():
    user = User.query.get(session['user_id'])
    if not user:
        flash('You need to sign in first')
        return redirect(url_for('signin'))
    create_user_graph()
    return render_template('user_summary.html', user=user)


