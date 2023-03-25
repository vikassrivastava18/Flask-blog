import flask
from flask import current_app as app, url_for, request, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import redirect
from .forms import LoginForm, RegistrationForm, RegistrationEditForm
from application.models import User, Follower
from application.database import db


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if request.method == 'GET':
        return flask.render_template('login.html', form=form)

    else:
        if form.validate_on_submit():

            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                flask.flash('Wrong credentials!')
                return redirect(url_for('login'))
            login_user(user)

            flask.flash('Logged in successfully.')
            return redirect(url_for('articles'))

        # return flask.redirect(next or flask.url_for('login'))
        return flask.render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('registration.html', title='Register', form=form)
    else:

        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            # Follow oneself to see one's own posts
            follow = Follower(follower_id=user.user_id, followed_id=user.user_id)
            db.session.add(follow)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))

        return render_template('registration.html', title='Register', form=form)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationEditForm()
    if request.method == 'GET':
        return render_template('profile_edit.html', title='Register', form=form, user=current_user)
    else:
        if form.validate_on_submit():
            user = current_user
            user.email = form.email.data
            user.username = form.username.data
            db.session.add(user)
            db.session.commit()

            flash('Profile changed successfully!')
    return render_template('profile_edit.html', title='Register', form=form, user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully, thanks for visiting')
    return redirect(url_for('home'))
