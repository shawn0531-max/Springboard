"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connecting to DB"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = 'users'

    def __repr__(self):
        """Show user info"""
        u = self
        return f"<User {u.f_name} {u.l_name} {u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)

    f_name = db.Column(db.String(25),
                       nullable = False)
    
    l_name = db.Column(db.String(25),
                       nullable = False)
    
    image_url = db.Column(db.String(),
                          nullable = False,
                          default = ('https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png'))

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """User Posts"""

    __tablename__= 'posts'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)

    title = db.Column(db.String(25),
                      nullable = False)

    content = db.Column(db.String(),
                        nullable = False)

    created_at = db.Column(db.DateTime,
                            nullable = False, 
                            default = datetime.datetime.now)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                            nullable = False)


class Tag(db.Model):
    """Tags for posts"""

    __tablename__= 'tags'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True,
                    nullable = False)

    name = db.Column(db.String(25),
                    nullable = False)

    posts = db.relationship('Post', secondary="posts_tags", cascade="all,delete", backref="tags" )


class PostTag(db.Model):
    """Relational table of post ids and tag ids"""

    __tablename__= 'posts_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    
    tag_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key = True)