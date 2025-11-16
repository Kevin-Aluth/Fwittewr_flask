from .extensions import db
from flask_login import UserMixin
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import backref
from datetime import datetime, timezone

liked_posts = db.Table(
    'liked_posts',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

liked_comments = db.Table(
    'liked_comments',
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    created_posts = db.relationship('Post', backref='user', lazy='select')
    created_comments = db.relationship('Comment', backref='user', lazy='select')
    liked_posts = db.relationship('Post', secondary=liked_posts, backref='liked_users', lazy='select')
    liked_comments = db.relationship('Comment', secondary=liked_comments, backref = 'liked_users', lazy='select')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    deleted = db.Column(db.Boolean, default=False)
    
    comments = db.relationship('Comment', backref='referenced_post', lazy='select')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    deleted = db.Column(db.Boolean, default=False)

    comments = db.relationship('Comment', backref=backref('referenced_comment', remote_side=[id]), lazy='select')
    referenced_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    
    referenced_post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        CheckConstraint(
            'referenced_comment_id IS NOT NULL OR referenced_post_id IS NOT NULL',
            name='check_comment_or_post_not_null'
        ),
    )
