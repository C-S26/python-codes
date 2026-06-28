from flask import Flask, redirect, url_for

app = Flask(__name__)

# Fake session state
user_paid = True


@app.route('/')
def home():
    return '''
    <h2>Welcome</h2>
    <a href="/login">Login</a>
    '''


@app.route('/login')
def login():
    return '''
    <h3>Logged in as user</h3>
    <a href="/payment">Go to Payment</a>
    '''


@app.route('/payment')
def payment():
    return '''
    <h3>Payment Page</h3>
    <a href="/success">Complete Payment</a>
    '''


# Vulnerable endpoint
@app.route('/success')
def success():
    global user_paid
    user_paid = False
    return redirect(url_for('premium'))


@app.route('/premium')
def premium():
    if user_paid:
        return "<h2>Premium Content Access Granted 🎉</h2>"
    else:
        return "Access Denied"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)