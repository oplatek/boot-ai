# import click
from flask import Flask
from flask.ext.socketio import SocketIO
from .db import DialogDB


socketio = SocketIO()
db = None


def create_app(debug, dialog_dir):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    db = DialogDB(dialog_dir)

    from .chat.routes import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    from .api.routes import api as api_blueprint
    app.register_blueprint(api_blueprint)

    socketio.init_app(app)


    @app.route('/d')
    def index():
        return 'debug'

    return app
