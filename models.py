from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
"""Models for Blogly."""

db = SQLAlchemy()
DEFAULT_IMAGE_URL = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'

def connect_db(app):
    '''Connect to database.'''
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User.'''
    __tablename__='users'

    def __repr__(self):
        u = self
        return f'<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url={u.image_url}>'
    
    @property
    def full_name(self):
        '''Return full name'''
        return f'{self.first_name} {self.last_name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL )

    posts = db.relationship('Post', backref='user',cascade="all, delete-orphan")

class Post(db.Model):
    '''Post.'''
    __tablename__='posts'

    def __repr__(self):
        p = self
        return f'<Post id={p.id}, title={p.title}, content={p.content}, created_at={p.created_at}, user_id={p.user_id} >'

    @property
    def friendly_date(self):
        '''Returns nicer format for date'''
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
class PostTag(db.Model):
    '''PostTag.'''
    
    __tablename__='posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    '''Tag.'''
    
    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')