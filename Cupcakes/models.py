"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connecting to DB"""
    db.app = app
    db.init_app(app)

class Cupcake(db.Model):
    """represents any cupcake"""

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)

    flavor = db.Column(db.Text, nullable = False)

    size = db.Column(db.Text, nullable = False)

    rating = db.Column(db.Float, nullable = False)

    image = db.Column(db.Text, nullable = False, default = "https://tinyurl.com/demo-cupcake")