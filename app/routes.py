#!/usr/bin/env python3
# app/routes.py
from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request,
    jsonify,
    flash
    )
from app import app, db, quiz_questions


@app.route('/')
def home():
    show_popup = session.pop('show_popup', False)
    return render_template('index.html', show_popup=show_popup)

@app.route('/signup')
def signup():
    if request.method == 'POST':
        session['show_popup'] = True
        return redirect(url_for('home'))
    else:
        session.pop('show_popup', None)
        return render_template('signup.html')

@app.route('/home')
def home_page():
    username = session.get('username')
    print("Username from session: ", username)
    return render_template('home.html', username=username)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')[:20]
    password = request.form.get('password')
    print(f"Received login request for username: {username}, password: {password}")

    users_ref = db.collection('users')
    user = users_ref.where('username', '==', username).get()
    if not user:
        print("User not found.")
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('home'))

    user_data = user[0].to_dict()
    if user_data.get('password') != password:
        print("Incorrect password.")
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('home'))

    print("Login successful.")
    flash('Login successful', 'success')
    session['login_success'] = True
    session['username'] = username
    print("Session after login: ", session)
    return redirect(url_for('home_page'))

@app.route('/add', methods=['POST'])
def add_document():
    try:
        username = request.form.get('username')[:20]
        name = request.form.get('name')[:20].capitalize()
        surname = request.form.get('surname')[:20].capitalize()
        email = request.form.get('email').lower()
        gender = request.form.get('gender')
        age = int(request.form.get('age'))
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        password_meets_requirements = request.form.get('password-requirements')

        if not username or not name or not surname or not email or not gender or not password or not confirm_password:
            return render_template('signup.html', error="All fields are required")

        if age < 0 or age > 200:
            return render_template('signup.html', error="Age must be between 0 and 200")

        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")

        existing_users = db.collection('users').where('username', '==', username).get()
        existing_users.extend(db.collection('users').where('name', '==', name).where('surname', '==', surname).get())
        existing_users.extend(db.collection('users').where('email', '==', email).get())

        if existing_users:
            return render_template('signup.html', error="Account Already Exists. Please try again.")

        if len(password) < 6:
            return render_template('signup.html', error="Password must be at least 6 characters long")

        data = {
            'username': username,
            'name': name,
            'surname': surname,
            'email': email,
            'gender': gender,
            'age': age,
            'password': password
        }

        db.collection('users').add(data)

        flash('Signup successful', 'success')
        return redirect(url_for('home'))

    except ValueError:
        return render_template('signup.html', error="Age must be a valid integer")

    except Exception as e:
        print(f"Error: {e}")
        return render_template('signup.html', error=f"Internal Server Error: {e}")

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout successful', 'success')
    return redirect(url_for('home'))

@app.route('/profile/<username>')
def profile(username):
    user_ref = db.collection('users').where('username', '==', username).limit(1).get()
    if user_ref:
        user_data = user_ref[0].to_dict()
        return render_template('profile.html', user=user_data)
    else:
        flash('User not found', 'error')
        return redirect(url_for('home'))

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=quiz_questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answers = request.json
    score = 0
    for question in quiz_questions:
        question_id = f"question{quiz_questions.index(question) + 1}"
        if question_id in answers and answers[question_id] == question['correct']:
            score += 1
    return jsonify({'score': score})
