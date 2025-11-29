import os

import flask

from database import db, init_db
from models import User


def encryption(data) -> str:
    return str(hash(data))


app = flask.Flask(__name__, template_folder='../../frontend', static_folder='../../frontend')
app.secret_key = os.getenv('SECRET_KEY', 'extremely_secure')
init_db(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return flask.redirect(flask.url_for('sign_up'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if flask.request.method == 'POST':
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        hashed_password = encryption(flask.request.form["password"])

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            print('User with such username already exists')
        elif existing_email:
            print('User with such email already exists')
        else:
            created_user = User(username=username, email=email, password=hashed_password)
            db.session.add(created_user)
            db.session.commit()
            flask.session["user_id"] = created_user.id
            return flask.redirect(flask.url_for('user_page'))
    return flask.render_template('reg.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if flask.request.method == 'POST':
        username = flask.request.form["username"]
        hashed_password = encryption(flask.request.form["password"])
        user = User.query.filter_by(username=username).first()
        if user and user.password == hashed_password:
            flask.session["user_id"] = user.id
            return flask.redirect(flask.url_for('user_page'))
        else:
            print("Invalid username or password")
    return flask.render_template('vhod.html')


@app.route('/user_page')
def user_page():
    user_id = flask.session.get('user_id')
    if not user_id:
        return flask.redirect(flask.url_for('sign_in'))

    user = User.query.get(user_id)
    if not user:
        flask.session.pop('user_id', None)
        return flask.redirect(flask.url_for('sign_in'))

    return flask.render_template('user.html', user=user, avatars={user.id: "bob.jpg"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
