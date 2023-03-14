import datetime
import pytz
from dateutil.parser import parse
from typing import Union
from db.models import Notification
from db import db_manager
import exceptions
from bot.schemas import TemporaryReminder, PermanentReminder, Bookmark


def add_reminder(user_id: int,
                 notification_type: str,
                 text: str,
                 date: str,
                 attachments: str = '',
                 frequency: int = 0) -> Union[TemporaryReminder, PermanentReminder, Bookmark]:
    """
    Adding reminder to db_manager including getting parameters.
    Returns modernized NamedTuple class which include all needful information about reminder.
    It can be temporary or permanent reminders and even bookmarks classes.
    """
    if notification_type != 'book':
        date = parse(date, fuzzy=True)
    print(date, type(date))
    reminder_add = db_manager.insert(
        {
            'user_id': user_id,
            'type': notification_type,
            'text': text,
            'time': date,
            'attachments': attachments,
            'frequency': frequency
        }
    )
    print(reminder_add)
    ret = _recognize_category(id=reminder_add.notification_id, title=text, date=date, category=notification_type, frequency=frequency)
    return ret


def _recognize_category(id: int,
                        title: str,
                        date: str,
                        category: str,
                        frequency: int = 0,
                        is_done: bool = False) -> Union[TemporaryReminder, PermanentReminder, Bookmark]:
    if category == 'temp':
        return TemporaryReminder(id=id, title=title, type=category, date=date, is_done=is_done)
    elif category == 'perm':
        return PermanentReminder(id=id, title=title, type=category, date=date, frequency=frequency, is_done=is_done)
    else:
        return Bookmark(id=id, title=title, type=category, is_done=is_done)


def get_all_reminders() -> list:
    """
    Returns list of all reminders from database.
    """
    notifications = Notification.select().order_by(Notification.time.asc()).dicts().execute()
    return notifications


def get_permanent_reminders() -> list:
    """
    Returns list of permanent reminders from db_manager.
    """
    notifications = Notification.select().where(Notification.notification_type == 'perm').order_by(Notification.time.asc()).dicts().execute()
    return notifications


def get_temporary_reminders() -> list:
    """
    Returns list of temporary reminders from db_manager.
    """
    notifications = Notification.select().where(Notification.notification_type == 'temp').order_by(Notification.time.asc()).dicts().execute()
    return notifications


def get_bookmarks() -> list:
    """
    Returns list of bookmarks from db_manager.
    """
    notifications = Notification.select().where(Notification.notification_type == 'book').order_by(Notification.time.asc()).dicts().execute()
    return notifications


def delete_done_reminders() -> str:
    """
    Returns message with successful cleaning db_manager by 'is_done' parameter.
    """
    db_manager.clean_done_tasks()
    return 'done reminders were cleaned'


def delete_reminder(row_id) -> object:
    """
    Returns reminder which was deleted by user.
    """
    try:
        id, title, category, date, is_done, frequency = db_manager.delete_by_id(row_id)
    except exceptions.NotConsistIndb_manager as e:
        return str(e)
    return _recognize_category(id=id, title=title, date=date, category=category, frequency=frequency, is_done=is_done)


def done_reminder(row_id) -> object:
    """
    Returns reminder which 'is_done' parameter was marked as True by user.
    """
    try:
        id, title, category, date, is_done, frequency = db_manager.mark_done(row_id)
    except exceptions.NotConsistIndb_manager as e:
        return str(e)
    return _recognize_category(id=id, title=title, date=date, category=category, frequency=frequency, is_done=is_done)


# def _get_now_formatted() -> str:
#     """
#     Returns data on str type
#     """
#     return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """
    Returns datetime with Moscow timezone.
    """
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


# def _parse_message(message) -> TemporaryReminder:
#     # deprecated
#     data = message.split('.')
#     frequency = 1
#     try:
#         type = data[0]
#         title = data[1]
#         date = parse(data[2], fuzzy=True)
#         if type == 'perm':
#             frequency = data[3]
#     except IndexError:
#         raise exceptions.NotCorrectMessage("can't parse this message")

#     if type == 'temp':
#         return TemporaryReminder(title=title, date=date, type=type, is_done=False)
#     elif type == 'perm':
#         return PermanentReminder(title=title, date=date, type=type, frequency=frequency, is_done=False)
#     elif type == 'book':
#         return Bookmark(title=title, type=type, is_done=False)
#     else:
#         raise exceptions.NotCorrectMessage("not correct category")
