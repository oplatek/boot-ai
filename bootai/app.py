import logging
import click
import json
from flask import render_template, Flask, request, Response
app = Flask(__name__)


logger = logging.getLogger(__name__)

@app.route('/')
def assistant():
    return render_template('action-selection.html')


@app.route('/api/dialogue/', methods=['GET'])
def comments_handler():
    try:
        args = request.args
        logger.info("/api/dialogue args: %s", args)
        user, dialogue, turn = args['user_id'], args['dialogue_id'], 'turn_id_todo'

        print('TODO get_messages for the user and turn. Call some appropriate function')
        import random
        messages = [{"style": "success", "id": 1, "text": "Great! You and two other people agreed to choose action %fd." % random.random()}]
        logging.info("messages[%s, %s] to %s: %s",  dialogue, turn, user, messages)
        response = Response(json.dumps(messages), mimetype='application/json', headers={'Cache-Control': 'no-cache'})
        raise Exception('todo fix all the remaining parts')
    except Exception as e:
        logger.error('Invalid request: %s', e)
        logger.exception(e)
        err_msgs = [{'style': 'danger', 'text': 'Server error: "%s"' % e}]
        print('TODO add messages %s', err_msgs)
        response = Response(json.dumps(err_msgs), mimetype='application/json', headers={'Cache-Control': 'no-cache'})
    return response


# TODO switch to github version of flask to use click argument parsing
@click.command()
@click.option('--level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING','ERROR']))
def main(level):
    logging.basicConfig(level=getattr(logging, level))
    app.run(debug=True)

if __name__ == "__main__":
    main()

