# import click
import eventlet
eventlet.monkey_patch()
import logging
import os
from flask import Flask
from flask.ext.socketio import SocketIO
from flask.ext.login import LoginManager
from .db import DialogDB, User, PriorityQueue, ComplexEncoder


pq = PriorityQueue()
ddb = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'  # FIXME laod from env via click
socketio = SocketIO(app, async_mode=eventlet.__name__)
logger = logging.getLogger(__name__)

login_manager = LoginManager()
login_manager.login_view = "chat.login"



def setup_app(debug, dialog_dir, config=None):
    global ddb, app, socketio
    app.debug = debug
    app.json_encoder = ComplexEncoder

    ddb = DialogDB(dialog_dir)

    from .chat.routes import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    from .api.routes import api as api_blueprint
    app.register_blueprint(api_blueprint)

    configure_app(app, config)

    @login_manager.user_loader
    def load_user(id):
        return User(id)
    login_manager.init_app(app)
    configure_logging(app)

    pq.run_async()  # FIXME Put into App class and run it as app.run()
    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    # app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)

    # Use instance folder instead of env variables to make deployment easier.
    app.config.from_envvar('MAIL_PASSWORD', silent=(app.debug or app.testing))


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    from logging.handlers import SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # Testing
    # app.logger.info("testing info.")
    # app.logger.warn("testing warn.")
    # app.logger.error("testing error.")

    mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
                               app.config['MAIL_USERNAME'],
                               app.config['ADMINS'],
                               'O_ops... %s failed!' % app.config['PROJECT'],
                               (app.config['MAIL_USERNAME'],
                                app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(mail_handler)
