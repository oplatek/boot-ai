from flask import render_template, current_app, session, redirect, url_for, Blueprint, request, flash, abort
from .forms import LoginForm, AssignForm
from ..db import User, Role
from .. import ddb
from flask.ext.login import login_required, login_user, current_user, logout_user


chat = Blueprint('chat', __name__)


def _redirect_to_role(role):
    flash('You are logged as %s. You cannot change roles' % role, 'error')
    return redirect(url_for('chat.%s' % role))


@chat.route('/assistant')
@login_required
def assistant():
    current_app.logger.info("Rendering assistant view")
    dialog_id = session.get('dialog', None)
    role = session.get('role', None)
    if dialog_id and role:
        if role == Role.user:
            return _redirect_to_role(role)
        else:
            return render_template('action-selection.html', dialog_id=dialog_id, role=role, author=current_user.nick)
    else:
        return redirect(url_for('chat.assign'))


@chat.route('/user')
@login_required
def user():
    # FIXME change it for user, too similar to assistant
    current_app.logger.info("Rendering user view")
    dialog_id = session.get('dialog', None)
    role = session.get('role', None)
    if dialog_id and role:
        if role == Role.assistant:
            return _redirect_to_role(role)
        else:
            return render_template('action-selection.html', dialog_id=dialog_id, role=role, author=current_user.nick)
    else:
        return redirect(url_for('chat.assign'))


@chat.route('/')
def index():
    nick = session.get('nick')
    return render_template('index.html', nick=nick)


@chat.route('/logout')
def logout():
    logout_user()
    flash('You have been successfully logout', 'success')
    return redirect(url_for('chat.login'))


@chat.route('/assign', methods=['GET', 'POST'])
@login_required
def assign():
    current_app.logger.info('Assign view with session: %s' % session)
    form = AssignForm()
    if request.method == 'GET':
        if 'role' in session and 'dialog' in session:
            role, dialog_id = session['role'], session['dialog']
            current_app.logger.info('Flashing errors')
            flash('You have a role %s and dialog already assigned. If you create a new one you cannot finish the current one!' % role, 'error')
            return render_template('assign.html', form=form, role=role, dialog_id=dialog_id)
        else:
            return render_template('assign.html', form=form, role=role, dialog_id=dialog_id)
    elif form.validate_on_submit():
        current_app.logger.info('Assigned form validated')
        role, session['dialog'] = ddb.assign_role_dialog(session['nick'])
        session['role'] = role
        flash('You have been assigned role %s' % role, 'warning')
        return redirect(url_for('chat.%s' % role))
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
            session['nick'] = form.name.data
            return redirect(next_red or url_for('chat.assign'))
        else:
            flash('Login failed, wrong creditials', 'error')
            return redirect(url_for('chat.login'))
    return render_template('login.html', form=form)

