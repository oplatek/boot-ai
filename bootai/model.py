import .db


def predict_actions(dialog_id, role, turn=-1):
    if turn == -1:
        # FIXME dynamically find out next_turn based on db 
        next_turn = 1
    # FIXME predict actions
    predicted_actions = [
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored'),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored'),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored'),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored'),
        Utterance(next_turn, role, 'SYSTEM', 'Here the actions will be stored'),
        ]
    json_actions = [u.__repr_json__() for u in predict_actions]
    return json_actions


class UserModel(class): 
    pass


