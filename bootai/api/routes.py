import json
from os import path
from flask import request, Response, current_app, Blueprint, session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio
from ..db import record_action_selection


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/dialog/new', methods=['GET'])
def dialog_new():
    return Response(json.dumps({'TODO':'FIXME'}), mimetype='application/json', headers={'Cache-Control': 'no-cache'})



def get_roledialog_key(dialog_id=None, role=None):
    if not dialog_id:
        dialog_id = session['dialog']
    if not role:
        role = session['role']
    return '%s%s' % (dialog_id, role) 

def get_userdialog_key(dialog_id=None, nick=None):
    if not dialog_id:
        dialog_id = session['dialog']
    if not nick:
        nick = session['nick']
    return  '%s%s' % (dialog_id, nick)

def get_dialog_key(dialog_id=None):
    if not dialog_id:
        dialog_id = session['dialog']
    return dialog_id


@socketio.on('new_action', namespace='/api')
def new_action(msg):
    role_room = get_roledialog_key()

    emit('messages', 'New action was suggested. Please, condsider it as alternative for your choice')
    print('TODO reset timer and postpone timeout')
    print('validate msg', msg)
    emit('new_action', msg, room=role_room())


@socketio.on('proposed_action', namespace='/api')
def proposed_action(msg):
    timeout_select, timeout_turn, user_messages = record_action_selection(msg)
    for msg in messages:
        emit('messages', msg, room=get_userdialog_key())
    if timeout_select:
        emit('timeout_select','',room=get_roledialog_key())
    if timeout_turn:
        emit('timeout_turn', '', room=get_roledialog_key())


@socketio.on('join_dialog', namespace='/api')
def join_dialog(msg):
    join_room(get_dialog_key())
    join_room(get_roledialog_key())
    join_room(get_userdialog_key())
    players_live = 666  # todo use the db
    emit('messages', 
            {'style':'info', 'text': 'Welcome %s, number players online in this dialog: %d.' % (session['nick'], players_live)}, 
            room=get_dialog_key()) 
    emit('messages', 
            {'sytle':'info', 'text': 'Your, role is %s' % session['role']}, 
            room=get_userdialog_key()) 


@socketio.on('leave', namespace='/api')
def leave(msg):
    leave_room(get_dialog_key())
    leave_room(get_roledialog_key())
    leave_room(get_userdialog_key())
    emit('messages', {'msg': session.get('name') + ' has left the room.'}, room=get_dialog_key())


def notify_role(dialog_id, role, msg, **kwargs):
    assert role in ['assistant', 'role']
    emit('messages', msg, room=get_roledialog_key(**kwargs))


def notifly_user(dialog_id, user, msg, **kwargs):
    emit('messages', msg, room=get_userdialog_key(**kwargs))


def send_history(history, **kwargs):
    emit('history', history, room=get_dialog_key(**kwargs))


def send_user_actions(actions, **kwargs):
    emit('actions', actions, room=get_dialog_key(role='user', **kwargs))


def send_assistant_actions(actions, **kwargs):
    emit('actions', actions, room=get_dialog_key(role='user', **kwargs))


def send_user_stats():
    user_room = get_userdialog_key()
    emit('stats', {'correct': 1, 'created': 2, 'errors': 3}, room=user_room)


@api.route('/messages/dialog/<dialog_id>/user/<user_id>/turn/<int:turn_id>', methods=['GET'])
def user_message(dialog_id, user_id, turn_id):
    messages = []
    try:
        import random
        messages = [{"style": "success", "id": 1, "text": "Great! You and two other people agreed to choose action %fd." % random.random()}]
        # raise Exception('todo fix all the remaining parts')
    except Exception as e:
        current_app.logger.error('Invalid request: %s', e)
        current_app.logger.exception(e)
        messages.append({'style': 'danger', 'text': 'Server error: "%s"' % e})
    current_app.logger.info("API: send messages[%s, %s] to %s: %s",  dialog_id, turn_id, user_id, messages)
    return Response(json.dumps(messages), mimetype='application/json', headers={'Cache-Control': 'no-cache'})


@api.route('/dialog/valid/<dialog_id>/user/<user_id>')
def dialog_valid_for_user(dialog_id, user_id):
    ok = True
    errors = 'MADE UP ERORRS'
    if ok:
        return Response(
            json.dumps(
                {"msg": "User %d passed the criteria for dialog" % (user_id, dialog_id), 
                'status': 200}), 
            mimetype='application/json', headers={'Cache-Control': 'no-cache'})
    else:
        return Response(
            json.dumps(
                {"msg": "User %d passed the criteria for dialog" % (user_id, dialog_id), 
                'status': 404}), 
            mimetype='application/json', headers={'Cache-Control': 'no-cache'})



@api.route('/dialog/reward_code/<dialog_id>/user/<user_id>')
def reimbursed_task(dialog_id, user_id):
    if reimbursed:
        code = 410
        response = Response(
            json.dumps(
                {"msg": "The task for (dialog: %s, user: %s) was already reimbursed!" % (dialog_id, user_id), 
                'status': code}), 
            mimetype='application/json', headers={'Cache-Control': 'no-cache'})
        response.status_code = code
    else:
        response = validate_task(dialog_id, user_id)
    return response


@api.route('/dialog/db/dstc2')
def dialog_db():
    dstc2 = path.abspath(path.join(path.dirname(__file__), '../../data/db/data.dstc2.db.json'))
    return Response(json.load(open(dstc2)), mimetype='application/json')
