from flask import render_template, current_app, session, redirect, url_for, Blueprint
from .forms import LoginForm
from bootai import db


chat = Blueprint('chat', __name__)

@chat.route('/assist')
def assistant():
    current_app.logger.info("Rendering assistant view")
    dialog_id = session.get('dialog', None)
    role_id = session.get('role', None)
    author = session.get('author', None)
    if dialog_id and role_id and author:
        assert role_id == 'assistant', 'role_id == %s' % role_id
        current_app.logger.warn("User was logged of. Redirecting to login")
        current_app.logger.info("dialog was logged of. Redirecting to login")
        return render_template('action-selection.html', dialog_id=dialog_id, role=role, author=author)
    else:
        redirect(url_for('login'))


@chat.route('/user')
def user():
    # FIXME change it for user, too similar to assistant
    current_app.logger.info("Rendering assistant view")
    dialog_id = session.get('dialog', None)
    role_id = session.get('role', None)
    author = session.get('author', None)
    if dialog_id and role_id and author:
        assert role_id == 'user', 'role_id == %s' % role_id
        current_app.logger.warn("User was logged of. Redirecting to login")
        current_app.logger.info("dialog was logged of. Redirecting to login")
        return render_template('action-selection.html', dialog_id=dialog_id, role=role, author=author)
    else:
        redirect(url_for('chat.login'))


@chat.route('/')
def index():
    return render_template('index.html')


@chat.route('/login', methods=['GET', 'POSTS'])
def login():
    current_app.logger.info("Logging user")
    form = LoginForm()
    if form.validate_on_submit():
        session['author'] = form.name.data
        session['role'], session['dialog'] = db.assing_role_dialog()
        if session['role'] == 'user':
            return redirect(url_for('user'))
        elif session['role'] == 'assistant':
            return redirect(url_for('assistant'))
        else:
            current_app.logger.error('Unknown role %s', session['role'])
            del session['role'] 
            del session['dialog'] 
    elif request.method == 'GET':
        form.name.data = session.get('author', '')
    return render_template('login.html', form=form)

