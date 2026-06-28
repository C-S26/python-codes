from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route('/')
def home():
    return '''
    <h2>Reflected XSS Lab</h2>

    <form action="/search">
        <input type="text" name="q" placeholder="Search">
        <button type="submit">Search</button>
    </form>
    '''


@app.route('/search')
def search():
    q = request.args.get('q', '')

    # INTENTIONALLY VULNERABLE
    return render_template_string(f'''
        <h1>Search Results</h1>
        <p>You searched for: {q}</p>
        <a href="/">Back</a>
    ''')


@app.route('/reset')
def reset():
    return '''
    <h3>Nothing to reset in reflected XSS lab.</h3>
    <a href="/">Go Back</a>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
