from .extensions import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from datetime import datetime, timezone

liked_posts = db.Table(
    'liked_posts',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    created_posts = db.relationship('Post', backref='user', lazy='select')
    liked_posts = db.relationship('Post', secondary=liked_posts, backref='liked_users', lazy='select')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    comments = db.relationship('Comment', backref='referenced_post', lazy='select')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
