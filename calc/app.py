# Put your app in here.
from operations import add, sub, mult, div

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/add')
def add_op():
    a = request.args.get('a')
    b = request.args.get('b')
    a = int(a)
    b = int(b)
    return str(add(a,b))

@app.route('/sub')
def sub_op():
    a = request.args.get('a')
    b = request.args.get('b')
    a = int(a)
    b = int(b)
    return str(sub(a,b))

@app.route('/mult')
def mult_op():
    a = request.args.get('a')
    b = request.args.get('b')
    a = int(a)
    b = int(b)
    return str(mult(a,b))

@app.route('/div')
def div_op():
    a = request.args.get('a')
    b = request.args.get('b')
    a = int(a)
    b = int(b)
    return str(div(a,b))

@app.route('/math/<operation>')
def single_op(operation):
    a = request.args.get('a')
    b = request.args.get('b')
    a = int(a)
    b = int(b)

    if operation == 'add':
        return str(add(a,b))

    if operation == 'sub':
        return str(sub(a,b))

    if operation == 'mult':
        return str(mult(a,b))

    if operation == 'div':
        return str(div(a,b))