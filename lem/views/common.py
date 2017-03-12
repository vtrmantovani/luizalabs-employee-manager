import flask
from flask import Blueprint, current_app as app, redirect, session, url_for
from flask_login import login_user, logout_user, login_required
from flask_principal import AnonymousIdentity, Identity, identity_changed, PermissionDenied

from lem.business import auth_user
from lem.forms import LoginForm

common = Blueprint('common', __name__)


@common.route('/', methods=['GET'])
@login_required
def home():
    return flask.render_template('home.html')


@common.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = auth_user(form.data['email'], form.data['password'])
        if user:
            login_user(user)

            # Tell Flask-Principal the identity changed
            identity_changed.send(app._get_current_object(),
                                  identity=Identity(user.id))

            next_action = flask.request.args.get('next')
            return flask.redirect(next_action or flask.url_for('common.home'))
        else:
            flask.flash('Credenciais inválidas', 'error')

    return flask.render_template('login/login.html', form=form)


@common.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app._get_current_object(),
                          identity=AnonymousIdentity())

    return flask.redirect(flask.url_for('common.login'))


@common.route('/forbidden', methods=['GET'])
def forbidden():
    return flask.render_template('site/forbidden.html'), 403


def internal_server_error(exception):
    if isinstance(exception, PermissionDenied):
        return redirect(url_for('common.forbidden'))
    return flask.render_template('site/internal_server_error.html'), 500


def not_found(exception):
    return flask.render_template('site/not_found.html'), 404
