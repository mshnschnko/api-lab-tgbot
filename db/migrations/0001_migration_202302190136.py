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
    time = DateTimeField(formats='%Y-%m-%d %H:%M:%S')
    attachments = CharField(max_length=100)
    is_done = BooleanField(default=False)
    is_periodic = BooleanField(default=False)
    class Meta:
        table_name = "notification"


