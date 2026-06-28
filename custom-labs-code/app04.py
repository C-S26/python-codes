from flask import Flask, request, jsonify

app = Flask(__name__)

# Default user (used for reset)
DEFAULT_USER = {
    "username": "user",
    "role": "user",
    "isAdmin": False
}

# Working copy
user = DEFAULT_USER.copy()


# Home (instructions)
@app.route('/')
def home():
    return '''
    <h2>API Security Lab - Mass Assignment</h2>
    <p><b>Instructions:</b></p>
    <ul>
        <li>1. View profile → <code>/profile</code></li>
        <li>2. Update profile → <code>/update</code> (POST JSON)</li>
        <li>3. Try sending unexpected fields</li>
        <li>4. Access admin panel → <code>/admin</code></li>
        <li>5. Reset lab → <code>/reset</code></li>
    </ul>
    <p><b>Goal:</b> Become <u>admin</u> 🔥</p>
    '''


# View profile (JSON)
@app.route('/profile', methods=['GET'])
def profile():
    return jsonify(user)


# Vulnerable API (mass assignment)
@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    # VULNERABILITY: blindly updating everything
    user.update(data)

    return jsonify({
        "message": "Profile updated",
        "user": user
    })


# Admin panel (hidden logic)
@app.route('/admin', methods=['GET'])
def admin():
    if user.get("isAdmin") or user.get("role") == "admin":
        return jsonify({
            "message": "Welcome Admin! 🔥",
            "secret": "FLAG-ADMIN-ACCESS"
        })
    return jsonify({"error": "Access Denied"}), 403


# Reset lab
@app.route('/reset', methods=['GET'])
def reset():
    global user
    user = DEFAULT_USER.copy()
    return jsonify({"message": "Lab reset successful ✅"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)