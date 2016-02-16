import json
from os import path
from flask import request, Response, current_app, Blueprint, session
from flask.ext.socketio import emit, join_room, leave_room
from .. import socketio 
model as mdl


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
    timeout_select, timeout_turn, user_messages = db.record_action_selection(msg)
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
    dialog_id, role = session['dialog_id'], session['role']
    send_history(db.history(dialog_id))
    send_actions(dialog_id, role)


@socketio.on('leave', namespace='/api')
def leave(msg):
    leave_room(get_dialog_key())
    leave_room(get_roledialog_key())
    leave_room(get_userdialog_key())
    emit('messages', {'msg': session.get('name') + ' has left the room.'}, room=get_dialog_key())


def notify_role(role: Role, msg: string, **kwargs) -> None:
    emit('messages', msg, room=get_roledialog_key(role=role, **kwargs))


def notify_user(msg, **kwargs):
    emit('messages', msg, room=get_userdialog_key(**kwargs))


def send_history(history, **kwargs):
    emit('history', history, room=get_dialog_key(**kwargs))


def send_actions(role, dialog_id, **kwargs):

    class Callback(object):
        def __init__(self, dialog_id, role):
            self.dialog = DialogDB.get_dialog(dialo_id)
            self.role = role
            self.proposed_actions = mdl.predict_actions(dialog_id, role)

        def __call__(self, selected:Utterance)->None:
            if self.proposed_actions:
                self.dialog.turn_alternatives.append(self.proposed_actions)  # FIXME not api
                self.dialog.selecte_utts.append(selected)
                self.dialog.save() 
                logger.info('Callback was called with selected action %s', selected)
                notify_role(self.role, 'Turn finished', dialog_id=self.dialog.dialo_id)
                send_history(json.dumps(self.dialog.selected_history, cls=ComplexEncodera))

                next_role = role.next()
                send_actions(next_role, dialog_id)
            else:
                logger.warn("Model for role %s in dialog %s generated no proposed actions", self.role, self.dialog.dialog_id)

        def register_response(self):
            # TODO we suppose that proposed_action[0] is the best
            r = Response(self.dialog.dialog_id, 
                    self.dialog.last_turn_finished + 1, self.role, 
                    self, 
                    self.proposed_actions[0])
            pq.register(r)

    cb = Callback(dialog_id, role)
    cb.register_response()

    emit('actions', cb.proposed_actions, room=get_dialog_key(role=role, **kwargs))


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
