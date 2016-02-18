#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bootai import setup_app, socketio, app
import click
import logging


logger = logging.getLogger(__name__)


# TODO switch to github version of flask to use click argument parsing
# TODO use nested commands in click
@click.command()
@click.option('--log-level', default='DEBUG', type=click.Choice(['DEBUG', 'INFO', 'WARNING','ERROR']))
@click.option('--debug/--no-debug', default=True)
@click.option('--dialog-dir', default='data/dialog', type=click.Path(exists=True))
def main(log_level, debug, dialog_dir):
    setup_app(debug, dialog_dir)
    logging.basicConfig(level=getattr(logging, log_level))
    socketio.run(app)


if __name__ == "__main__":
    main()
