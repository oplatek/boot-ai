import json
from flask import request, Response, current_app, Blueprint


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/dialog/new', methods=['GET'])
def dialog_new():
    return Response(json.dumps({'TODO':'FIXME'}), mimetype='application/json', headers={'Cache-Control': 'no-cache'})


@api.route('/messages/dialog/<dialog_id>/user/<user_id>/turn/<int:turn_id>', methods=['GET'])
def dialog_request(dialog_id, user_id, turn_id):
    try:
        args = request.args
        current_app.logger.info("/dialog args: %s", )

        print('TODO get_messages for the user and turn. Call some appropriate function')
        import random
        messages = [{"style": "success", "id": 1, "text": "Great! You and two other people agreed to choose action %fd." % random.random()}]
        current_app.info("messages[%s, %s] to %s: %s",  dialog_id, turn_id, user_id, messages)
        response = Response(json.dumps(messages), mimetype='application/json', headers={'Cache-Control': 'no-cache'})
        raise Exception('todo fix all the remaining parts')
    except Exception as e:
        current_app.logger.error('Invalid request: %s', e)
        current_app.logger.exception(e)
        err_msgs = [{'style': 'danger', 'text': 'Server error: "%s"' % e}]
        print('TODO add messages %s', err_msgs)
        response = Response(json.dumps(err_msgs), mimetype='application/json', headers={'Cache-Control': 'no-cache'})
    return response


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
