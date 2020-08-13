"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import flask_sqlalchemy
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def users():
    user_list = User.query.all()
    return render_template('userlist.html', user_list=user_list)

@app.route('/users/new')
def user_info():
    return render_template('new_user.html')

@app.route('/create_user', methods=["POST"])
def create_user():
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    image_url = request.form['image_url']

    user = User(f_name=f_name, l_name=l_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    user = User.query.get(user_id)
    
    posts = Post.query.filter((Post.user_id == user_id))
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_details(user_id):
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/edit_user_<int:user_id>', methods=['POST'])
def change_info(user_id):
    f_name = request.form['f_name']
    l_name = request.form['l_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)

    user.f_name = f_name
    user.l_name = l_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')

@app.route('/delete_<int:user_id>')
def delete_user(user_id):
    
    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):

    user = User.query.get(user_id)

    tags = Tag.query.all()

    return render_template('new_post.html', user=user, tags=tags)

@app.route('/create_post_<int:user_id>', methods=['POST'])
def create_post(user_id):

    content = request.form['post_area']
    title = request.form['title']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get(post_id)
    u_id = post.user_id
    user = User.query.get(u_id)

    tags = post.tags

    return render_template('post_detail.html', user=user, post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):

    post = Post.query.get(post_id)

    tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/edit_post_<int:post_id>', methods=["POST"])
def change_post(post_id):

    content = request.form['edit_area']
    title = request.form['title']

    post = Post.query.get(post_id)

    post.content = content
    post.title = title

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):

    post = Post.query.get(post_id)
    u_id = post.user_id
    
    Post.query.filter_by(id = post_id).delete()

    db.session.commit()

    return redirect(f'/users/{u_id}')

@app.route('/tags')
def tag_list():

    tag_list = Tag.query.all()

    return render_template('tag_list.html', tags=tag_list)

@app.route('/tags/new')
def make_tag():

    return render_template('new_tag.html')

@app.route('/create_tag', methods=["POST"])
def create_tag():
    

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_info(tag_id):

    tag = Tag.query.get(tag_id)


    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tag_edit(tag_id):
    
    tag = Tag.query.get(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/edit_tag_<int:tag_id>', methods=["POST"])
def change_tag(tag_id):

    new_tag = request.form['tag_edit']

    tag = Tag.query.get(tag_id)

    tag.name = new_tag

    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):

    Tag.query.filter_by(id=tag_id).delete()

    db.session.commit()

    return redirect('/tags')