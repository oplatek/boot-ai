#!/usr/bin/env python
# -*- coding: utf-8 -*-
from heapq import heappop, heappush
from enum import Enum
from collections import Counter
import json
from os.path import isdir
import uuid
import random
import time
import datetime
from flask.ext.login import UserMixin
import logging
import eventlet
eventlet.monkey_patch()  # FIXME disable monkypatching
from threading import Thread, Event  # FIXME disable monkypatching


logger = logging.getLogger(__name__)

class Role(Enum):
    assistant = 1
    user = 2

    def __str__(self):
        return self.name

    def next(self):
        if self == Role.assitant:
            return Role.user
        else:
            return Role.assistant


class Response(object):
    def __init__(self, dialog_id: string, turn_to_appear: int, role: string, callback, system_winner, num_respondents=1):
        self.utt = Utterance
        self.dialog_id = dialog_id
        self.role = role
        self.turn = turn_to_appear
        self.num_respondents = num_respondents
        self._callback_f = callback
        self._system_winner = system_winner
        self.called = False
        self.alternatives = Counter()

    def __call__(self):
        self._call_back(self._system_winner)

    def _call_back(self, selected):
        if self.called:
            return RuntimeError('We respond only once once')
        else:
            self.called = True
        self._callback_f(selected)

    def elect(self):
        # We assume that the number of possile answers can be inifinite
        # but the number of respondents is small.
        n_max = self.num_respondents
        most_common = self.alternatives.most_common(2)

        valid = False
        if len(most_common) == 1:
            valid = most_common[0][1] >= (n_max / 2)
        elif len(most_common) == 2:
            to_expect = n_max - len(self.alternatives) 
            valid = most_common[0][1] > (most_common[1][1] + to_expect)

        if valid:
            return most_common[0][0]
        else:
            return None

    def add_candidate(utt: Utterance) -> None:
        self.alternatives[Utterance] += 1
        winner = self.elect() 
        if winner:
            self._call_back(winner)
        
    def __hash__(self):
        return (self.dialo_id, self.role, self.turn)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()




class PriorityQueue(object):
    def __init__(self):
        self._thread = Thread(target=self.run)
        self._thread.deamon = True

        self.new_item = Event()
        self._tasks
        self.should_run = True 
        self.pq = []
        self.entry_finder = {}

    def run_async(self):
        self._thread.start()

    def self.run(self):
        while should_run:
            if not pq:
                self.new_item.wait()
            else:
                top_time = self.pq[0][0]
                now = datetime.datetime.now()
                if now <= top_time:
                    _, response = heappop(self.pq)
                    del self.entry_finder[response]
                    if response.called:
                        logger.info('Response %s was already called %s', response)
                    else:
                        logger.info('Response %s is called from PQ', response)
                        response()
                else:
                    diff = top_time - now 
                    self.new_item.wait(diff.total_seconds())  # Blocking call

    def register(response:Response, delay_s: float) -> None:
        run_time = datetime.datetime.now() + datetime.timedelta(seconds=delay_s)
        top_changed = self.pq and run_time < self.pq[0][0]

        if response in self.entry_finder:
            raise KeyError('You cannot register the same response for second time')
        else:
            self.entry_finder[response] = run_time
            heappush(self.pq, (run_time, response))

        if top_changed:
            self.new_item.set()
        

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

        

def record_action_selection(dialog_id, role, msg):
    assert 'turn' in msg and 'text' in msg, msg
    print('TODO parse and store msg')
    print('todo setup timeouts for live session e.g. from config')
    timeout_selec, timeout_turn = True, True
    user_messages = [{"style": "info", "text": 'Turn finished, wait for reply'}]
    return timeout_select, timeout_turn, user_messages 


def action_most_voted(dialog_id, role, turn):
    return 'Faked action'

def history(dialog_id):
    print('use DialogDB to retreive dialog_id dialog')
    d = Dialog()
    return [u.__repr_json__() for  u in d.selected_history()]


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
        role = Role.assistant
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
    def __init__(self, dialog_id=None, similar_id=None, path=None):
        if dialog_id:
            self.dialog_id= dialog_id
        else:
            self.dialog_id = uuid.uuid1()

        # if two dialogs were collected based on shared history they should have identical similar_id
        if similar_id:
            self.similar_id = similar_id
        else:
            self.shared_history_id = self.dialog_id
        self.path = path
        self.selected_utts = []
        self.turn_alternatives = []

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
                    "selected": self.selected_utts,
                    "turn_alternatives": self.turn_alternatives,
                }
        print("Fix missing items in self_dict")
        return json.dumps(self_dict, cls=ComplexEncoder)

    def save(self, path=None):
        if not path:
            path = self.path
        with open(path, 'w') as w:
            json.dump(self.__repr_json__(), w)

    @property
    def selected_history(self):
        return self.selected_utts

    @property
    def last_turn_selected(self) -> int:
        return len(self.selected_utts)

    @property
    def last_turn_finished(self):
        diff = len(self.turn_alternative) - len(self.selected_utts)
        assert 0 <=  diff <= 1, '%d' % diff
        return diff == 0

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
        self.role = role
        self.selected = selected
        self.text = text
        self._dialog = dialog

    def __hash__(self):
        return (self.dialo_id, self.role, self.turn)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


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
