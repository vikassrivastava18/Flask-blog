from datetime import datetime

from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(128))
    articles = db.relationship("Article")

    def get_id(self):
        return (self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    image_src = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    likes = db.relationship("ArticleLike")


class Follower(db.Model):
    __tablename__ = 'follower'
    __table_args__ = (
        db.UniqueConstraint('follower_id', 'followed_id', name='unique_follower_constraint'),
    )
    follower_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True, nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True, nullable=False)


class ArticleLike(db.Model):
    __tablename__ = 'likes'
    __table_args__ = (
        db.UniqueConstraint('article_id', 'user_id', name='unique_like_constraint'),
    )
    like_id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.article_id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"))


class ArticleComment(db.Model):
    __tablename__ = 'comment'
    __table_args__ = (
        db.UniqueConstraint('article_id', 'user_id', name='unique_comment_constraint'),
    )
    comment_id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.article_id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="CASCADE"))
    comment = db.Column(db.String)


