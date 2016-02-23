from .db import Utterance, Dialog, Role


def predict_actions(dialog: Dialog, role:Role, turn=-1):
    if turn == -1:
        # FIXME dynamically find out next_turn based on db 
        next_turn = 1
    # FIXME predict actions
    actions = [
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored1', dialog),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored2', dialog),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored3', dialog),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored4', dialog),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored5', dialog),
        ]
    return actions


class UserModel(object):
    pass
