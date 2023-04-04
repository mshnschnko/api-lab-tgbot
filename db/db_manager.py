from typing import Dict, List, Tuple
from datetime import timedelta
from dateutil.parser import parse
from .models import *

def insert(column_values: Dict) -> object:
    notification = Notification(user_id = column_values['user_id'],
                                notification_type = column_values['type'],
                                text = column_values['text'],
                                time = column_values['time'],
                                attachments = column_values['attachments'],
                                frequency = column_values['frequency'])
    notification.save()
    print("YFNBAB", notification.get())
    return notification

def fetchall(columns: List[str]) -> List[Tuple]:
    notifications = Notification.select().dicts().execute()
    return notifications

def clean_done_tasks() -> None:
    query = Notification.delete().where(Notification.is_done == True)
    query.execute()

def delete_by_id(id: int) -> Tuple:
    notification = Notification.get(Notification.notification_id == id)
    notification_id = notification.notification_id
    text = notification.text
    notification_type = notification.notification_type
    time = notification.time
    is_done = notification.is_done
    frequency = notification.frequency
    notification.delete_instance()
    return notification_id, text, notification_type, time, is_done, frequency

def mark_done(id: int) -> Tuple:
    notification = Notification.get(Notification.notification_id == id)
    if notification.is_done == False:
        notification = Notification(is_done = True)
        notification.notification_id = id
        notification.save()
    else:
        notification = Notification(is_done = False)
        notification.notification_id = id
        notification.save()
    notification = Notification.get(Notification.notification_id == id)
    notification_id = notification.notification_id
    text = notification.text
    notification_type = notification.notification_type
    time = notification.time
    is_done = notification.is_done
    frequency = notification.frequency
    return notification_id, text, notification_type, time, is_done, frequency

def set_date_with_id(id: int, date: str, frequency_str: str) -> None:
    hours, minutes, seconds = map(int, frequency_str.split(":"))
    print("hours, minutes, seconds: ", hours, minutes, seconds)
    frequency = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    temp = date.split(" ")
    hours, minutes, seconds = map(int, temp[1].split(":"))
    date = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    date = temp[0] + ' ' + str(date + frequency)
    date = parse(date, fuzzy=True)
    notification = Notification(time = date)
    notification.notification_id = id
    notification.save()


def edit_date_with_id(id: int, date: str):
    new_date = parse(date, fuzzy=True)
    notification = Notification(time = new_date)
    notification.notification_id = id
    notification.save()

def edit_title_with_id(id: int, data: str):
    notification = Notification(text = data)
    notification.notification_id = id
    notification.save()

def find_by_date(date: str) -> List:
    notifications = Notification.select().where(Notification.time == date).dicts().execute()
    return notifications

def find_by_id(id: int) -> Notification:
    notification = Notification.get(Notification.notification_id == id)
    return notification
