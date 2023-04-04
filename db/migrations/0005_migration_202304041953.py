# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Notification(peewee.Model):
    notification_id = AutoField(primary_key=True)
    user_id = IntegerField()
    notification_type = CharField(max_length=20)
    text = CharField(max_length=200)
    time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', null=True)
    attachments = TextField(null=True)
    is_done = BooleanField(default=False, null=True)
    frequency = IntegerField(default=0, null=True)
    class Meta:
        table_name = "notification"


def forward(old_orm, new_orm):
    old_notification = old_orm['notification']
    notification = new_orm['notification']
    return [
        # Don't know how to do the conversion correctly, use the naive,
        notification.update({notification.attachments: old_notification.attachments}).where(old_notification.attachments.is_null(False)),
    ]


def backward(old_orm, new_orm):
    old_notification = old_orm['notification']
    notification = new_orm['notification']
    return [
        # Convert datatype of the field notification.attachments: TEXT -> VARCHAR(200),
        notification.update({notification.attachments: old_notification.attachments.cast('VARCHAR')}).where(old_notification.attachments.is_null(False)),
    ]
