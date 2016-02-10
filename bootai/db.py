#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from os.path import isdir
import uuid
import random
import time
from flask.ext.login import UserMixin
import logging


logger = logging.getLogger(__name__)


class User(UserMixin):
    def __init__(self, nick):
        # Fixme implement proper authentication. See https://flask-login.readthedocs.org/en/latest/#how-it-works.
        self.nick = nick
        logger.warn('TODO implement authentication')
        self.id = nick

    @classmethod
    def get(cls, nick):
        logging.warn('TODO check that user can be created, return None if not valid')
        return cls(nick)

        




class DialogDB(object):
    """Prototype for DialoeDB.
    TODO split to abstract API and JSON implementation
    """

    def __init__(self, path):
        assert isdir(path)

    def list_dialogs(self):
        pass

    def get_dialog(self, dialog_id):
        pass

    def assign_role_dialog(self):
        # FIXME group users together, find appropriate dialog and role
        # role = random.choice(['assistant', 'user'])
        role = 'assistant'
        dialog_id = 'dialog-%s-%04d' % (time.strftime('%y%m%d-%H-%M-%S'), random.randint(0,9999))
        return role, dialog_id


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__repr_JSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class Dialog(object):
    assist_model = None
    user_model = None
    def __init__(self, dialog_id=None, similar_id=None, turn=0):
        if dialog_id:
            self.dialog_id= dialog_id
        else:
            self.dialog_id = uuid.uuid1()

        # if two dialogs were collected basd on shared history they should have identical similar_id
        if similar_id:
            self.similar_id = similar_id
        else:
            self.shared_history_id = self.dialog_id
        self.utterances = []
        self.turn = turn

    @property
    def user_model(self):
        m = self.__class__.user_model
        assert m is not None
        return m

    @property
    def assist_model(self):
        m = self.__class__.assist_model
        assert m is not None
        return m


    @classmethod
    def from_json(cls, json_file):

        assert is_json or is_path_to_json
        dialog_dict = todo_parse
        return cls(dialog_dict)

    def __repr_json__(self):
        self_dict = {
                    "dialog_id": self.dialog_id,
                    "similar_id":  self.similar_id,
                    "utterances": self.utterances
                }
        print("Fix missing items in self_dict")
        return json.dumps(self_dict, cls=ComplexEncoder)

    def save(self, path):
        with open(path, 'w') as w:
            json.dump(self.__repr_json__(), w)

    @property
    def selected_history(self):
        pass

    @property
    def last_turn(self):
        pass

    @property
    def last_turn_finished(self):
        pass

    def assistant_suggestions(self, n=10):
        hist = self.selected_history()
        return self.assist_model.predict(hist, n) 

    def user_suggestions(self, n=10):
        hist = self.selected_history()
        return self.user_model.predict(hist, n) 


class Utterance(object):
    def __init__(self, turn, role, author, text, dialog, selected=False):
        self.turn = turn
        self.author = author 
        self.role = check_role(role)
        self.selected = selected
        self.text = text
        self._dialog = dialog
    
    @classmethod
    def check_role(role):
        assert role in ['assistant', 'user']
        return role

    def __repr_json__(self):
        self_dict = {
                "turn": self.turn,
                "author": self.author,
                "role": self.role,
                "selected": self.selected,
                "text": self.text,
                "dialog_id": self._dialog.dialog_id
                }
        return json.dumps(self_dict)
