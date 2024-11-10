from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

data_file_path = 'user_data.json'

if not os.path.exists(data_file_path):
    with open(data_file_path, 'w') as f:
        json.dump([], f)


# *******************************DEFAULT*******************************


@app.route('/')
def index():
    return render_template('index.html')


# *******************************HOME*******************************


@app.route('/home')
def home():
    return render_template('home.html')


# ********************************REGISTER*******************************


@app.route('/register', methods=['POST'])
def register_user():
    # Get form data
    full_name = request.form.get('fullName')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirmPassword')

    # Basic validation
    if password != confirm_password:
        return jsonify({"status": "error", "message": "Passwords do not match"}), 400

    # Load existing users
    with open(data_file_path, 'r') as f:
        users = json.load(f)

    # Check if the email already exists
    for user in users:
        if user['email'] == email:
            return jsonify({"status": "error", "message": "Email already exists"}), 400

    # Add new user
    new_user = {
        "fullName": full_name,
        "email": email,
        "password": password  # Remember, don't store plain text passwords in production
    }
    users.append(new_user)

    # Save updated data
    with open(data_file_path, 'w') as f:
        json.dump(users, f, indent=4)

    return jsonify({"status": "success", "message": "Registration successful"}), 200


# Route to serve the registration page
@app.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')


# *****************************LOGIN**********************************


@app.route('/login', methods=['POST'])
def login_user():
    # Get login form data
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Read users from JSON file
    with open(data_file_path, 'r') as f:
        users = json.load(f)

    # Check for a user with matching email and password
    for user in users:
        if user['email'] == email and user['password'] == password:
            return jsonify({"status": "success", "message": "Login successful"}), 200
            # return redirect(url_for('home'))
        

    # If no match found
    return jsonify({"status": "error", "message": "Invalid email or password"}), 401

# Route to serve the login page
@app.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
