import json
import logging
from os import path
from flask import Response, current_app, Blueprint, session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio, ddb, pq, db, model as mdl
from ..db import Role, DialogDB, Utterance, Dialog, ComplexEncoder


api = Blueprint('api', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)



@api.route('/dialog/new', methods=['GET'])
def dialog_new():
    return Response(json.dumps({'TODO': 'FIXME'}), mimetype='application/json', headers={'Cache-Control': 'no-cache'})


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
    return '%s%s' % (dialog_id, nick)


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
    timeout_select, timeout_turn, user_messages = ddb.record_action_selection(msg)
    for msg in user_messages:
        emit('messages', msg, room=get_userdialog_key())
    if timeout_select:
        emit('timeout_select', '', room=get_roledialog_key())
    if timeout_turn:
        emit('timeout_turn', '', room=get_roledialog_key())


@socketio.on('join_dialog', namespace='/api')
def join_dialog(msg):
    logger.info('join_dialog: %s', msg)
    join_room(get_dialog_key())
    join_room(get_roledialog_key())
    join_room(get_userdialog_key())
    players_live = 666  # todo use the db
    emit('messages', 
            {'style': 'info', 'text': 'Welcome %s, number players online in this dialog: %d.' % (session['nick'], players_live)}, 
            room=get_dialog_key())
    emit('messages', 
            {'sytle': 'info', 'text': 'Your, role is %s' % session['role']}, 
            room=get_userdialog_key()) 
    dialog, role = ddb.get_dialog(session['dialog']), getattr(Role, session['role'])
    send_history(dialog.selected_history, dialog.dialog_id)
    Callback(dialog, role)(Utterance.get_dummy_start(dialog))


@socketio.on('leave', namespace='/api')
def leave(msg):
    leave_room(get_dialog_key())
    leave_room(get_roledialog_key())
    leave_room(get_userdialog_key())
    emit('messages', {'msg': session.get('name') + ' has left the room.'}, room=get_dialog_key())


def notify_role(role: Role, msg: str, **kwargs) -> None:
    room = get_roledialog_key(role=role, **kwargs)
    emit('messages', msg, room=room)


def notify_user(msg, **kwargs):
    emit('messages', msg, room=get_userdialog_key(**kwargs))


def send_history(history, dialog_id, namespace='/api'):
    logger.debug('history: %s', history if len(history) < 3 else history[0:2])
    # history_msg = json.dumps([{'text': u.text, 'author': u.author} for u in history])
    history_msg = [{'text': u.text, 'author': u.author} for u in history]
    socketio.emit('history', history_msg, room=get_dialog_key(dialog_id=dialog_id), namespace='/api')


class Callback(object):
    def __init__(self, dialog: Dialog, role: Role, timeout_s=2):
        self.dialog = dialog
        self.role = role
        self.proposed_actions = mdl.predict_actions(self.dialog, self.role)
        self.timeout_s = timeout_s

    def __call__(self, selected:Utterance)->None:
        if self.proposed_actions:
            self.dialog.turn_alternatives.append(self.proposed_actions)  # FIXME not api
            self.dialog.selected_utts.append(selected)
            self.dialog.save() 
            logger.info('Callback was called with selected action %s', selected)
            # see notify_role
            dialog_id = self.dialog.dialog_id
            socketio.emit('messages', {'text': 'Turn %d finished' % self.dialog.last_turn_selected, 'style': 'danger'}, room=get_roledialog_key(role=self.role, dialog_id=dialog_id), namespace='/api')
            # see send_history

            send_history(
                    self.dialog.selected_history,
                    dialog_id=dialog_id)
            socketio.emit('actions', json.dumps(self.proposed_actions, cls=ComplexEncoder),
                    room=get_roledialog_key(role=self.role, dialog_id=self.dialog.dialog_id), 
                    namespace='/api')

            cb_next = Callback(self.dialog, self.role.next(), timeout_s=self.timeout_s)
            cb_next.register_response()
        else:
            logger.warn("Model for role %s in dialog %s generated no proposed actions", self.role, self.dialog.dialog_id)

    def register_response(self):
        # TODO we suppose that proposed_action[0] is the best
        r = db.Response(self.dialog.dialog_id, 
                self.dialog.last_turn_finished + 1, self.role, 
                self, 
                self.proposed_actions[0])
        pq.register(r, self.timeout_s)


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
    current_app.logger.info("API: send messages[%s, %s] to %s: %s", dialog_id, turn_id, user_id, messages)
    return Response(json.dumps(messages), mimetype='application/json', headers={'Cache-Control': 'no-cache'})


@api.route('/dialog/valid/<dialog_id>/user/<user_id>')
def dialog_valid_for_user(dialog_id, user_id):
    ok = True
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


def validate_task(dialog_id, user_id):
    return {"msg": "Your dialog as always is valid", "status": 200}


@api.route('/dialog/reward_code/<dialog_id>/user/<user_id>')
def reimbursed_task(dialog_id, user_id):
    reimbursed = 'you have been already reimbursed'
    if reimbursed:
        code = 410
        response = Response(
            json.dumps(
                {"msg": "The task for (dialog: %s, user: %s) was already reimbursed!" % (dialog_id, user_id), 
                'status': code}), 
            mimetype='application/json', headers={'Cache-Control': 'no-cache'})
        response.status_code = code
    else:
        anw = validate_task(dialog_id, user_id)
        response = Response(
            json.dumps(anw),
            mimetype='application/json', headers={'Cache-Control': 'no-cache'})
    return response


@api.route('/dialog/db/dstc2')
def dialog_db():
    dstc2 = path.abspath(path.join(path.dirname(__file__), '../../data/db/data.dstc2.db.json'))
    return Response(json.load(open(dstc2)), mimetype='application/json')
