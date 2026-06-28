from flask import Flask, request, jsonify
import copy

app = Flask(__name__)

# ---------------------------
# DATABASE CLASS (clean state handling)
# ---------------------------
class DB:
    def __init__(self):
        self.reset()

    def reset(self):
        self.users = [
            {"username": "admin"},
            {"username": "carlos"},
            {"username": "user"}
        ]

db = DB()

# ---------------------------
# FRONTEND FILTER (simulated)
# ---------------------------
@app.before_request
def frontend_block():
    # Simulate frontend blocking direct /admin access
    if request.path.startswith("/admin"):
        return "Access denied by frontend", 403

# ---------------------------
# HELPER (backend trusts header)
# ---------------------------
def get_real_path():
    return request.headers.get("X-Original-URL", request.path)

# ---------------------------
# BACKEND ROUTING (vulnerable)
# ---------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    real_path = get_real_path()

    # Admin panel
    if real_path == "/admin":
        return jsonify({
            "message": "Admin panel",
            "users": db.users
        })

    # Delete user
    if real_path == "/admin/delete":
        username = request.args.get("username")

        db.users = [u for u in db.users if u["username"] != username]

        return jsonify({
            "message": f"{username} deleted",
            "users": db.users
        })

    return "Not Found", 404

# ---------------------------
# RESET LAB
# ---------------------------
@app.route("/reset", methods=["POST"])
def reset():
    db.reset()
    return jsonify({"message": "Lab reset successful"})

# ---------------------------
# HEALTH CHECK (optional)
# ---------------------------
@app.route("/")
def home():
    return "Lab is running"

# ---------------------------
# RUN
# ---------------------------
app.run(host="0.0.0.0", port=5000)