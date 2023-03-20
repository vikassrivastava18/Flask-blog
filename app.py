import os

from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
import logging
from flask_restful import Resource, Api
from flask_login import LoginManager


logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def create_app():
    app = Flask(__name__, template_folder="templates")

    if os.getenv('ENV', "development") == "production":
        app.logger.info("Currently no production config is setup.")
        raise Exception("Currently no production config is setup.")
    else:
        app.logger.info("Staring Local Development.")
        print("Staring Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    app.logger.info("App setup complete")
    return app, api
    # app.logger.info("App setup complete")


login_manager = LoginManager()
app, api = create_app()
app.static_folder = 'static'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Import all the controllers so they are loaded
from application.controllers import *
from application.auth.controllers import *
# Crete all the API endpoints
from application.api import UserAPI, ArticleAPI
api.add_resource(UserAPI, "/api/user", "/api/user/<string:username>")
api.add_resource(ArticleAPI, "/api/article", "/api/article/<int:article_id>")


if __name__ == '__main__':
    # Run the Flask app
    app.run(host='127.0.0.1', port=5000)



