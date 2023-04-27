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
    attachments = CharField(max_length=200, null=True)
    is_done = BooleanField(default=False, null=True)
    frequency = IntegerField(default=0, null=True)
    class Meta:
        table_name = "notification"


def forward(old_orm, new_orm):
    notification = new_orm['notification']
    return [
        # Apply default value '' to the field notification.notification_type,
        notification.update({notification.notification_type: ''}).where(notification.notification_type.is_null(True)),
    ]
