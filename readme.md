# Blog-lite
## Project for my Diploma Web course


## Features

- Authentication - It is session based using Flask-Login. Users can register using a unique email and a username. The password (minimum 6 length) is hashed using werkzeug.security. Flask-Wtf is used for data validation.

- Follow - A user can follow/unfollow other users. The posts of the following users are shown in users feed.

- Posts - A user can read posts, also write/edit/delete new posts. They can upload an image for the post which is displayed in the post details page.The other users can like/comment on them. 

- Explore - The user can explore all the recent posts in the application, shown using pagination.
- API - The posts and user info could be accessesd through API.


## Tech

Dillinger uses a number of open source projects to work properly:

- Framework - Flask (Sqlite, Jinja-2, Bootstrap, Wtf)
- Authentication - Flask-Login
- Tools - Pycharm, Postman, Git


## Installation

Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
create virtualenv:  python -m venv venv
activate: source venv/bin/activate
install dependencies: pip install -r requirements.txt
Run app - python app.py
```

