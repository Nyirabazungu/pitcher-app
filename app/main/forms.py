from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required



class UpdateProfile(FlaskForm):

    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):

    category = StringField('Pitch category',validators=[Required()])
    pitches= TextAreaField('User pitch',validators=[Required()])
    submit = SubmitField('Submit') 
   

class CommentForm(FlaskForm):

    comment = TextAreaField('Write you comment.',validators = [Required()])
    submit = SubmitField('Submit')   