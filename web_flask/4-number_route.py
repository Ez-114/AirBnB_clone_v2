#!/usr/bin/python3
"""start a web server"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """display hello text"""

    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """goes to hbnb"""

    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    """display c followed by passed text"""

    return "C " + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pyiscool(text="is cool"):
    """Display text"""

    return "Python " + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def isanum(n):
    """display a text that validate a passed variable is an int"""

    return "{:d} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
