#!/usr/bin/env python3
from firebase_admin import firestore

db = firestore.client()

def save_quiz_result(user_id, score, quiz_id):
    doc_ref = db.collection('quiz_results').document()
    doc_ref.set({
        'user_id': user_id,
        'score': score,
        'quiz_id': quiz_id,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def add_quiz_question(question, options, correct_option):
    doc_ref = db.collection('quiz_questions').document()
    doc_ref.set({
        'question': question,
        'options': options,
        'correct_option': correct_option
    })
