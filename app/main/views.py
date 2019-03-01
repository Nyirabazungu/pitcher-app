from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PitchForm,UpdateProfile
from .. import db
from ..models import User,Pitch,Comment
from flask_login import login_required,current_user
from .. import db,photos
import markdown2  


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to The best pitches Website Online'

    return render_template('index.html', title = title )


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = current_user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

    return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)    

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()
   
    if form.validate_on_submit():
        # title = form.title.data
       pitches_description  = form.pitches_description .data
       category = form.category.data

        # Updateddescription instance
       new_pitch = Pitch(pitches_description = pitches_description ,category= category ,user_id = current_user.id)

        # savedescription method
       new_pitch.save_pitch()
       return redirect(url_for('.index',pitches_description = pitches_description ))

       return render_template('new_pitch.html', pitch_form = form, user = current_user) 

@main.route('/pitch')
def single_pitch(id):
    pitch=pitch.query.get(id)
    if pitch is None:
        abort(404)
    format_pitch = markdown2.markdown(pitch.user_pitch,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('pitch.html',pitch = pitch,format_pitch=format_pitch)