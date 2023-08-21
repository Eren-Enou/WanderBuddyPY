import os

from datetime import datetime
from functools import wraps
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from app.models import User, Trip
from app import db, app


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Check if username already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400
        
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    # return jsonify({"message": "User created successfully"}), 201
    return redirect(url_for('home'))  # Redirect to a relevant page

@app.route('/')
def home():
    return render_template('home.html')
    # return render_template(os.path.join(app.root_path, 'templates', 'home.html'))

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    # Check if user exists and password is correct 
    # (This example uses plain text password matching for simplicity, but in a real application, you should use hashed passwords)
    if user and user.password == password:
        # Store user's ID and username in the session
        session['user_id'] = user.id
        session['username'] = username

        flash('Logged in successfully.')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password.')
        return redirect(url_for('login_form'))

    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login_form'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    # Assuming you've stored user_id in the session during login
    user_id = session['user_id']
    
    # Query for all trips related to this user
    user_trips = Trip.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', trips=user_trips)


@app.route('/add_trip', methods=['POST'])
@login_required
def add_trip():
    destination = request.form.get('destination')
    
    # Convert string dates to date objects
    start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()

    # Assuming you have a relationship between user and trips
    new_trip = Trip(destination=destination, start_date=start_date, end_date=end_date, user_id=session['user_id'])
    
    db.session.add(new_trip)
    db.session.commit()

    flash('Trip added successfully!')
    return redirect(url_for('dashboard'))

@app.route('/edit_trip/<int:trip_id>', methods=['GET', 'POST'])
@login_required
def edit_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        flash('Trip not found!')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Update the trip details
        trip.destination = request.form.get('destination')
        trip.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        trip.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        db.session.commit()
        flash('Trip updated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('edit_trip.html', trip=trip)

@app.route('/create_trip', methods=['GET', 'POST'])
@login_required
def create_trip():
    if request.method == 'POST':
        destination = request.form.get('destination')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        budget = float(request.form.get('budget'))  # Convert the budget string to a float
        will_fly = True if request.form.get('will_fly') == 'yes' else False  # Convert 'yes' or 'no' to a boolean
        description = request.form.get('description')

        # Assuming you also store the user_id for each trip and it's stored in the session during login
        user_id = session['user_id']

        new_trip = Trip(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            will_fly=will_fly,
            description=description,
            user_id=user_id
        )
        
        db.session.add(new_trip)
        db.session.commit()

        flash('Trip created successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('create_trip.html')
