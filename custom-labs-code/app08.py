from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# Temporary storage
messages = []


@app.route('/')
def index():
    return render_template('index1.html', messages=messages)


@app.route('/post', methods=['POST'])
def post_message():
    message = request.form.get('message')

    # INTENTIONALLY VULNERABLE
    messages.append(message)

    return redirect('/')


@app.route('/reset')
def reset():
    messages.clear()

    return '''
    <h3>Messages cleared.</h3>
    <a href="/">Go Back</a>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
