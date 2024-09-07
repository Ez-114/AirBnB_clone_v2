#!/usr/bin/python3
"""start a web server"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """display hello text"""

    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """goes to hbnb"""

    return 'HBNB'

@app.route('/c/<text>')
def cisfun(text):
    """display c followed by passed text"""

    return "C " + text.replace('_', ' ')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
