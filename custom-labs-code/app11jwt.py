from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'

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

@app.route('/')
def home():
    return '''
    <h2>Northstar Systems Portal</h2>

    <!-- TODO: remove legacy admin migration -->
    <!-- old admin route still active -->

    <p>Internal employee management portal.</p>

    <ul>
        <li><a href="/login">Login</a></li>
        <li><a href="/profile?id=1">Profile</a></li>
        <li><a href="/premium">Premium</a></li>
        <li><a href="/help">Help</a></li>
    </ul>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():

    payload = {
        "user": "student",
        "role": "user",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({
        "token": token
    })

@app.route('/jwt-profile')
def jwt_profile():

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({
            "error": "Authorization header missing"
        }), 401

    try:

        token = auth_header.replace("Bearer ", "")

        data = jwt.decode(
            token,
            options={"verify_signature": False},
            algorithms=["HS256"]
        )

        return jsonify({
            "message": "Token accepted",
            "decoded": data
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 401

@app.route('/profile')
def profile():

    user_id = int(request.args.get('id', 1))

    if user_id in users:
        return jsonify(users[user_id])

    return jsonify({
        "error": "User not found"
    })

@app.route('/premium')
def premium():

    if users[1]['premium'] == True:
        return jsonify({
            "message": "Premium access granted"
        })

    return jsonify({
        "error": "Subscription required"
    }), 403

@app.route('/payment-success', methods=['GET', 'POST'])
def payment_success():

    users[1]['premium'] = True

    return jsonify({
        "message": "Premium unlocked"
    })

@app.route('/update', methods=['POST'])
def update():

    data = request.get_json()

    for key, value in data.items():
        users[1][key] = value

    return jsonify({
        "message": "Profile updated",
        "updated_user": users[1]
    })

@app.route('/admin')
def admin():

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({
            "error": "Authorization required"
        }), 401

    try:

        token = auth_header.replace("Bearer ", "")

        data = jwt.decode(
            token,
            options={"verify_signature": False},
            algorithms=["HS256"]
        )

        if data.get("role") == "admin":
            return jsonify({
                "message": "Welcome Admin",
                "flag": "ADMIN-ACCESS-GRANTED"
            })

        return jsonify({
            "error": "Admin only"
        }), 403

    except:
        return jsonify({
            "error": "Invalid token"
        }), 401

@app.route('/admin-panel-9382')
def hidden_admin():

    return jsonify({
        "message": "Hidden admin panel discovered"
    })

@app.route('/help')
def help_page():
    return '''
    <h3>Help Center</h3>

    <p>For support contact administrator.</p>

    <!-- old beta endpoint still enabled -->
    '''

@app.route('/robots.txt')
def robots():

    return '''
User-agent: *
Disallow: /admin-panel-9382
Disallow: /backup.txt
'''

@app.route('/backup.txt')
def backup():

    return '''
Internal Notes:
- old admin route still active
- jwt verification disabled temporarily
- remove debug references before production
'''

@app.route('/debug.js')
def debug():

    return '''
// DEBUG FILE

const oldAdminPath = "/admin-panel-9382";

// TODO:
// re-enable JWT verification
// remove admin migration code
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)