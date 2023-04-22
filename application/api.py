import os

import flask
from flask import request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from werkzeug.utils import secure_filename

from application.models import User, Article
from application.database import db

from werkzeug.security import generate_password_hash

from application.validation import NotFoundError, BusinessValidationError

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('email')
update_user_parser.add_argument('password')

resource_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
}

article_fields = {
    'article_id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'timestamp': fields.DateTime
}


class UserAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, username):
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            raise NotFoundError(status_code=404)
        return user

    @marshal_with(resource_fields)
    def put(self, username):
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return NotFoundError(status_code=404)
        args = update_user_parser.parse_args()
        print("args", args)
        user.email = args.get("email", None)
        user.password_hash = generate_password_hash(args.get("password", None))
        db.session.add(user)
        db.session.commit()
        return user

    @marshal_with(resource_fields)
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        email = args.get("email", None)
        password = args.get("password", None)
        print("password", password)
        if username is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001",
                                          error_message="username is required")

        if email is None:
            raise BusinessValidationError(status_code=400, error_code="BE1002",
                                          error_message="email is required")

        if "@" in email:
            pass
        else:
            raise BusinessValidationError(status_code=400, error_code="BE1003", error_message="Invalid email")

        user = db.session.query(User).filter((User.username == username) | (User.email == email)).first()
        if user:
            raise BusinessValidationError(status_code=400, error_code="BE1004", error_message="Duplicate user")

        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def delete(self, username):
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return NotFoundError(status_code=404)
        db.session.delete(user)
        db.session.commit()
        return 201


class ArticleAPI(Resource):
    @marshal_with(article_fields)
    def get(self, article_id):
        article = db.session.query(Article).filter(Article.article_id == article_id).first()
        if article is None:
            raise NotFoundError(status_code=404)
        return article

    @marshal_with(article_fields)
    def post(self):
        title = request.form.get("title", None)
        content = request.form.get("content", None)
        file = request.files.get('image', '')
        filename = secure_filename(file.filename)
        print("filename", filename)
        if title is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="title is required")
        if content is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="content is required")

        file.save(os.path.join(os.getcwd() + '/static/images', filename))
        article = Article(title=title, content=content, image_src='/static/images/' + filename)
        db.session.add(article)
        db.session.commit()
        return article

    @marshal_with(article_fields)
    def put(self, article_id):
        article = db.session.query(Article).filter(Article.article_id == article_id).first()
        if article is None:
            raise NotFoundError(status_code=404)
        title = request.form.get("title", None)
        content = request.form.get("content", None)
        file = request.files.get('image', '')

        if title is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="title is required")
        if content is None:
            raise BusinessValidationError(status_code=400, error_code="BE1001", error_message="content is required")
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getcwd() + '/static/images', filename))
        print("filename", filename)

        article.title = title
        article.content = content
        article.image_src = filename
        db.session.add(article)
        db.session.commit()
        return article

    def delete(self, article_id):
        article = db.session.query(Article).filter(Article.article_id == article_id).first()
        if article is None:
            return NotFoundError(status_code=404)
        db.session.delete(article)
        db.session.commit()
        return 201
