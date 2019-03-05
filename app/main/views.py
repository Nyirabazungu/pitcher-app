from flask import render_template,request,redirect,url_for,abort,request
from . import main
from ..models import  User,Pitch,Comment
from flask_login import login_required, current_user
from .forms import PitchForm,CommentForm,UpdateProfile
from .. import db,photos


# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to The Pitches Application'
    pitches = Pitch.get_pitches(id)
    

    return render_template('index.html', title = title, pitches=pitches)


@main.route('/user/<uname>')

def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

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
        db.session.Updatecommit()

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
   return redirect(url_for('main.update_profile',uname=uname))

@main.route('/pitch/new', methods=['GET', 'POST'])
@login_required

def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = form.pitch.data
        print(pitch)
        new_pitch = Pitch(pitch=pitch, user_id=current_user.id)
        new_pitch.save_pitches()
        return redirect(url_for('main.index'))


        # db.session.add(new_pitch)
        # db.session.commit()

    return render_template('new_pitch.html', pitch_form= form)

@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required

def new_comment(id):
    form = CommentForm()
    comments=Comment.query.filter_by(pitch_id=id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        print(comment)
        new_comment = Comment(comment=comment,pitch_id=id,user_id=current_user.id)
        new_comment.save_comments()
        return redirect(url_for('main.index'))
    
    return render_template('new_comment.html', comment_form= form,comments=comments)     




