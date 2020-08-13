from unittest import TestCase
from app import app
from flask import redirect, session
from models import db, User, Post
import datetime

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()

        Post.query.delete()
        User.query.delete()

        user = User(f_name='Captain', l_name='Crunch', image_url='https://images-na.ssl-images-amazon.com/images/I/91zoQgd4TfL._SY355_.jpg')
        post = Post(title='Test Post', content='Testing 1,2,3 testing 1,2,3.', user_id='1')

        db.session.add(user)
        db.session.add(post)

    def test_post_list(self):
        with self.client:
            resp = self.client.get('/users/1')

            self.assertIn(b'Test Post</a></li>', resp.data)

    def test_post_details(self):
        with self.client:
            resp = self.client.get('/posts/1')

            user = User.query.get('1')
            u_id = user.id

            post = Post.query.get('1')
            pu_id = post.user_id

            self.assertIn(b'<p><i>By: Captain Crunch</i></p>', resp.data)
            self.assertEqual(1,pu_id)

    def test_post_delete(self):
        with self.client:
            resp = self.client.get('/posts/1/delete', follow_redirects=True)


            self.assertNotIn(b'<h1>Test Post</h1>', resp.data)

    def tearDown(self):
        db.session.rollback()