from wtforms import DecimalField, StringField, SelectMultipleField, SelectField, IntegerField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired, NumberRange, Length


class BioForm(FlaskForm):
    name = StringField('What is Your Name?', validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired()])
    sex = SelectField('Sex', choices=[('Male', 'Male'),
                                      ('Female', 'Female'),
                                      ('Undefined', 'Undefined')], validators=[InputRequired()])
    likes = StringField('What Do You Like?', validators=[InputRequired()])
    interests = StringField('What are your Interests?', validators=[InputRequired()])
    