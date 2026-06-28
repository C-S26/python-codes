from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------------------
# DATABASE
# ---------------------------

USERS = [
    {
        "username": "student",
        "password": "student123",
        "role": "user"
    },
    {
        "username": "carlos",
        "password": "admin123",
        "role": "admin"
    }
]

# ---------------------------
# HOME
# ---------------------------

@app.route('/')
def home():
    return '''
    <h2>API Security Lab - NoSQL Injection</h2>

    <p><b>Instructions:</b></p>

    <ul>
        <li>1. Send POST requests to <code>/login</code></li>
        <li>2. Test normal login behavior</li>
        <li>3. Analyze how JSON input is processed</li>
        <li>4. Access <code>/admin</code></li>
        <li>5. Reset lab → <code>/reset</code></li>
    </ul>

    <p><b>Goal:</b> Login as <u>admin</u></p>

    <p><b>Sample Request:</b></p>

    <pre>
{
  "username":"student",
  "password":"student123"
}
    </pre>
    '''

# ---------------------------
# SESSION STATE
# ---------------------------

current_role = None


# ---------------------------
# LOGIN
# ---------------------------

@app.route('/login', methods=['POST'])
def login():

    global current_role

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    username = data.get("username")
    password = data.get("password")

    for user in USERS:

        username_match = False
        password_match = False

        if isinstance(username, dict):
            if "$ne" in username:
                username_match = (
                    user["username"] != username["$ne"]
                )
        else:
            username_match = (
                user["username"] == username
            )

        if isinstance(password, dict):
            if "$ne" in password:
                password_match = (
                    user["password"] != password["$ne"]
                )
        else:
            password_match = (
                user["password"] == password
            )

        if username_match and password_match:

            current_role = user["role"]

            return jsonify({
                "message": "Login successful",
                "username": user["username"],
                "role": user["role"]
            })

    return jsonify({
        "error": "Invalid credentials"
    }), 401


# ---------------------------
# ADMIN PANEL
# ---------------------------

@app.route('/admin')
def admin():

    global current_role

    if current_role == "admin":

        return jsonify({
            "message": "Welcome Admin",
            "flag": "NOSQL-ADMIN-ACCESS"
        })

    return jsonify({
        "error": "Access Denied"
    }), 403

# ---------------------------
# RESET
# ---------------------------

@app.route('/reset')
def reset():

    return jsonify({
        "message": "Nothing to reset"
    })


# ---------------------------
# RUN
# ---------------------------

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )