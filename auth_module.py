import bcrypt
import pyotp
import os
import json

# Load user database
USER_DB_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USER_DB_FILE, "w") as file:
        json.dump(users, file)

# Initialize user database
users = load_users()

# Function to register a new user
def register_user(username, password):
    if username in users:
        return "User already exists!"
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    totp_secret = pyotp.random_base32()  # Generate secret for MFA

    users[username] = {
        "password": hashed_password.decode(),
        "mfa_secret": totp_secret
    }
    save_users(users)
    return f"User {username} registered! MFA Secret: {totp_secret}"

# Function to authenticate user
def authenticate_user(username, password, otp_code):
    if username not in users:
        return "User not found!"
    
    stored_password = users[username]["password"].encode()
    if not bcrypt.checkpw(password.encode(), stored_password):
        return "Incorrect password!"

    totp = pyotp.TOTP(users[username]["mfa_secret"])
    if not totp.verify(otp_code):
        return "Invalid OTP!"

    return "Login successful!"
