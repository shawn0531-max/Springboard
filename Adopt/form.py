from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, AnyOf, NumberRange

class AddPetForm(FlaskForm):
    """Form to add pet information"""
    name = StringField("Pet Name", validators=[InputRequired()])

    species = StringField("Pet Species", validators=[InputRequired(), AnyOf(['dog', 'cat', 'porcupine'])])

    photo_url = StringField("Pet Picture URL", default='https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483141.jpg', validators=[Optional(),URL()])

    age = IntegerField("Pet Age", validators=[Optional(), NumberRange(0,30)])

    notes = StringField("Notes Specific to Pet", validators=[Optional()])

    available = BooleanField("Available to Adopt", default=True)

class EditPetForm(FlaskForm):
    """Form to edit pet information"""
    photo_url = StringField("Pet Picture URL", validators=[Optional(),URL()])

    age = IntegerField("Pet Age", validators=[Optional(), NumberRange(0,30)])

    available = BooleanField("Available to Adopt")    