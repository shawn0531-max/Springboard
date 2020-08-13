from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddCupcakeForm(FlaskForm):
    """Form to add a cupcake"""
    flavor = StringField("Cupcake Flavor", validators=[InputRequired()])

    size = StringField("Cupcake Size", validators=[InputRequired()])

    rating = FloatField("Cupcake Rating", validators=[InputRequired(), NumberRange(0,10)])

    image = StringField("Cupcake picture", default=("https://tinyurl.com/demo-cupcake"), validators=[URL(), Optional()])