from flask import Flask, request, jsonify
from auth_module import register_user, authenticate_user

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    return jsonify({"message": register_user(username, password)})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    otp_code = data["otp"]
    return jsonify({"message": authenticate_user(username, password, otp_code)})

if __name__ == "__main__":
    app.run(debug=True)
