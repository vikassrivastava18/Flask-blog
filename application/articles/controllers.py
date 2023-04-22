import os
import flask
from flask import current_app as app, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from application.database import db
from .forms import ArticleForm, ArticleEditForm
from application.models import Article, User, Follower, ArticleComment
from app import PAGINATION_COUNT
from application.forms import MessageForm


@app.route("/articles", methods=["GET"])
@login_required
def articles():
    page = request.args.get('page', 1, type=int)
    # articles = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page=PAGINATION_COUNT)
    articles = db.session.query(Article, User) \
        .join(Article, Article.author == User.user_id) \
        .order_by(Article.timestamp.desc()).paginate(page, per_page=PAGINATION_COUNT)
    for article in articles.items:
        print("article", article)
    return render_template("articles.html", articles=articles)


@app.route("/article-create", methods=["GET", "POST"])
@login_required
def article_create():
    form = ArticleForm()

    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(os.getcwd() + '/static/images', filename))
        article = Article(title=form.title.data, content=form.content.data, image_src=filename,
                          author=current_user.user_id)
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('articles'))

    return render_template('article_create.html', form=form)


@app.route("/article-edit/<article_id>", methods=["GET", "POST"])
@login_required
def article_edit(article_id):
    form = ArticleEditForm()
    article = Article.query.filter_by(article_id=article_id).first()
    print(article.author, current_user)
    if not article.author == current_user.user_id:
        flask.flash("Can't edit others posts!")
        return redirect(url_for('articles'))
    if form.validate_on_submit():
        f = form.image.data
        if not f:
            filename = article.image_src
        else:
            filename = secure_filename(f.filename)
            f.save(os.path.join(os.getcwd() + '/static/images', filename))
        article.title = form.title.data
        article.content = form.content.data
        article.image_src = filename
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('articles'))
    #
    return render_template('article_edit.html', form=form, article=article)


@app.route("/article-delete/<article_id>", methods=["GET", "POST"])
@login_required
def article_delete(article_id):
    article = Article.query.filter_by(article_id=article_id).first()
    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('articles_by_author', user_name=article.author))


@app.route("/articles-by/<user_name>", methods=["GET", "POST"])
@login_required
def articles_by_author(user_name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=user_name).first()

    _articles = db.session.query(Article, User) \
        .join(Article, Article.author == User.user_id)\
        .filter_by(author=user.user_id).order_by(Article.timestamp.desc())\
        .paginate(page, per_page=PAGINATION_COUNT)
    following = Follower.query.filter_by(follower_id=current_user.user_id, followed_id=user.user_id).first()

    if following:
        return render_template("articles_by_author.html", articles=_articles, username=user_name, following=True)
    else:
        return render_template("articles_by_author.html", articles=_articles, username=user_name, following=False)


# TODO -> Bad codes, make changes.
@app.route("/article-details/<article_id>", methods=["GET", "POST"])
@login_required
def articles_details(article_id):
    form = MessageForm()
    if request.method == 'GET':
        article = db.session.query(Article, User)\
                .join(Article, Article.author == User.user_id)\
                .filter(Article.article_id == article_id).first()
        messages = db.session.query(ArticleComment, User)\
            .join(ArticleComment, ArticleComment.user_id == User.user_id)\
            .filter(ArticleComment.article_id == article_id)\
            .all()

        return render_template("article_detail.html", article=article, messages=messages, form=form)
    else:
        if form.validate_on_submit():
            comment = ArticleComment(article_id=article_id, user_id=current_user.user_id,
                                     comment=form.comment.data)
            db.session.add(comment)
            db.session.commit()
            flask.flash('Comment posted successfully')
            return redirect(url_for('articles_details', article_id=article_id))