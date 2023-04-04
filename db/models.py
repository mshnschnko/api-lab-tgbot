from peewee import *
from .db_config import *

conn = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

class BaseModel(Model):
    class Meta:
        database = conn

# class Notification(BaseModel):
#     notification_id = AutoField(column_name = 'notification_id')
#     user_id = IntegerField(column_name='user_id', null=False)
#     text = CharField(max_length=200, null=False)
#     time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', null=True)
#     attachments = CharField(max_length=100, null=True)
#     is_done = BooleanField(default=False, null=True)
#     is_periodic = BooleanField(default=False, null=True)

class Notification(BaseModel):
    notification_id = AutoField(column_name = 'notification_id')
    user_id = IntegerField(column_name='user_id', null=False)
    notification_type = CharField(max_length=20)
    text = CharField(max_length=200, null=False)
    time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', null=True)
    attachments = TextField(null=True)
    is_done = BooleanField(default=False, null=True)
    frequency = IntegerField(default=0, null=True)