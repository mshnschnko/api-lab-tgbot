from typing import Dict, List, Tuple
from datetime import timedelta, datetime
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

def clean_done_tasks(user_id: int) -> None:
    query = Notification.delete().where(Notification.user_id == user_id).where(Notification.is_done == True)
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

def set_date_with_id(id: int, date: datetime, frequency: int) -> None:
    # hours, minutes, seconds = map(int, frequency_str.split(":"))
    # print("hours, minutes, seconds: ", hours, minutes, seconds)
    frequency = timedelta(minutes=frequency)
    # temp = date.split(" ")
    # hours, minutes, seconds = map(int, temp[1].split(":"))
    # date = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    # date = temp[0] + ' ' + str(date + frequency)
    # date = parse(date, fuzzy=True)
    notification = Notification(time = date + frequency)
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

def edit_frequency_with_id(id: int, frequncy: str):
    notification = Notification(frequency = frequncy)
    notification.notification_id = id
    notification.save()

def add_attachment_with_id(id: int, attachment: str):
    notification = Notification.get(Notification.notification_id == id)
    new_attachments = notification.attachments + attachment
    updated_notification = Notification(attachments = new_attachments)
    updated_notification.notification_id = id
    updated_notification.save()

def del_attachments_with_id(id: int, indices: list) -> int:
    print(indices)
    notification = Notification.get(Notification.notification_id == id)
    attachments = notification.attachments.split(';')
    attachments.pop(-1)
    # print(*attachments)
    if min(indices) < 0 or max(indices) > len(attachments):
        return -1
    new_attachments = list(att for idx, att in enumerate(attachments) if not idx in indices)
    # print(*new_attachments)
    new_attachments_str = ';'.join(new_attachments)
    new_attachments_str += ';'
    # print(new_attachments_str)
    notification = Notification(attachments=new_attachments_str)
    notification.notification_id = id
    notification.save()
    return 0

def find_by_date(date: str) -> List:
    notifications = Notification.select().where(Notification.time == date).dicts().execute()
    return notifications

def find_by_id(id: int) -> Notification:
    notification = Notification.get(Notification.notification_id == id)
    return notification
