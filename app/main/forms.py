from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    category = StringField('Pitch category',validators=[Required()])
    pitches_destription= TextAreaField('User pitch',validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):

    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
   