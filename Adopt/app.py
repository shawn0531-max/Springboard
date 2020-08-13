from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from model import db, connect_db, Pet
from form import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home():
"""shows all pets and some information on each"""
    pets = Pet.query.all()

    return render_template('home.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
"""shows add pet form and handles submission of new pet"""
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data

        species = form.species.data

        photo_url = form.photo_url.data

        age = form.age.data

        notes = form.notes.data

        available = form.available.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)

        db.session.add(pet)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('add.html', form=form)
    
@app.route('/<int:id>', methods=['GET', 'POST'])
def edit_pet(id):
"""shows full info on single pet, shows form to edit pet info,
handles submission of new info for that pet"""
    pet = Pet.query.get(id)

    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet = Pet.query.get(id)

        pet.photo_url = form.photo_url.data

        pet.age = form.age.data

        pet.available = form.available.data

        db.session.commit()

        return redirect('/')
    else:
        return render_template('edit.html', form=form, id=id, pet=pet)