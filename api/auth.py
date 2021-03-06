from flask import Blueprint, g, current_app, session, jsonify, redirect, request
from requests_oauthlib import OAuth2Session

from api.user import User, does_user_exist
from api.decos import authed

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


def token_updater(token):
    pass


def make_discord_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=current_app.config['discord']['CLIENT_ID'],
        token=token,
        state=state,
        scope=scope,
        redirect_uri=current_app.config['discord']['REDIRECT_URI'],
        auto_refresh_kwargs={
            'client_id': current_app.config['discord']['CLIENT_ID'],
            'client_secret': current_app.config['discord']['CLIENT_SECRET'],
        },
        auto_refresh_url=current_app.config['discord']['TOKEN_URL'],
        token_updater=token_updater)


@auth.route('/logout', methods=['POST'])
@authed
def auth_logout():
    g.user = None
    return jsonify({})


@auth.route('/discord')
def auth_discord():
    discord = make_discord_session(scope=('identify',))
    auth_url, state = discord.authorization_url(current_app.config['discord']['AUTH_URL'])
    session['state'] = state
    return redirect(auth_url)


@auth.route('/discord/callback')
def auth_discord_callback():
    if request.values.get('error'):
        return request.values['error']

    if 'state' not in session:
        return 'no state', 400

    discord = make_discord_session(state=session['state'])
    token = discord.fetch_token(
        current_app.config['discord']['TOKEN_URL'],
        client_secret=current_app.config['discord']['CLIENT_SECRET'],
        authorization_response=request.url)

    discord = make_discord_session(token=token)
    data = discord.get(current_app.config['discord']['API_BASE_URL'] + '/users/@me').json()

    if not does_user_exist(data['id']):
        return 'Unknown User', 403

    user = User(data['id'], data)

    if not user.has_permission("api.login"):
        return 'You are not permitted to log in.', 403

    g.user = user

    return redirect("/", 302)


@auth.route('/@me')
@authed
def auth_me():
    return g.user.to_dict()
