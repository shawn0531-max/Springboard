"""Flask app for Feedback"""

from flask import Flask, request, redirect, render_template, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from models import db, connect_db, User, set_bcrypt, Feedback
from form import RegisterForm, LoginForm, LogoutForm, DeleteForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

set_bcrypt(app)
connect_db(app)
db.create_all()

@app.route('/')
def home():
    if session.get('user', default=None) is not None:
        username = session['user']
        user = User.query.get(username)
        return redirect(f'/users/{username}')
    else:
        return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()
        session['user'] = new_user.username

        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)
        
        if user:
            flash(f"Welcome back {user.username}!")
            session['user'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            flash("Username or password is invalid") 
            return redirect('/login')
    else:
        return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    form = LogoutForm()

    if form.validate_on_submit():
        flash("You have logged out")
        session.pop('user')
        return redirect('/')
    else:
        flash("Are you sure you want to log out?") 
        return render_template('logout.html', form=form)

@app.route('/users/<username>')
def users_info(username):
    if 'user' not in session:
        flash('Please sign in or register first')
        return redirect('/')
    else:
        user = User.query.get(username)
        feedback = Feedback.query.filter_by(username=username)
        return render_template('user.html', user=user, feedback=feedback)

@app.route('/users/<username>/delete', methods=['GET','POST'])
def delete_user(username):
    if session.get('user', default=None) is None:
        flash('Please login or register')
        return redirect('/')
    else:
        form = DeleteForm()
        
        if form.validate_on_submit():
            flash("Profile deleted")
            user = User.query.get(username)
            session.pop('user')
            db.session.delete(user)
            db.session.commit()
            return redirect('/')
        else:
            flash("Are you sure you want to delete your profile?")
            user = User.query.get(username)
            return render_template('delete.html', form=form, user=user)

@app.route('/users/<username>/feedback/add', methods=["GET", 'POST'])
def create_feedback(username):
    form = FeedbackForm()

    if 'user' not in session:
        flash('Please sign in or register first')
        return redirect('/')
    else:
        if form.validate_on_submit():
            flash("Feedback added")
            user = User.query.get(username)

            title = form.title.data
            content = form.content.data

            feedback = Feedback(title=title, content=content, username=username)

            db.session.add(feedback)
            db.session.commit()

            return redirect(f'/users/{user.username}')
        else:
            user = User.query.get(username)
            return render_template('feedback.html', form=form, user=user)

@app.route('/feedback/<int:f_id>/update', methods=["GET", 'POST'])
def update_feedback(f_id):
    if session.get('user', default=None) is None:
        flash('Please login or register')
        return redirect('/')
    else:
        feedback = Feedback.query.get(f_id)
        user = User.query.get(feedback.username)
        form = FeedbackForm(obj=feedback)

        if user.username != feedback.username:
            flash('You can not edit this post')
            return redirect(f'/users/{user.username}')
        else:
            if form.validate_on_submit():
                flash("Feedback updated")
                

                feedback.title = form.title.data
                feedback.content = form.content.data

                db.session.commit()

                return redirect(f'/users/{user.username}')
            else:
                return render_template('update_feed.html', form=form, user=user, feedback=feedback)

@app.route('/feedback/<int:f_id>/delete', methods=["GET", 'POST'])
def delete_feedback(f_id):
    if session.get('user', default=None) is None:
        flash('Please login or register')
        return redirect('/')
    else:
        feedback = Feedback.query.get(f_id)
        user = User.query.get(feedback.username)
        form = DeleteForm()

        if user.username != feedback.username:
            flash('You can not edit this post')
            return redirect(f'/users/{user.username}')
        else:
            if form.validate_on_submit():
                flash("Feedback deleted")
                
                db.session.delete(feedback)
                db.session.commit()

                return redirect(f'/users/{user.username}')
            else:
                flash('Are you sure you want to delete this feedback?')
                return render_template('feed_delete.html', form=form, user=user, feedback=feedback)