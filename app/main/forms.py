from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    pitches= TextAreaField('Write your Pitch',validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):

    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):

    comment= TextAreaField('Comment',validators=[Required()])
    submit = SubmitField('Submit')