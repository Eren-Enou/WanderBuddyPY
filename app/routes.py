from flask import render_template, request, redirect, url_for
from app.models.user import User
from app import db, app

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')

    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('home.html'))  # Redirect to a relevant page

@app.route('/')
def home():
    return render_template('home.html')