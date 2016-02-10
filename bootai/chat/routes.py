from flask import render_template, current_app, session, redirect, url_for, Blueprint, request, flash, abort
from .forms import LoginForm, AssignForm
from bootai import db, login_manager
from ..db import User
from flask.ext.login import login_required, login_user, current_user, logout_user, confirm_login, login_fresh


chat = Blueprint('chat', __name__)


def _redirect_to_role(role_id):
    flash('You are logged as %s. You cannot change roles' % role_id, 'error')
    return redirect(url_for('chat.%s' % role_id))


@chat.route('/assistant')
@login_required
def assistant():
    current_app.logger.info("Rendering assistant view")
    dialog_id = session.get('dialog', None)
    role_id = session.get('role', None)
    if dialog_id and role_id:
        assert role_id in ['assistant', 'user']
        if  role_id == 'user':
            return _redirect_to_role(role_id)
        return render_template('action-selection.html', dialog_id=dialog_id, role=role_id, author=current_user.nick)
    else:
        return redirect(url_for('chat.assign'))


@chat.route('/user')
@login_required
def user():
    # FIXME change it for user, too similar to assistant
    current_app.logger.info("Rendering user view")
    dialog_id = session.get('dialog', None)
    role_id = session.get('role', None)
    if dialog_id and role_id:
        assert role_id in ['assistant', 'user']
        if  role_id == 'assistant':
            return _redirect_to_role(role_id)
        return render_template('action-selection.html', dialog_id=dialog_id, role=role_id, author=current_user.nick)
    else:
        return redirect(url_for('chat.assign'))


@chat.route('/')
def index():
    return render_template('index.html')


@chat.route('/logout')
def logout():
    logout_user()
    flash('You have been succesfully logout')
    return redirect(url_for('chat.login'))


@chat.route('/assign', methods=['GET', 'POST'])
@login_required
def assign():
    current_app.logger.info('Assign view with session: %s' % session)
    form = AssignForm()
    if request.method == 'GET':
        if 'role' in session and 'dialog' in session:
            current_app.logger.info('Flashing errors') 
            flash('You have a session already assigned. If you create a new one you cannot finish the current one!', 'error')
        return render_template('assign.html', form=form)
    elif form.validate_on_submit():
        current_app.logger.info('Assigned form validated')
        role, session['dialog'] = db.assign_role_dialog()
        session['role'] = role
        flash(('You have been assigned role %s' % role, 'warning'))
        if role == 'user' or role =='assistant':
            return redirect(url_for('chat.%s' % role))
        else:
            raise RuntimeError('Unknow role: %s' % role)
    else:
       return render_template('assign.html', form=form)
    # TODO ensure that assign can be POSTed from AssignForm on this page




@chat.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info("Login view")
    form = LoginForm()
    if form.validate_on_submit():
        if login_user(User(form.name.data), remember=True):
            flash('Logged in succesfully!', 'success')

            next_red = request.args.get('next')
            # FIXME not secure, todo implement next_is_valid
            # if not next_is_valid(next_red):
            #     return abort(400)
            return redirect(next_red or url_for('chat.assign'))
        else:
            flash('Login failed, wrong creditials')
            return redirect(url_for('chat.login'))
    return render_template('login.html', form=form)

