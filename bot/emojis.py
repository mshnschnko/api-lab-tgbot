from typing import Tuple

EMOJI_DONE = '✅'
EMOJI_NOT_DONE = '❌'
EMOJI_BELL = '🔔'
EMOJI_NOTIFY = '📢'
EMOJI_PERMANENT = '🔁'
EMOJI_TEMPORARY = '🔂'
EMOJI_BOOKMARK = '📝'
EMOJI_REPEAT = '♻️'
EMOJI_BOOKMARK_2 = '📒'


def emojis_recognize(data_done: bool, data_type: str) -> Tuple[str, str]:
    # data_done = bool(data_done)
    # stick_done = EMOJI_DONE if bool(data_done) else EMOJI_NOT_DONE
    if isinstance(data_done, str):
        if data_done == 'True':
            stick_done = EMOJI_DONE
        else:
            stick_done = EMOJI_NOT_DONE
    elif isinstance(data_done, bool):
        stick_done = EMOJI_DONE if data_done else EMOJI_NOT_DONE
    else:
        stick_done = EMOJI_DONE if data_done else EMOJI_NOT_DONE
    # print(data_done, type(bool(data_done)))
    if data_type == 'perm':
        stick_type = EMOJI_PERMANENT
    elif data_type == 'temp':
        stick_type = EMOJI_TEMPORARY
    else:
        stick_type = EMOJI_BOOKMARK
    return stick_done, stick_type
