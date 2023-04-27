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
    attachments = CharField(max_length=200, null=True)
    is_done = BooleanField(default=False, null=True)
    frequency = IntegerField(default=0, null=True)
    class Meta:
        table_name = "notification"


def forward(old_orm, new_orm):
    old_notification = old_orm['notification']
    notification = new_orm['notification']
    return [
        # Convert datatype of the field notification.attachments: VARCHAR(100) -> VARCHAR(200),
        notification.update({notification.attachments: fn.SUBSTRING(old_notification.attachments, 1, 200)}).where(old_notification.attachments.is_null(False)),
    ]


def backward(old_orm, new_orm):
    old_notification = old_orm['notification']
    notification = new_orm['notification']
    return [
        # Convert datatype of the field notification.attachments: VARCHAR(200) -> VARCHAR(100),
        notification.update({notification.attachments: fn.SUBSTRING(old_notification.attachments, 1, 100)}).where(old_notification.attachments.is_null(False)),
    ]
