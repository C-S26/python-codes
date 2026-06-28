from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)

# Fake login (no password for simplicity)
@app.route('/login')
def login():
    user = request.args.get('user', 'user')

    # Create fake JWT (no signature)
    payload = {"user": user}
    token = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

    return jsonify({"token": token})


# Protected endpoint
@app.route('/admin')
def admin():
    token = request.headers.get('Authorization')

    if not token:
        return "No token provided", 401

    try:
        # Decode token (NO validation!)
        decoded = base64.urlsafe_b64decode(token).decode()
        data = json.loads(decoded)

        if data.get("user") == "admin":
            return "Welcome Admin! 🚀"
        else:
            return "Access Denied", 403

    except:
        return "Invalid token", 400


@app.route('/')
def home():
    return "Use /login?user=user to get token"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)