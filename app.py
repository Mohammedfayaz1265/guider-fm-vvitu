from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json

app = Flask(__name__)
app.secret_key = "vvitu_fm_2026"

USERS_FILE = 'users.json'

# Load college data
with open('college_data.json', 'r', encoding='utf-8') as f:
    college_data = json.load(f)

# Import improved chatbot
from chatbot import get_response

def save_user(name, phone):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)
    
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    for u in users:
        if u.get('phone') == phone:
            return
    users.append({"name": name.strip(), "phone": phone.strip()})
    
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    data = request.get_json()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()

    if len(name) < 2:
        return jsonify({'success': False, 'message': 'Please enter a valid name'})
    if len(phone) != 10 or not phone.isdigit():
        return jsonify({'success': False, 'message': 'Please enter 10-digit mobile number'})

    save_user(name, phone)
    session['user'] = {"name": name, "phone": phone}
    return jsonify({'success': True})

@app.route('/home')
def home():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('index.html', user_name=session['user']['name'])

@app.route('/chat')
def chat_page():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('chat.html', user_name=session['user']['name'])

@app.route('/chat', methods=['POST'])
def chat():
    if not session.get('user'):
        return jsonify({'response': 'Please login first!'})
    
    msg = request.get_json().get('message', '').strip()
    if not msg:
        return jsonify({'response': 'Please type something 😊'})
    
    response = get_response(msg, college_data)
    return jsonify({'response': response})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)
