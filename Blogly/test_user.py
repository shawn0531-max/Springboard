from unittest import TestCase
from app import app
from flask import redirect, session
from models import db, User

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()

        User.query.delete()

        user = User(f_name='Captain', l_name='Crunch', image_url='https://images-na.ssl-images-amazon.com/images/I/91zoQgd4TfL._SY355_.jpg')

        db.session.add(user)
    
        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()

    def test_userlist(self):
        with self.client:
            resp = self.client.get('/users')
            self.assertIn(b'Crunch</a></li>', resp.data)

    def test_create_user(self):
        with self.client:
            d = {"f_name":"test", "l_name":"person", "image_url":"https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"}
            resp = self.client.post('/create_user', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('person</a></li>', html)

    def test_show_details(self):
        with self.client:
            resp = self.client.get('/users/1')
            
            self.assertIn(b'<h1>Captain Crunch</h1>', resp.data)

    def test_edit_details(self):
        with self.client:
            resp = self.client.get('/users/1/edit')

            self.assertIn(b'First Name</label>', resp.data)
            self.assertIn(b'Last Name</label>', resp.data)
            self.assertIn(b'URL</label>', resp.data)