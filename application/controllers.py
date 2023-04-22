from flask import request, url_for, flash
from flask import render_template
from flask import current_app as app
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from application.database import db
from application.models import Article, User, Follower, ArticleLike

PAGINATION_COUNT = 5


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route('/feed/<username>')
@login_required
def feed(username):
    # Send the posts written by the people followed by current user
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    following_ids = [follow.followed_id for follow in \
                     Follower.query.filter_by(follower_id=user.user_id).all()]

    feed_posts = db.session.query(Article, User) \
        .join(Article, Article.author == User.user_id) \
        .filter(Article.author.in_(following_ids))\
        .order_by(Article.timestamp.desc())\
        .paginate(page, per_page=PAGINATION_COUNT)

    return render_template("articles.html", articles=feed_posts)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    follow = Follower(follower_id=current_user.user_id, followed_id=user.user_id)
    db.session.add(follow)
    db.session.commit()

    flash('Started following the user:' + user.username)
    return redirect(url_for('articles_by_author', user_name=user.username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    Follower.query.filter_by(follower_id=current_user.user_id, followed_id=user.user_id).delete()

    db.session.commit()

    flash('Stopped following the user:' + user.username)
    return redirect(url_for('articles_by_author', user_name=user.username))


@app.route('/like/<int:article_id>')
@login_required
def like(article_id):
    try:
        like = ArticleLike(article_id=article_id, user_id=current_user.user_id)
        db.session.add(like)
        db.session.commit()

    except Exception as e:
        flash('You already like the article')
    return redirect(url_for('articles_details', article_id=article_id))


@app.route('/search')
@login_required
def search():
    page = request.args.get('page', 1, type=int)
    user_query = request.args.get('search_user')
    users = User.query.filter(User.username.like('%' + user_query + '%')) \
        .paginate(page, per_page=PAGINATION_COUNT)

    return render_template("search_result.html", users=users)