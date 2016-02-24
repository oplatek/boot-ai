from .db import Utterance, Dialog, Role


def predict_actions(dialog: Dialog, role:Role, turn=-1):
    next_turn = len(dialog.selected_utts)
    # FIXME predict actions
    actions = [
        Utterance(next_turn, role, str(role), 'Here the actions will be stored1', dialog),
        Utterance(next_turn, role, str(role), 'Here the actions will be stored2', dialog),
        Utterance(next_turn, role, str(role), 'Here the actions will be stored3', dialog),
        Utterance(next_turn, role, str(role), 'Here the actions will be stored4', dialog),
        Utterance(next_turn, role, str(role), 'Here the actions will be stored5', dialog),
        ]
    return actions


class UserModel(object):
    pass
