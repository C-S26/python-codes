app.py
from flask import Flask, request, jsonify
import jwt
import datetime

# ============================================================
# Mini CTF Security Lab
# ============================================================
# This application is intentionally vulnerable.
#
# Vulnerabilities Included:
# 1. IDOR (Insecure Direct Object Reference)
# 2. JWT Authentication Bypass
# 3. Business Logic Flaw
# 4. API Mass Assignment
# 5. Hidden Admin Endpoint
# 6. Information Disclosure via Source Code
#
# Students can use:
# - Browser
# - Burp Suite
# - curl
# - Postman
#
# Recommended Activities:
# - Intercept requests
# - Modify parameters
# - Analyze JWT tokens
# - Inspect page source
# - Identify hidden endpoints
# ============================================================

app = Flask(__name__)

# Weak secret intentionally used for lab purposes
app.config['SECRET_KEY'] = 'secret123'

# ============================================================
# Simulated Database
# ============================================================
# User 1 = normal user
# User 2 = admin user
#
# This data is intentionally exposed through vulnerable routes
# for educational purposes.
# ============================================================

users = {
    1: {
        "id": 1,
        "username": "student",
        "role": "user",
        "premium": False,
        "isAdmin": False
    },
    2: {
        "id": 2,
        "username": "carlos",
        "role": "admin",
        "premium": True,
        "isAdmin": True
    }
}

# ============================================================
# HOME PAGE
# ============================================================
# This page intentionally leaks a hidden admin endpoint inside
# HTML comments.
#
# Students should:
# - View page source
# - Inspect comments
# - Discover hidden functionality
#
# Demonstrates:
# - Information disclosure
# - Security through obscurity failure
# ============================================================

@app.route('/')
def home():
    return '''
    <h2>Mini CTF Security Lab</h2>

    <!-- Internal admin path: /admin-panel-9382 -->
    <!-- Debug note: beta admin migration pending -->

    <p>Practice environment for OWASP vulnerabilities.</p>

    <h3>Lab Challenges</h3>

    <ul>
        <li><b>JWT Authentication Lab</b><br>
        Obtain token from /login and test token validation using /jwt-profile</li><br>

        <li><b>IDOR Lab</b><br>
        Access profile data using /profile?id=1 and test parameter manipulation</li><br>

        <li><b>Business Logic Lab</b><br>
        Analyze premium access flow using /premium and /payment-success</li><br>

        <li><b>API Mass Assignment Lab</b><br>
        Send JSON requests to /update and observe backend behavior</li><br>

        <li><b>Hidden Admin Functionality</b><br>
        Inspect source code and discover hidden administrative endpoint</li>
    </ul>
    '''

# ============================================================
# JWT LOGIN
# ============================================================
# Generates a JWT token for the student user.
#
# Intentionally vulnerable because later endpoint disables
# signature verification.
#
# Students can:
# - Decode token
# - Modify payload
# - Reuse manipulated token
# ============================================================

@app.route('/login')
def login():

    payload = {
        "user": "student",
        "role": "user",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        "token": token
    })

# ============================================================
# JWT PROFILE
# ============================================================
# Vulnerability:
# Signature verification disabled.
#
# This allows attackers to:
# - Modify role field
# - Forge admin access
# - Reuse manipulated token
#
# OWASP:
# A07 Identification and Authentication Failures
# ============================================================

@app.route('/jwt-profile')
def jwt_profile():

    token = request.headers.get('Authorization')

    if not token:
        return jsonify({"error": "Token missing"}), 401

    try:
        data = jwt.decode(
            token,
            options={"verify_signature": False},
            algorithms=['HS256']
        )

        return jsonify({
            "message": "Token accepted",
            "decoded": data
        })

    except:
        return jsonify({"error": "Invalid token"}), 401

# ============================================================
# IDOR LAB
# ============================================================
# Vulnerability:
# User-controlled parameter directly accesses user data.
#
# Students can:
# - Change id=1 to id=2
# - Access another user's information
#
# OWASP:
# A01 Broken Access Control
# ============================================================

@app.route('/profile')
def profile():

    user_id = int(request.args.get('id', 1))

    if user_id in users:
        return jsonify(users[user_id])

    return jsonify({"error": "User not found"})

# ============================================================
# BUSINESS LOGIC LAB
# ============================================================
# Vulnerability:
# Application trusts frontend/payment flow.
#
# Students can:
# - Directly access payment-success endpoint
# - Bypass intended workflow
#
# OWASP:
# A01 Broken Access Control
# ============================================================

@app.route('/premium')
def premium():

    paid = request.args.get('paid')

    if paid == 'true':
        return jsonify({
            "message": "Premium access granted"
        })

    return jsonify({
        "error": "Payment required"
    }), 403

@app.route('/payment-success')
def payment_success():

    return jsonify({
        "message": "Premium unlocked"
    })

# ============================================================
# API MASS ASSIGNMENT LAB
# ============================================================
# Vulnerability:
# Backend blindly trusts JSON input.
#
# Students can send:
# {
#   "role": "admin"
# }
#
# or:
# {
#   "isAdmin": true
# }
#
# Result:
# Privilege escalation.
#
# OWASP:
# A01 Broken Access Control
# A04 Insecure Design
# ============================================================

@app.route('/update', methods=['POST'])
def update():

    data = request.get_json()

    for key, value in data.items():
        users[1][key] = value

    return jsonify({
        "message": "Profile updated",
        "updated_user": users[1]
    })

# ============================================================
# ADMIN ACCESS CHECK
# ============================================================
# Access depends on:
# - role field
# - isAdmin field
#
# Students can manipulate these using:
# - JWT modification
# - Mass assignment
# ============================================================

@app.route('/admin')
def admin():

    if users[1]['role'] == 'admin' or users[1]['isAdmin'] == True:
        return jsonify({
            "message": "Welcome Admin",
            "flag": "ADMIN-ACCESS-GRANTED"
        })

    return jsonify({
        "error": "Unauthorized"
    }), 401

# ============================================================
# HIDDEN ADMIN PANEL
# ============================================================
# This endpoint is intentionally hidden.
#
# Students should discover it through:
# - Page source inspection
# - HTML comments
# - Burp analysis
#
# Demonstrates:
# - Information leakage
# - Hidden endpoint discovery
# ============================================================

@app.route('/admin-panel-9382')
def hidden_admin():

    return jsonify({
        "message": "Hidden admin panel discovered"
    })

# ============================================================
# APPLICATION START
# ============================================================
# host='0.0.0.0' allows external access.
# Required for:
# - EC2 hosting
# - ngrok
# - cloudflared
# ============================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
