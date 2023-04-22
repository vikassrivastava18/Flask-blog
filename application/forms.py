from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class MessageForm(FlaskForm):
    comment = TextAreaField('comment', validators=[DataRequired()])
    submit = SubmitField('submit')