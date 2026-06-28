from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index2.html')


@app.route('/reset')
def reset():
    return '''
    <h3>Nothing stored in DOM XSS lab.</h3>
    <a href="/">Go Back</a>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
