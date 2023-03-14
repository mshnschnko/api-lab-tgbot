# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Notification(peewee.Model):
    notification_id = AutoField(primary_key=True)
    user_id = IntegerField()
    text = CharField(max_length=200)
    time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', null=True)
    attachments = CharField(max_length=100, null=True)
    is_done = BooleanField(default=False, null=True)
    is_periodic = BooleanField(default=False, null=True)
    class Meta:
        table_name = "notification"


def backward(old_orm, new_orm):
    notification = new_orm['notification']
    return [
        # Apply default value False to the field notification.is_done,
        notification.update({notification.is_done: False}).where(notification.is_done.is_null(True)),
        # Apply default value False to the field notification.is_periodic,
        notification.update({notification.is_periodic: False}).where(notification.is_periodic.is_null(True)),
        # Apply default value datetime.datetime(2023, 2, 19, 1, 38, 18, 364519) to the field notification.time,
        notification.update({notification.time: datetime.datetime(2023, 2, 19, 1, 38, 18, 364519)}).where(notification.time.is_null(True)),
        # Apply default value '' to the field notification.attachments,
        notification.update({notification.attachments: ''}).where(notification.attachments.is_null(True)),
    ]
