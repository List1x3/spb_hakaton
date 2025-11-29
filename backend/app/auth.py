import flask
from database import users
from models import User


def encryption(data) -> int:
    return hash(data)


#probably frontend folder shoud be restructured
app = flask.Flask(__name__, template_folder='../../frontend', static_folder='../../frontend')
#todo
app.secret_key = 'extremely_secure'


#probably should be changed with normal home page for guests?
@app.route('/')
def home():
    return flask.redirect(flask.url_for('sign_up'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if flask.request.method == 'POST':
        created_user: User
        username = flask.request.form["username"]
        email = flask.request.form["email"]
        hashed_password = encryption(flask.request.form["password"])
        is_successful = False
        #need data base
        if len(list(filter(lambda x: x.username == username, users))) > 0:
            print('User with such username already exists')
            #need data base
        elif len(list(filter(lambda x: x.email == email, users))) > 0:
            #need ui
            print('User with such email already exists')
        else:
            created_user = User(username=username, email=email, password=hashed_password)
            #need data base
            users.append(created_user)
            is_successful = True
        if is_successful:
            flask.session["user_id"] = created_user.id
            return flask.redirect(flask.url_for('user_page'))
    return flask.render_template('reg.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if flask.request.method == 'POST':
        username = flask.request.form["username"]
        hashed_password = encryption(flask.request.form["password"])
        is_successful = False
        #need data base
        such_users = list(filter(lambda x: x.username == username, users))
        #need data base
        if len(such_users) == 1 and such_users[0].password == hashed_password:
            is_successful = True
        if is_successful:
            flask.session["user_id"] = such_users[0].id
            return flask.redirect(flask.url_for('user_page'))
        else:
            #need ui
            print("Invalid username or password")
    return flask.render_template('vhod.html')


@app.route('/user_page')
def user_page():
    user_id = flask.session.pop('user_id')
    user = list(filter(lambda x: x.id == user_id, users))[0]
    #need data base
    return flask.render_template('user.html', user=user.__dict__, avatars={123: "bob.jpg"})


if __name__ == '__main__':
    app.run(debug=True)