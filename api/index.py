import os
import json
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
# Required for importing chatbot correctly in vercel / local
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from chatbot import generate_chatbot_response
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.environ.get("SECRET_KEY", "vvitu2026fayazmasthan")
USERS_FILE = os.path.join(base_dir, "users.json")
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            try:
                return json.load(f)
            except:
                return []
    return []
def save_users(users):
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Warning: Could not save users.json (Vercel Read-Only File System): {e}")
@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("verified"):
        return redirect(url_for("home"))
        
    if request.method == "POST":
        name = request.form.get("student_name")
        mobile = request.form.get("mobile_number")
        if name and mobile:
            users = load_users()
            # check if user already exists
            found = False
            for u in users:
                if u.get('mobile') == mobile:
                    u['name'] = name # update name if they log in again
                    found = True
                    break
            if not found:
                users.append({"name": name, "mobile": mobile})
            
            save_users(users)
            
            session["verified"] = True
            session["user_name"] = name
            session["mobile"] = mobile
            return redirect(url_for("home"))
            
    return render_template("login.html")
@app.route("/home")
def home():
    if not session.get("verified"):
        return redirect(url_for("login"))
    return render_template("index.html", user_name=session.get("user_name", "Student"))
@app.route("/chat")
def chat():
    if not session.get("verified"):
        return redirect(url_for("login"))
    return render_template("chat.html")
@app.route("/api/send-msg", methods=["POST"])
def send_msg():
    if not session.get("verified"):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    msg = data.get("message", "")
    if not msg:
        return jsonify({"error": "Empty message"}), 400
        
    # Get response from chatbot.py
    response_text = generate_chatbot_response(msg)
    return jsonify({"response": response_text})
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        mobile = request.form.get("mobile")
        if action == "delete" and mobile:
            users = load_users()
            users = [u for u in users if u.get("mobile") != mobile]
            save_users(users)
            return redirect(url_for("admin"))
    users = load_users()
    return render_template("admin.html", users=users)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
