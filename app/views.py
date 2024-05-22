#!/usr/bin/env python3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from firebase_admin import auth

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = auth.create_user(email=email, password=password)
        flash('User created successfully')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = auth.get_user_by_email(email)
        if user and auth.verify_password_hash(password, user.password_hash):
            session['user_id'] = user.uid
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.login'))


@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Calculate score and save result
        score = 0
        user_id = session.get('user_id')
        for question_id, answer in request.form.items():
            correct_answer = get_correct_answer(question_id)  # Implement this function
            if answer == correct_answer:
                score += 1
        save_quiz_result(user_id, score, 'quiz1')
        return redirect(url_for('main.results', score=score))
    questions = get_quiz_questions()  # Implement this function
    return render_template('quiz.html', questions=questions)

@main.route('/results')
def results():
    score = request.args.get('score')
    return render_template('results.html', score=score)
