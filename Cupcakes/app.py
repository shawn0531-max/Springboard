"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from models import db, connect_db, Cupcake
from functions import serial_cupcake
from form import AddCupcakeForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
    form = AddCupcakeForm()

    if form.validate_on_submit():
        return redirect('/')
    else:
        return render_template('home.html', form=form)

@app.route('/api/cupcakes')
def all_cupcakes():
    cupcakes = Cupcake.query.all()

    serialized = [serial_cupcake(c) for c in cupcakes]
    
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:c_id>')
def cupcake(c_id):
    cupcake = Cupcake.query.get_or_404(c_id)

    serialized = serial_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():

    flavor = request.json['flavor']
    rating = request.json['rating']
    size = request.json['size']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, rating=rating, size=size, image=image or None)
    
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serial_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:c_id>', methods=['PATCH'])
def update_cupcake(c_id):

    cupcake = Cupcake.query.get_or_404(c_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    serialized = serial_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:c_id>', methods=['DELETE'])
def delete_cupcake(c_id):

    cupcake = Cupcake.query.get_or_404(c_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message = "Deleted")