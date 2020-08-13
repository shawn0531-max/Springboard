from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connecting to DB"""
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """Represents any pet created"""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    name = db.Column(db.String(30), nullable = False)

    species = db.Column(db.String(30), nullable = False)

    photo_url = db.Column(db.String(), default = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483141.jpg')

    age = db.Column(db.Integer)

    notes = db.Column(db.String())

    available = db.Column(db.Boolean, nullable = False, default = True)