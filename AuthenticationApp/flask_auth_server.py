from flask import Flask, request, jsonify
import bcrypt
import jwt
import os
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

app = Flask(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

# Generate RSA Key Pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Serialize Public Key
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Mock user storage
users = {
    "testuser": bcrypt.hashpw("password123".encode(), bcrypt.gensalt())
}

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    username = data.get("username")
    password = data.get("password").encode()
    
    if username in users and bcrypt.checkpw(password, users[username]):
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({"username": username, "exp": exp_time}, SECRET_KEY, algorithm="HS256")
        return jsonify({"passkey": token}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    token = data.get("passkey")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "username": decoded["username"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)  



