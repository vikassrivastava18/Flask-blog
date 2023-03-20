from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.models import User


class ArticleForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    image = FileField(validators=[FileRequired()])
    submit = SubmitField('submit')


class ArticleEditForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])
    image = FileField()
    submit = SubmitField('submit')


class MessageForm(FlaskForm):
    comment = TextAreaField('comment', validators=[DataRequired()])
    submit = SubmitField('submit')
