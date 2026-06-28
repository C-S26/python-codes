from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>SSTI Demo Lab</h2>

    <p>Enter your name:</p>

    <form action="/greet">
        <input type="text" name="name" placeholder="Your Name">
        <button type="submit">Submit</button>
    </form>

    <hr>

    <p>
        Goal: Observe how user input is rendered inside a template.
    </p>
    '''

@app.route('/greet')
def greet():
    name = request.args.get("name", "Guest")

    # Intentionally unsafe for demonstration purposes
    template = f"""
    <h1>Welcome!</h1>

    <p>Hello {name}</p>

    <a href="/">Back</a>
    """

    return render_template_string(template) # Renders the template with user input, vulnerable to SSTI

@app.route('/reset')
def reset():
    return '''
    <h3>Nothing to reset.</h3>
    <a href="/">Back</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)