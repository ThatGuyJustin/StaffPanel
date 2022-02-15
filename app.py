from flask import Flask, g, session
import os; os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import yaml
from yaml import load

from database import core_protect, litebans

from api.user import User
from api.auth import auth
from api.api import api

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(api)


@app.route('/ping')
def hello_world():
    return 'Pong!'


if __name__ == '__main__':
    app.run()


@app.before_first_request
def before_first_request():
    with open('config.yaml', 'r') as f:
        data = load(f, Loader=yaml.UnsafeLoader)

    app.config.update(data['web'])
    app.secret_key = data['web']['SECRET_KEY']
    app.config['token'] = data.get('token')

    litebans.connect()
    core_protect.connect()


@app.before_request
def check_auth():
    g.user = None

    if 'user' in session:
        g.user = User(session['user']['id'], session['user'])


@app.after_request
def save_auth(response):
    if g.user and 'user' not in session:
        session['user'] = g.user.to_dict()
    elif not g.user and 'user' in session:
        del session['user']

    print(session)

    return response


@app.context_processor
def inject_data():
    return dict(
        user=g.user,
    )
