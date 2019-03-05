from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import  User,Comment,Pitch
from flask_login import login_required,current_user
from .forms import PitchForm,UpdateProfile,CommentForm
from .. import db,photos


# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    

    title = 'Home - Welcome to The Pitch Application'
    pitches = Pitch.get_pitches(id)

    return render_template('index.html', title = title ,pitches=pitches)

@main.route('/incubators/')
def incubators():
    
    pitches= Pitch.get_pitches()
    title = 'Home - Welcome to The best Pitches Website Online'  
    return render_template('index.html', title = title, pitches= pitches)

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
   return redirect(url_for('main.profile',uname=uname))
   
       
@main.route('/newpich',methods = ["GET","POST"])
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitches = form.pitches.data
        print(pitches)
        new_pitchs = Pitch(pitches = pitches)
        new_pitchs.save_pitches()
        return redirect(url_for('main.index'))


        db.session.add()
        db.session.commit()

    return render_template('new_pitch.html',pitch_form=form)


@main.route('/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required

def new_comment(id):
    form = CommentForm()
    comments=Comment.query.filter_by(pitch_id=id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        # user_id= form.user_id.data
        print(comment)
        new_comment = Comment(comment =comment,pitch_id=id)
        new_comment.save_comments()
        return redirect(url_for('main.index')) 
 
    return render_template('new_comment.html', comment_form= form,comments=comments) 
